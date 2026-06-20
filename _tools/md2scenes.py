#!/usr/bin/env python3
# 読み物版 第NNN回.md → scenes_NNN.js（決定論変換）。roster.json/bg規則はデータ駆動。
import re, json, sys, os

YOMI='/Users/ngmt.mtk/Shortcuts/三国志演義_読み物版'
SPRITES=os.path.expanduser('~/sangokushi-engi-vn/assets/sprites')

# 名 → 立ち絵キー（関羽伝13体を再利用＋ギャップは将来生成。ファイルが在る時だけスプライト発行＝無ければname-only）
ROSTER={
 '曹操':'caocao_base','劉備':'liubei_base','関羽':'guanyu_base','張飛':'zhangfei_base',
 '諸葛亮':'zhugeliang_base','孫権':'sunquan_base','呂蒙':'lumeng_base','馬超':'machao_base',
 '張遼':'zhangliao_base','龐徳':'pangde_base','于禁':'yujin_base','顔良':'yanliang_base','関平':'guanping_base',
 # ギャップ（画像は後から増分。キーだけ予約）
 '司馬懿':'simayi_base','周瑜':'zhouyu_base','姜維':'jiangwei_base','魯肅':'lusu_base','趙雲':'zhaoyun_base',
 '袁紹':'yuanshao_base','董卓':'dongzhuo_base','呂布':'lvbu_base','王允':'wangyun_base','孫策':'sunce_base',
 '陳宮':'chengong_base','鄧艾':'dengai_base','魏延':'weiyan_base','曹丕':'caopi_base','曹叡':'caorui_base',
 '司馬昭':'simazhao_base','鍾会':'zhonghui_base','陸遜':'luxun_base','賈詡':'jiaxu_base','張郃':'zhanghe_base',
 '劉表':'liubiao_base','荀彧':'xunyu_base','黄忠':'huangzhong_base','献帝':'xiandi_base','劉禅':'liushan_base',
 '孫堅':'sunjian_base','貂蝉':'diaochan_base','孟獲':'menghuo_base','孫乾':'sunqian_base',
}
# 背景アーキタイプ（~16枚で全120回。moodはCSS色補正で昼夜＝画像は増やさない）
BG_RULES=[ # (キーワード正規表現, bgキー)
 (r'宮|殿|朝廷|帝|后|禁中|内裏|玉座','bg_kyutei'),
 (r'城|門|楼|関|砦','bg_jokaku'),
 (r'戦|陣|軍|攻|囲|討|合戦|出陣|追撃|伏兵','bg_senjo'),
 (r'山|谷|嶺|坂|林|野','bg_sanya'),
 (r'河|江|水|船|渡|湖|海','bg_suijo'),
 (r'都|市|酒|楼|邸|屋敷|館','bg_toshi'),
 (r'書|室|帳|帷|閨|奥','bg_shitsunai'),
]
BG_DEFAULT='bg_jin'  # 陣営/野外の汎用
def mood_of(t):
    if re.search(r'夜|宵|更|燭|月',t): return 'night'
    if re.search(r'夜明け|暁|払暁|朝|曙',t): return 'dawn'
    if re.search(r'夕|暮|黄昏',t): return 'dusk'
    if re.search(r'雨|嵐|風|雷|水攻|大水',t): return 'storm'
    if re.search(r'秋|寒|雪|冬',t): return 'cool'
    return 'warm'
def bg_of(title, firsttext):
    s=title+' '+firsttext
    for pat,key in BG_RULES:
        if re.search(pat,s): return key
    return BG_DEFAULT

def split_sentences(p):
    # 1ビート1〜2文。句点で割り、2文ずつまとめる（オーバーフロー回避）
    parts=re.findall(r'[^。！？]*[。！？]', p) or [p]
    parts=[x.strip() for x in parts if x.strip()]
    out=[]; i=0
    while i<len(parts):
        chunk=parts[i]
        if i+1<len(parts) and len(parts[i])+len(parts[i+1])<=54:
            chunk=parts[i]+parts[i+1]; i+=2
        else: i+=1
        out.append(chunk)
    return out

def convert(n):
    f=f'{YOMI}/第{n:03d}回.md'
    lines=open(f,encoding='utf-8').read().split('\n')
    title=lines[0].replace('# 三国志演義 ','').strip()
    acts=[]; cur=None
    for ln in lines[1:]:
        if ln.startswith('## '):
            if cur: acts.append(cur)
            cur={'title':ln[3:].strip(),'items':[]}
        elif cur is not None:
            cur['items'].append(ln)
    if cur: acts.append(cur)
    order=[]; scenes={}
    for ai,act in enumerate(acts):
        akey=f'act{ai+1:02d}'; order.append(akey); beats=[]
        firsttext=next((x for x in act['items'] if x.strip() and not x.startswith(('**','〔','---'))),'')
        beats.append({'t':'bg','bg':bg_of(act['title'],firsttext),'mood':mood_of(act['title']+firsttext)})
        cur_sprite=None
        for raw in act['items']:
            s=raw.strip()
            if not s or s=='---' or s=='〔挿絵〕': continue
            m=re.match(r'^\*\*(.+?)\*\*「(.*)」$', s)
            if m:
                name=m.group(1); text=m.group(2)
                key=ROSTER.get(name)
                if key and os.path.exists(f'{SPRITES}/{key}.png') and key!=cur_sprite:
                    beats.append({'t':'sprite','key':key}); cur_sprite=key
                beats.append({'t':'say','name':name,'text':text})
            else:
                for sent in split_sentences(s):
                    beats.append({'t':'narrate','text':sent})
        scenes[akey]=beats
    return title, order, scenes

OUT=os.path.expanduser('~/sangokushi-engi-vn/scenes')
if __name__=='__main__':
    if sys.argv[1]=='all':
        os.makedirs(OUT,exist_ok=True)
        manifest=[]; tot_b=0
        from collections import Counter; C=Counter()
        for n in range(1,121):
            title,order,scenes=convert(n)
            js=('window.SCENE_ORDER='+json.dumps(order)+';\n'
                +'window.SCENES='+json.dumps(scenes,ensure_ascii=False)+';\n'
                +'window.EP_TITLE='+json.dumps(title,ensure_ascii=False)+';\n')
            open(f'{OUT}/scenes_{n:03d}.js','w',encoding='utf-8').write(js)
            b=sum(len(v) for v in scenes.values()); tot_b+=b
            for v in scenes.values():
                for bt in v: C[bt['t']]+=1
            manifest.append({'n':n,'title':title,'acts':len(order),'beats':b})
        json.dump(manifest,open(f'{OUT}/manifest.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
        # roster.json = 名→立ち絵base key（エンジンのネームタブ/スポットライトの単一真実源）
        json.dump(ROSTER,open(f'{OUT}/roster.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
        print(f'全120回書き出し完了 → {OUT}/scenes_001..120.js')
        print(f'総ビート={tot_b}  種別={dict(C)}')
    else:
        n=int(sys.argv[1])
        title,order,scenes=convert(n)
        print(f'第{n}回「{title}」幕={len(order)} ビート={sum(len(v) for v in scenes.values())}')
