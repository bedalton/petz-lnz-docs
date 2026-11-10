"""Re-evaluate SHADE-001 arithmetic, assembly, copy boundaries and saved MCP cells."""
import importlib.metadata
import json
from io import BytesIO
from pathlib import Path
from PIL import Image
import petz_renderer
from petz_renderer.formats.pe import ResourceFile
from research_common import ROOT,SHA,adult
from shade_slope_probe import synthetic,numerical

def main():
    folder=ROOT/'scratch/research/shade-001';path=ROOT/'experiments/shade-001.json'
    report=json.loads(path.read_text());assert report==json.loads((folder/'report.json').read_text())
    assert report['synthetic']==json.loads(json.dumps(synthetic()))
    for name,digest in report['source_hashes'].items():
        for root in (Path(petz_renderer.__file__).parent,ROOT/'petz-renderer-mcp/src/petz_renderer'):assert SHA((root/name).read_bytes())==digest
    for name,version in report['dependencies'].items():assert importlib.metadata.version(name)==version
    for name,digest in report['engine_hashes'].items():assert SHA((ROOT/name).read_bytes())==digest
    counts={'copies':0,'numerical_loads':0,'mcp_pairs':0,'rgba_cells':0}
    for case in report['cases']:
        source,raw,leaf,_,_,_=adult(case['species']);assert SHA(raw)==case['source_sha256'] and str(source.relative_to(ROOT))==case['source_path']
        original=ResourceFile(raw)
        for name,filename in case['paths'].items():
            data=(folder/filename).read_bytes();assert SHA(data)==case['input_hashes'][name]
            assert len(data)==len(raw) and data[:leaf.offset]==raw[:leaf.offset] and data[leaf.offset+leaf.size:]==raw[leaf.offset+leaf.size:]
            edited=ResourceFile(data);assert original.resources==edited.resources
            for resource in original.resources:
                if resource!=leaf:assert original.read(resource.type,resource.name,resource.language)==edited.read(resource.type,resource.name,resource.language)
            counts['copies']+=1
        assert numerical(folder,case)==case['checks'];counts['numerical_loads']+=len(case['checks'])
        for pose in ('standing','sitting','lying'):
            for yaw in (0,64):
                rows={r['variant']:r for r in case['checks'] if r['pose']==pose and r['yaw']==yaw}
                for left,right in (('absent','strong'),('empty','zero')):
                    assert rows[left]['fills']==rows[right]['fills'] and rows[left]['offsets']==rows[right]['offsets']
    for rec in report['comparisons']:
        png=(folder/(rec['stem']+'.png')).read_bytes();assert SHA(png)==rec['png_sha256']
        meta=json.loads((folder/(rec['stem']+'-render.json')).read_text())
        assert meta['game_version']==rec['game_version']=='petz4' and meta['renderer_version']==rec['renderer_version']
        im=Image.open(BytesIO(png)).convert('RGBA')
        for cell,digest in zip(meta['cells'],rec['cell_hashes'],strict=True):
            x,y=cell['origin'];assert SHA(im.crop((x,y,x+meta['cell_width'],y+meta['cell_height'])).tobytes())==digest==cell['pixel_sha256'];counts['rgba_cells']+=1
        equal=rec['cell_hashes'][0]==rec['cell_hashes'][1];assert equal==rec['cells_equal']
        assert equal==(rec['pair'][0] in ('absent','empty'))
        counts['mcp_pairs']+=1
    assert counts=={'copies':14,'numerical_loads':84,'mcp_pairs':48,'rgba_cells':96}
    result={'experiment':'SHADE-001','report_sha256':SHA(path.read_bytes()),'verified':counts,'parser_cases':6,'arithmetic_slots':765,'palette_assertions':3328}
    (ROOT/'scratch/research/shade-001-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
