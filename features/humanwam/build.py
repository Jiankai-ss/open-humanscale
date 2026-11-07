from pathlib import Path
from html.parser import HTMLParser
import re
import argparse

ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--output-dir',type=Path,default=ROOT/'dist')
DIST=parser.parse_args().output_dir
DIST.mkdir(parents=True,exist_ok=True)
article=(ROOT/'article.html').read_text()
class Text(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]; self.skip=0
    def handle_starttag(self,tag,attrs):
        if tag in ('button','video','script','style','nav'): self.skip+=1
        if not self.skip and tag in ('p','h1','h2','h3','h4','figcaption','section','figure'): self.parts.append('\n\n')
        if tag=='br' and not self.skip:self.parts.append('\n')
    def handle_endtag(self,tag):
        if tag in ('button','video','script','style','nav'): self.skip-=1
        if not self.skip and tag in ('p','h1','h2','h3','h4','figcaption'): self.parts.append('\n\n')
    def handle_data(self,data):
        if not self.skip:self.parts.append(data)
p=Text(); p.feed(article)
text=re.sub(r'\n[ \t]*\n(?:\s*\n)+','\n\n',''.join(p.parts)).strip()
text+='\n\n论文：https://arxiv.org/pdf/2611.06817\n项目：https://dagroup-pku.github.io/open-humanscale/\n'
(DIST/'article.txt').write_text(text)
page='''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>6万小时人机经验，能让机器人直接上手吗？HumanWAM的Scaling与零样本实验</title>
<meta name="description" content="从胶棒收纳与双手接续讲起：HumanWAM如何把约6万小时人机经验变成零样本操作，用成功率检验Scaling，再用视觉目标引导执行。">
<link rel="canonical" href="https://jiankai-ss.github.io/open-humanscale/humanwam/">
<meta property="og:type" content="article"><meta property="og:title" content="6万小时人机经验，能让机器人直接上手吗？HumanWAM的Scaling与零样本实验">
<meta property="og:description" content="20项真机评测，三条Scaling路线，一张目标图：看预训练能力如何被直接调用。">
<meta property="og:url" content="https://jiankai-ss.github.io/open-humanscale/humanwam/">
<meta property="og:image" content="https://jiankai-ss.github.io/open-humanscale/humanwam/assets/humanwam-intro-v1.jpg">
<meta name="theme-color" content="#111b22"><link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Crect width='40' height='40' rx='8' fill='%23d5f67b'/%3E%3Ctext x='9' y='29' fill='%23111b22' font-size='27' font-family='Arial'%3EH%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="benchmark-motion.css"><link rel="stylesheet" href="style.css">
<script src="benchmark-data-v20.js" defer></script><script src="benchmark-motion.js" defer></script><script src="app.js" defer></script></head>
<body><a class="skip-link" href="#story">跳到正文</a><div class="progress" aria-hidden="true"></div>
<nav class="topbar" aria-label="页面导航"><a class="brand" href="#top"><b>H</b> HumanWAM<span> / FIELD NOTES</span></a><div class="nav-links"><a href="#zero">直接上手</a><a href="#scaling">Scaling</a><a href="#goals">视觉目标</a><a href="#open">开源</a></div><button class="copy-button" data-copy>复制文稿</button><a class="download" href="article.txt" download>下载 ↗</a></nav>
<main id="story">ARTICLE</main>
<dialog id="figure-dialog" aria-labelledby="figure-caption"><div class="dialog-bar"><p id="figure-caption"></p><button type="button" data-close aria-label="关闭放大图片">关闭 ×</button></div><img alt=""></dialog>
<div class="toast" role="status" aria-live="polite" hidden></div>
</body></html>'''
(DIST/'index.html').write_text(page.replace('ARTICLE',article))
print(f'Built standalone feature: {len(re.sub(chr(92)+"s", "", text))} characters, {article.count("<video ")} videos.')
