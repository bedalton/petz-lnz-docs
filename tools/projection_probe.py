"""Asset-free Project Ball implementation probe; no MCP or game claims."""
import hashlib
import importlib.metadata
import json
import platform
from pathlib import Path
from types import SimpleNamespace
from petz_renderer.appearance.core import Projection, Move
from petz_renderer.formats.animation import BallFrame, BallPosition
from petz_renderer.rendering.positions import modify_positions

ROOT = Path(__file__).resolve().parents[1]
frame = BallFrame((0, 0, 0, 20, 0, 0), 0,
                  tuple(BallPosition(x, 0, 0, 0, 0, 0) for x in (0, 10, 20)), ())
cases = []
def run(name, rows, expected, moves=()):
    appearance = SimpleNamespace(species=0, shape=None, moves=moves,
                                 projections=tuple(Projection(*r) for r in rows))
    result = modify_positions(appearance, frame)
    actual = [b.x for b in result.balls]
    assert actual == expected, (name, actual, expected)
    assert all(b.y == b.z == 0 for b in result.balls)
    cases.append(dict(name=name, rows=rows, moves=[vars(m) for m in moves], x=actual))
for percent, end in [(0, 0), (50, 5), (100, 10), (150, 15), (-50, -5)]:
    run(f'percent_{percent}', [(0, 1, percent)], [0, end, 20])
run('repeat', [(0, 1, 50), (0, 1, 50)], [0, 2, 20])
run('chain', [(0, 1, 50), (1, 2, 50)], [0, 5, 12])
run('reverse_chain', [(1, 2, 50), (0, 1, 50)], [0, 5, 15])
run('invalid_ids', [(-1, 1, 50), (0, 3, 50)], [0, 10, 20])
run('self', [(1, 1, 0)], [0, 10, 20])
run('move_before_projection', [(0, 1, 50)], [2, 6, 20], (Move(0, 2, 0, 0, 0),))
report = dict(backend='direct Python implementation; no MCP/render/game',
              python=platform.python_version(), renderer=importlib.metadata.version('petz-renderer-mcp'),
              source_hashes={p: hashlib.sha256((ROOT/'petz-renderer-mcp'/p).read_bytes()).hexdigest()
                for p in ['src/petz_renderer/appearance/core.py', 'src/petz_renderer/rendering/positions.py']},
              controls=dict(species=0, coordinates=[0,10,20], rotations=0, shape='bypassed: three-ball frame'), cases=cases)
(ROOT/'experiments/project-001.json').write_text(json.dumps(report, indent=2)+'\n')
print(f'{len(cases)} synthetic cases passed')
