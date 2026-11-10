"""UPDATE-003: read-only old/new stills for available change-notice sample pets."""
import json,sys
from dataclasses import asdict
from pathlib import Path
from hashlib import sha256
from petz_renderer.formats.resolver import ResourceResolver
from petz_renderer.local import load_saved_assets
from petz_renderer.rendering.preparation import prepare_frame
from petz_renderer.rendering.output import render_portrait
ROOT=Path('/workspace');H=lambda b:sha256(b).hexdigest()
def main():
    out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False);resolver=ResourceResolver((ROOT/'games/petz4',));rows=[]
    for name in ('Fuzzkin','Goobe','Homebody'):
        path=f'Adopted Petz/{name}.pet';source=ROOT/'games/petz4'/path;original=H(source.read_bytes())
        for pose in ('standing','sitting','lying'):
            a=load_saved_assets(resolver,path,pose=pose)
            for degrees,yaw in ((0,0),(90,64)):
                prepared=prepare_frame(a.appearance,a.sizes,a.frame,textures=a.textures,fatness=a.preview.fatness,yaw=yaw)
                portrait=render_portrait(a,yaw=yaw);stem=f'{name}-{pose}-{degrees}';(out/(stem+'.png')).write_bytes(portrait.png)
                row={'name':name,'path':path,'pose':pose,'yaw_degrees':degrees,'stem':stem,'input_sha256':original,'png_sha256':H(portrait.png),'indexed_sha256':H(portrait.indices),'size':[portrait.width,portrait.height],'preview':asdict(a.preview),'geometry':[asdict(b) for b in prepared.geometry.balls],'textured_paints':sum(p.paint is not None for b in prepared.balls for p in b.paints),'paint_count':sum(len(b.paints) for b in prepared.balls),'provenance':[asdict(use) for use in a.provenance]}
                rows.append(row)
        assert H(source.read_bytes())==original
    (out/'report.json').write_text(json.dumps(rows,indent=2)+'\n');print(len(rows),'saved-pet stills',out,flush=True)
if __name__=='__main__':main()
