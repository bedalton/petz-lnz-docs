"""Asset-free differential controls for the six paths in RENDERER_CHANGES.md.
Run with a source root inserted before imports to compare historical/current code.
"""
import inspect,json,sys
from dataclasses import replace
from hashlib import sha256
from petz_renderer.appearance.core import read_core,PaintBall,Texture,AddBall,Projection
from petz_renderer.formats.animation import BallFrame,BallPosition
from petz_renderer.rendering.attachment import default_geometry
from petz_renderer.rendering.blocks import CircleBlock,draw_circle_block
from petz_renderer.rendering.raster import PixelRect
from petz_renderer.rendering.framebuffer import Framebuffer
from petz_renderer.rendering.paint import prepare_paint_blocks
from petz_renderer.rendering.texture import TiledTexture,remap_texture
H=lambda b:sha256(b).hexdigest()

def main():
    art=TiledTexture(64,64,bytes(10+(x+3*y)%10 for y in range(64) for x in range(64)),0,0)
    texture=Texture('synthetic',True,-1,64,64);paint=remap_texture(art,125,has_levels=True,own_level=-1)
    # Same authored rows; old parser leaves paint texture3, new v1 follows ball3 after override.
    parser=[]
    for version in (None,1,2):
        data={'Ballz Info':('125 244 -1 0 -1 20 0 5',)*4,'Color Info Override':('3 125 0 7',),'Paint Ballz':('0 50 0 0 -1 125 244 0 -1 0 3 0',)}
        if version is not None:data['Lnz Version']=(str(version),)
        a=read_core(data);parser.append({'version':version,'ball3_texture':a.balls[3].texture,'paint_texture':a.paint_balls[0].texture})
    outlines=[]
    for style in (-1,0,1,2,4,25):
        for textured in (False,True):
            fb=Framebuffer(64,64,background=253)
            block=CircleBlock(PixelRect(16,16,39,39),125,244,style,0,paint=paint if textured else None)
            draw_circle_block(fb,block,seed=1)
            outlines.append({'style':style,'textured':textured,'sha256':H(fb.pixels),'clip_thickness':block.clip.outline_thickness,'body_pixels':sum(10<=v<=149 for v in fb.pixels),'outline_pixels':fb.pixels.count(244)})
    paints=[];supports='textures' in inspect.signature(prepare_paint_blocks).parameters
    for color in (0,9,10,125,149,150,244):
        for outline in (-1,1,4):
            pb=PaintBall(0,65,(0,0,-1),244 if color==0 else color,244,0,outline,0,0,False)
            kw={'textures':(art,),'entries':(texture,),'paint_angles':[(0,0)],'frame_angles':(3,-2)} if supports else {}
            blocks=prepare_paint_blocks((pb,),0,PixelRect(8,8,47,47),BallPosition(0,0,0,0,0,0),**kw)
            assert len(blocks)==1;fb=Framebuffer(64,64,background=253);draw_circle_block(fb,blocks[0],clip_against=CircleBlock(PixelRect(8,8,47,47),125,outline_type=-1).clip)
            p=blocks[0].paint
            paints.append({'authored_color':color,'outline':outline,'textured':p is not None,'angles':blocks[0].angles,'remapped_sha256':H(p.texture.pixels) if p else None,'sha256':H(fb.pixels)})
    clipping=[]
    child=CircleBlock(PixelRect(0,0,40,40),180)
    for style in (-4,-3,-2,-1,0,1,2,4):
        host=CircleBlock(PixelRect(12,12,35,35),125,244,style,0);fb=Framebuffer(64,64,background=253)
        draw_circle_block(fb,child,clip_against=host.clip)
        clipping.append({'host_style':style,'inset':host.clip.outline_thickness,'sha256':H(fb.pixels),'pixels':fb.pixels.count(180)})
    # Exactly67 real slots; add ids67/68. No unplaced-anchor/sentinel in these controls.
    balls=(BallPosition(10,-3,20,0,0,0),)*67;frame=BallFrame((0,)*6,0,balls,())
    add=AddBall(0,30,10,-20,125,244,-1,0,-1,0,20,8,0)
    core=replace(read_core({}),pet_scale=256,ball_scale=256,add_balls=(add,replace(add,x=-20,y=-10,z=30)))
    projections=[]
    for start,end in ((0,67),(67,0),(67,68)):
        for percent in (0,50,100,150):
            a=replace(core,projections=(Projection(start,end,percent),));g=default_geometry(a,(20,)*67,frame)
            before=default_geometry(core,(20,)*67,frame)
            source=(before[start].x,before[start].y,before[start].z);target=(before[end].x,before[end].y,before[end].z)
            expected=tuple(u+(1 if v-u>=0 else -1)*(abs((v-u)*percent)//100) for u,v in zip(source,target))
            actual=(g[end].x,g[end].y,g[end].z)
            projections.append({'start':start,'end':end,'percent':percent,'before':target,'expected':expected,'actual':actual,'matches_expected':actual==expected})
    result={'parser':parser,'outlines':outlines,'paint_texture_api':supports,'paints':paints,'clipping':clipping,'projections':projections}
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
