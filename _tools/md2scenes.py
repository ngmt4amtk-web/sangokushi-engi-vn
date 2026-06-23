#!/usr/bin/env python3
# 読み物版 第NNN回.md → scenes_NNN.js（決定論変換）。roster.json/bg規則はデータ駆動。
# 2026-06-21 監査改善: 挿絵スキップ強化 / ト書き・心内独白の話者解決 / 括弧深度を見た文分割 /
#                      幕全文からのmood優勢判定 / 死の幕末fx / 別名で死蔵立ち絵を救済 / パス堅牢化。
import re, json, sys, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YOMI = os.environ.get('SANGOKUSHI_YOMI', '/Users/ngmt.mtk/Shortcuts/三国志演義_読み物版')
SPRITES = os.path.join(REPO, 'assets', 'sprites')
OUT = os.path.join(REPO, 'scenes')

# 名 → 立ち絵キー（関羽伝13体を再利用＋ギャップは将来生成。ファイルが在る時だけスプライト発行＝無ければname-only）
ROSTER={
 # 関羽伝から流用（13体・生成不要）
 '曹操':'caocao_base','劉備':'liubei_base','関羽':'guanyu_base','張飛':'zhangfei_base',
 '諸葛亮':'zhugeliang_base','孫権':'sunquan_base','呂蒙':'lumeng_base','馬超':'machao_base',
 '張遼':'zhangliao_base','龐徳':'pangde_base','于禁':'yujin_base','顔良':'yanliang_base','関平':'guanping_base',
 # 蜀
 '趙雲':'zhaoyun_base','黄忠':'huangzhong_base','姜維':'jiangwei_base','龐統':'pangtong_base','魏延':'weiyan_base',
 '法正':'fazheng_base','馬岱':'madai_base','厳顔':'yanyan_base','徐庶':'xushu_base','馬謖':'masu_base',
 '関興':'guanxing_base','張苞':'zhangbao_base','劉禅':'liushan_base','黄月英':'yueying_base','関銀屏':'guanyinping_base',
 '周倉':'zhoucang_base','廖化':'liaohua_base',
 # 魏
 '司馬懿':'simayi_base','夏侯惇':'xiahoudun_base','夏侯淵':'xiahouyuan_base','典韋':'dianwei_base','許褚':'xuchu_base',
 '徐晃':'xuhuang_base','張郃':'zhanghe_base','郭嘉':'guojia_base','荀彧':'xunyu_base','賈詡':'jiaxu_base',
 '曹仁':'caoren_base','曹丕':'caopi_base','曹叡':'caorui_base','司馬師':'simashi_base','司馬昭':'simazhao_base',
 '鄧艾':'dengai_base','鍾会':'zhonghui_base','楽進':'yuejin_base','李典':'lidian_base','程昱':'chengyu_base',
 '曹真':'caozhen_base','満寵':'manchong_base','荀攸':'xunyou_base','甄姫':'zhenji_base',
 # 呉
 '孫堅':'sunjian_base','孫策':'sunce_base','周瑜':'zhouyu_base','陸遜':'luxun_base','甘寧':'ganning_base',
 '太史慈':'taishici_base','黄蓋':'huanggai_base','周泰':'zhoutai_base','凌統':'lingtong_base','丁奉':'dingfeng_base',
 '韓当':'handang_base','程普':'chengpu_base','魯肅':'lusu_base','諸葛瑾':'zhugejin_base','孫尚香':'sunshangxiang_base',
 '大喬':'daqiao_base','小喬':'xiaoqiao_base','朱然':'zhuran_base','徐盛':'xusheng_base','張昭':'zhangzhao_base',
 # 群雄・晋
 '呂布':'lvbu_base','貂蝉':'diaochan_base','董卓':'dongzhuo_base','袁紹':'yuanshao_base','袁術':'yuanshu_base',
 '公孫瓚':'gongsunzan_base','張角':'zhangjiao_base','華雄':'huaxiong_base','文醜':'wenchou_base','陳宮':'chengong_base',
 '王允':'wangyun_base','李儒':'liru_base','何進':'hejin_base','左慈':'zuoci_base','于吉':'yuji_base',
 '高順':'gaoshun_base','張繡':'zhangxiu_base','孟獲':'menghuo_base','祝融':'zhurong_base','賈充':'jiachong_base',
 '諸葛誕':'zhugedan_base','文鴦':'wenyang_base','献帝':'xiandi_base','劉表':'liubiao_base','孫乾':'sunqian_base',
 # 別名（原典が称号/通称で呼ぶため死蔵していた立ち絵を救済）
 '孫夫人':'sunshangxiang_base','祝融夫人':'zhurong_base','単福':'xushu_base','元直':'xushu_base',
 # 増補（2026-06-22・頻出の顔なし武将に立ち絵を追加。画像指示_codex.md「増補」節で生成→PNG投入で自動昇格。それまでは固有モブ顔にフォールバック）
 '董承':'dongcheng_base','張松':'zhangsong_base','劉璋':'liuzhang_base','郭淮':'guohuai_base','李傕':'lijue_base',
 '陳登':'chendeng_base','闞澤':'kanze_base','華歆':'huaxin_base','司馬徽':'simahui_base','蔡瑁':'caimao_base',
 '孔融':'kongrong_base','楊脩':'yangxiu_base','費禕':'feiyi_base','劉曄':'liuye_base','曹洪':'caohong_base',
 '馬騰':'mateng_base','蔣幹':'jianggan_base','許攸':'xuyou_base','呉国太':'wuguotai_base','夏侯霸':'xiahouba_base',
 '韓遂':'hansui_base','郭図':'guotu_base','王平':'wangping_base','鄧芝':'dengzhi_base','糜竺':'mizhu_base',
 '馬良':'maliang_base','審配':'shenpei_base','劉琦':'liuqi_base','司馬炎':'simayan_base','陶謙':'taoqian_base',
 # 増補2(2026-06-22・頻出の名前付き端役を昇格＝モブ衝突を源で減らす。PNG投入で自動昇格)
 '孟達':'mengda_base','田豊':'tianfeng_base','楊儀':'yangyi_base','華佗':'huatuo_base','管輅':'guanlu_base',
 '李粛':'lisu_base','秦宓':'qinmi_base','顧雍':'guyong_base','郭汜':'guosi_base','張温':'zhangwen_base',
 '吉平':'jiping_base','許芝':'xuzhi_base',
}
# モブ（役割キーワード→汎用テンプレ。固有名の端役で立ち絵が無い時の演じ分け）
MOB_RULES=[
 (r'貂蝉|夫人|妃|后|姫|娘|女|侍女|婦','mob_josei'),
 (r'老婆|媼|嫗|母','mob_roujo'),
 (r'宦官|黄門|常侍','mob_kankan'),
 (r'道士|方士|僧|仙|隠者|童子','mob_doshi'),
 (r'賊|蛮|羌|匈奴|胡人|胡兵|羯|氐','mob_zoku'),   # 胡/民/農/商の裸一致を避け実在武将(胡遵・曹安民等)の誤分類を防ぐ
 (r'使者|使い|伝令|早馬|飛報','mob_shisha'),
 (r'百姓|農夫|農民|庶民|商人|樵夫|村人|町人','mob_shomin'),
 (r'門番|番兵|兵|卒|軍士|小者|手の者','mob_heishi'),
 (r'将|督|尉|司馬|校尉|太守|刺史','mob_busho'),
]
MARTIAL_POOL=['mob_busho','mob_busho_young','mob_busho_old','mob_busho_b','mob_busho_c','mob_busho_d']  # 顔なし武将。場面内の登場順で別パターンを割当（_b/_c/_dは生成後に自動で使われる）
CIVIL_POOL=['mob_bunkan','mob_bunkan_young','mob_bunkan_old','mob_bunkan_b','mob_bunkan_c','mob_bunkan_d']
def _exists(k): return bool(k) and os.path.exists(f'{SPRITES}/{k}.png')
def _namehash(name):
    h=0
    for c in name: h=(h*31+ord(c))&0xffffffff
    return h
