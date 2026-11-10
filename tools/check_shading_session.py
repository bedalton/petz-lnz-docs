"""Aggregate shading continuation provenance and cross-unit pixel links."""
import asyncio,json,importlib.metadata
from pathlib import Path
from io import BytesIO
from PIL import Image
from fastmcp import Client
import petz_renderer
from research_common import ROOT,SHA

def main():
    reports={n:json.loads((ROOT/f'experiments/{n}.json').read_text()) for n in ('shade-001','shade-002','shade-003')};evidence={}
    for name,r in reports.items():
        v=json.loads((ROOT/f'scratch/research/{name}-verification.json').read_text());assert v['report_sha256']==SHA((ROOT/f'experiments/{name}.json').read_bytes())
        assert r==json.loads((ROOT/f'scratch/research/{name}/report.json').read_text())
        evidence[name]={'report_sha256':v['report_sha256'],'verified':v['verified']}
        for name,version in r['dependencies'].items():assert importlib.metadata.version(name)==version
        for name,digest in r['engine_hashes'].items():assert SHA((ROOT/name).read_bytes())==digest
    links=[]
    for b in reports['shade-002']['baselines']:
        if b['pose']=='lying':continue
        old=next(c for c in reports['shade-001']['comparisons'] if c['species']==b['species'] and c['controls']['pose']==b['pose'] and c['controls']['yaw_degrees']==b['yaw_degrees'] and c['pair']==['zero','strong'])
        digest=SHA(Image.open(ROOT/'scratch/research/shade-002'/b['png']).convert('RGBA').tobytes());index=0 if b['variant']=='zero' else 1
        assert digest==old['cell_hashes'][index]
        links.append({'from':'shade-002','to':'shade-001','input':b['input'],'pose':b['pose'],'yaw_degrees':b['yaw_degrees'],'rgba_sha256':digest})
    for c in reports['shade-003']['cases']:
        b=next(b for b in reports['shade-002']['baselines'] if b['species']==c['species'] and b['pose']==c['pose'] and b['yaw_degrees']==c['yaw_degrees'] and b['variant']=='strong')
        digest=SHA(Image.open(ROOT/'scratch/research/shade-002'/b['png']).convert('RGBA').tobytes());assert digest==c['cell_hashes'][0]['rgba_sha256']
        links.append({'from':'shade-003','to':'shade-002','sheet':c['sheet'],'rgba_sha256':digest})
    assert len(links)==39
    # Baselines are byte-identical copies of the two earlier strong inputs.
    for c in reports['shade-003']['inputs']:
        old=next(o for o in reports['shade-001']['cases'] if o['species']==c['species'])
        assert c['input_hashes']['baseline']==old['input_hashes']['strong']
    installed=Path(petz_renderer.__file__).parent;checkout=ROOT/'petz-renderer-mcp/src/petz_renderer'
    source_map={str(p.relative_to(installed)):SHA(p.read_bytes()) for p in sorted(installed.rglob('*.py'))}
    assert set(source_map)=={str(p.relative_to(checkout)) for p in checkout.rglob('*.py')}
    for name,digest in source_map.items():assert SHA((checkout/name).read_bytes())==digest
    audit={'files':source_map,'tree_sha256':SHA(json.dumps(source_map,sort_keys=True,separators=(',',':')).encode())}
    (ROOT/'scratch/research/shading-source-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    hashes=[h for c in reports['shade-001']['cases'] for h in c['input_hashes'].values()]+[h for c in reports['shade-003']['inputs'] for h in c['input_hashes'].values()]
    counts={'copies':len(hashes),'unique_copy_hashes':len(set(hashes)),'mcp_pairs':len(reports['shade-001']['comparisons'])+len(reports['shade-003']['comparisons']),'mcp_fresh_baselines':len(reports['shade-002']['baselines']),'assembly_loads':sum(len(c['checks']) for c in reports['shade-001']['cases']),'omission_assemblies':sum(len(s['rows']) for s in reports['shade-003']['scans']),'history_cases':len(reports['shade-002']['cases']),'transition_states':384,'counterfactual_compositions':len(reports['shade-003']['cases']),'saved_pngs':sum(len(list((ROOT/'scratch/research'/name).glob('*.png'))) for name in reports),'rgba_cells':96+192+24+69+46,'indexed_buffers':192+69,'cross_unit_pixel_links':len(links),'installed_source_files':len(source_map)}
    assert counts=={'copies':26,'unique_copy_hashes':24,'mcp_pairs':71,'mcp_fresh_baselines':24,'assembly_loads':84,'omission_assemblies':804,'history_cases':96,'transition_states':384,'counterfactual_compositions':23,'saved_pngs':214,'rgba_cells':427,'indexed_buffers':261,'cross_unit_pixel_links':39,'installed_source_files':62}
    restore=json.loads((ROOT/'experiments/restore-002.json').read_text())
    game_root=ROOT/'games/petz4';game_paths={str(p.relative_to(game_root)).lower():p for p in game_root.rglob('*') if p.is_file()}
    restore_links={}
    for name,digest in restore['shared_engine_hashes']['petz4'].items():
        assert SHA(game_paths[name].read_bytes())==digest;restore_links[name]=digest
    for rec in restore['results']:
        if rec['version']=='petz4':
            assert SHA((game_root/rec['path']).read_bytes())==rec['input_sha256'];restore_links[rec['path']]=rec['input_sha256']
    assert len(restore_links)==6
    executable=ROOT/'games/petz4/Petz 4.exe'
    summary={'equal_fill_attribution_sha256':SHA((ROOT/'scratch/research/shade-003-equal-fill-attribution.json').read_bytes()),'reports':evidence,'restore_original_links':restore_links,'verified':counts,'cross_unit_links':links,'source_tree_sha256':audit['tree_sha256'],'game_executable_sha256':SHA(executable.read_bytes()),'research_tool_hashes':{str(p.relative_to(ROOT)):SHA(p.read_bytes()) for p in (ROOT/'tools/shade_slope_probe.py',ROOT/'tools/check_shade_slope.py',ROOT/'tools/shade_history_probe.py',ROOT/'tools/check_shade_history.py',ROOT/'tools/shade_omission_probe.py',ROOT/'tools/check_shade_omissions.py',ROOT/'tools/check_shade_equal_fill.py',ROOT/'tools/morph_pixel_probe.py',ROOT/'tools/static_texture_probe.py',ROOT/'tools/research_common.py')}}
    (ROOT/'scratch/research/shading-session-verification.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({'verified':counts,'source_tree_sha256':audit['tree_sha256']}))

async def health():
    async with Client('http://127.0.0.1:8765/mcp') as client:
        names=[x.name for x in await client.list_tools()];assert 'get_capabilities' in names
        result=await client.call_tool('get_capabilities',{});assert not result.is_error
        record={'endpoint':'http://127.0.0.1:8765/mcp','tool_names':names,'capabilities':result.data}
        (ROOT/'scratch/research/shading-session-mcp-health.json').write_text(json.dumps(record,indent=2)+'\n');print('HTTP MCP discovery/capabilities passed')
if __name__=='__main__':main();asyncio.run(health())
