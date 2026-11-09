"""Shared safeguards for private, seed-resolved experimental resource copies."""
import base64, hashlib, json
from pathlib import Path
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.appearance.lnz import parse_sections

ROOT=Path(__file__).resolve().parents[1]
SHA=lambda b: hashlib.sha256(b).hexdigest()

def adult(species, version="petz4", *, filename=None, selector=None):
    default_file,default_selector,master=('Scottie.dog','SC','DOGMASTER') if species=='Dogz' else ('Siamese.cat','SI','CATMASTER')
    filename = default_file if filename is None else filename
    selector = default_selector if selector is None else selector
    source=ROOT/'games'/version/'Resource'/species/filename
    raw=source.read_bytes(); pe=ResourceFile(raw)
    leaf=next(r for r in pe.resources if r.type=='LNZ' and r.name==selector)
    sections=dict(parse_sections(pe.read('LNZ',selector),0))
    masterfile=ResourceFile((ROOT/f'games/{version}/Resource/{species} {version[-1]} Rez.dll').read_bytes())
    return source,raw,leaf,sections,masterfile,master

def write_copy(raw,leaf,sections,target):
    payload=('\n'.join('['+k+']\n'+'\n'.join(v) for k,v in sections.items())+'\n').encode('cp1252')
    if len(payload)>leaf.size: raise ValueError('replacement exceeds original resource span')
    edited=raw[:leaf.offset]+payload.ljust(leaf.size,b' ')+raw[leaf.offset+leaf.size:]
    before,after=ResourceFile(raw),ResourceFile(edited)
    assert before.resources==after.resources
    for r in before.resources:
        if r!=leaf: assert before.read(r.type,r.name,r.language)==after.read(r.type,r.name,r.language)
    assert raw[:leaf.offset]==edited[:leaf.offset] and raw[leaf.offset+leaf.size:]==edited[leaf.offset+leaf.size:]
    target.write_bytes(edited)
    return SHA(edited)

async def save_result(client,op,args,folder,stem):
    result=await client.call_tool(op,args)
    if result.is_error: raise RuntimeError(str(result.data))
    png=base64.b64decode(next(c.data for c in result.content if c.type=='image'))
    (folder/f'{stem}.png').write_bytes(png)
    (folder/f'{stem}-render.json').write_text(json.dumps(result.data,indent=2)+'\n')
    return png,result.data
