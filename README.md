# 三國演義 ─ 読み物版 VN（全120回）

羅貫中『三国志演義』全120回を、**報告調の地の文＋会話の二層**で読む一本道ノベルゲーム。
桃園結義から三分帰晋まで。選択肢なし・通読型。GitHub Pages で配信（PWA・オフライン対応）。

▶ https://ngmt4amtk-web.github.io/sangokushi-engi-vn/

## 構成
- `index.html` … 単一エンジン（描画・ページネーション・立ち絵スポットライト・ログ・オート/スキップ・**セーブ/続きから/読了管理**・文字速度/サイズ・PWA登録）
- `scenes/scenes_NNN.js` … 各回のビート列。原典mdから `_tools/md2scenes.py` で**決定論生成**（手編集しない）
- `scenes/manifest.json` … 全120回の目次（タイトル/幕数/ビート数）
- `scenes/roster.json` … 名→立ち絵キー（ネームタブ・スポットライトの真実源）
- `scenes/faction.json` … 名→陣営（ネームタブ色。未登録名は名前ハッシュで一意色に吸収）
- `assets/sprites/` … 立ち絵（緑背景→透過切り抜き済）／`assets/bg/` … 背景8枚（moodで昼夜・天候を色補正）
- `assets/ogp.jpg` `assets/title_kv.jpg` `assets/icon-*.png` … ブランド画像（`_tools/gen_brand.py` で生成）
- `manifest.webmanifest` `sw.js` … PWA（インストール可・オフライン読書）

## 生成（再ビルド）
```sh
python3 _tools/md2scenes.py all     # 原典md → scenes_001..120.js + manifest + roster
python3 _tools/make_faction.py      # faction.json
python3 _tools/gen_brand.py         # タイトル/OGP/アイコン
```
原典の置き場所は環境変数 `SANGOKUSHI_YOMI` で上書き可（既定 `~/Shortcuts/三国志演義_読み物版`）。
スクリプトはリポジトリ位置を `__file__` から解決するため、クローン先に依存しない。

## 原典記法（md2scenes が解釈する）
- `## 第N幕　…` … 幕（act）境界
- 地の文 … 句読点で文単位に分割（**鉤括弧・引用の内側では分割しない**＝詔/書状/長台詞の途中改行を防ぐ）
- `**名前**「台詞」` … 会話。`**名前**（ト書き）「台詞」` と `**名前**（心内独白）` も話者として解決
- 複数段落にまたがる長台詞は1つの会話に結合（例：第57回 諸葛亮の弔辞）
- `〔挿絵〕` `〔挿絵：説明〕` … 画像指示。本文には出さずスキップ（将来CG化用の印）

## ライセンス / クレジット
- 原作『三国志演義』（羅貫中）はパブリックドメイン。
- 現代日本語訳・脚色・実装・立ち絵/背景は本リポジトリ著者による。
