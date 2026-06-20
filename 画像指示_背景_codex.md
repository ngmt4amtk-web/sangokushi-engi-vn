# 画像生成指示（codex用）── 三国志演義VN 背景（8枚で全120回・mood色補正で昼夜兼用）

## 実行
このmdの内容を `chatgpt-image-save` スキルで生成・保存する。
- 主担当 **ChatGPT優先**（制限時Gemini）。背景はjpgで可（透過不要）。
- 1項目=1枚。**人物・文字を入れない**（立ち絵と衝突する）。中央〜下を暗く空ける（文字窓と立ち絵が乗る）。破綻は再生成。
- 8枚で全120回を覆う（昼夜はアプリ側のmood色補正で付くので、各場所は1枚でよい・時間帯を描き込みすぎない＝ニュートラルな暗めで）。

## 保存先（絶対パス・厳守。無ければ作成。名前だけで探さない）
/Users/ngmt.mtk/sangokushi-engi-vn/assets/bg/
※ ファイル名は各項目の指定を厳守（bg_kyutei.jpg 等）。背景はそのまま使う（切り抜き不要）。

## 生成リスト
### 1. 背景：宮廷・朝廷の大広間 (bg_kyutei)
- 主担当：ChatGPT（制限時Gemini）  ファイル名：bg_kyutei.jpg  サイズ：1024×1536（縦2:3）
- プロンプト：cinematic Chinese historical environment concept art, late Han dynasty / Three Kingdoms era, painterly, atmospheric, volumetric light, depth of field, muted desaturated cinematic color grade with deep crimson and antique gold accents, no people, portrait orientation 2:3 , the grand throne hall of a late Han imperial palace, towering red-lacquered pillars receding into shadow, a distant raised dais and throne under heavy drapery, rows of bronze braziers and hanging lanterns, coffered ceiling, solemn oppressive grandeur , vertical 2:3 composition, keep the lower-center and lower-third darker and open for text window and standing characters, main motif in the upper third or to the sides, atmospheric haze, no people no characters no text
- ネガティブ：people, characters, figures, soldiers, crowd, portrait, close-up, text, watermark, signature, modern objects, bright flat lighting

### 2. 背景：城門・城楼 (bg_jokaku)
- 主担当：ChatGPT（制限時Gemini）  ファイル名：bg_jokaku.jpg  サイズ：1024×1536（縦2:3）
- プロンプト：cinematic Chinese historical environment concept art, late Han dynasty / Three Kingdoms era, painterly, atmospheric, volumetric light, depth of field, muted desaturated cinematic color grade with deep crimson and antique gold accents, no people, portrait orientation 2:3 , a massive Han dynasty city gate and rampart seen from slightly below, heavy timber-and-stone gatehouse with a tiled watchtower, thick crenellated walls, war-banners on poles, imposing fortified silhouette against a hazy sky , vertical 2:3 composition, keep the lower-center and lower-third darker and open for text window and standing characters, main motif in the upper third or to the sides, atmospheric haze, no people no characters no text
- ネガティブ：people, characters, figures, soldiers, crowd, portrait, close-up, text, watermark, signature, modern objects, bright flat lighting

### 3. 背景：戦場・野の合戦場 (bg_senjo)
- 主担当：ChatGPT（制限時Gemini）  ファイル名：bg_senjo.jpg  サイズ：1024×1536（縦2:3）
- プロンプト：cinematic Chinese historical environment concept art, late Han dynasty / Three Kingdoms era, painterly, atmospheric, volumetric light, depth of field, muted desaturated cinematic color grade with deep crimson and antique gold accents, no people, portrait orientation 2:3 , a vast open battlefield plain where armies have formed, churned earth with scattered spears and war-banners planted in the ground, distant low hills, drifting dust and smoke haze on the horizon, ominous wide emptiness , vertical 2:3 composition, keep the lower-center and lower-third darker and open for text window and standing characters, main motif in the upper third or to the sides, atmospheric haze, no people no characters no text
- ネガティブ：people, characters, figures, soldiers, crowd, portrait, close-up, text, watermark, signature, modern objects, bright flat lighting