def _pick(name, pool):
    avail=[k for k in pool if _exists(k)] or [pool[0]]
    return avail[_namehash(name)%len(avail)]
def resolve_sprite(name, bg=None, ep=None):
    # 関羽は晩年(麦城〜玉泉山＝死と顕聖)で晩年立ち絵に切替（死蔵差分の活用）
    if name=='関羽' and ep is not None and ep>=76 and _exists('guanyu_late'):
        return 'guanyu_late'
    if name in ROSTER and _exists(ROSTER[name]):   # 立ち絵が在る時だけ採用。無ければモブへフォールバック＝先行配線を安全に（PNG投入で自動昇格）
        return ROSTER[name]
    if '・' in name:                       # 連名は筆頭の人物に寄せる
        first=name.split('・')[0]
        if first in ROSTER and _exists(ROSTER[first]): return ROSTER[first]
    for pat,key in MOB_RULES:
        if re.search(pat,name):
            if key=='mob_busho': return _pick(name, MARTIAL_POOL)
            return key
    # 顔無しゼロ＝場面のbgで文/武の既定モブを出す（名前で顔を散らす）
    if bg in ('bg_kyutei','bg_shitsunai','bg_toshi'): return _pick(name, CIVIL_POOL)
    return _pick(name, MARTIAL_POOL)

