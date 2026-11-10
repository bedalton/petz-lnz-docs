"""Replay SHADE-002 state-isolated histories and audit saved pixels/baselines."""
import importlib.metadata
import json
from io import BytesIO
from pathlib import Path
from PIL import Image
import petz_renderer
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from shade_history_probe import compose,synthetic,HISTORIES
from research_common import ROOT,SHA

def main():
    folder=ROOT/'scratch/research/shade-002';path=ROOT/'experiments/shade-002.json';report=json.loads(path.read_text())
    assert report==json.loads((folder/'report.json').read_text()) and report['synthetic']==synthetic()
    for name,digest in report['source_hashes'].items():
        for root in (Path(petz_renderer.__file__).parent,ROOT/'petz-renderer-mcp/src/petz_renderer'):assert SHA((root/name).read_bytes())==digest
    for name,version in report['dependencies'].items():assert importlib.metadata.version(name)==version
    for name,digest in report['engine_hashes'].items():assert SHA((ROOT/name).read_bytes())==digest
    prior=json.loads((ROOT/'experiments/shade-001.json').read_text());input_root=ROOT/'scratch/research/shade-001';resolver=ResourceResolver((ROOT/'games/petz4',input_root));assets={}
    counts={'histories':0,'transition_states':0,'rgba_cells':0,'indexed_buffers':0,'mcp_baselines':0}
    for rec in report['cases']:
        c=next(c for c in prior['cases'] if c['species']==rec['species'])
        assert SHA((ROOT/c['source_path']).read_bytes())==c['source_sha256']
        assert rec['input_sha256']==c['input_hashes'][rec['variant']]==SHA((input_root/rec['input']).read_bytes())
        key=(rec['input'],rec['pose'])
        if key not in assets:assets[key]=load_breed_assets(resolver,rec['input'],pose=rec['pose'],seed=0,age=100,fatness=50)
        actual,private,png,baseline=compose(assets[key],{'yaw':rec['yaw_units'],'fatness':50},HISTORIES[rec['history']])
        for k,v in actual.items():assert json.loads(json.dumps(v))==rec[k],(rec['sheet'],k)
        assert SHA(png)==rec['sheet_sha256']==SHA((folder/rec['sheet']).read_bytes())
        state_raw=(folder/rec['private_state_file']).read_bytes();assert SHA(state_raw)==rec['private_state_sha256']
        assert json.loads(json.dumps(private))==json.loads(state_raw)
        w,h=rec['cell_size'];im=Image.open(BytesIO(png)).convert('RGBA')
        for i,digest in enumerate(rec['cell_hashes']):assert SHA(im.crop((w*i,0,w*(i+1),h)).tobytes())==digest['rgba_sha256']
        b=next(b for b in report['baselines'] if b['input']==rec['input'] and b['pose']==rec['pose'] and b['yaw_degrees']==rec['yaw_degrees'])
        assert SHA(baseline)==b['png_sha256']
        baseim=Image.open(BytesIO(baseline)).convert('RGBA');assert SHA(baseim.tobytes())==rec['cell_hashes'][0]['rgba_sha256']
        counts['histories']+=1;counts['transition_states']+=len(private['trace']);counts['rgba_cells']+=2;counts['indexed_buffers']+=2
    for b in report['baselines']:
        assert SHA((folder/b['png']).read_bytes())==b['png_sha256'] and b['local_mcp_match']
        meta=json.loads((folder/(Path(b['png']).stem+'-mcp.json')).read_text());assert meta['game_version']=='petz4'
        assert meta['png_sha256']==b['png_sha256']
        assert meta['appearance']['input_sha256']==b['input_sha256']
        assert meta['appearance']['age']==100 and meta['appearance']['fatness']==50 and meta['appearance']['seed']==0
        assert meta['camera']['requested_degrees']==b['yaw_degrees']
        counts['mcp_baselines']+=1
    summary={history:{'cases':sum(c['history']==history for c in report['cases']),'changed_pixels':sum(c['history']==history and c['changed_pixels']>0 for c in report['cases']),'changed_offsets':sum(c['history']==history and bool(c['changed_offsets']) for c in report['cases']),'changed_fills':sum(c['history']==history and bool(c['changed_fills']) for c in report['cases'])} for history in HISTORIES}
    assert summary==report['summary']
    assert counts=={'histories':96,'transition_states':384,'rgba_cells':192,'indexed_buffers':192,'mcp_baselines':24}
    result={'experiment':'SHADE-002','report_sha256':SHA(path.read_bytes()),'verified':counts,'synthetic_events':sum(len(t['events']) for t in report['synthetic']['threshold_traces']),'summary':summary}
    (ROOT/'scratch/research/shade-002-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
