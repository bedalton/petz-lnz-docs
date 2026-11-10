"""Verify the 2026-11-10 texture/pixel continuation without rerendering."""
import json,importlib.metadata
from io import BytesIO
from pathlib import Path
from PIL import Image
from petz_renderer.formats.resolver import ResourceResolver
from research_common import ROOT,SHA
import petz_renderer
def main():
    installed=Path(petz_renderer.__file__).parent;cells=0;sheets=0;mcp=0;states=0
    for experiment in ('morph-005','texture-001','texture-002'):
        public=json.loads((ROOT/'experiments'/f'{experiment}.json').read_text());folder=ROOT/'scratch/research'/experiment
        private=json.loads((folder/'report.json').read_text())
        for name,expected in public['source_hashes'].items():assert SHA((installed/name).read_bytes())==expected
        for name,version in public['dependency_versions'].items():assert importlib.metadata.version(name)==version
        resolver=ResourceResolver((ROOT/'games/petz4',))
        for path,expected in public['shared_engine_hashes'].items():assert SHA(resolver.read_bytes(path,limit=268435456).data)==expected
        if experiment=='texture-002':assert public==private;continue
        if experiment=='morph-005':
            assert public==private
            for c in public['cases']:
                source=ROOT/'scratch/research/morph-003'/c['input'];assert SHA(source.read_bytes())==c['input_sha256']
            records=public['cases']
            for b in public['baselines']:
                png=folder/b['png'];assert SHA(png.read_bytes())==b['png_sha256']
                metadata=json.loads(png.with_name(png.stem+'-mcp.json').read_text());assert metadata['png_sha256']==b['png_sha256'];mcp+=1
        else:
            records=[]
            for c,full in zip(public['cases'],private['cases'],strict=True):
                assert SHA((ROOT/'games/petz4'/c['source']).read_bytes())==c['source_sha256']
                records.extend(c[key] for key in ('resets','third_resets','sequence'))
                metadata=json.loads((folder/f"{c['species']}-{c['pose']}-{c['yaw_degrees']}-mcp.json").read_text())
                assert metadata['png_sha256']==c['first_png_sha256'];mcp+=1
                for f,p in zip(c['sequence']['frames'],full['sequence']['frames'],strict=True):
                    assert SHA(json.dumps(p['orientation_state'],sort_keys=True).encode())==f['orientation_state_sha256'];states+=1
        for r in records:
            path=folder/r['sheet'];assert SHA(path.read_bytes())==r['sheet_sha256'];sheets+=1
            with Image.open(path) as source:
                image=source.convert('RGBA');w,h=r['cell_size'];assert image.size==(w*len(r['cell_hashes']),h)
                for i,hashes in enumerate(r['cell_hashes']):
                    cell=image.crop((w*i,0,w*(i+1),h));assert SHA(cell.tobytes())==hashes['rgba_sha256'];cells+=1
    summary={'sheet_pngs_verified':sheets,'rgba_cells_verified':cells,'local_mcp_baselines_verified':mcp,'orientation_snapshots_verified':states,'source_dependency_and_engine_hashes_match':True}
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
