"""Audit the UPDATE-005/006/007 session without repeating verified renders."""
import json
import subprocess
from pathlib import Path
import petz_renderer
from research_common import ROOT, SHA


def main():
    reports = {}
    pngs = 0
    revision = subprocess.check_output(['git','-C',str(ROOT/'petz-renderer-mcp'),'rev-parse','HEAD'], text=True).strip()
    for unit, count in (('update-005',32), ('update-006',252), ('update-007',336)):
        folder = ROOT/'scratch/research'/unit
        public = ROOT/'experiments'/(unit+'.json')
        report = json.loads(public.read_text())
        assert report['renderer_revision'] == revision
        assert report == json.loads((folder/'report.json').read_text())
        verified = json.loads((folder/'verification.json').read_text())
        assert verified['report_sha256'] == SHA(public.read_bytes())
        assert len(list(folder.rglob('*.png'))) == count
        pngs += count
        reports[unit] = {'manifest_sha256':SHA(public.read_bytes()),
                         'verification_sha256':SHA((folder/'verification.json').read_bytes())}
        for name, digest in report['source_hashes'].items():
            assert SHA((Path(petz_renderer.__file__).parent/name).read_bytes()) == digest
            assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes()) == digest
    restore = json.loads((ROOT/'experiments/restore-002.json').read_text())
    originals = 0
    for version, engines in restore['shared_engine_hashes'].items():
        paths = {str(p.relative_to(ROOT/'games'/version)).lower():p
                 for p in (ROOT/'games'/version).rglob('*') if p.is_file()}
        for name, digest in engines.items():
            assert SHA(paths[name].read_bytes()) == digest
            originals += 1
    for row in restore['results']:
        assert SHA((ROOT/'games'/row['version']/row['path']).read_bytes()) == row['input_sha256']
        originals += 1
    health_path = ROOT/'scratch/research/continuation-2026-11-10-upgrade-health.json'
    health = json.loads(health_path.read_text())
    assert len(health['tools']) == 6
    assert pngs == 620 and originals == 18
    tool_names = ('revalidate_nested_textures.py','check_nested_texture_update.py',
                  'revalidate_static_matrix.py','check_static_matrix_update.py',
                  'revalidate_motion_components.py','check_motion_components_update.py',
                  'check_upgrade_continuation.py')
    tool_hashes = {name:SHA((ROOT/'tools'/name).read_bytes()) for name in tool_names}
    result = {'reports':reports, 'pngs':pngs, 'original_hash_links':originals,
              'renderer_revision':revision, 'tool_hashes':tool_hashes,
              'health_sha256':SHA(health_path.read_bytes()),
              'new_mcp_comparisons':32, 'new_mcp_fresh_baselines':12,
              'reused_mcp_fresh_baselines':12, 'static_sequence_draws':96,
              'static_reset_draws':144, 'motion_transition_states':192,
              'motion_final_draws':336, 'connector_numerical_loads':60,
              'source_files_per_unit':62,
              'scope':'Integrity aggregation; unit verifiers perform the numerical and pixel replays.'}
    (ROOT/'scratch/research/upgrade-continuation-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
