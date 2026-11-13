#!/usr/bin/env python3
"""Export image-generator artwork and paired raster lettering sheets, without SVG.

Pillow/numpy inspect alpha and dimensions only. ImageMagick performs format,
crop and resize operations; CUnet performs illustration super-resolution.
The manifest records the image generator's source paths and manuscript copy.
"""
import argparse,json,os,subprocess,sys,time
from pathlib import Path
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from CUnet.upscale import upscale_image

def run(*args):
    subprocess.run([str(x) for x in args],check=True,stdout=subprocess.DEVNULL)

def crop_sheet(source,root,layer):
    pic=Image.open(source).convert('RGBA');a=np.asarray(pic.getchannel('A'));h,w=a.shape
    has_right=bool(layer.get('fact'))
    spans=[(0,w,'02-标题与正文-透明底.png',2400)]
    if has_right:
        # Ignore isolated antialiasing specks, but reject a sheet without a gutter.
        empty=(a>16).sum(axis=0)<=max(2,int(h*.003))
        runs=[];start=None
        for x in range(int(w*.40),int(w*.78)):
            if empty[x] and start is None:start=x
            if not empty[x] and start is not None:runs.append((start,x));start=None
        if start is not None:runs.append((start,int(w*.78)))
        assert runs,'No transparent crop gutter'
        lo,hi=max(runs,key=lambda t:t[1]-t[0]);assert hi-lo>w*.015,(lo,hi,w)
        split=(lo+hi)//2
        name={'worksheet':'03-观察记录-透明底.png','extension':'03-亲子延伸-透明底.png','recall':'03-回想提示-透明底.png'}.get(layer.get('role'),'03-雨林小百科-透明底.png')
        spans=[(0,split,'02-标题与正文-透明底.png',2400),(split,w,name,2000)]
    run('magick',source,'-units','PixelsPerInch','-density','300','-define','png:color-type=6',root/'00-标题与百科合画-透明底.png')
    metadata=[]
    for left,right,name,width in spans:
        ys,xs=np.where(a[:,left:right]>16);assert len(xs)>0
        pad=max(24,int(w*.025));x1=max(left,left+int(xs.min())-pad);x2=min(right,left+int(xs.max())+pad+1)
        y1=max(0,int(ys.min())-pad);y2=min(h,int(ys.max())+pad+1)
        geom=f'{x2-x1}x{y2-y1}+{x1}+{y1}'
        run('magick',source,'-crop',geom,'+repage','-resize',f'{width}x','-units','PixelsPerInch','-density','300','-define','png:color-type=6',root/name)
        metadata.append({'name':name,'source_crop':geom})
    return metadata

def scene(source,destination,cpu,model):
    im=Image.open(source);assert im.size==(1254,1254),f'Expected native 1254px source, got {im.size}'
    metadata=upscale_image(source,destination,cpu,model,overwrite=True)
    archived=destination.parent/'插画原图-1254px.png'
    run('magick',source,'-units','PixelsPerInch','-density','300','-define','png:color-type=2',archived)
    assert Image.open(archived).tobytes()==im.convert('RGB').tobytes()
    return {**metadata,'archived_source':archived.name}

def process(args):
    pages={p['page']:p for p in json.loads(args.pages.read_text())}
    donefile=args.results.parent/'exported.jsonl'
    done={}
    if donefile.exists():
        for line in donefile.read_text().splitlines():
            item=json.loads(line);done[item['id']]=item
    failed={}
    while True:
        records=[]
        if args.results.exists():
            for line in args.results.read_text().splitlines():
                try:records.append(json.loads(line))
                except json.JSONDecodeError:pass
        for r in records:
            if r['id'] in done or r['id'] in failed:continue
            p=pages[r['page']];root=args.output/p['stem'];root.mkdir(parents=True,exist_ok=True)
            try:
                source=Path(r['path'])
                with Image.open(source) as im:im.verify()
                if r['kind']=='scene':meta=scene(source,root/'01-原图-2508px.png',args.cpu,args.model)
                else:meta=crop_sheet(source,root,p['layer'])
                entry={**r,'export':meta};done[r['id']]=entry
                with donefile.open('a') as f:f.write(json.dumps(entry,ensure_ascii=False)+'\n')
                print('EXPORTED',r['id'],flush=True)
            except Exception as e:
                failed[r['id']]=str(e);print('NEEDS_REVIEW',r['id'],repr(e),flush=True)
                (args.results.parent/'export-errors.json').write_text(json.dumps(failed,ensure_ascii=False,indent=2))
        if not args.watch or len(done)+len(failed)>=args.expected:break
        time.sleep(5)

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--pages',type=Path,required=True)
    ap.add_argument('--results',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--cpu',type=Path,required=True)
    ap.add_argument('--model',type=Path,required=True)
    ap.add_argument('--watch',action='store_true');ap.add_argument('--expected',type=int,default=76)
    process(ap.parse_args())