# 地の文の「焦点人物」＝立ち絵が在るロスター人物が段落の早い位置に主語的に現れたら、その人を映す（紹介/描写の間も表示）
_ROSTER_NAMES=sorted([nm for nm,k in ROSTER.items() if _exists(k)], key=len, reverse=True)
def focus_in(text):
    best=None; bestpos=10**9
    head=text[:60]
    for nm in _ROSTER_NAMES:
        p=head.find(nm)
        if p>=0 and p<bestpos:
            nxt=text[p+len(nm):p+len(nm)+1]
            if nxt in 'はがもをにへとのや、。・　 と':   # 助詞/中黒/空白＝独立した人物言及（複合名の途中でない）。名前列挙(張角・張宝)は筆頭を焦点に
                bestpos=p; best=nm
    return best
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

# mood＝時刻/天候の色補正。幕全文を走査し優勢な気配を頻度で採る（warm偏重の是正）。
# 旧版の「朝→朝廷」「月→正月」「風→そよ風」等の誤検出を語彙で排除。
MOOD_KW={
 'night': r'夜陰|夜襲|夜討|夜半|深夜|宵闇|宵|夜更け|更ける|灯火|篝火|篝|燭|月明|月光|月夜|寝静|寝所|夜',
 'dawn':  r'夜明け|暁|払暁|曙|黎明|鶏鳴|東の空が白',
 'dusk':  r'夕暮|日暮れ|黄昏|夕陽|夕日|落日|残照|夕',
 'storm': r'大雨|長雨|豪雨|雨|嵐|雷|大水|洪水|水攻|霧|烈風|暴風|吹雪',
 'cool':  r'大雪|雪|氷|霜|凍|厳寒|寒風|秋風|冬',
}
def mood_of(text):
    best='warm'; bestc=0
    for mood,pat in MOOD_KW.items():
        c=len(re.findall(pat,text))
        if c>bestc: bestc=c; best=mood
    return best
def bg_of(title, firsttext):
    s=title+' '+firsttext
    for pat,key in BG_RULES:
        if re.search(pat,s): return key
    return BG_DEFAULT

_OPEN='「『（〔【'; _CLOSE='」』）〕】'
def split_sentences(p):
    # 1ビート1〜2文。句点で割るが、括弧/引用の内側(depth>0)では割らない＝詔・書状・台詞の途中改行を防ぐ。
    parts=[]; buf=''; depth=0
    for ch in p:
        buf+=ch
        if ch in _OPEN: depth+=1
        elif ch in _CLOSE:
            if depth>0: depth-=1
        elif ch in '。！？' and depth==0:
            parts.append(buf); buf=''
    if buf.strip(): parts.append(buf)
    parts=[x.strip() for x in parts if x.strip()]
    out=[]; i=0
    while i<len(parts):
        chunk=parts[i]
        if i+1<len(parts) and len(parts[i])+len(parts[i+1])<=54:
            chunk=parts[i]+parts[i+1]; i+=2
        else: i+=1
        out.append(chunk)
    return out

