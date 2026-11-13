"""Build a private, read-only Petz4 baseline gallery via local MCP.

Run with the renderer environment from /workspace. Existing matching checkpoint
renders are verified and reused; inputs and runtime must match the checkpoint.
No input resources are edited. Images and detailed metadata stay ignored.
"""
import asyncio
import base64
import hashlib
import importlib.metadata
import io
import json
import platform
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from PIL import Image, ImageDraw, ImageFont
import petz_renderer

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'clean_dogs'
OUT = BASE / 'reference'
VIEWS = [('front', 'standing', 0), ('three-quarter', 'standing', 45),
         ('side', 'standing', 90), ('rear', 'standing', 180),
         ('sitting-side', 'sitting', 90), ('lying-side', 'lying', 90)]
CONTROLS = dict(seed=41, age=100, fatness=50, look='adult')
FONT = ImageFont.load_default(size=16)
SMALL = ImageFont.load_default(size=13)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, obj):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(obj, indent=2) + '\n')
    temp.replace(path)


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def link(path):
    return quote(str(path), safe='/.-')


def make_inventory():
    stocks = {p.stem.replace(' ', '').lower(): p for p in
              (ROOT / 'games/petz4/Resource/Dogz').glob('*.dog')}
    rows = []
    for p in sorted((BASE / 'petz4').glob('*.dog')):
        family = p.stem.split('--')[0].replace(' ', '').lower()
        stock = stocks[family]
        rows.append(dict(name=p.stem, key=slug(p.stem), path=str(p.relative_to(ROOT)),
                         sha256=sha(p), stock=str(stock.relative_to(ROOT)),
                         stock_key=slug(stock.stem), family=stock.stem))
    if not rows or len({r['key'] for r in rows}) != len(rows):
        raise ValueError('No inputs or ambiguous normalized filenames')
    return rows


