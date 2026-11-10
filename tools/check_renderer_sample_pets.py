"""UPDATE-003: match updated direct sample stills to local MCP; verify old/new inputs."""
import asyncio,json,sys
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from research_common import ROOT,SHA,save_result
OUT=ROOT/'scratch/research/update-003'
def eligibility():
    from petz_renderer.formats.resolver import ResourceResolver
    from petz_renderer.local import load_saved_assets
    resolver=ResourceResolver((ROOT/'games/petz4',));result=[]
    for name in ('Fuzzkin','Goobe','Homebody'):
        a=load_saved_assets(resolver,f'Adopted Petz/{name}.pet',pose='standing')
        result.append({'name':name,'lnz_version':a.appearance.lnz_version,'configured_paint_textures':sum(p.texture>=0 for p in a.appearance.paint_balls),'input_sha256':a.preview.input_sha256})
    return result
async def main():
    import petz_renderer
    source_record=json.loads((ROOT/'experiments/update-001.json').read_text())
    for name,h in source_record['source_hashes'].items():assert SHA((Path(petz_renderer.__file__).parent/name).read_bytes())==h
    old=json.loads((OUT/'old/report.json').read_text());new=json.loads((OUT/'new/report.json').read_text());rows=[]
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-version','petz4','--game-root',str(ROOT/'games/petz4')])
    async with Client(transport) as client:
        for o,n in zip(old,new,strict=True):
            for field in ('name','path','pose','yaw_degrees','input_sha256'):assert o[field]==n[field]
            assert SHA((ROOT/'games/petz4'/n['path']).read_bytes())==n['input_sha256']
            for label,rec in (('old',o),('new',n)):assert SHA((OUT/label/(rec['stem']+'.png')).read_bytes())==rec['png_sha256']
            args={'path':n['path'],'pose':n['pose'],'yaw_degrees':n['yaw_degrees']}
            png,meta=await save_result(client,'render_pet',args,OUT,n['stem']+'-mcp');assert SHA(png)==n['png_sha256'] and meta['game_version']=='petz4'
            assert meta['appearance']['input_sha256']==n['input_sha256'] and meta['appearance']['fatness_source']=='saved' and meta['appearance']['age_source']=='saved'
            rows.append({'name':n['name'],'controls':args,'input_sha256':n['input_sha256'],'old_png_sha256':o['png_sha256'],'png_sha256':n['png_sha256'],'same_png':o['png_sha256']==n['png_sha256'],'old_size':o['size'],'size':n['size'],'changed_ball_ids':[i for i,(a,b) in enumerate(zip(o['geometry'],n['geometry'],strict=True)) if a!=b],'old_textured_paints':o['textured_paints'],'textured_paints':n['textured_paints'],'saved_age':meta['appearance']['age'],'saved_fatness':meta['appearance']['fatness'],'game_version':meta['game_version'],'mcp_match':True})
    summary={'experiment':'UPDATE-003','renderer_revision':json.loads((ROOT/'experiments/update-001.json').read_text())['renderer_revision'],'backend':'historical-source and updated direct render; fresh local stdio MCP matches','source_manifest_sha256':SHA((ROOT/'experiments/update-001.json').read_bytes()),'old_private_report_sha256':SHA((OUT/'old/report.json').read_bytes()),'new_private_report_sha256':SHA((OUT/'new/report.json').read_bytes()),'cases':rows,'summary':{'saved_pets':3,'views_per_revision':18,'mcp_matches':18,'png_changed':sum(not r['same_png'] for r in rows),'geometry_changed':sum(bool(r['changed_ball_ids']) for r in rows),'textured_paint_increased':sum(r['textured_paints']>r['old_textured_paints'] for r in rows)},'current_eligibility':eligibility(),'unavailable_notice_samples':['Frisky','Chip'],'scope':'Saved age/fatness/seed preserved; Petz4 native-port renderer only, no game validation'}
    for path in (OUT/'report.json',ROOT/'experiments/update-003.json'):path.write_text(json.dumps(summary,indent=2)+'\n')
    print(summary['summary'],flush=True)
if __name__=='__main__':asyncio.run(main())