# 話者行の解析：**名**「台詞」 / **名**（ト書き）「台詞」 / **名**（心内独白）の3形態。
_SAY_HEAD=re.compile(r'^\*\*(.+?)\*\*(.*)$')
_STAGE=re.compile(r'^([（(][^「」]*?[)）])\s*(.*)$')
_QUOTE=re.compile(r'^「(.*)」$')
_PAREN_ONLY=re.compile(r'^[（(].*[)）]$')
def parse_say(s):
    m=_SAY_HEAD.match(s)
    if not m: return None
    name=m.group(1).strip(); rest=m.group(2).strip()
    if not name: return None
    stage=''
    sm=_STAGE.match(rest)
    if sm and '「' in sm.group(2):        # ト書き＋台詞
        stage=sm.group(1); rest=sm.group(2).strip()
    qm=_QUOTE.match(rest)
    if qm:
        return name, (stage+qm.group(1)) if stage else qm.group(1)
    if _PAREN_ONLY.match(rest):           # 心内独白（鉤括弧なし・全文が括弧）
        return name, rest
    return None                            # 台詞でない＝地の文として扱う

# 幕末が誰かの死で閉じる時だけ静かな暗転(fade)を1つ添える（保守的・ストロボ化回避）。
_DEATH=re.compile(r'息絶え|事切れ|こと切れ|絶命|落命|薨去|薨じ|崩御|身罷|世を去っ|自刎|自害|刎ねて|斃れ|討ち死に|戦死|陣没|みまかっ')
_KILL=re.compile(r'斬り捨て|斬って捨て|一刀のもとに|一刀の下に|首を刎ね|首を斬|討ち取った|突き伏せ|刺し殺|斬り落と|真っ二つ|斬り伏せ')  # 戦場の見せ場に閃光fxを1幕1回だけ
_INSET=re.compile(r'^[〔［【]?挿絵')   # 〔挿絵〕も〔挿絵：…〕も（裸の挿絵も）全てスキップ
_TRANS=re.compile(r'^(そのころ|さて|一方|やがて|こうして|ほどなく|まもなく|間もなく|翌|数日|十数日|幾日|時に|これより|その後|のちに|折しも|かくて|ここで|話は)')  # 場面転換/時の飛び＝立ち絵を一旦消す
_QOPEN=re.compile(r'^\*\*[^*]+\*\*(?:[（(][^「」]*[)）])?「')  # 話者が鉤括弧を開く行

