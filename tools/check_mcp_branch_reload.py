"""UPDATE-009: verify installed sources, restarted HTTP schema and branch contract."""
import asyncio,base64,json,subprocess,sys
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from young_breed_probe import ROOT,digest,provenance
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.output import render_portrait
OUT=ROOT/'scratch/research/update-009'
async def main():
 OUT.mkdir(parents=True,exist_ok=True)
 report={'provenance':provenance(),'backend':'restarted local HTTP and fresh local stdio MCP','schemas':{},'http_renders':[],'branches':[]}
 async with Client('http://127.0.0.1:8765/mcp') as client:
  tools={t.name:t for t in await client.list_tools()};assert len(tools)==6
  for name,fields in {'inspect_input':['branch_choices'],'render_pet':['branch_choices'],'render_contact_sheet':['branch_choices'],'compare_appearance':['before_branch_choices','after_branch_choices']}.items():
   report['schemas'][name]={}
   for field in fields:
    schema=tools[name].input_schema['properties'][field]['anyOf'][0]['items']['properties']['branch']
    assert schema['minimum']==1 and 'One-based authored' in schema['description'],(name,field,schema)
    report['schemas'][name][field]=schema
  cap=await client.call_tool('get_capabilities');assert not cap.is_error
  (OUT/'http-capabilities.json').write_text(json.dumps(cap.data,indent=2)+'\n')
  for species,filename in [('Dogz','Scottie.dog'),('Catz','Siamese.cat')]:
   for look in ('adult','puppy'):
    args={'path':f'Resource/{species}/{filename}','pose':'standing','seed':41,'age':12,'fatness':50,'look':look,'yaw_degrees':0}
    response=await client.call_tool('render_pet',args);assert not response.is_error
    png=base64.b64decode(next(x.data for x in response.content if x.type=='image'))
    (OUT/f'{species}-{look}.png').write_bytes(png)
    report['http_renders'].append({'controls':args,'png_sha256':digest(png),'appearance':response.data['appearance']})
 previous=json.loads((ROOT/'experiments/young-004.json').read_text())
 branch=next(r for r in previous['mcp'] if (r['species'],r['mode'],r['label'])==('Dogz','branch','branch-valid'))
 fixture=next(r for r in previous['copies'] if (r['species'],r['mode'])==('Dogz','branch'))
 assert digest((ROOT/'scratch/research/young-004'/fixture['path']).read_bytes())==fixture['sha256']
 report['fixture']=fixture
 transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(ROOT/'scratch/research/young-004')])
 async with Client(transport) as client:
  for number in (0,1,2,3):
   args=dict(branch['controls']);args['branch_choices']=[{**args['branch_choices'][0],'branch':number}]
   response=await client.call_tool('render_pet',args,raise_on_error=False)
   assert response.is_error==(number!=1)
   row={'controls':args,'success':not response.is_error}
   if response.is_error:
    blocks=[x.text for x in response.content if x.type=='text'];row['error_text']=blocks
    text=' '.join(blocks)
    if number==0:assert 'greater than or equal to 1' in text,text
    if number==2:assert 'ZZMISSING' in text and 'missing_asset' in text,text
    if number==3:assert 'declared range' in text,text
   else:
    png=base64.b64decode(next(x.data for x in response.content if x.type=='image'));(OUT/'branch1.png').write_bytes(png)
    row['png_sha256']=digest(png);row['matches_prior_branch1']=digest(png)==branch['png_sha256']
    direct_args={k:v for k,v in args.items() if k not in ('path','yaw_degrees','branch_choices')}
    direct_args['branch_selections']={x['block_id']:x['branch'] for x in args['branch_choices']}
    direct=render_portrait(load_breed_assets(ResourceResolver((ROOT/'games/petz4',ROOT/'scratch/research/young-004')),args['path'],**direct_args),yaw=0)
    assert png==direct.png
    row['matches_fresh_direct']=True
   report['branches'].append(row)
 originals=json.loads(subprocess.check_output([sys.executable,str(ROOT/'tools/check_game_restore.py')],text=True));assert all(x['ok'] for x in originals['checks'])
 report['originals']=originals
 report['script_sha256']=digest(Path(__file__).read_bytes())
 report['install_log_sha256']=digest((ROOT/'scratch/update-009-install.log').read_bytes())
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');(ROOT/'experiments/update-009.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'revision':report['provenance']['revision'],'installed_sources':len(report['provenance']['sources']),'http_tools':len(tools),'http_schema_fields':sum(len(x) for x in report['schemas'].values()),'http_renders':len(report['http_renders']),'branch_checks':len(report['branches']),'originals':len(originals['checks'])},indent=2));print('RELOAD CHECK PASS')
if __name__=='__main__':asyncio.run(main())