### 4. 背景：軍営・陣幕 (bg_jin・最頻/既定)
- 主担当：ChatGPT（制限時Gemini）  ファイル名：bg_jin.jpg  サイズ：1024×1536（縦2:3）
- プロンプト：cinematic Chinese historical environment concept art, late Han dynasty / Three Kingdoms era, painterly, atmospheric, volumetric light, depth of field, muted desaturated cinematic color grade with deep crimson and antique gold accents, no people, portrait orientation 2:3 , a military encampment of a Han warlord, rows of dark canvas tents and a large command tent topped with banners, a wooden palisade, glowing campfires and torches, war-horse posts, a stern field camp under a heavy sky , vertical 2:3 composition, keep the lower-center and lower-third darker and open for text window and standing characters, main motif in the upper third or to the sides, atmospheric haze, no people no characters no text
- ネガティブ：people, characters, figures, soldiers, crowd, portrait, close-up, text, watermark, signature, modern objects, bright flat lighting

### 5. 背景：山野・峠道・林 (bg_sanya)
- 主担当：ChatGPT（制限時Gemini）  ファイル名：bg_sanya.jpg  サイズ：1024×1536（縦2:3）
- プロンプト：cinematic Chinese historical environment concept art, late Han dynasty / Three Kingdoms era, painterly, atmospheric, volumetric light, depth of field, muted desaturated cinematic color grade with deep crimson and antique gold accents, no people, portrait orientation 2:3 , a wild mountain pass and forest road in the Three Kingdoms wilderness, steep rocky slopes and gnarled pines, a winding dirt path climbing away, mist drifting between the peaks, lonely and remote , vertical 2:3 composition, keep the lower-center and lower-third darker and open for text window and standing characters, main motif in the upper third or to the sides, atmospheric haze, no people no characters no text
- ネガティブ：people, characters, figures, soldiers, crowd, portrait, close-up, text, watermark, signature, modern objects, bright flat lighting

### 6. 背景：大河・水上・船着き (bg_suijo)
- 主担当：ChatGPT（制限時Gemini）  ファイル名：bg_suijo.jpg  サイズ：1024×1536（縦2:3）
- プロンプト：cinematic Chinese historical environment concept art, late Han dynasty / Three Kingdoms era, painterly, atmospheric, volumetric light, depth of field, muted desaturated cinematic color grade with deep crimson and antique gold accents, no people, portrait orientation 2:3 , the great Yangtze river at a war-time crossing, dark wide water, moored wooden war-junks and a timber jetty, reeds in the foreground, mist over the far bank, a brooding riverine expanse , vertical 2:3 composition, keep the lower-center and lower-third darker and open for text window and standing characters, main motif in the upper third or to the sides, atmospheric haze, no people no characters no text
- ネガティブ：people, characters, figures, soldiers, crowd, portrait, close-up, text, watermark, signature, modern objects, bright flat lighting

### 7. 背景：都市の通り・酒楼 (bg_toshi)
- 主担当：ChatGPT（制限時Gemini）  ファイル名：bg_toshi.jpg  サイズ：1024×1536（縦2:3）
- プロンプト：cinematic Chinese historical environment concept art, late Han dynasty / Three Kingdoms era, painterly, atmospheric, volumetric light, depth of field, muted desaturated cinematic color grade with deep crimson and antique gold accents, no people, portrait orientation 2:3 , a street of a late Han market town, low tile-roofed timber buildings, hanging cloth shop-banners and a tavern with a wine-flag, a dusty avenue, paper lanterns, a lived-in but subdued townscape at dusk , vertical 2:3 composition, keep the lower-center and lower-third darker and open for text window and standing characters, main motif in the upper third or to the sides, atmospheric haze, no people no characters no text
- ネガティブ：people, characters, figures, soldiers, crowd, portrait, close-up, text, watermark, signature, modern objects, bright flat lighting

### 8. 背景：書斎・室内・帷帳 (bg_shitsunai)
- 主担当：ChatGPT（制限時Gemini）  ファイル名：bg_shitsunai.jpg  サイズ：1024×1536（縦2:3）
- プロンプト：cinematic Chinese historical environment concept art, late Han dynasty / Three Kingdoms era, painterly, atmospheric, volumetric light, depth of field, muted desaturated cinematic color grade with deep crimson and antique gold accents, no people, portrait orientation 2:3 , the dim interior of a Han scholar-official study chamber, a low lacquered desk with bamboo scrolls and an ink-stone, a painted folding screen and hanging drapery, a single oil lamp, intimate shadowed quiet , vertical 2:3 composition, keep the lower-center and lower-third darker and open for text window and standing characters, main motif in the upper third or to the sides, atmospheric haze, no people no characters no text
- ネガティブ：people, characters, figures, soldiers, crowd, portrait, close-up, text, watermark, signature, modern objects, bright flat lighting

## 完了報告（codex→私/あなた）
- 各ファイル：保存フルパス／使った生成器／OK or 再生成
- 出せなかった項目があれば明記
