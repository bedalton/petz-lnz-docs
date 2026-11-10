"""LINE-020: all-byte connector texture shade/sign and edge controls."""
import importlib.metadata
import json
import sys
from dataclasses import replace
from pathlib import Path
import petz_renderer
from petz_renderer.rendering.framebuffer import Framebuffer
from petz_renderer.rendering.lines import LineBlock, LineRenderer
from petz_renderer.rendering.texture import TiledTexture, TexturePaint
from research_common import ROOT, SHA
OUT = ROOT/'scratch/research/line-020'


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    records, private = [], []
    for axis in ('horizontal','vertical'):
        points = (10,12,265,12) if axis=='horizontal' else (12,10,12,265)
        tw,th = (256,3) if axis=='horizontal' else (3,256)
        pixels = bytes(x if axis=='horizontal' else y for y in range(th) for x in range(tw))
        texture = TiledTexture(tw,th,pixels,0,0)
        left,top = (10,11) if axis=='horizontal' else (11,10)
        for shade in (-128,-1,0,1,127):
            for sign in (False,True):
                for edge in (-1,0,1):
                    block = LineBlock(*points,start_thick=3,end_thick=3,color=125,
                                      left_color=180,right_color=200,fuzz=0,edge_mode=edge,
                                      paint=TexturePaint(texture,shade,sign))
                    fb,plain = Framebuffer(280,280,background=254),Framebuffer(280,280,background=254)
                    renderer = LineRenderer(seed=1)
                    renderer.draw(fb,block)
                    LineRenderer(seed=1).draw(plain,replace(block,paint=None))
                    expected = bytearray(plain.pixels)
                    samples,edges,zeros,specials = [],0,0,{}
                    for i,value in enumerate(plain.pixels):
                        if value==254:continue
                        x,y = i%280,i//280
                        if value==125:
                            sample = pixels[(y-top)*tw+x-left]
                            result = sample if sign and sample>=10 else (sample+shade)%256
                            expected[i]=result
                            samples.append([x,y,sample,result])
                            zeros += result==0
                            if sample in (0,8,9,10,127,128,149,150,254,255):specials[str(sample)]=result
                        else:
                            assert value in (180,200)
                            edges+=1
                    assert fb.pixels==bytes(expected)
                    assert renderer._state==1 and not any(renderer._tables)
                    record={'axis':axis,'shade_offset':shade,'has_sign':sign,'edge_mode':edge,
                            'texture_size':[tw,th],'sample_assertions':len(samples),
                            'explicit_edge_assertions':edges,'zero_output_samples':zeros,
                            'boundary_samples':specials,'indexed_sha256':SHA(fb.pixels),
                            'plain_indexed_sha256':SHA(plain.pixels)}
                    records.append(record)
                    private.append({'record':record,'pixels':list(fb.pixels),'samples':samples})
    installed=Path(petz_renderer.__file__).parent
    sources={n:SHA((installed/n).read_bytes()) for n in
             ('rendering/lines.py','rendering/texture.py','rendering/framebuffer.py')}
    for name,digest in sources.items():
        assert SHA((ROOT/'petz-renderer-mcp/src/petz_renderer'/name).read_bytes())==digest
    payload=json.dumps(private,separators=(',',':')).encode()
    (OUT/'pixels.json').write_bytes(payload)
    report={'experiment':'LINE-020','backend':'asset-free direct indexed raster; no MCP',
            'renderer_revision':'9d72d7afd5f7460ef18133c6179caaf8055082d9',
            'python':sys.version,'dependencies':{'petz-renderer-mcp':importlib.metadata.version('petz-renderer-mcp')},
            'source_hashes':sources,'private_pixels_sha256':SHA(payload),
            'controls':{'canvas':[280,280],'background':254,'texture_values':'0..255 along long axis',
                        'seed':1,'widths':[3,3],'fuzz':0,'fill':125,'explicit_edges':[180,200]},
            'records':records,
            'summary':{'fixtures':len(records),'sample_assertions':sum(r['sample_assertions'] for r in records),
                       'explicit_edge_assertions':sum(r['explicit_edge_assertions'] for r in records),
                       'zero_output_samples':sum(r['zero_output_samples'] for r in records)}}
    for target in (OUT/'report.json',ROOT/'experiments/line-020.json'):
        target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['summary']))


if __name__=='__main__':
    main()