def build_sheets(manifest):
    # The renderer returns tightly cropped canvases. Align their reported
    # projection origins in a shared canvas, then use a uniform 2x pixel zoom.
    frames = manifest['renders']
    left = max(r['metadata']['offset'][0] for r in frames) + 8
    top = max(r['metadata']['offset'][1] for r in frames) + 8
    right = max(r['size'][0]-r['metadata']['offset'][0] for r in frames) + 8
    bottom = max(r['size'][1]-r['metadata']['offset'][1] for r in frames) + 8
    native_w, native_h = left+right, top+bottom
    w, h = 2*native_w, 2*native_h
    bar = 34
    for entry in manifest['inputs']:
        sheet = Image.new('RGB', (3*w, 2*(h+bar)+bar), '#747b85')
        d = ImageDraw.Draw(sheet)
        d.text((10, 8), entry['label'], font=FONT, fill='white')
        for i, (view, _, _) in enumerate(VIEWS):
            record = next(r for r in frames if r['key'] == entry['key'] and r['view'] == view)
            im = Image.open(OUT / record['image']).convert('RGBA')
            ox, oy = record['metadata']['offset']
            tile = Image.new('RGBA', (native_w, native_h), '#a4a9b0')
            tile.alpha_composite(im, (left-ox, top-oy))
            tile = tile.resize((w,h), Image.Resampling.NEAREST)
            x, y = (i % 3)*w, bar + (i//3)*(h+bar)
            sheet.paste(tile.convert('RGB'), (x, y+bar))
            d.text((x+10, y+8), view, font=FONT, fill='white')
        name = f"{entry['key']}--views.png"
        sheet.save(OUT / name)
        entry['sheet'] = name
        entry['sheet_sha256'] = sha(OUT / name)
    # Overview thumbnails alone are fitted per input; full sheets remain unscaled.
    rows = manifest['blanks']
    cw, ch = 360, 228
    overview = Image.new('RGB', (4*cw, ((len(rows)+3)//4)*ch), '#747b85')
    d = ImageDraw.Draw(overview)
    for i, entry in enumerate(rows):
        x, y = (i%4)*cw, (i//4)*ch
        d.text((x+8, y+8), entry['name'], font=SMALL, fill='white')
        for j, view in enumerate(('front', 'side')):
            record = next(r for r in manifest['renders'] if r['key'] == 'blank-'+entry['key'] and r['view'] == view)
            im = Image.open(OUT / record['image']).convert('RGBA')
            box = im.getbbox()
            im = im.crop(box)
            im.thumbnail((cw//2-16, ch-65), Image.Resampling.NEAREST)
            tile = Image.new('RGBA', (cw//2, ch-36), '#a4a9b0')
            tile.alpha_composite(im, ((cw//2-im.width)//2, (ch-65-im.height)//2+6))
            overview.paste(tile.convert('RGB'), (x+j*cw//2,y+30))
            d.text((x+j*cw//2+8,y+ch-22), view, font=SMALL, fill='white')
    overview.save(OUT / 'overview.png')
    manifest['overview_sha256'] = sha(OUT / 'overview.png')
    manifest['sheet_layout'] = dict(canvas=[w,h], columns=3, rows=2,
        background='#a4a9b0', native_canvas=[native_w,native_h], origin=[left,top],
        scaling='uniform 2x nearest-neighbor; overview alone fits individual silhouettes')


def write_readme(manifest):
    lines = ['# Blank dog baseline catalog', '',
        'Petz 4 reference gallery for choosing an authoring baseline. '
        'These are renderer-observed previews, not game-validated appearances.', '',
        '## Start here', '',
        '![All blanks: front and side](reference/overview.png)', '',
        'Open a full six-view sheet below before choosing. Overview thumbnails are '
        'individually fitted: **do not compare body size from the overview**. '
        'Full sheets align renderer projection origins in one shared canvas and use the same 2x nearest-neighbor pixel zoom, with no per-dog resizing. '
        'Gray backgrounds are presentation composites; breed colors and geometry were not edited.', '',
        'The six views are standing front (yaw 0), three-quarter (45), side (90), '
        'rear (180), sitting side and lying side. Read sheets left to right, top to bottom. '
        'Controls: adult look, age 100, fatness 50, seed 41; Petz 4 stock named poses. '
        'A single seed does not cover all breed variations.', '',
        '## Form cues for a first shortlist', '',
        'These are qualitative observations from this catalog at its fixed controls, '
        'not breed standards or a complete anatomy validation. Confirm the exact '
        'ear variant in its full sheet.', '',
        '| Family | Form cues visible in these previews |',
        '| --- | --- |',
        '| Bulldog | Broad head/muzzle, sturdy torso and relatively short legs |',
        '| Chihuahua | Slender legs, rounded head and large upright ears |',
        '| Dachshund | Long low torso, short legs and hanging ears |',
        '| Dalmatian | Lean elongated torso and longer legs; several ear variants supplied |',
        '| Great Dane | Leggy, angular silhouette and a long muzzle; several ear variants supplied |',
        '| Labrador | Sturdy torso, broader muzzle and raised tail; several ear variants supplied |',
        '| Mutt | Rounded muzzle/cheeks and curved tail; several ear variants supplied |',
        '| Poodle | Rounded topknot, ear masses and tail pom |',
        '| Scottie | Pointed ears, bearded muzzle and short-legged silhouette |',
        '| Sheepdog | Shaggy outline, covered face and bushy tail |', '',
        '## Blank files and stock counterparts', '',
        'Names before `--` select the stock family; names after it describe the supplied '
        'ear variant. Those variant labels come from filenames and are not a verified '
        'inventory of all edits. Stock counterparts are family references, not proof of '
        'identical geometry. Rendered differences can include more than coat color.', '',
        '| Editable blank (copy before editing) | Blank six views | Original stock | Stock six views |',
        '| --- | --- | --- | --- |']
    for row in manifest['blanks']:
        key = row['key']
        lines.append(f"| [{row['name']}]( {link(Path(row['path']).relative_to('clean_dogs'))} ) | "
                     f"[Blank](reference/blank-{key}--views.png) | "
                     f"[{row['family']}]({link('../'+row['stock'])}) | "
                     f"[Stock](reference/stock-{row['stock_key']}--views.png) |".replace(']( ', '](').replace(' )', ')'))
    lines += ['', '## Choose by form', '',
        'Compare body length/height and leg proportions first, then head/muzzle, '
        'ear silhouette and tail. Use the stock coat to help locate overlapping '
        'parts when a white blank is hard to read; use the blank sheet to verify '
        'what is actually present in the editable file. Check sitting/lying '
        'before accepting an ear or attachment construction. A breed name alone '
        'does not establish which baseline best matches a new picture.', '',
        'For the edit workflow and evidence limits, see the '
        '[authoring guide](../agent-guides/picture-to-breed.md) and '
        '[feature map](../agent-guides/feature-to-control.md).', '',
        '## Reproduce and transfer', '',
        f"Generated by local stdio MCP from renderer checkout `{manifest['runtime']['checkout_revision']}`. "
        'Installed source hashes, dependency versions, capabilities, pose hashes, '
        'per-render arguments/metadata, input/output hashes and integrity results '
        'are in [the private manifest](reference/manifest.json). '
        'Inputs are read-only throughout rendering.', '',
        'Re-run from `/workspace` with the matching environment:', '',
        '```sh',
        'scratch/petz-local-venv/bin/python tools/render_clean_dogs.py',
        '```', '',
        'The script resumes only matching input/runtime checkpoints and verifies '
        'cached PNG hashes. It rebuilds sheets/index from those frames. '
        'To produce a fresh catalog with changed inputs or runtime, archive the '
        'existing `clean_dogs/reference/` folder first.', '',
        'Breed files and `reference/` are intentionally ignored by Git. '
        '**Transfer the entire `clean_dogs/` folder, including images, to the authoring '
        'agent** along with the documentation. Stock-file links require the matching '
        '`games/petz4/` folder; stock preview sheets remain usable without that folder. '
        'Private metadata can contain local paths. No proprietary assets or renders '
        'are included in documentation commits.', '']
    (BASE / 'README.md').write_text('\n'.join(lines))


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'raw').mkdir(exist_ok=True)
    blanks = make_inventory()
    installed = Path(petz_renderer.__file__).parent
    runtime = dict(backend='local stdio MCP', python=sys.version, platform=platform.platform(),
        checkout_revision=subprocess.check_output(['git','-C',str(ROOT/'petz-renderer-mcp'),'rev-parse','HEAD'],text=True).strip(),
        installed_sources={str(p.relative_to(installed)):sha(p) for p in sorted(installed.rglob('*.py'))},
        packages={n:importlib.metadata.version(n) for n in ('petz-renderer-mcp','Pillow','numpy','pefile','pydantic','fastmcp')},
        engines={str(p.relative_to(ROOT)):sha(p) for p in sorted((ROOT/'games/petz4/Resource').glob('*.dll'))})
    inputs = [dict(key='blank-'+r['key'], path=r['path'], sha256=r['sha256'], label='BLANK: '+r['name']) for r in blanks]
    for path in sorted({r['stock'] for r in blanks}):
        p=ROOT/path
        inputs.append(dict(key='stock-'+slug(p.stem),path=path,sha256=sha(p),label='STOCK: '+p.stem))
    fingerprint = hashlib.sha256(json.dumps(dict(runtime=runtime,inputs=inputs,controls=CONTROLS,views=VIEWS),sort_keys=True).encode()).hexdigest()
    target = OUT / 'manifest.json'
    if target.exists():
        manifest=json.loads(target.read_text())
        if manifest['fingerprint'] != fingerprint:
            raise ValueError('Inputs/runtime changed: archive reference/ before rebuilding')
    else:
        manifest=dict(fingerprint=fingerprint,runtime=runtime,controls=CONTROLS,views=VIEWS,
                      inputs=inputs,blanks=blanks,renders=[])
    # Ensure this environment really is the recorded checkout; no source edits.
    checkout = ROOT/'petz-renderer-mcp/src/petz_renderer'
    mismatches=[n for n,h in runtime['installed_sources'].items() if not (checkout/n).exists() or sha(checkout/n)!=h]
    if mismatches:
        raise ValueError(f'Installed/checkout source mismatch: {mismatches}')
    transport=StdioTransport(sys.executable,['-I','-m','petz_renderer.service.local_mcp',
        '--game-root',str(ROOT/'games/petz4'),'--asset-root',str(BASE)])
    async with Client(transport) as client:
        for name in ('get_capabilities','list_poses'):
            result=await client.call_tool(name)
            dump(OUT/(name+'.json'),result.data)
            manifest[name+'_sha256']=sha(OUT/(name+'.json'))
        for entry in inputs:
            toolpath=entry['path'].removeprefix('clean_dogs/') if entry['path'].startswith('clean_dogs/') else entry['path'].removeprefix('games/petz4/')
            inspected=await client.call_tool('inspect_input',dict(path=toolpath,seed=41))
            if inspected.is_error:
                raise RuntimeError(str(inspected))
            dump(OUT/(entry['key']+'--inspect.json'),inspected.data)
            for view,pose,yaw in VIEWS:
                previous=next((r for r in manifest['renders'] if r['key']==entry['key'] and r['view']==view),None)
                if previous:
                    if sha(OUT/previous['image']) != previous['png_sha256']:
                        raise ValueError('Cached render hash mismatch')
                    continue
                args=dict(path=toolpath,pose=pose,yaw_degrees=yaw,**CONTROLS)
                result=await client.call_tool('render_pet',args)
                if result.is_error:
                    raise RuntimeError(str(result))
                image=next(c for c in result.content if c.type=='image')
                png=base64.b64decode(image.data)
                name=f"raw/{entry['key']}--{view}.png"
                (OUT/name).write_bytes(png)
                im=Image.open(io.BytesIO(png)).convert('RGBA')
                bbox=im.getbbox()
                if bbox is None:
                    raise ValueError('Empty render')
                record=dict(key=entry['key'],view=view,arguments=args,image=name,png_sha256=sha(OUT/name),
                            size=list(im.size),alpha_bbox=list(bbox),metadata=result.data)
                manifest['renders'].append(record)
                dump(target,manifest)
            print(f"{entry['key']}: six views complete ({len(manifest['renders'])})",flush=True)
    unchanged={entry['path']:sha(ROOT/entry['path'])==entry['sha256'] for entry in inputs}
    engine_unchanged={p:sha(ROOT/p)==h for p,h in runtime['engines'].items()}
    manifest['integrity']=dict(inputs_unchanged=unchanged,engines_unchanged=engine_unchanged,
        installed_matches_checkout=True,renderer_source_count=len(runtime['installed_sources']))
    if not all(unchanged.values()) or not all(engine_unchanged.values()):
        raise ValueError('Source integrity check failed')
    build_sheets(manifest)
    manifest['script_sha256']=sha(Path(__file__))
    dump(target,manifest)
    write_readme(manifest)
    print(f"Done: {len(inputs)} inputs, {len(manifest['renders'])} renders; inputs unchanged",flush=True)


if __name__=='__main__':
    asyncio.run(main())
