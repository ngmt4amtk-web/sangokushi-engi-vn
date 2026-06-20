#!/usr/bin/env python3
# raw/*.png(緑#00B140) → sprites/<key>_base.png(透過)。chroma_key.py(純PIL)流用。
import os, glob, sys
from PIL import Image, ImageChops
RAW=os.path.expanduser('~/sangokushi-engi-vn/assets/raw')
DST=os.path.expanduser('~/sangokushi-engi-vn/assets/sprites')
os.makedirs(DST,exist_ok=True)
LOW,HIGH=20,90; OUT_H=1200; BBOX_ALPHA=12
LUT=[255 if i<=LOW else (0 if i>=HIGH else int(round(255*(HIGH-i)/(HIGH-LOW)))) for i in range(256)]
def key_one(path):
    im=Image.open(path).convert('RGB'); R,G,B=im.split()
    maxRB=ImageChops.lighter(R,B); greenness=ImageChops.subtract(G,maxRB)
    alpha=greenness.point(LUT); newG=ImageChops.darker(G,maxRB)
    out=Image.merge('RGBA',(R,newG,B,alpha))
    mask=alpha.point(lambda a:255 if a>BBOX_ALPHA else 0); bb=mask.getbbox()
    if bb: out=out.crop(bb)
    w,h=out.size
    if h>OUT_H: out=out.resize((max(1,round(w*OUT_H/h)),OUT_H),Image.LANCZOS)
    return out
ok=0; skip=0
for p in sorted(glob.glob(f'{RAW}/*.png')):
    base=os.path.splitext(os.path.basename(p))[0]
    key=base if base.startswith('mob_') else base+'_base'
    try:
        out=key_one(p); out.save(f'{DST}/{key}.png'); ok+=1
    except Exception as e:
        print('  skip',base,e); skip+=1
print(f'切り抜き完了：{ok}体 → assets/sprites/  (skip {skip})')
