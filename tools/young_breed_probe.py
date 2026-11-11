"""YOUNG-001: local MCP age/look controls; never edits game inputs."""
import argparse, asyncio, base64, hashlib, importlib.metadata, io, json, platform, subprocess, sys
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'scratch/research/young-001'
def digest(data): return hashlib.sha256(data).hexdigest()
def provenance():
    import petz_renderer
    installed=Path(petz_renderer.__file__).parent
    sources={str(p.relative_to(ROOT/'petz-renderer-mcp/src')):digest(p.read_bytes()) for p in (ROOT/'petz-renderer-mcp/src/petz_renderer').rglob('*.py')}
    assert all(digest((installed.parent/p).read_bytes())==h for p,h in sources.items())
    return {'revision':subprocess.check_output(['git','-C',str(ROOT/'petz-renderer-mcp'),'rev-parse','HEAD'],text=True).strip(),'sources':sources,'python':sys.version,'platform':platform.platform(),'dependencies':{d.metadata['Name']:d.version for d in importlib.metadata.distributions()}}
def cases():
    result={}
    def add(label,**args): result[label]={'pose':'standing','yaw_degrees':0,'seed':41,'fatness':50,**args}
    for age in (0,6,11,12,13,50,99,100):
        for yaw in (0,90): add(f'age-{age}-standing-{yaw}',look='age',age=age,yaw_degrees=yaw)
    for pose in ('standing','sitting','lying'):
        for yaw in (0,90):
            for age in (0,100): add(f'adult-{age}-{pose}-{yaw}',look='adult',age=age,pose=pose,yaw_degrees=yaw)
            if pose!='standing':
                for age in (0,12,100): add(f'age-{age}-{pose}-{yaw}',look='age',age=age,pose=pose,yaw_degrees=yaw)
    for look in ('puppy','kitten'):
        for age in (0,100):
            for yaw in (0,90): add(f'{look}-{age}-standing-{yaw}',look=look,age=age,yaw_degrees=yaw)
    result['default']={'pose':'standing','yaw_degrees':0}
    add('explicit-default',look='age',age=12)
    add('zero-seed',look='age',age=12,seed=0)
    return result
async def run(verify):
    expected=json.loads((ROOT/'experiments/young-001.json').read_text()) if verify else None
    if not verify: OUT.mkdir(parents=True,exist_ok=False)
    report={'backend':'local stdio MCP','provenance':provenance(),'cases':[],'relationships':[]}
    if verify: assert report['provenance']==expected['provenance'], 'provenance drift'
    for version in ('petz3','petz4','petz5'):
        transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games'/version),'--game-version',version])
        async with Client(transport) as client:
            tools=await client.list_tools(); assert len(tools)==6
            assert 'look' in next(t.input_schema for t in tools if t.name=='render_pet')['properties']
            for species,breed in [('Dogz','Scottie.dog'),('Catz','Siamese.cat')]:
                path=f'Resource/{species}/{breed}'; key=f'{version}-{species}'; bylabel={}
                inspection=await client.call_tool('inspect_input',{'path':path,'seed':41})
                if not verify: (OUT/f'{key}-inspect.json').write_text(json.dumps(inspection.data,indent=2))
                for label,args in cases().items():
                    controls={'path':path,**args}; response=await client.call_tool('render_pet',controls); assert not response.is_error
                    png=base64.b64decode(next(c.data for c in response.content if c.type=='image'))
                    im=Image.open(io.BytesIO(png)).convert('RGBA')
                    row={'version':version,'species':species,'label':label,'controls':controls,'input_sha256':digest((ROOT/'games'/version/path).read_bytes()),'png_sha256':digest(png),'rgba_sha256':digest(im.tobytes()),'size':list(im.size),'offset':response.data['offset'],'appearance':response.data['appearance'],'pose':response.data['pose']}
                    report['cases'].append(row); bylabel[label]=row
                    stem=f'{key}-{label}'
                    if verify:
                        old=next(x for x in expected['cases'] if (x['version'],x['species'],x['label'])==(version,species,label)); assert row==old,stem
                        assert digest((OUT/f'{stem}.png').read_bytes())==row['png_sha256']
                    else:
                        (OUT/f'{stem}.png').write_bytes(png); (OUT/f'{stem}.json').write_text(json.dumps(response.data,indent=2))
                        (OUT/'checkpoint.json').write_text(json.dumps(report,indent=2))
                def equal(a,b,kind):
                    lhs,rhs=bylabel[a],bylabel[b]
                    assert (lhs['rgba_sha256'],lhs['size'],lhs['offset'])==(rhs['rgba_sha256'],rhs['size'],rhs['offset']),(key,a,b)
                    report['relationships'].append({'version':version,'species':species,'kind':kind,'a':a,'b':b,'equal':True})
                for pose in ('standing','sitting','lying'):
                    for yaw in (0,90):
                        equal(f'adult-0-{pose}-{yaw}',f'adult-100-{pose}-{yaw}','forced adult ignores age')
                        equal(f'age-100-{pose}-{yaw}',f'adult-100-{pose}-{yaw}','age100 adult endpoint')
                for yaw in (0,90):
                    for age in (0,100): equal(f'puppy-{age}-standing-{yaw}',f'kitten-{age}-standing-{yaw}','young aliases')
                    equal(f'puppy-0-standing-{yaw}',f'puppy-100-standing-{yaw}','forced young ignores age')
                    equal(f'age-12-standing-{yaw}',f'puppy-0-standing-{yaw}','age12 young endpoint')
                equal('default','explicit-default','default age12 seed41 fatness50')
                equal('zero-seed','explicit-default','zero seed resolves41')
                print(f'{key}: {len(bylabel)} renders, relationships pass',flush=True)
    if verify: assert report==expected; print('FULL REPLAY PASS')
    else: (ROOT/'experiments/young-001.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--verify',action='store_true'); asyncio.run(run(p.parse_args().verify))
