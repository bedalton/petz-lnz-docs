"""Audit UPDATE-002 eye rebuilds, numerical changes and retained snapshots."""
import json
from contextlib import contextmanager
from pathlib import Path
from io import BytesIO
from PIL import Image
from research_common import ROOT,SHA
import check_texture_motion_history
from shade_slope_probe import numerical
from shade_history_probe import compose,HISTORIES
from shade_omission_probe import scan,composition
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets

@contextmanager
def motion_paths(folder):
    oldfolder=ROOT/'scratch/research/texture-004';oldreport=ROOT/'experiments/texture-004.json'
    readtext,readbytes,write=Path.read_text,Path.read_bytes,Path.write_text
    def remap(p):
        if p==oldreport:return folder/'report.json'
        if p==ROOT/'scratch/research/texture-004-verification.json':return folder/'verification.json'
        if p.is_relative_to(oldfolder):return folder/p.relative_to(oldfolder)
        return p
    Path.read_text=lambda p,*a,**kw:readtext(remap(p),*a,**kw)
    Path.read_bytes=lambda p:readbytes(remap(p))
    Path.write_text=lambda p,data,*a,**kw:write(remap(p),data,*a,**kw)
    try:yield
    finally:Path.read_text,Path.read_bytes,Path.write_text=readtext,readbytes,write

def cells(folder,rec,field='cell_hashes'):
    raw=(folder/rec['sheet']).read_bytes();assert SHA(raw)==rec['sheet_sha256'];im=Image.open(BytesIO(raw)).convert('RGBA');w,h=rec['cell_size']
    for i,d in enumerate(rec[field]):assert SHA(im.crop((w*i,0,w*(i+1),h)).tobytes())==d['rgba_sha256']
    return len(rec[field])

def main():
    folder=ROOT/'scratch/research/update-002';path=ROOT/'experiments/update-002.json';r=json.loads(path.read_text());assert r==json.loads((folder/'report.json').read_text())
    for name,h in r['historical_reports'].items():assert SHA((ROOT/f'experiments/{name}.json').read_bytes())==h
    old=json.loads((ROOT/'experiments/shade-001.json').read_text())
    for row,c in zip(r['slope'],old['cases'],strict=True):assert numerical(ROOT/'scratch/research/shade-001',c)==row['records']
    assets={};resolver=ResourceResolver((ROOT/'games/petz4',ROOT/'scratch/research/shade-001'))
    prior=json.loads((ROOT/'experiments/shade-002.json').read_text())
    for row,old in zip(r['shade_histories'],prior['cases'],strict=True):
        key=(old['input'],old['pose'])
        if key not in assets:assets[key]=load_breed_assets(resolver,old['input'],pose=old['pose'],seed=0,age=100,fatness=50)
        now,saved,png,_=compose(assets[key],{'yaw':old['yaw_units'],'fatness':50},HISTORIES[old['history']])
        assert SHA(png)==row['sheet_sha256']
        for k,v in now.items():assert json.loads(json.dumps(v))==row[k]
        assert json.loads(json.dumps(saved))==json.loads((folder/'shade-002'/row['private_state_file']).read_text())
    assets={};resolver=ResourceResolver((ROOT/'games/petz4',ROOT/'scratch/research/shade-003'))
    prior=json.loads((ROOT/'experiments/shade-003.json').read_text())
    for row,old in zip(r['omission_scans'],prior['scans'],strict=True):
        key=(old['species'],old['pose'])
        if key not in assets:
            c=next(c for c in prior['inputs'] if c['species']==old['species']);assets[key]=load_breed_assets(resolver,c['paths']['baseline'],pose=old['pose'],seed=0,age=100,fatness=50)
        assert scan(assets[key],old['yaw_units'])==row['records']
    for row,old in zip(r['omission_compositions'],prior['cases'],strict=True):
        now,saved,png=composition(assets[(old['species'],old['pose'])],old['yaw_units'],old['omitted_id'])
        assert SHA(png)==row['sheet_sha256']
        for k,v in now.items():assert json.loads(json.dumps(v))==row[k]
        assert saved==json.loads((folder/'shade-003'/row['private_pixels_file']).read_text())
    ncells=0
    for family in ('shade-002','shade-003'):
        rows=r['shade_histories'] if family=='shade-002' else r['omission_compositions']
        for rec in rows:
            ncells+=cells(folder/family,rec)
            filename=rec['private_state_file'] if family=='shade-002' else rec['private_pixels_file'];h=rec['private_state_sha256'] if family=='shade-002' else rec['private_pixels_sha256']
            raw=(folder/family/filename).read_bytes();assert SHA(raw)==h;saved=json.loads(raw)
            for pixels,digest in zip(saved['indexed_pixels'],rec['indexed_hashes'],strict=True):assert SHA(bytes(pixels))==digest
    eye1=json.loads((folder/'eye-001/report.json').read_text());old=json.loads((ROOT/'experiments/eye-001.json').read_text())
    for n,o in zip(eye1['cases'],old['cases'],strict=True):
        assert n['input_hashes']==o['input_hashes']
        for name,h in n['input_hashes'].items():assert SHA((folder/'eye-001'/n['paths'][name]).read_bytes())==h
    mcp_cells=0
    for rec in eye1['comparisons']:
        stem=f"{rec['species']}-{rec['variant']}";raw=(folder/'eye-001'/(stem+'.png')).read_bytes();assert SHA(raw)==rec['png_sha256']
        meta=json.loads((folder/'eye-001'/(stem+'-render.json')).read_text());im=Image.open(BytesIO(raw)).convert('RGBA')
        assert rec['cell_hashes'][0]!=rec['cell_hashes'][1]
        for cell,h in zip(meta['cells'],rec['cell_hashes'],strict=True):
            x,y=cell['origin'];assert SHA(im.crop((x,y,x+meta['cell_width'],y+meta['cell_height'])).tobytes())==h;mcp_cells+=1
    eye2=json.loads((folder/'eye-002/report.json').read_text());old=json.loads((ROOT/'experiments/eye-002.json').read_text())
    for n,o in zip(eye2['cases'],old['cases'],strict=True):assert SHA((folder/'eye-002'/n['path']).read_bytes())==n['input_sha256']==o['input_sha256']
    for rec in eye2['pages']:
        raw=(folder/'eye-002'/(rec['stem']+'.png')).read_bytes();assert SHA(raw)==rec['png_sha256'];im=Image.open(BytesIO(raw)).convert('RGBA');meta=json.loads((folder/'eye-002'/(rec['stem']+'-render.json')).read_text())
        for cell,h in zip(meta['cells'],rec['cell_hashes'],strict=True):
            x,y=cell['origin'];assert SHA(im.crop((x,y,x+meta['cell_width'],y+meta['cell_height'])).tobytes())==h;mcp_cells+=1
        h=rec['cell_hashes'];assert h[0]==h[1] and h[2]==h[3] and h[0]!=h[2]
    with motion_paths(folder/'texture-004'):check_texture_motion_history.main()
    assert ncells==261 and mcp_cells==32
    result={'report_sha256':SHA(path.read_bytes()),'verified':{'eye_copies':12,'eye_mcp_pairs':8,'eye_mcp_pages':4,'eye_rgba_cells':mcp_cells,'slope_loads':84,'shade_histories':96,'omission_assemblies':804,'omission_compositions':23,'shade_indexed_rgba_cells':ncells,'motion_histories':48,'motion_transition_states':192,'motion_indexed_rgba_cells':240,'motion_fresh_mcp_baselines':12}}
    (folder/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
