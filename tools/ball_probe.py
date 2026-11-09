"""Controlled private Petz 4 ball edits through local stdio MCP."""
import asyncio, base64, hashlib, json, sys
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.appearance.lnz import parse_sections
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'scratch/research/ball-001'
sha=lambda b: hashlib.sha256(b).hexdigest()

def prepare(species, filename, selector, master):
    source=ROOT/'games/petz4/Resource'/species/filename
    raw=source.read_bytes(); pe=ResourceFile(raw)
    leaf=next(r for r in pe.resources if r.type=='LNZ' and r.name==selector)
    sections=dict(parse_sections(pe.read('LNZ',selector),0))
    rez=ResourceFile((ROOT/f'games/petz4/Resource/{species} 4 Rez.dll').read_bytes())
    ms=parse_sections(rez.read('LNZ',master),0)
    ball=int(ms['Key Balls'][0].split(',')[0].split()[0])
    (OUT/f'{species}-inventory.json').write_text(json.dumps({'breed_sections':{k:len(v) for k,v in sections.items()},'master_sections':{k:len(v) for k,v in ms.items()},'head_ball':ball},indent=2))
    paths={}
    for variant in ('control','size','color','move'):
        s=dict(sections)
        if variant!='control':
            name,row={'size':('Ball Size Override',f'{ball}, 25'),'color':('Color Info Override',f'{ball}, 125'),'move':('Move',f'{ball}, 20, 0, 0')}[variant]
            s[name]=(*s.get(name,()),row)
        payload=('\n'.join('['+k+']\n'+'\n'.join(v) for k,v in s.items())+'\n').encode('cp1252')
        assert len(payload)<=leaf.size
        edited=raw[:leaf.offset]+payload.ljust(leaf.size,b' ')+raw[leaf.offset+leaf.size:]
        check=ResourceFile(edited)
        for r in pe.resources:
            if r!=leaf: assert pe.read(r.type,r.name,r.language)==check.read(r.type,r.name,r.language)
        assert raw[:leaf.offset]==edited[:leaf.offset] and raw[leaf.offset+leaf.size:]==edited[leaf.offset+leaf.size:]
        path=OUT/f'{species}-{variant}{source.suffix}';path.write_bytes(edited);paths[variant]=path.name
    return source,ball,paths

async def main():
    OUT.mkdir(parents=True,exist_ok=True)
    cases=[('Dogz','Scottie.dog','SC','DOGMASTER'),('Catz','Siamese.cat','SI','CATMASTER')]
    prepared=[(s,*prepare(s,f,n,m)) for s,f,n,m in cases]
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    report=[]
    async with Client(transport) as client:
        for species,source,ball,paths in prepared:
            original=None
            for variant,path in [('original',str(source.relative_to(ROOT/'games/petz4'))),*paths.items()]:
                args={'path':path,'seed':0,'age':100,'fatness':50,'pose':'standing','yaw_degrees':0}
                result=await client.call_tool('render_pet',args)
                png=base64.b64decode(next(c.data for c in result.content if c.type=='image'))
                stem=f'{species}-{variant}'
                (OUT/f'{stem}.png').write_bytes(png)
                (OUT/f'{stem}-render.json').write_text(json.dumps(result.data,indent=2))
                if variant=='original': original=png
                if variant=='control': assert png==original,'resolved control changed pixels'
                row={'species':species,'variant':variant,'ball':ball,'controls':args,'png_sha256':sha(png),'input_sha256':sha((source if variant=='original' else OUT/path).read_bytes()),'matches_original':png==original}
                report.append(row);(OUT/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(row),flush=True)
    assert all(not r['matches_original'] for r in report if r['variant'] in ('size','color','move'))
if __name__=='__main__':asyncio.run(main())
