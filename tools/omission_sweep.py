"""Omit each base ball in synthetic variation sheets with a repeated control."""
import argparse,asyncio,json,sys
from dataclasses import fields
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.appearance.layers import load_layer
from petz_renderer.appearance.variations import inspect_variations
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from research_common import ROOT,SHA,adult,write_copy,save_result
OUT=ROOT/'scratch/research/omit-001'

def prepare():
    cases=[]
    for species in ('Dogz','Catz'):
        source,raw,leaf,base,master,_=adult(species)
        baseline=load_layer(ResourceFile(raw),master,name=leaf.name,seed=0).appearance
        sections=dict(base);rows=list(base.get('Omissions',()))
        rows.append('#68.0')  # Branch 68 is unchanged control; branches 67..1 omit 0..66.
        for ball in range(67):rows.extend((f'#{67-ball}',str(ball)))
        rows.append('##');sections['Omissions']=tuple(rows)
        path=OUT/f'{species}-sweep{source.suffix}'
        digest=write_copy(raw,leaf,sections,path)
        content=ResourceFile(path.read_bytes()).read('LNZ',leaf.name)
        seeds={}
        for seed in range(10000):
            trace=inspect_variations(content,seed=seed)
            assert len(trace.blocks)==1
            branch=trace.blocks[0].selected_branch
            seeds.setdefault(branch,seed)
            if len(seeds)==68:break
        assert len(seeds)==68
        resolver=ResourceResolver((ROOT/'games/petz4',OUT))
        for branch,seed in seeds.items():
            resolved=load_layer(ResourceFile(path.read_bytes()),master,name=leaf.name,seed=seed)
            expected_sections=dict(load_layer(ResourceFile(raw),master,name=leaf.name,seed=0).sections)
            ball=None if branch==68 else 67-branch
            if ball is not None: expected_sections['Omissions']=(*expected_sections.get('Omissions',()),str(ball))
            assert dict(resolved.sections)==expected_sections,(species,branch)
            actual=load_breed_assets(resolver,path.name,pose='standing',seed=seed,age=100,fatness=50).appearance
            expected_omissions=baseline.omissions if ball is None else baseline.omissions|{ball}
            assert actual.omissions==expected_omissions
            assert all(getattr(actual,f.name)==getattr(baseline,f.name) for f in fields(baseline) if f.name not in ('omissions','lines'))
            if ball is None: assert actual==baseline
        cases.append({'species':species,'path':path.name,'source_sha256':SHA(raw),'input_sha256':digest,'control_seed':seeds[68],'seed_by_ball':{str(i):seeds[67-i] for i in range(67)},'already_omitted_base_ids':sorted(i for i in baseline.omissions if i<67),'branch_block_id':trace.blocks[0].block_id})
    return cases

def line_evidence(cases):
    for case in cases:
        _,_,leaf,_,master,_=adult(case['species'])
        breed=ResourceFile((OUT/case['path']).read_bytes())
        case['baseline_line_count']=len(load_layer(breed,master,name=leaf.name,seed=case['control_seed']).appearance.lines)
        case['line_count_by_ball']={ball:len(load_layer(breed,master,name=leaf.name,seed=seed).appearance.lines) for ball,seed in case['seed_by_ball'].items()}

def checkpoint(value):
    path=OUT/'progress.json'; temporary=path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value,indent=2)+'\n');temporary.replace(path)

async def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--resume',action='store_true')
    args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    if args.resume:
        saved=json.loads((OUT/'progress.json').read_text())
        cases,pages,observations=(saved[k] for k in ('cases','pages','observations'))
        for c in cases:
            assert SHA((OUT/c['path']).read_bytes())==c['input_sha256']
            assert SHA(adult(c['species'])[1])==c['source_sha256']
        for page in pages:
            assert SHA((OUT/f"{page['stem']}.png").read_bytes())==page['png_sha256']
    else:
        if (OUT/'progress.json').exists():raise SystemExit('Checkpoint exists: use --resume or archive the output directory first.')
        cases=prepare();pages=[];observations=[]
        checkpoint({'cases':cases,'pages':pages,'observations':observations})
    line_evidence(cases)
    checkpoint({'cases':cases,'pages':pages,'observations':observations})
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(OUT)])
    async with Client(transport) as client:
        for c in cases:
            inspection=await client.call_tool('inspect_input',{'path':c['path'],'seed':c['control_seed']})
            assert not inspection.is_error
            (OUT/f"{c['species']}-inspect.json").write_text(json.dumps(inspection.data,indent=2)+'\n')
            for yaw in (0,90):
                for start in range(0,67,15):
                    ids=list(range(start,min(start+15,67)))
                    stem=f"{c['species']}-yaw{yaw}-ids{start}-{ids[-1]}"
                    if any(p['stem']==stem for p in pages):continue
                    seeds=[c['control_seed']]+[c['seed_by_ball'][str(i)] for i in ids]
                    args={'path':c['path'],'pose':'standing','age':100,'fatness':50,'yaw_degrees':yaw,'seeds':seeds,'columns':4}
                    stem=f"{c['species']}-yaw{yaw}-ids{start}-{ids[-1]}"
                    png,meta=await save_result(client,'render_contact_sheet',args,OUT,stem)
                    assert len(meta['cells'])==len(seeds)
                    control=meta['cells'][0]['pixel_sha256']
                    for ball,cell in zip(ids,meta['cells'][1:]):
                        observations.append({'species':c['species'],'yaw':yaw,'ball':ball,'same_as_control':cell['pixel_sha256']==control,'pixel_sha256':cell['pixel_sha256'],'sheet':stem,'cell_index':ids.index(ball)+1})
                    pages.append({'species':c['species'],'controls':args,'cell_ball_ids':[None]+ids,'png_sha256':SHA(png),'stem':stem})
                    checkpoint({'cases':cases,'pages':pages,'observations':observations})
                    print(stem,flush=True)
    assert len(pages)==20 and len(observations)==268
    assert len({(o['species'],o['yaw'],o['ball']) for o in observations})==268
    for c in cases:
        for observation in observations:
            if observation['species']==c['species'] and observation['ball'] in c['already_omitted_base_ids']:assert observation['same_as_control']
    report={'experiment':'OMIT-001','renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9','python':sys.version,'cases':cases,'pages':pages,'observations':observations}
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');(ROOT/'experiments/omit-001.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':asyncio.run(main())
