"""Check local documentation targets, JSON syntax, hashes and private-file exclusion."""
import json,re,subprocess
from pathlib import Path
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1]
errors=[]
folders=('docs','sources','format-reference','visual-editing','experiments','agent-guides','troubleshooting','clean_dogs','texture-index')
pages=list(ROOT.glob('*.md'))+[p for name in folders for p in (ROOT/name).rglob('*.md')]
for page in pages:
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',page.read_text()):
        if '://' in target or target.startswith(('#','mailto:')):continue
        path=unquote(target.split('#')[0])
        if not (page.parent/path).exists():errors.append(f'{page.relative_to(ROOT)}: missing {target}')
def hashes(obj,where):
    if isinstance(obj,dict):
        for key,value in obj.items():
            if key.endswith('sha256') and value is not None and not re.fullmatch('[0-9a-f]{64}',str(value)):
                errors.append(f'{where}: invalid {key}')
            hashes(value,where)
    elif isinstance(obj,list):
        for value in obj:hashes(value,where)
for path in (ROOT/'experiments').glob('*.json'):
    try: hashes(json.loads(path.read_text()),path.name)
    except ValueError as exc:errors.append(f'{path.name}: {exc}')
tracked=subprocess.check_output(['git','-c',f'safe.directory={ROOT}','ls-files','-z'],cwd=ROOT).decode().split('\0')
for path in tracked:
    if path.startswith('texture-index/') and Path(path).suffix.lower() == '.import':
        errors.append(f'texture editor sidecar tracked: {path}')
    shared_blank = Path(path).parent == Path('clean_dogs/petz4') and Path(path).suffix.lower() == '.dog'
    if path.startswith(('games/','scratch/','petz-renderer-mcp/')) or (Path(path).suffix.lower() in ('.dog','.cat','.pet','.dll','.exe','.lnz') and not shared_blank):
        errors.append(f'private asset tracked: {path}')
if errors:raise SystemExit('\n'.join(errors))
print(f'Checked {len(pages)} Markdown pages, experiment JSON/hash syntax and tracked private-file exclusion.')
