"""Audit SHADE-003 copy-only omission sweep, counterfactuals and MCP sheets."""
import json,importlib.metadata
from io import BytesIO
from pathlib import Path
from PIL import Image
import petz_renderer
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from research_common import ROOT,SHA,adult
from shade_omission_probe import scan,composition

def main():
    folder=ROOT/'scratch/research/shade-003';path=ROOT/'experiments/shade-003.json';report=json.loads(path.read_text());assert report==json.loads((folder/'report.json').read_text())
    for name,digest in report['source_hashes'].items():
        for root in (Path(petz_renderer.__file__).parent,ROOT/'petz-renderer-mcp/src/petz_renderer'):assert SHA((root/name).read_bytes())==digest
    for name,version in report['dependencies'].items():assert importlib.metadata.version(name)==version
    for name,digest in report['engine_hashes'].items():assert SHA((ROOT/name).read_bytes())==digest
    counts={'copies':0,'sweep_cases':0,'compositions':0,'indexed_buffers':0,'rgba_cells':0,'mcp_pairs':0,'mcp_rgba_cells':0};resolver=ResourceResolver((ROOT/'games/petz4',folder));assets={}
    for c in report['inputs']:
        source,raw,leaf,_,_,_=adult(c['species']);assert SHA(raw)==c['source_sha256'] and str(source.relative_to(ROOT))==c['source_path'];original=ResourceFile(raw)
        for name,filename in c['paths'].items():
            data=(folder/filename).read_bytes();assert SHA(data)==c['input_hashes'][name]
            assert len(data)==len(raw) and data[:leaf.offset]==raw[:leaf.offset] and data[leaf.offset+leaf.size:]==raw[leaf.offset+leaf.size:]
            edited=ResourceFile(data);assert edited.resources==original.resources
            for resource in original.resources:
                if resource!=leaf:assert original.read(resource.type,resource.name,resource.language)==edited.read(resource.type,resource.name,resource.language)
            counts['copies']+=1
        for pose in ('standing','sitting','lying'):
            a=load_breed_assets(resolver,c['paths']['baseline'],pose=pose,seed=0,age=100,fatness=50);assets[(c['species'],pose)]=a
            for yaw in (0,64):
                rec=next(s for s in report['scans'] if s['species']==c['species'] and s['pose']==pose and s['yaw_units']==yaw)
                actual=scan(a,yaw)
                for k,v in actual.items():assert v==rec[k]
                counts['sweep_cases']+=len(actual['rows'])
    for rec in report['cases']:
        a=assets[(rec['species'],rec['pose'])];actual,private,png=composition(a,rec['yaw_units'],rec['omitted_id'])
        for k,v in actual.items():assert json.loads(json.dumps(v))==rec[k],(rec['sheet'],k)
        assert SHA(png)==rec['sheet_sha256']==SHA((folder/rec['sheet']).read_bytes())
        raw=(folder/rec['private_pixels_file']).read_bytes();assert SHA(raw)==rec['private_pixels_sha256'] and json.loads(raw)==private
        w,h=rec['cell_size'];im=Image.open(BytesIO(png)).convert('RGBA')
        for i,digest in enumerate(rec['cell_hashes']):assert SHA(im.crop((i*w,0,(i+1)*w,h)).tobytes())==digest['rgba_sha256']
        c=next(c for c in report['inputs'] if c['species']==rec['species'])
        loaded=load_breed_assets(resolver,c['paths'][f"omit{rec['omitted_id']}"],pose=rec['pose'],seed=0,age=100,fatness=50)
        assert loaded.appearance.omissions==a.appearance.omissions|{rec['omitted_id']}
        from dataclasses import replace
        assert loaded.appearance.lines==tuple(line for line in a.appearance.lines if line.start not in loaded.appearance.omissions and line.end not in loaded.appearance.omissions)
        assert replace(loaded.appearance,omissions=a.appearance.omissions,lines=a.appearance.lines)==a.appearance
        counts['compositions']+=1;counts['indexed_buffers']+=3;counts['rgba_cells']+=3
    for rec in report['comparisons']:
        png=(folder/(rec['stem']+'.png')).read_bytes();assert SHA(png)==rec['png_sha256']
        meta=json.loads((folder/(rec['stem']+'-render.json')).read_text());assert meta['game_version']==rec['game_version']=='petz4' and meta['renderer_version']==rec['renderer_version']
        im=Image.open(BytesIO(png)).convert('RGBA')
        for cell,digest in zip(meta['cells'],rec['cell_hashes'],strict=True):
            x,y=cell['origin'];assert SHA(im.crop((x,y,x+meta['cell_width'],y+meta['cell_height'])).tobytes())==digest==cell['pixel_sha256'];counts['mcp_rgba_cells']+=1
        direct=next(c for c in report['cases'] if rec['stem']==c['sheet'][:-4]+'-mcp')
        assert [h['rgba_sha256'] for h in direct['cell_hashes'][:2]]==rec['cell_hashes']
        counts['mcp_pairs']+=1
    assert counts['sweep_cases']==804 and counts['compositions']==counts['mcp_pairs']==23 and counts['indexed_buffers']==counts['rgba_cells']==69 and counts['mcp_rgba_cells']==46
    summary={'sweep_cases':sum(len(s['rows']) for s in report['scans']),'depth_changed':sum(r['depth']!=s['base_depth'] for s in report['scans'] for r in s['rows']),'fill_changed':sum(bool(r['changed_fills']) for s in report['scans'] for r in s['rows']),'compositions':len(report['cases']),'shade_pixel_changed':sum(bool(c['omitted_vs_held_changed_pixels']) for c in report['cases']),'mcp_pairs':len(report['comparisons'])}
    assert summary==report['summary']
    result={'experiment':'SHADE-003','report_sha256':SHA(path.read_bytes()),'verified':counts,'summary':report['summary']}
    (ROOT/'scratch/research/shade-003-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
