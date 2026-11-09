"""Extract factual ball labels/hashes, never stock LNZ rows, for atlas scaffolding."""
import hashlib,json,re
from pathlib import Path
from petz_renderer.formats.pe import ResourceFile
from petz_renderer.appearance.lnz import parse_sections
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'scratch/research/anatomy-001'

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    report=[]
    for version in (3,4,5):
        for species,filename,master in [('Dogz','Dalmatian.dog','DOGMASTER'),('Catz','Siamese.cat','CATMASTER')]:
            root=ROOT/f'games/petz{version}'
            path=root/'Resource'/species/filename
            raw=path.read_bytes(); pe=ResourceFile(raw)
            leaves=[r for r in pe.resources if r.type=='LNZ' and not str(r.name).endswith(('PUP','KIT'))]
            assert len(leaves)==1
            leaf=leaves[0]; payload=pe.read(leaf.type,leaf.name,leaf.language)
            sections=parse_sections(payload,0)
            assert len(sections['Ballz Info'])==67
            labels=[]
            if species=='Catz':
                for row in sections['Ballz Info']:
                    match=re.search(r'eBall_([A-Za-z0-9_]+)',row)
                    assert match
                    labels.append(match[1])
            else:
                text=payload.decode('cp1252')
                body=re.search(r'\[Ballz Info\]([^\[]*)',text)[1]
                for line in body.splitlines():
                    if re.match(r'\s*[+-]?\d',line):
                        assert ';' in line
                        labels.append(line.split(';',1)[1].strip())
            assert len(labels)==67
            rezpath=root/f'Resource/{species} {version} Rez.dll'
            rezraw=rezpath.read_bytes(); rez=ResourceFile(rezraw)
            masterbytes=rez.read('LNZ',master); ms=parse_sections(masterbytes)
            row={'game_version':f'petz{version}','species':species,'breed':filename,'resource':leaf.name,'input_sha256':hashlib.sha256(raw).hexdigest(),'lnz_sha256':hashlib.sha256(payload).hexdigest(),'master_file_sha256':hashlib.sha256(rezraw).hexdigest(),'master_lnz_sha256':hashlib.sha256(masterbytes).hexdigest(),'labels':labels,'keys':[int(re.match(r'[+-]?\d+',v)[0]) for v in ms['Key Balls']],'eyes':[[int(x) for x in re.match(r'\s*(\d+),\s*(\d+)',v).groups()] for v in ms['Eyes']],'breed_sections':{k:len(v) for k,v in sections.items()},'master_sections':{k:len(v) for k,v in ms.items()}}
            report.append(row)
    for species in ('Dogz','Catz'):
        rows=[r for r in report if r['species']==species]
        assert all(r['labels']==rows[0]['labels'] and r['keys']==rows[0]['keys'] and r['eyes']==rows[0]['eyes'] for r in rows)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    public=ROOT/'experiments/anatomy-001.json'
    public.write_text(json.dumps(report,indent=2)+'\n')
    for species in ('Dogz','Catz'):
        row=next(r for r in report if r['species']==species)
        lines=[f'# {species} base-ball label index','', 'Status: asset-reported labels; visual identification remains pending except for the initial head probes.','', 'The sampled stock labels and master key/eye IDs agree in Petz 3, 4 and 5. This is not a complete cross-breed or visual validation. L/R below preserves the asset label; anatomical-side conventions still need visual confirmation.','', '[Evidence and procedure](../../experiments/anatomy-001.md). Added balls begin after this index and need breed-specific mappings.','', '| ID | Asset label | Visual test |','| --- | --- | --- |']
        lines += [f'| {i} | {label} | {"BALL-001 (Petz 4 only)" if i==row["keys"][0] else "Pending"} |' for i,label in enumerate(row['labels'])]
        (ROOT/f'format-reference/anatomy/{species.lower()}.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':main()