def merge_multiline_quotes(items):
    # 複数段落にまたがる長台詞（例ep57諸葛亮の弔辞）を1行に結合し、話者属性を保つ
    out=[]; i=0; n=len(items)
    while i<n:
        st=items[i].strip()
        if _QOPEN.match(st) and st.count('「')>st.count('」'):
            buf=st; j=i+1
            while j<n and buf.count('「')>buf.count('」'):
                nxt=items[j].strip()
                if nxt and nxt!='---' and not _INSET.match(nxt.lstrip('〔［【')):
                    buf+=nxt
                j+=1
            out.append(buf); i=j
        else:
            out.append(items[i]); i+=1
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
        items=merge_multiline_quotes(act['items'])
        firsttext=next((x for x in items if x.strip() and not x.startswith(('**','〔','［','【','---'))),'')
        actbg=bg_of(act['title'],firsttext)
        # moodは幕の全文(地の文)から優勢気配を採る
        acttext=act['title']+' '+' '.join(x for x in items if not x.lstrip().startswith(('**','〔','［','【','---')))
        beats.append({'t':'bg','bg':actbg,'mood':mood_of(acttext)})
        cur_sprite=None; flashed=False; last_say_name=None; mob_assign={}; mob_ctr={'m':0,'c':0}; narr_run=0
        for raw in items:
            s=raw.strip()
            if not s or s=='---': continue
            if _INSET.match(s.lstrip('〔［【')) or s.startswith(('〔挿絵','［挿絵','【挿絵')): continue
            parsed=parse_say(s)
            if parsed:
                name,text=parsed
                key=resolve_sprite(name, actbg, n)
                # 立ち絵無しの武将/文官は「場面内の登場順」で別パターンを割当＝同種別人を確実に描き分け（場面内で一意・名前タブ色と二重の手掛かり）
                if key and (key.startswith('mob_busho') or key.startswith('mob_bunkan')):
                    tp='m' if key.startswith('mob_busho') else 'c'
                    pool=MARTIAL_POOL if tp=='m' else CIVIL_POOL
                    avail=[k for k in pool if _exists(k)] or [pool[0]]
                    if name in mob_assign: key=mob_assign[name]
                    else: key=avail[mob_ctr[tp]%len(avail)]; mob_ctr[tp]+=1; mob_assign[name]=key
                if key and os.path.exists(f'{SPRITES}/{key}.png') and key!=cur_sprite:
                    beats.append({'t':'sprite','key':key}); cur_sprite=key
                beats.append({'t':'say','name':name,'text':text}); last_say_name=name; narr_run=0
            else:
                # 立ち絵の表示/クリアのタイミング＝地の文の「焦点」を映す
                is_tr=bool(_TRANS.match(s))
                if is_tr and cur_sprite:                       # 場面転換語＝一旦消す
                    beats.append({'t':'hide'}); cur_sprite=None; narr_run=0
                foc=focus_in(s)
                if foc:                                         # 段落が或る人物の紹介/描写＝その人の立ち絵を出す（喋ってなくても）
                    fk=resolve_sprite(foc, actbg, n)
                    if fk and _exists(fk) and fk!=cur_sprite:
                        beats.append({'t':'sprite','key':fk}); cur_sprite=fk
                    narr_run=0
                else:                                           # 焦点人物なしの地の文が続く＝会話/描写が終わった→立ち絵を消す
                    narr_run+=1
                    if cur_sprite and narr_run>=2:
                        beats.append({'t':'hide'}); cur_sprite=None
                for sent in split_sentences(s):
                    if actbg=='bg_senjo' and not flashed and _KILL.search(sent):
                        beats.append({'t':'fx','fx':'flash'}); flashed=True
                    beats.append({'t':'narrate','text':sent})
        # 幕末が死で閉じるなら静かな暗転
        if beats and beats[-1].get('t')=='narrate' and _DEATH.search(beats[-1].get('text','')):
            beats.append({'t':'fx','fx':'fade'})
        scenes[akey]=beats
    return title, order, scenes

if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='all':
        os.makedirs(OUT,exist_ok=True)
        manifest=[]; tot_b=0
        from collections import Counter; C=Counter(); M=Counter()
        for n in range(1,121):
            title,order,scenes=convert(n)
            js=('window.SCENE_ORDER='+json.dumps(order)+';\n'
                +'window.SCENES='+json.dumps(scenes,ensure_ascii=False)+';\n'
                +'window.EP_TITLE='+json.dumps(title,ensure_ascii=False)+';\n')
            open(f'{OUT}/scenes_{n:03d}.js','w',encoding='utf-8').write(js)
            b=sum(len(v) for v in scenes.values()); tot_b+=b
            for v in scenes.values():
                for bt in v:
                    C[bt['t']]+=1
                    if bt['t']=='bg': M[bt.get('mood')]+=1
            manifest.append({'n':n,'title':title,'acts':len(order),'beats':b})
        json.dump(manifest,open(f'{OUT}/manifest.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
        # roster.json = 名→立ち絵base key（エンジンのネームタブ/スポットライトの単一真実源）
        json.dump(ROSTER,open(f'{OUT}/roster.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
        print(f'全120回書き出し完了 → {OUT}/scenes_001..120.js')
        print(f'総ビート={tot_b}  種別={dict(C)}')
        print(f'mood分布={dict(M)}')
    elif len(sys.argv)>1:
        n=int(sys.argv[1])
        title,order,scenes=convert(n)
        print(f'第{n}回「{title}」幕={len(order)} ビート={sum(len(v) for v in scenes.values())}')
    else:
        print('usage: md2scenes.py [all|N]')
