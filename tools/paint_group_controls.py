"""PAINT-004: asset-free paint group preparation controls; --verify replays."""
from dataclasses import asdict, replace
import importlib.metadata
import itertools
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
import petz_renderer
from petz_renderer.appearance.core import PaintBall, Texture
from petz_renderer.appearance.preview import section_diagnostics
from petz_renderer.rendering.paint import prepare_paint_blocks
from petz_renderer.rendering.raster import PixelRect
from petz_renderer.rendering.shading import shade_color
from petz_renderer.rendering.texture import TiledTexture
from research_common import ROOT, SHA

PATH=ROOT/'experiments/paint-004.json'

def evaluate():
    cases=[]
    animation=SimpleNamespace(rot_byte7=0,rot_byte8=0,rot_byte6=0)
    texture=TiledTexture(16,16,bytes(range(256)),16,16)
    for color,offset,textured in itertools.product((9,10,35,125,149,150),(-6,0,6),(False,True)):
        baseline=None
        for group in (0,-1,1,2,15,255):
            paint=PaintBall(0,50,(0.,0.,-1.),color,-1,0,0,group,0 if textured else -1,True)
            blocks=prepare_paint_blocks((paint,),0,PixelRect(0,0,41,41),animation,
                shade_offset=offset,textures=(texture,),entries=(Texture('synthetic',True,-1,16,16),))
            assert len(blocks)==1
            block=blocks[0]
            assert block.fill==shade_color(color,offset)&255
            assert (block.paint is not None)==(textured and 10<=block.fill<=149)
            if baseline is None:baseline=block
            assert block==baseline
            appearance=SimpleNamespace(paint_balls=(paint,),balls=(),add_balls=())
            diagnostic=section_diagnostics({'Paint Ballz':()},appearance,layer='synthetic')
            assert bool(diagnostic)==(group!=0)
            positive=prepare_paint_blocks((replace(paint,color=65),),0,PixelRect(0,0,41,41),animation,
                shade_offset=offset,textures=(texture,),entries=(Texture('synthetic',True,-1,16,16),))[0]
            assert positive.fill!=block.fill
            cases.append({'color':color,'shade_offset':offset,'textured':textured,'group':group,
                'fill':block.fill,'texture_prepared':block.paint is not None,
                'command_sha256':SHA(repr(block).encode()),
                'diagnostics':[asdict(d) for d in diagnostic]})
    package=Path(petz_renderer.__file__).parent
    sources={str(p.relative_to(package)):SHA(p.read_bytes()) for p in sorted(package.rglob('*.py'))}
    for name,digest in sources.items():assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes())==digest
    return {'experiment':'PAINT-004','backend':'installed local Python preparation API; synthetic assets; no MCP or raster calls',
        'renderer_revision':subprocess.check_output(['git','-C',str(ROOT/'petz-renderer-mcp'),'rev-parse','HEAD'],text=True).strip(),
        'package_version':importlib.metadata.version('petz-renderer-mcp'),'source_hashes':sources,
        'controls':{'host_bounds':[0,0,41,41],'direction':[0,0,-1],'diameter_percent':50,'rotations':[0,0,0],
            'texture_dimensions':[16,16],'texture_sha256':SHA(texture.pixels),'texture_has_levels':True,'texture_own_level':-1},
        'summary':{'commands':len(cases),'group_comparisons':len(cases)//6*5,
            'nonzero_group_diagnostics':sum(bool(c['diagnostics']) for c in cases),'color_positive_controls':len(cases)},'cases':cases}

def main():
    report=evaluate()
    if '--verify' in sys.argv:assert report==json.loads(PATH.read_text())
    else:
        if PATH.exists():raise FileExistsError(PATH)
        PATH.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['summary']))

if __name__=='__main__':main()
