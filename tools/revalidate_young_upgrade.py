"""UPDATE-010: retain historical young evidence and replay on installed build."""
import argparse, asyncio, base64, io, json, subprocess, sys
from PIL import Image
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from petz_renderer.rendering.output import render_portrait
from young_breed_probe import ROOT, digest, provenance
OUT=ROOT/'scratch/research/update-010'
MANIFEST=ROOT/'experiments/update-010.json'
def decoded(png):
 im=Image.open(io.BytesIO(png)).convert('RGBA');return im.size,digest(im.tobytes())
def aligned_difference(a,ao,b,bo):
 ims=[Image.open(io.BytesIO(x)).convert('RGBA') for x in (a,b)]
 left,top=min(-ao[0],-bo[0]),min(-ao[1],-bo[1])
 right=max(im.width-o[0] for im,o in zip(ims,(ao,bo)))
 bottom=max(im.height-o[1] for im,o in zip(ims,(ao,bo)))
 canv=[]
 for im,o in zip(ims,(ao,bo)):
  c=Image.new('RGBA',(right-left,bottom-top));c.paste(im,(-o[0]-left,-o[1]-top));canv.append(c)
 return sum(x!=y for x,y in zip(canv[0].getdata(),canv[1].getdata()))
def signature(row):return row['size'],row['offset'],row['rgba_sha256']
def output_record(png,offset,old,oldpath,stem,verify):
 historical=oldpath.read_bytes();assert digest(historical)==old['png_sha256']
 size,rgba=decoded(png);path=OUT/f'{stem}.png'
 if verify:assert path.read_bytes()==png
 else:path.write_bytes(png)
 return {'png_sha256':digest(png),'rgba_sha256':rgba,'size':list(size),'offset':list(offset),
 'historical_png_sha256':old['png_sha256'],'historical_rgba_sha256':decoded(historical)[1],
 'same_png':digest(png)==old['png_sha256'],
 'same_aligned_rgba':(list(size),list(offset),rgba)==(old['size'],old['offset'],decoded(historical)[1]),
 'pixels_vs_historical':aligned_difference(png,offset,historical,old['offset'])}
async def run(verify):
 previous=json.loads(MANIFEST.read_text()) if verify else None
 if not verify:OUT.mkdir(parents=True,exist_ok=False)
 first=json.loads((ROOT/'experiments/young-001.json').read_text());second=json.loads((ROOT/'experiments/young-002.json').read_text())
 report={'provenance':provenance(),'backend':'local stdio MCP; installed direct saved renderer; historical aligned decoded RGBA comparisons',
 'prior_manifests':{n:digest((ROOT/f'experiments/{n}.json').read_bytes()) for n in ('young-001','young-002')},'fresh':[],'saved':[],'relationships':[],'mcp_saved':[]}
 bykey={}
 for version in ('petz3','petz4','petz5'):
  transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games'/version),'--game-version',version])
  async with Client(transport) as client:
   assert len(await client.list_tools())==6
   for old in (x for x in first['cases'] if x['version']==version):
    assert digest((ROOT/'games'/version/old['controls']['path']).read_bytes())==old['input_sha256']
    response=await client.call_tool('render_pet',old['controls']);assert not response.is_error
    png=base64.b64decode(next(c.data for c in response.content if c.type=='image'))
    stem=f"{version}-{old['species']}-{old['label']}"
    row={'version':version,'species':old['species'],'label':old['label'],'controls':old['controls'],'input_sha256':old['input_sha256'],**output_record(png,response.data['offset'],old,ROOT/'scratch/research/young-001'/f'{stem}.png',stem,verify),'appearance':response.data['appearance']}
    report['fresh'].append(row);bykey[version,old['species'],old['label']]=row
   print(f'{version}: 102 fresh MCP historical comparisons',flush=True)
 for rel in first['relationships']:
  a=bykey[rel['version'],rel['species'],rel['a']];b=bykey[rel['version'],rel['species'],rel['b']]
  report['relationships'].append({'unit':'young-001',**rel,'equal':signature(a)==signature(b)})
 resolver=ResourceResolver((ROOT/'games/petz4',ROOT/'scratch/research/young-002'));saved={}
 for source in second['copies']:
  assert digest((ROOT/'games/petz4'/source['source']).read_bytes())==source['source_sha256']
  for variant in source['variants'].values():assert digest((ROOT/'scratch/research/young-002'/variant['path']).read_bytes())==variant['sha256']
 for old in second['cases']:
  source=next(x for x in second['copies'] if x['name']==old['name']);path=source['variants'][old['mode']]['path']
  assets=load_saved_assets(resolver,path,pose='standing',age=old['age'],look=old['look']);result=render_portrait(assets,yaw=old['yaw_degrees']*256//360)
  stem=f"{old['name']}-{old['mode']}-{old['look']}-{old['age']}-{old['yaw_degrees']}"
  row={k:old[k] for k in ('name','mode','look','age','yaw_degrees')}
  row.update(output_record(result.png,result.offset,old,ROOT/'scratch/research/young-002'/f'{stem}.png',stem,verify));row['appearance_mode']=assets.preview.mode
  row['layers']=[{'label':x.label,'sha256':x.sha256} for x in assets.preview.layers]
  report['saved'].append(row);saved[old['name'],old['mode'],old['look'],old['age'],old['yaw_degrees']]=(result,row)
 for rel in second['relationships']:
  a=saved[rel['name'],*rel['a'],rel['yaw_degrees']];b=saved[rel['name'],*rel['b'],rel['yaw_degrees']]
  report['relationships'].append({'unit':'young-002',**rel,'equal_commands_and_png':a[0].prepared==b[0].prepared and a[0].png==b[0].png})
 transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(ROOT/'scratch/research/young-002')])
 async with Client(transport) as client:
  for old in second['mcp']:
   source=next(x for x in second['copies'] if x['name']==old['name']);args={'path':source['variants'][old['mode']]['path'],'look':old['look'],'age':old['age'],'pose':'standing','yaw_degrees':0}
   response=await client.call_tool('render_pet',args);assert not response.is_error
   png=base64.b64decode(next(c.data for c in response.content if c.type=='image'));assert png==saved[old['name'],old['mode'],old['look'],old['age'],0][0].png
   report['mcp_saved'].append({'controls':args,'png_sha256':digest(png),'appearance':response.data['appearance']})
 originals=json.loads(subprocess.check_output([sys.executable,str(ROOT/'tools/check_game_restore.py')],text=True));assert all(x['ok'] for x in originals['checks']);report['originals']=originals
 report['script_sha256']=digest(__import__('pathlib').Path(__file__).read_bytes())
 report['summary']={'fresh':len(report['fresh']),'fresh_changed':sum(not x['same_aligned_rgba'] for x in report['fresh']),'saved':len(report['saved']),'saved_changed':sum(not x['same_aligned_rgba'] for x in report['saved']),'relationships':len(report['relationships']),'failed_relationships':[x for x in report['relationships'] if not x.get('equal',x.get('equal_commands_and_png'))],'saved_mcp_matches':len(report['mcp_saved'])}
 if verify:assert report==previous;print('FULL REPLAY PASS',flush=True)
 else:MANIFEST.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report['summary'],indent=2),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');asyncio.run(run(p.parse_args().verify))
