"""Audit copied engine/baseline/save hashes without changing game files."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    old = json.loads((ROOT / 'experiments/restore-002.json').read_text())
    expected = {}
    for version, entries in old['shared_engine_hashes'].items():
        for path, digest in entries.items():
            expected[f'{version}/{path}'.lower()] = digest
    for row in old['results']:
        expected[f"{row['version']}/{row['path']}".lower()] = row['input_sha256']
    for row in json.loads((ROOT / 'experiments/update-003.json').read_text())['cases']:
        expected[f"petz4/{row['controls']['path']}".lower()] = row['input_sha256']
    files = {}
    for path in (ROOT / 'games').rglob('*'):
        if path.is_file():
            key = path.relative_to(ROOT / 'games').as_posix().lower()
            assert key not in files, f'Ambiguous path: {key}'
            files[key] = path
    rows = []
    for key, digest in sorted(expected.items()):
        path = files.get(key)
        actual = hashlib.sha256(path.read_bytes()).hexdigest() if path else None
        rows.append(dict(path=key, expected_sha256=digest, actual_sha256=actual, ok=actual == digest))
    report = {'scope': 'Recorded engines, six stock breeds and three Petz4 saves; not a complete installation manifest or game validation', 'files_per_version': {v: sum(k.startswith(v + '/') for k in files) for v in old['shared_engine_hashes']}, 'checks': rows}
    print(json.dumps(report, indent=2))
    assert all(r['ok'] for r in rows), 'Game file mismatch; see report'

if __name__ == '__main__':
    main()
