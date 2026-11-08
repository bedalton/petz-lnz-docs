"""Run read-only local MCP checks; private outputs stay under scratch."""
import asyncio
import base64
import hashlib
import json
import sys
from pathlib import Path
from fastmcp import Client
from fastmcp.client.transports import StdioTransport

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'scratch/research/smoke-001'

async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    results = []
    for version in ('petz4', 'petz3', 'petz5'):
        transport = StdioTransport(sys.executable, ['-I', '-m', 'petz_renderer.service.local_mcp',
            '--game-root', str(ROOT / 'games' / version), '--game-version', version])
        async with Client(transport) as client:
            caps = await client.call_tool('get_capabilities')
            (OUT / f'{version}-capabilities.json').write_text(json.dumps(caps.data, indent=2))
            for species, filename in [('Dogz', 'Scottie.dog'), ('Catz', 'Siamese.cat')]:
                path = f'Resource/{species}/{filename}'
                row = {'version': version, 'path': path, 'parameters': {'seed': 0, 'pose': 'standing', 'yaw_degrees': 0, 'age': 100, 'fatness': 50}}
                try:
                    inspected = await client.call_tool('inspect_input', {'path': path, 'seed': 0})
                    rendered = await client.call_tool('render_pet', {'path': path, **row['parameters']})
                    image = next(c for c in rendered.content if c.type == 'image')
                    png = base64.b64decode(image.data)
                    stem = f'{version}-{species.lower()}'
                    (OUT / f'{stem}.png').write_bytes(png)
                    (OUT / f'{stem}-inspect.json').write_text(json.dumps(inspected.data, indent=2))
                    (OUT / f'{stem}-render.json').write_text(json.dumps(rendered.data, indent=2))
                    row.update(ok=not rendered.is_error, input_sha256=hashlib.sha256((ROOT/'games'/version/path).read_bytes()).hexdigest(), png_sha256=hashlib.sha256(png).hexdigest(), png_bytes=len(png))
                except Exception as exc:
                    row.update(ok=False, error=str(exc))
                results.append(row)
                (OUT/'report.json').write_text(json.dumps(results, indent=2))
                print(json.dumps(row), flush=True)
    if not all(r['ok'] for r in results):
        raise SystemExit(1)

if __name__ == '__main__':
    asyncio.run(main())
