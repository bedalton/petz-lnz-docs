"""Audit geometry of base IDs unchanged in both OMIT-001 views (no new renders)."""
import json
import subprocess
import sys
from pathlib import Path
import petz_renderer
from dataclasses import asdict
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_breed_assets
from petz_renderer.rendering.pose import posed_geometry
from research_common import ROOT, SHA, adult


def main():
    sweep_bytes = (ROOT / 'experiments/omit-001.json').read_bytes()
    sweep = json.loads(sweep_bytes)
    revision = subprocess.check_output(
        ['git', '-C', str(ROOT / 'petz-renderer-mcp'), 'rev-parse', 'HEAD'], text=True
    ).strip()
    assert revision == sweep['renderer_revision']
    resolver = ResourceResolver((ROOT / 'games/petz4',))
    cases = []
    for case in sweep['cases']:
        species = case['species']
        source, raw, *_ = adult(species)
        assert SHA(raw) == case['source_sha256']
        observations = [o for o in sweep['observations'] if o['species'] == species]
        ids = [i for i in range(67) if all(
            next(o for o in observations if o['ball'] == i and o['yaw'] == yaw)['same_as_control']
            for yaw in (0, 90))]
        poses = {}
        for pose in ('standing', 'sitting', 'lying'):
            assets = load_breed_assets(resolver, source.relative_to(ROOT / 'games/petz4').as_posix(), pose=pose, seed=0, age=100, fatness=50)
            shape = posed_geometry(assets.appearance, assets.sizes, assets.frame, fatness=50)
            poses[pose] = {str(i): asdict(shape[i]) for i in ids}
        cases.append({'species': species, 'source_sha256': SHA(raw), 'ids': ids,
                      'master_sha256': SHA((ROOT / f'games/petz4/Resource/{species} 4 Rez.dll').read_bytes()),
                      'already_omitted_ids': case['already_omitted_base_ids'], 'poses': poses})
    report = {'experiment': 'VIS-001', 'backend': 'local Python renderer geometry API; no raster calls',
              'renderer_revision': revision, 'python': sys.version,
              'installed_python_sources_sha256': SHA(b''.join(
                  p.relative_to(Path(petz_renderer.__file__).parent).as_posix().encode() + b'\0' + p.read_bytes()
                  for p in sorted(Path(petz_renderer.__file__).parent.rglob('*.py')))),
              'omission_manifest_sha256': SHA(sweep_bytes),
              'controls': {'seed': 0, 'age': 100, 'fatness': 50,
                           'poses': ['standing', 'sitting', 'lying']}, 'cases': cases}
    (ROOT / 'experiments/vis-001.json').write_text(json.dumps(report, indent=2) + '\n')
    for case in cases:
        print(case['species'], {i: [(p, case['poses'][p][str(i)]['radius'],
                                    case['poses'][p][str(i)]['visible'])
                                   for p in case['poses']] for i in case['ids']})


if __name__ == '__main__':
    main()
