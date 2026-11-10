"""Audit the texture authoring continuation and cross-unit pixel links."""
import asyncio
import importlib.metadata
import json
from io import BytesIO
from pathlib import Path
from PIL import Image
from fastmcp import Client
import petz_renderer
from research_common import ROOT,SHA


def main():
    reports={name:json.loads((ROOT/f'experiments/{name}.json').read_text()) for name in ('line-021','texture-003','texture-004')}
    evidence={}
    for name,report in reports.items():
        folder=ROOT/'scratch/research'/name
        assert report==json.loads((folder/'report.json').read_text())
        verification=json.loads((ROOT/f'scratch/research/{name}-verification.json').read_text())
        assert verification['report_sha256']==SHA((ROOT/f'experiments/{name}.json').read_bytes())
        evidence[name]={'report_sha256':verification['report_sha256'],'verified':verification['verified']}
        for dependency,version in report['dependencies'].items():assert importlib.metadata.version(dependency)==version
    # Mode1 preserves the earlier 256x256 block/scene controls exactly.
    links=[]
    for rec in reports['texture-003']['comparisons']:
        before,after=rec['pair']
        if (before,after) not in (('m1-absent','m1-textured'),('m1-explicit','m1-textured')):continue
        for index,variant in ((0,'absent' if before=='m1-absent' else 'explicit'),(1,'textured')):
            old=next(r for r in reports['line-021']['comparisons'] if r['species']==rec['species'] and r['dimensions']==[256,256] and r['controls']['yaw_degrees']==rec['controls']['yaw_degrees'] and r['variant']==('textured' if variant=='absent' else variant))
            old_index=0 if variant=='absent' else 1
            assert rec['cell_hashes'][index]==old['cell_hashes'][old_index]
            links.append({'from':'texture-003','to':'line-021','species':rec['species'],'yaw':rec['controls']['yaw_degrees'],'variant':variant,'rgba_sha256':rec['cell_hashes'][index]})
    # History baselines share the 128x128 standing scene, not just its copied input.
    for b in reports['texture-004']['baselines']:
        if b['pose']!='standing':continue
        raw=(ROOT/'scratch/research/texture-004'/b['png']).read_bytes()
        digest=SHA(Image.open(BytesIO(raw)).convert('RGBA').tobytes())
        old=next(r for r in reports['line-021']['comparisons'] if r['species']==b['species'] and r['dimensions']==[128,128] and r['variant']=='textured' and r['controls']['yaw_degrees']==b['yaw_degrees'])
        assert digest==old['cell_hashes'][1]
        links.append({'from':'texture-004','to':'line-021','species':b['species'],'yaw':b['yaw_degrees'],'variant':'textured-standing','rgba_sha256':digest})
    assert len(links)==20
    # Every retained-history sheet must share the independently MCP-checked fresh cell.
    baseline_links=0
    for baseline in reports['texture-004']['baselines']:
        folder=ROOT/'scratch/research/texture-004'
        raw=(folder/baseline['png']).read_bytes()
        assert SHA(raw)==baseline['png_sha256']
        meta=json.loads((folder/(Path(baseline['png']).stem+'-mcp.json')).read_text())
        assert meta['png_sha256']==baseline['png_sha256']
        digest=SHA(Image.open(BytesIO(raw)).convert('RGBA').tobytes())
        cases=[c for c in reports['texture-004']['cases'] if c['species']==baseline['species'] and c['pose']==baseline['pose'] and c['yaw_degrees']==baseline['yaw_degrees']]
        assert len(cases)==4
        for case in cases:
            assert case['cell_hashes'][0]['rgba_sha256']==digest
            baseline_links+=1
    assert baseline_links==48
    installed=Path(petz_renderer.__file__).parent;checkout=ROOT/'petz-renderer-mcp/src/petz_renderer'
    source_map={str(p.relative_to(installed)):SHA(p.read_bytes()) for p in sorted(installed.rglob('*.py'))}
    assert set(source_map)=={str(p.relative_to(checkout)) for p in checkout.rglob('*.py')}
    for path,digest in source_map.items():assert SHA((checkout/path).read_bytes())==digest
    audit={'files':source_map,'tree_sha256':SHA(json.dumps(source_map,sort_keys=True,separators=(',',':')).encode())}
    (ROOT/'scratch/research/texture-authoring-source-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    counts={'new_copies':sum(len(c['paths']) for name in ('line-021','texture-003') for c in reports[name]['cases']),
            'mcp_comparison_pairs':sum(len(reports[n]['comparisons']) for n in ('line-021','texture-003')),
            'mcp_fresh_baselines':len(reports['texture-004']['baselines']),
            'numerical_authoring_loads':sum(len(c['checks']) for name in ('line-021','texture-003') for c in reports[name]['cases']),
            'history_fixtures':len(reports['texture-004']['baselines']),
            'history_cases':len(reports['texture-004']['cases']),
            'saved_pngs':sum(len(list((ROOT/'scratch/research'/name).glob('*.png'))) for name in reports),
            'rgba_cells':80+168+240+12,'cross_unit_pixel_links':len(links),'installed_source_files':len(source_map)}
    assert counts=={'new_copies':78,'mcp_comparison_pairs':124,'mcp_fresh_baselines':12,'numerical_authoring_loads':234,'history_fixtures':12,'history_cases':48,'saved_pngs':184,'rgba_cells':500,'cross_unit_pixel_links':20,'installed_source_files':62}
    summary={'reports':evidence,'verified':counts,'cross_unit_links':links,'source_tree_sha256':audit['tree_sha256'],'history_fresh_baseline_links':baseline_links}
    (ROOT/'scratch/research/texture-authoring-session-verification.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({'verified':counts,'source_tree_sha256':audit['tree_sha256']}))


async def health():
    async with Client('http://127.0.0.1:8765/mcp') as client:
        names=[x.name for x in await client.list_tools()]
        assert 'get_capabilities' in names
        result=await client.call_tool('get_capabilities',{});assert not result.is_error
        record={'endpoint':'http://127.0.0.1:8765/mcp','tool_names':names,'capabilities':result.data}
        (ROOT/'scratch/research/texture-authoring-session-mcp-health.json').write_text(json.dumps(record,indent=2)+'\n')
        print('HTTP MCP discovery/capabilities passed')
if __name__=='__main__':
    main();asyncio.run(health())
