"""Audit old/new asset-free controls without promoting native-port claims to game evidence."""
import json,subprocess,sys
from pathlib import Path
from research_common import ROOT,SHA
OUT=ROOT/'scratch/research/update-001'
old=json.loads((OUT/'old-controls.json').read_text());new=json.loads((OUT/'new-controls.json').read_text())
for name,source in (('old',OUT/'old-source/src'),('new',None)):
    command=[sys.executable,'-I','-c',f'import sys,runpy; '+(f'sys.path.insert(0,{str(source)!r}); ' if source else '')+f'runpy.run_path({str(ROOT/"tools/renderer_change_controls.py")!r},run_name="__main__")']
    assert json.loads(subprocess.check_output(command))==({'old':old,'new':new}[name])
assert [r['paint_texture'] for r in old['parser']]==[3,3,3]
assert [r['paint_texture'] for r in new['parser']]==[7,7,3]
assert all(r['matches_expected'] for r in new['projections'])
assert sum(r['matches_expected'] for r in old['projections'])==3
assert sum(r['textured'] for r in old['paints'])==0
assert sum(r['textured'] for r in new['paints'])==9
for color in (10,125,149):
    samples=[r for r in new['paints'] if r['authored_color']==color]
    assert len({r['sha256'] for r in samples})==1
    assert all(r['textured'] and r['angles']==[3,-2] for r in samples)
assert len({r['remapped_sha256'] for r in new['paints'] if r['outline']==-1 and r['textured']})==3
for oldrow,newrow in zip(old['outlines'],new['outlines'],strict=True):
    changed=oldrow['sha256']!=newrow['sha256']
    assert changed==(newrow['textured'] and newrow['style'] in (1,2,4))
for oldrow,newrow in zip(old['clipping'],new['clipping'],strict=True):
    assert newrow['inset']==(newrow['host_style']-1 if newrow['host_style']>=1 else 0)
    assert (oldrow['sha256']!=newrow['sha256'])==(newrow['host_style']<1)
source=OUT/'old-source/src/petz_renderer';before=json.loads((OUT/'before.json').read_text())
for name,h in before['old_installed_sources'].items():assert SHA((source/name).read_bytes())==h
summary={'old_controls_sha256':SHA((OUT/'old-controls.json').read_bytes()),'new_controls_sha256':SHA((OUT/'new-controls.json').read_bytes()),'change_notice_sha256':SHA((ROOT/'RENDERER_CHANGES.md').read_bytes()),'renderer_revision':before['checkout_revision'],'counts':{'parser':3,'outline_rasters_per_revision':12,'paint_rasters_per_revision':21,'clip_rasters_per_revision':8,'project_cases_per_revision':12},'classifications':{'blanket_textured_paint_incomplete':'withdrawn for updated renderer; renderer-only support confirmed','blanket_textured_outline_incomplete':'withdrawn for updated renderer; renderer-only support confirmed','non_outline_clip_inset_one':'corrected to zero','paint_legacy_texture_is_direct_slot':'corrected below Lnz Version 2','add_ball_projection_no_effect':'withdrawn except percent100 identity control','group_colour_retint':'three synthetic resolved colours remap distinctly; saved-group integration not exercised'},'test_log_sha256':SHA((OUT/'pytest.log').read_bytes())}
assert '68 passed' in (OUT/'pytest.log').read_text()
for path in (OUT/'controls-verification.json',ROOT/'experiments/update-001-controls.json'):path.write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
