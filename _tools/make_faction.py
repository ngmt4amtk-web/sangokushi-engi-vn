import json,os
FAC={
 '蜀':'劉備 関羽 張飛 諸葛亮 趙雲 馬超 黄忠 姜維 龐統 魏延 法正 馬岱 厳顔 徐庶 馬謖 関興 張苞 劉禅 黄月英 関銀屏 周倉 廖化 関平 孫乾',
 '魏':'曹操 張遼 龐徳 于禁 夏侯惇 夏侯淵 典韋 許褚 徐晃 張郃 郭嘉 荀彧 賈詡 曹仁 曹丕 曹叡 楽進 李典 程昱 曹真 満寵 荀攸 甄姫',
 '晋':'司馬懿 司馬師 司馬昭 鄧艾 鍾会 賈充 諸葛誕 文鴦',
 '呉':'孫権 呂蒙 孫堅 孫策 周瑜 陸遜 甘寧 太史慈 黄蓋 周泰 凌統 丁奉 韓当 程普 魯肅 諸葛瑾 孫尚香 大喬 小喬 朱然 徐盛 張昭',
 '漢':'献帝',
 '群雄':'呂布 貂蝉 董卓 袁紹 袁術 公孫瓚 張角 華雄 顔良 文醜 陳宮 王允 李儒 何進 左慈 于吉 高順 張繡 劉表',
 '異':'孟獲 祝融',
}
out={}
for f,names in FAC.items():
    for n in names.split(): out[n]=f
json.dump(out,open('scenes/faction.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(f'faction.json: {len(out)}人を陣営付与')
