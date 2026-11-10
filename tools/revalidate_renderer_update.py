"""UPDATE-001: preserve old evidence; replay available MCP comparisons on new renderer."""
import asyncio,base64,hashlib,importlib.metadata,json,re,sys,subprocess
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
import petz_renderer
from research_common import ROOT,SHA,save_result
OUT=ROOT/'scratch/research/update-001'

def digests(obj):
    if isinstance(obj,dict):return set().union(*(digests(v) for v in obj.values())) if obj else set()
    if isinstance(obj,list):return set().union(*(digests(v) for v in obj)) if obj else set()
    return {obj} if isinstance(obj,str) and re.fullmatch('[0-9a-f]{64}',obj) else set()

def hashes(rec):
    values=rec.get('cell_hashes',[])
    return [v if isinstance(v,str) else v.get('rgba_sha256') for v in values]

def partition(values):return [values.index(v) for v in values]

async def main():
    assert not (OUT/'report.json').exists(),'completed report exists; choose another update folder'
    rows=[];pending=[];sources={};old_reports={}
    installed=Path(petz_renderer.__file__).parent;checkout=ROOT/'petz-renderer-mcp/src/petz_renderer'
    for p in sorted(installed.rglob('*.py')):
        name=str(p.relative_to(installed));h=SHA(p.read_bytes());assert SHA((checkout/name).read_bytes())==h;sources[name]=h
    before=json.loads((OUT/'before.json').read_text());changed=[name for name,h in sources.items() if before['old_installed_sources'].get(name)!=h]
    async with Client('http://127.0.0.1:8765/mcp') as client:
        names=[t.name for t in await client.list_tools()];caps=await client.call_tool('get_capabilities',{});assert not caps.is_error
        (OUT/'http-health.json').write_text(json.dumps({'tools':names,'capabilities':caps.data},indent=2)+'\n')
    # Every available standard path-based comparison/page is replayed; missing private inputs stay pending.
    for report_path in sorted((ROOT/'experiments').glob('*.json')):
        name=report_path.stem
        if name.startswith(('update-','restore-')):continue
        old=json.loads(report_path.read_text())
        if not isinstance(old,dict):continue
        available=old.get('comparisons',[])+old.get('pages',[])
        if not available:continue
        folder=ROOT/'scratch/research'/name;known=digests(old);jobs=[]
        for index,rec in enumerate(available):
            args=rec.get('controls',{});paths=[args[k] for k in ('before_path','after_path','path') if k in args]
            if not paths:continue
            version=rec.get('game_version',rec.get('version',old.get('game_version','petz4')))
            if version not in ('petz3','petz4','petz5'):version='petz4'
            possible=[folder,folder/version]
            asset_root=next((p for p in possible if all((p/path).is_file() for path in paths)),None)
            if asset_root is None:
                pending.append({'experiment':name,'index':index,'reason':'private input unavailable','paths':paths});continue
            input_hashes={p:SHA((asset_root/p).read_bytes()) for p in paths}
            if not all(h in known for h in input_hashes.values()):
                pending.append({'experiment':name,'index':index,'reason':'input hash not present in historical manifest','paths':paths});continue
            jobs.append((index,rec,args,asset_root,version,input_hashes))
        if not jobs:continue
        old_reports[name]=SHA(report_path.read_bytes())
        for asset_root,version in sorted({(job[3],job[4]) for job in jobs},key=lambda p:str(p)):
            transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-version',version,'--game-root',str(ROOT/'games'/version),'--asset-root',str(asset_root)])
            async with Client(transport) as client:
                for index,rec,args,root,v,input_hashes in jobs:
                    if (root,v)!=(asset_root,version):continue
                    op='render_contact_sheet' if 'path' in args else 'compare_appearance';stem=f'{name}-{index:04d}'
                    png,meta=await save_result(client,op,args,OUT,stem)
                    new=[c['pixel_sha256'] for c in meta['cells']];oldcells=hashes(rec)
                    row={'experiment':name,'index':index,'operation':op,'controls':args,'asset_root':str(asset_root.relative_to(ROOT)),'input_hashes':input_hashes,'game_version':meta['game_version'],'renderer_version':meta['renderer_version'],'stem':stem,'png_sha256':SHA(png),'old_cell_hashes':oldcells,'cell_hashes':new,'same_png':SHA(png)==rec['png_sha256'],'same_cells':oldcells==new if oldcells else None,'same_equality_relationships':partition(oldcells)==partition(new) if oldcells else ((new[0]==new[1])==rec['cells_equal'] if 'cells_equal' in rec else None)}
                    rows.append(row);(OUT/'progress.json').write_text(json.dumps(rows,indent=2)+'\n')
        print(name,len(jobs),'replayed',sum(r['experiment']==name and r['same_cells'] is False for r in rows),'pixel drift',flush=True)
    smoke=[];oldsmoke=json.loads((ROOT/'experiments/restore-002.json').read_text())['results']
    for version in ('petz3','petz4','petz5'):
        transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-version',version,'--game-root',str(ROOT/'games'/version)])
        async with Client(transport) as client:
            for old in (r for r in oldsmoke if r['version']==version):
                args={'path':old['path'],**old['parameters']};stem=f'smoke-{version}-'+('dogz' if '/Dogz/' in old['path'] else 'catz')
                result=await client.call_tool('inspect_input',{'path':old['path'],'seed':0});assert not result.is_error
                (OUT/(stem+'-inspect.json')).write_text(json.dumps(result.data,indent=2)+'\n')
                png,meta=await save_result(client,'render_pet',args,OUT,stem)
                assert SHA((ROOT/'games'/version/old['path']).read_bytes())==old['input_sha256']
                smoke.append({'version':version,'controls':args,'stem':stem,'input_sha256':old['input_sha256'],'png_sha256':SHA(png),'old_png_sha256':old['png_sha256'],'same_png':SHA(png)==old['png_sha256']})
    report={'experiment':'UPDATE-001','renderer_revision':before['checkout_revision'],'previous_renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','change_notice_sha256':before['change_notice_sha256'],'backend':'restarted local HTTP MCP health; fresh local stdio MCP replays','python':sys.version,'dependencies':{p:importlib.metadata.version(p) for p in ('petz-renderer-mcp','fastmcp','pillow','pytest')},'source_hashes':sources,'changed_sources':changed,'historical_reports':old_reports,'replays':rows,'pending':pending,'smoke':smoke,'summary':{'replays':len(rows),'pixel_drift':sum(r['same_cells'] is False for r in rows),'changed_relationships':sum(r['same_equality_relationships'] is False for r in rows),'pending':len(pending),'smoke_png_changed':sum(not r['same_png'] for r in smoke)}}
    for path in (OUT/'report.json',ROOT/'experiments/update-001.json'):path.write_text(json.dumps(report,indent=2)+'\n')
    print(report['summary'],flush=True)
if __name__=='__main__':asyncio.run(main())
