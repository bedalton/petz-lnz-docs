"""YOUNG-008: exhaustive tail subsets on a fixed sufficient background."""
import argparse, asyncio, base64, itertools, json, sys
from dataclasses import replace
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from petz_renderer.rendering.output import render_portrait
from young_breed_probe import ROOT, digest, provenance
from young_endpoint_attribution import difference, sig
from young_endpoint_fields import FACTORS, modify
OUT = ROOT/'scratch/research/young-008'
MANIFEST = ROOT/'experiments/young-008.json'
FACTORS_TAIL = tuple(f'add-{i}' for i in range(23, 29)) + ('count',)

def appearance(a, b, selected):
    full = modify(a, b, FACTORS)
    rows = list(a.add_balls)
    for i in range(23, 29):
        if f'add-{i}' in selected:
            rows[i] = b.add_balls[i]
    if 'count' in selected:
        rows = rows[:29] + list(b.add_balls[29:])
    return replace(full, add_balls=tuple(rows))

async def run(verify):
    previous = json.loads(MANIFEST.read_text()) if verify else None
    if not verify:
        OUT.mkdir(parents=True, exist_ok=False)
    prior_path = ROOT/'experiments/update-011.json'
    prior = json.loads(prior_path.read_text())
    source = prior['inputs']
    resolver = ResourceResolver((ROOT/'games/petz4', ROOT/'scratch/research/young-002'))
    report = {'provenance': provenance(), 'backend': 'direct installed renderer; local stdio MCP endpoint controls',
              'prior_manifest_sha256': digest(prior_path.read_bytes()), 'inputs': source,
              'script_sha256': digest(Path(__file__).read_bytes()), 'factors': FACTORS_TAIL,
              'fixtures': [], 'renders': [], 'mcp': []}
    # Normalize tuples before exact JSON replay comparison.
    report['factors'] = list(FACTORS_TAIL)
    endpoints = {}
    for mode in ('missing-adult', 'missing-young'):
        variant = source['variants'][mode]
        assert digest((ROOT/'scratch/research/young-002'/variant['path']).read_bytes()) == variant['sha256']
        for pose in ('standing', 'sitting', 'lying'):
            age = load_saved_assets(resolver, variant['path'], pose=pose, look='age', age=12)
            young = load_saved_assets(resolver, variant['path'], pose=pose, look='puppy', age=12)
            a, b = age.appearance, young.appearance
            assert {len(a.add_balls),len(b.add_balls)} == {29,32}
            for yaw in (0,90):
                target = render_portrait(young, yaw=yaw*256//360)
                endpoints[mode,pose,yaw] = target.png
                rows = []
                for mask in range(128):
                    selected = [f for i,f in enumerate(FACTORS_TAIL) if mask & (1 << i)]
                    result = render_portrait(replace(age,appearance=appearance(a,b,selected)),yaw=yaw*256//360)
                    stem = f'{mode}-{pose}-{yaw}-{mask:03d}'
                    if verify:
                        assert (OUT/f'{stem}.png').read_bytes() == result.png
                    else:
                        (OUT/f'{stem}.png').write_bytes(result.png)
                    row = {'mode':mode,'pose':pose,'yaw':yaw,'mask':mask,'selected':selected,
                           'file':f'{stem}.png','png_sha256':digest(result.png),'size':[result.width,result.height],
                           'offset':list(result.offset),'equals_young':sig(result)==sig(target),
                           'pixels_vs_young':difference(result,target)}
                    report['renders'].append(row); rows.append(row)
                assert rows[-1]['equals_young']
                link = next(r for r in prior['renders'] if (r['unit'],r['mode'],r['pose'],r['yaw'],r['label']) == ('young-007',mode,pose,yaw,'full'))
                assert rows[-1]['png_sha256'] == link['png_sha256']
                sufficient = [r['mask'] for r in rows if r['equals_young']]
                minimal = [m for m in sufficient if not any(n != m and n & m == n for n in sufficient)]
                violations = [[m,n] for m in sufficient for n in range(128) if m & n == m and n not in sufficient]
                report['fixtures'].append({'mode':mode,'pose':pose,'yaw':yaw,
                    'minimal_masks':minimal,'minimal_subsets':[[f for i,f in enumerate(FACTORS_TAIL) if m&(1<<i)] for m in minimal],
                    'sufficient_count':len(sufficient),'monotonicity_violations':violations,
                    'prior_full_sha256':link['png_sha256'], 'target_sha256':digest(target.png)})
            print(f'{mode}/{pose}: 256 subsets pass',flush=True)
    transport = StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp','--game-root',str(ROOT/'games/petz4'),'--asset-root',str(ROOT/'scratch/research/young-002')])
    async with Client(transport) as client:
        for mode in ('missing-adult','missing-young'):
            for pose in ('standing','sitting','lying'):
                for yaw in (0,90):
                    args = {'path':source['variants'][mode]['path'],'pose':pose,'look':'puppy','age':12,'yaw_degrees':yaw}
                    response = await client.call_tool('render_pet',args)
                    assert not response.is_error
                    png = base64.b64decode(next(c.data for c in response.content if c.type=='image'))
                    assert png == endpoints[mode,pose,yaw]
                    report['mcp'].append({'controls':args,'png_sha256':digest(png)})
    report['summary'] = {'renders':len(report['renders']),'mcp_matches':len(report['mcp']),
                         'prior_links':len(report['fixtures']), 'minimal_sets':sum(len(f['minimal_masks']) for f in report['fixtures']),
                         'monotonicity_violations':sum(len(f['monotonicity_violations']) for f in report['fixtures'])}
    if verify:
        assert report == previous
        print('FULL REPLAY PASS',flush=True)
    else:
        MANIFEST.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['summary']),flush=True)
if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');asyncio.run(run(p.parse_args().verify))
