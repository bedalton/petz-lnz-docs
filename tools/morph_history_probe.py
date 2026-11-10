"""MORPH-004: retained assembly state versus batched explicit histories."""
import json,sys,importlib.metadata
from dataclasses import asdict
from pathlib import Path
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.assembly import assemble_geometry
from research_common import ROOT,SHA,adult
OUT=ROOT/'scratch/research/morph-004'
HISTORIES={'a_then_b':((14,50),(15,50)),'b_then_a':((15,50),(14,50)),'cycle':((14,100),(15,100),(14,0),(14,50),(15,50)),'noops':((14,50),(14,50),(15,50),(15,50)),'unused':((13,100),(14,50),(15,50))}
def snapshot(g):
    count=len(g.balls)
    return {'balls':[asdict(b) for b in g.balls],'fills':g.fills,'sorted_order':g.ordering.sorted_order,'draw_order':g.ordering.draw_order,'bounds':asdict(g.ordering.bounds),'mask':g.state.order.group_mask,'shade_offsets':g.state.shade.offsets[:count],'shade_distances':g.state.shade.last_distances[:count]}
def main():
    OUT.mkdir(parents=True,exist_ok=False)
    prior=json.loads((ROOT/'experiments/morph-003.json').read_text());cases=[]
    resolver=ResourceResolver((ROOT/'games/petz4',ROOT/'scratch/research/morph-003'))
    for c in prior['cases']:
        source,raw,*_=adult(c['species']);assert SHA(raw)==c['source_sha256']
        for variant in ('dormant_body','dormant_head'):
            path=ROOT/'scratch/research/morph-003'/c['paths'][variant]
            assert SHA(path.read_bytes())==c['input_hashes'][variant]
            for pose in ('standing','sitting','lying'):
                a=load_breed_assets(resolver,path.name,pose=pose,seed=0,age=100,fatness=50)
                assert 13 not in {add.add_group for add in a.appearance.add_balls}
                call=lambda **kw:assemble_geometry(a.appearance,a.sizes,a.frame,fatness=50,**kw)
                untouched=call()
                repeated=call(state=untouched.state)
                baseline={'same_balls':untouched.balls==repeated.balls,'same_fills':untouched.fills==repeated.fills,'same_draw_order':untouched.ordering.draw_order==repeated.ordering.draw_order}
                assert baseline['same_balls'] and baseline['same_fills']
                results={}
                for name,history in HISTORIES.items():
                    direct=call(morph_updates=history)
                    current=call()
                    for n in range(1,len(history)+1):current=call(state=current.state,morph_updates=history[:n])
                    assert current.balls==direct.balls
                    assert current.ordering.bounds==direct.ordering.bounds
                    assert current.state.morph_updates==history
                    # Further identical frames must preserve immutable geometry and histories.
                    again=call(state=current.state,morph_updates=history)
                    assert again.balls==current.balls and again.fills==current.fills
                    rejected=False
                    try:call(state=current.state,morph_updates=((14,0),))
                    except ValueError as e:
                        assert 'history' in str(e);rejected=True
                    assert rejected
                    results[name]={'batch':snapshot(direct),'incremental':snapshot(current),'same_draw_order':direct.ordering.draw_order==current.ordering.draw_order,'same_sorted_order':direct.ordering.sorted_order==current.ordering.sorted_order,'same_fills':direct.fills==current.fills,'same_shade_offsets':direct.state.shade.offsets==current.state.shade.offsets,'same_shade_distances':direct.state.shade.last_distances==current.state.shade.last_distances,'rejects_nonprefix_history':rejected}
                assert all(results[n]['batch']['balls']==results['a_then_b']['batch']['balls'] for n in HISTORIES)
                assert results['noops']['batch']==results['a_then_b']['batch']
                assert results['unused']['batch']==results['a_then_b']['batch']
                cases.append({'species':c['species'],'variant':variant,'pose':pose,'baseline_repeated_frame':baseline,'input':path.name,'input_sha256':c['input_hashes'][variant],'histories':results})
    import petz_renderer
    installed=Path(petz_renderer.__file__).parent;hashes={}
    for name in ('appearance/evaluation.py','rendering/morphs.py','rendering/attachment.py','rendering/assembly.py','rendering/ordering.py','rendering/shading.py'):
        content=(installed/name).read_bytes();assert content==(ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes();hashes[name]=SHA(content)
    provenance=json.loads((ROOT/'experiments/restore-002.json').read_text())
    for path,expected in provenance['shared_engine_hashes']['petz4'].items():assert SHA(resolver.read_bytes(path,limit=268435456).data)==expected,path
    summary={key:sum(not h[key] for c in cases for h in c['histories'].values()) for key in ('same_draw_order','same_sorted_order','same_fills','same_shade_offsets','same_shade_distances')}
    report={'experiment':'MORPH-004','backend':'direct Python asset-backed assembly; no new MCP images','renderer_revision':prior['renderer_revision'],'python':sys.version,'controls':{'seed':0,'age':100,'fatness':50,'head_rotation':0},'reused_input_manifest':'morph-003.json','histories':HISTORIES,'cases':cases,'batch_incremental_difference_counts':summary,'source_hashes':hashes,'shared_engine_hashes':provenance['shared_engine_hashes']['petz4'],'dependency_versions':{name:importlib.metadata.version(name) for name in ('fastmcp','numpy','Pillow','pydantic')}}
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    public=json.loads(json.dumps(report))
    for c in public['cases']:
        for h in c['histories'].values():
            batch=h.pop('batch');incremental=h.pop('incremental')
            h['batch_snapshot_sha256']=SHA(json.dumps(batch,sort_keys=True).encode())
            h['incremental_snapshot_sha256']=SHA(json.dumps(incremental,sort_keys=True).encode())
            h['final_markers']=batch['balls'][-3:]
            h['draw_order_changed_positions']=[{'index':i,'batch':b,'incremental':v} for i,(b,v) in enumerate(zip(batch['draw_order'],incremental['draw_order'])) if b!=v]
            h['shade_distance_changed_ids']=[i for i,(b,v) in enumerate(zip(batch['shade_distances'],incremental['shade_distances'])) if b!=v]
        a=c['histories']['a_then_b'];b=c['histories']['b_then_a']
        # Snapshot hashes include histories only indirectly through evaluated state.
        c['retained_distinct_update_order_same_draw_order']=report['cases'][public['cases'].index(c)]['histories']['a_then_b']['incremental']['draw_order']==report['cases'][public['cases'].index(c)]['histories']['b_then_a']['incremental']['draw_order']
    (ROOT/'experiments/morph-004.json').write_text(json.dumps(public,indent=2)+'\n')
    print(json.dumps(summary));print('Assembly histories:',len(cases)*len(HISTORIES))
if __name__=='__main__':main()
