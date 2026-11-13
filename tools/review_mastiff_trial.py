"""Independently inspect the frozen Mastiff binaries and replay local MCP previews.

Run with the renderer environment; no authoring/evaluation files are overwritten.
Private inputs and output stay under /workspace. This is not a game test.
"""
import asyncio
import base64
import hashlib
import importlib.metadata
import json
import re
import sys
from pathlib import Path

import petz_renderer
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from petz_renderer.appearance.layers import load_layer
from petz_renderer.appearance.evaluation import body_areas
from petz_renderer.formats.pe import ResourceFile

ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / 'scratch/breed-attempts/english-mastiff'
OUT = ROOT / 'scratch/research/mastiff-review-001'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tokens(row):
    return re.split(r'[,\s]+', row.strip())


async def main():
    OUT.mkdir(parents=True, exist_ok=False)
    protected = {str(p.relative_to(ROOT)): sha(p) for p in TASK.rglob('*')
                 if p.is_file() and p.name != '.DS_Store'}
    (OUT/'protected-before.json').write_text(json.dumps(protected, indent=2)+'\n')
    paths = [ROOT / 'clean_dogs/petz4/Labrador.dog',
             TASK / 'inputs/baseline.dog', TASK / 'output/English Mastiff.dog',
             ROOT / 'games/petz4/Resource/Dogz 4 Rez.dll',
             ROOT / 'games/petz4/Resource/Catz 4 Rez.dll',
             ROOT / 'games/petz4/Resource/Petz 4 Rez.dll',
             ROOT / 'games/petz4/Petz 4.exe']
    hashes = {str(p.relative_to(ROOT)): sha(p) for p in paths}
    assert sha(paths[0]) == sha(paths[1])
    base, final, master = [ResourceFile(p.read_bytes()) for p in
                           (paths[0], paths[2], paths[3])]
    keys = lambda obj: [(x.type, x.name, x.language) for x in obj.resources]
    assert keys(base) == keys(final)
    changed = [k for k in keys(base) if base.read(*k) != final.read(*k)]
    result = {'inputs': hashes, 'resource_count': len(keys(base)),
              'changed_resources': changed, 'layers': {}}
    for name in ('LR', 'LRPUP'):
        a, b = [load_layer(obj, master, name=name, seed=41)
                for obj in (base, final)]
        sa, sb = a.sections, b.sections
        adds_a, adds_b = [list(map(tokens, s['Add Ball'])) for s in (sa, sb)]
        # Compare actual retained fields rather than assuming identity by index.
        retained = []
        for i, old in enumerate(adds_a):
            new = adds_b[i]
            fields = [j for j, (x, y) in enumerate(zip(old, new)) if x != y]
            assert len(old) == len(new) and fields == [6], (name, i, fields)
            assert old[6] == '0' and new[6] == '-1'
            retained.append({'id': 67 + i, 'changed_fields_zero_based': fields})
        assert len(sa['Ballz Info']) == len(sb['Ballz Info']) == 67
        old_lines, new_lines = [list(map(tokens, s['Linez'])) for s in (sa, sb)]
        assert [r[:2] for r in old_lines] == [r[:2] for r in new_lines[:len(old_lines)]]
        c = b.appearance
        total = len(c.balls) + len(c.add_balls)
        bad = []
        def check(section, val):
            if not 0 <= val < total:
                bad.append([section, val])
        for ball in c.add_balls:
            check('Add Ball parent', ball.base)
            if ball.size_base_ball >= 0:
                check('Add Ball size reference', ball.size_base_ball)
        for line in c.lines:
            check('Linez start', line.start)
            check('Linez end', line.end)
        for val in c.omissions:
            check('Omissions', val)
        for row in sb['Move']:
            t = tokens(row)
            check('Move target', int(t[0]))
            if len(t) > 4 and int(t[4]) >= 0:
                check('Move reference', int(t[4]))
        for row in sb['Project Ball']:
            for val in tokens(row)[:2]:
                check('Project Ball', int(val))
        for section in ('Color Info Override', 'Outline Color Override',
                        'Ball Size Override', 'Fuzz Override', 'Paint Ballz'):
            for row in sb.get(section, []):
                check(section, int(tokens(row)[0]))
        invalid_textures = [{'id': i, 'slot': ball.texture,
                             'omitted': i in c.omissions}
                            for i, ball in enumerate((*c.balls, *c.add_balls))
                            if ball.texture >= len(c.textures)]
        areas = body_areas(c)
        result['layers'][name] = {
            'base_counts': [len(a.appearance.balls), len(a.appearance.add_balls)],
            'final_counts': [len(c.balls), len(c.add_balls)],
            'retained_add_fields': retained,
            'new_nodes': [{'id': 67+i, 'parent': ball.base,
                           'body_area': areas[67+i]}
                          for i, ball in enumerate(c.add_balls) if i >= len(adds_a)],
            'omissions_added': sorted(c.omissions-a.appearance.omissions),
            'omissions_removed': sorted(a.appearance.omissions-c.omissions),
            'all_old_adds_omitted': all(i in c.omissions for i in range(67,95)),
            'raw_line_counts': [len(old_lines), len(new_lines)],
            'invalid_ball_references': bad,
            'invalid_effective_textures': invalid_textures,
            'base_body_extension': list(sa['Body Extension']),
            'final_body_extension': list(sb['Body Extension']),
        }
        assert not bad
    package = Path(petz_renderer.__file__).parent
    result['runtime'] = {
        'python': sys.version,
        'packages': {n: importlib.metadata.version(n) for n in
                     ('petz-renderer-mcp', 'fastmcp', 'Pillow', 'pefile')},
        'source_hashes': {str(p.relative_to(package)): sha(p)
                          for p in package.rglob('*.py')},
    }
    # Reuse the recorded requests as controls, but execute a fresh real MCP.
    records = json.loads((TASK/'evidence/evaluation-002/renders.json').read_text())
    transport = StdioTransport(sys.executable,
        ['-I', '-m', 'petz_renderer.service.local_mcp', '--game-root',
         str(ROOT/'games/petz4'), '--asset-root', str(TASK)])
    replays = []
    async with Client(transport) as client:
        for rec in records:
            response = await client.call_tool('render_pet', rec['args'])
            assert not response.is_error, rec['name']
            png = base64.b64decode(next(x.data for x in response.content if x.type == 'image'))
            digest = hashlib.sha256(png).hexdigest()
            assert digest == rec['png_sha256'], rec['name']
            assert sha(TASK/'evidence/evaluation-002/previews'/f"{rec['name']}.png") == digest
            (OUT/f"{rec['name']}.png").write_bytes(png)
            replays.append({'name': rec['name'], 'args': rec['args'],
                            'sha256': digest, 'metadata': response.data})
            print('Matched', rec['name'], flush=True)
    result['replays'] = replays
    after = {str(p.relative_to(ROOT)): sha(p) for p in TASK.rglob('*')
             if p.is_file() and p.name != '.DS_Store'}
    differences = {key: [protected.get(key), after.get(key)]
                   for key in protected.keys() | after.keys()
                   if protected.get(key) != after.get(key)}
    (OUT/'preservation-differences.json').write_text(json.dumps(differences, indent=2)+'\n')
    assert not differences, differences
    assert hashes == {str(p.relative_to(ROOT)): sha(p) for p in paths}
    result['protected_task_files'] = protected
    result['script_sha256'] = sha(Path(__file__))
    (OUT/'verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print('Verified', len(replays), 'MCP replays;', len(protected), 'task files unchanged')


if __name__ == '__main__':
    asyncio.run(main())
