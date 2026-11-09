"""Check whole-section inheritance through real breed copies and local MCP."""
import asyncio,json,sys
from dataclasses import asdict
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.appearance.layers import load_layer
from petz_renderer.appearance.lnz import parse_sections
from petz_renderer.formats.pe import ResourceFile
from research_common import ROOT,SHA,adult,write_copy,save_result
OUT=ROOT/'scratch/research/inherit-001'

async def main():
    OUT.mkdir(parents=True,exist_ok=True)
    cases=[]
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,masterfile,master=adult(species)
        keys=parse_sections(masterfile.read('LNZ',master))['Key Balls']
        for variant in ('absent','empty','partial','full'):
            sections=dict(base);sections.pop('Key Balls',None)
            if variant!='absent': sections['Key Balls']=() if variant=='empty' else keys[:1] if variant=='partial' else keys
            path=OUT/f'{species}-{variant}{source.suffix}'
            digest=write_copy(raw,leaf,sections,path)
            layer=load_layer(ResourceFile(path.read_bytes()),masterfile,name=leaf.name,seed=0)
            expected=tuple(keys) if variant=='absent' else sections['Key Balls']
            assert layer.sections['Key Balls']==expected
            cases.append({'species':species,'variant':variant,'input_sha256':digest,'path':path.name,'key_balls':asdict(layer.appearance.key_balls),'effective_rows':len(expected)})
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        baselines={}
        for case in cases:
            args={'path':case['path'],'pose':'standing','seed':0,'age':100,'fatness':50,'yaw_degrees':0}
            png,metadata=await save_result(client,'render_pet',args,OUT,f"{case['species']}-{case['variant']}")
            if case['variant']=='absent': baselines[case['species']]=png
            case.update(controls=args,png_sha256=SHA(png),matches_absent=png==baselines[case['species']],diagnostics=metadata.get('diagnostics',[]))
            (OUT/'report.json').write_text(json.dumps(cases,indent=2)+'\n')
            print(case['species'],case['variant'],case['effective_rows'],case['matches_absent'],flush=True)
    assert all(c['matches_absent'] for c in cases if c['variant']=='full')
    public=[{k:v for k,v in c.items() if k!='diagnostics'} for c in cases]
    (ROOT/'experiments/inherit-001.json').write_text(json.dumps(public,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
