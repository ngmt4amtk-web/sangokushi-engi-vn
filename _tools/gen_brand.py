#!/usr/bin/env python3
# タイトルKV・OGPカード・PWAアイコンを生成（黒地に金・明朝の荘厳トーン）
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A=os.path.join(REPO,'assets'); os.makedirs(A,exist_ok=True)
MIN='/System/Library/Fonts/ヒラギノ明朝 ProN.ttc'
BLACK=(14,11,10); GOLD=(184,146,60); GOLDL=(232,201,122); SILK=(232,220,192); CRIM=(158,43,37)
def font(sz): return ImageFont.truetype(MIN,sz)
def vgrad(w,h,top,bot):
    img=Image.new('RGB',(w,h)); px=img.load()
    for y in range(h):
        t=y/max(1,h-1)
        px[0,y]=tuple(int(top[i]+(bot[i]-top[i])*t) for i in range(3))
    return img.resize((w,h)) if False else Image.merge('RGB',[Image.new('L',(w,h)) for _ in range(3)]).point(lambda x:x) or img
def vgrad2(w,h,top,bot):
    base=Image.new('RGB',(w,h))
    d=ImageDraw.Draw(base)
    for y in range(h):
        t=y/max(1,h-1)
        d.line([(0,y),(w,y)],fill=tuple(int(top[i]+(bot[i]-top[i])*t) for i in range(3)))
    return base
def center_text(d,cx,cy,text,fnt,fill):
    b=d.textbbox((0,0),text,font=fnt); w=b[2]-b[0]; h=b[3]-b[1]
    d.text((cx-w/2-b[0],cy-h/2-b[1]),text,font=fnt,fill=fill)
    return w,h

# 1) title_kv.jpg 1600x1000 ─ 大きな金グラデ題字＋落款＋ヴィネット（HTML題字は別途上に乗る前提でも単体で映える）
W,H=1600,1000
kv=vgrad2(W,H,(8,10,8),(3,4,3))
# 放射ヴィネット
vig=Image.new('L',(W,H),0); vd=ImageDraw.Draw(vig)
vd.ellipse([W*0.12,H*0.06,W*0.88,H*0.96],fill=70); vig=vig.filter(ImageFilter.GaussianBlur(160))
glow=Image.new('RGB',(W,H),(26,38,30)); kv=Image.composite(glow,kv,vig)
# 巨大な薄い落款（背景テクスチャ）
wm=Image.new('RGBA',(W,H),(0,0,0,0)); wd=ImageDraw.Draw(wm)
wd.text((W*0.62,H*0.30),'演',font=font(620),fill=(184,146,60,18))
kv=Image.alpha_composite(kv.convert('RGBA'),wm).convert('RGB')
d=ImageDraw.Draw(kv)
# 金の細い罫
d.line([(W*0.5-220,H*0.70),(W*0.5+220,H*0.70)],fill=GOLD,width=2)
# 下部ヴィネット濃く
dark=Image.new('L',(W,H),0); dd=ImageDraw.Draw(dark)
dd.rectangle([0,int(H*0.6),W,H],fill=180); dark=dark.filter(ImageFilter.GaussianBlur(120))
kv=Image.composite(Image.new('RGB',(W,H),(4,5,4)),kv,dark)
kv.save(os.path.join(A,'title_kv.jpg'),quality=86)

# 2) ogp.jpg 1200x630 ─ 題字入り共有カード
W,H=1200,630
og=vgrad2(W,H,(16,20,16),(4,5,4))
vig=Image.new('L',(W,H),0); vd=ImageDraw.Draw(vig)
vd.ellipse([W*0.1,-H*0.2,W*0.9,H*1.2],fill=90); vig=vig.filter(ImageFilter.GaussianBlur(140))
og=Image.composite(Image.new('RGB',(W,H),(30,44,36)),og,vig)
d=ImageDraw.Draw(og)
# 金題字（縦グラデ風＝2色重ね）
title='三國演義'
tf=font(168)
b=d.textbbox((0,0),title,font=tf); tw=b[2]-b[0]; th=b[3]-b[1]
tx=(W-tw)/2-b[0]; ty=H*0.30-th/2-b[1]
# 影
d.text((tx+3,ty+4),title,font=tf,fill=(0,0,0))
d.text((tx,ty),title,font=tf,fill=GOLDL)
# サブ
center_text(d,W/2,H*0.66,'読み物版 ─ 全120回',font(46),SILK)
center_text(d,W/2,H*0.79,'桃園結義より三分帰晋まで',font(34),(201,191,168))
d.line([(W*0.5-260,H*0.555),(W*0.5+260,H*0.555)],fill=GOLD,width=2)
og.save(os.path.join(A,'ogp.jpg'),quality=88)

# 3) アイコン（PWA/apple-touch）黒地に金の「演」・角丸
def icon(sz,pad_ratio=0.0):
    im=Image.new('RGB',(sz,sz),BLACK); d=ImageDraw.Draw(im)
    # 金枠
    m=int(sz*0.07); d.rounded_rectangle([m,m,sz-m,sz-m],radius=int(sz*0.16),outline=GOLD,width=max(2,int(sz*0.02)))
    f=font(int(sz*0.62)); center_text(d,sz/2,sz*0.52,'演',f,GOLDL)
    return im
for s in (180,192,512):
    icon(s).save(os.path.join(A,f'icon-{s}.png'))
print('生成: title_kv.jpg, ogp.jpg, icon-180/192/512.png')
