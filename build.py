from pathlib import Path
from html.parser import HTMLParser
import re

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'dist'
articles = [(ROOT / f'article-{i:02}.html').read_text() for i in (1, 2)]
template = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Open-HumanScale双篇研究解读：从纯人类与人机混合Scaling，到零样本操作、视觉目标ICL与长程任务。"><title>Open-HumanScale · 两篇研究解读</title><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="benchmark-motion.css"><link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Crect width='40' height='40' rx='9' fill='%23246154'/%3E%3Ctext x='9' y='29' fill='white' font-size='27' font-family='serif'%3EH%3C/text%3E%3C/svg%3E"><script src="app.js" defer></script><script src="benchmark-data-v20.js" defer></script><script src="benchmark-motion.js" defer></script></head>
<body><div class="reading-progress" aria-hidden="true"></div>
<header class="masthead"><div class="masthead-inner"><a class="brand" href="#article-1">Open-<span>Human</span>Scale</a><span class="mast-label">RESEARCH / STORIES</span><div class="top-actions"><button id="phone-toggle" aria-pressed="false">手机预览</button><button id="copy">复制正文</button></div></div></header>
<div class="edition-bar"><div class="edition-tabs" role="tablist" aria-label="选择文章"><button role="tab" id="tab-1" data-tab="0" aria-controls="article-1" aria-selected="true"><small>01</small> Scaling与零样本</button><button role="tab" id="tab-2" data-tab="1" aria-controls="article-2" aria-selected="false"><small>02</small> 视觉目标与长程任务</button></div><span class="edition-note">两篇文稿 / 审阅版 02</span></div>
<noscript><p class="no-js-note">启用JavaScript可切换文章；也可以下载<a href="article-01.txt">第一篇</a>或<a href="article-02.txt">第二篇</a>文稿。</p></noscript>
<div class="page-layout"><aside class="sidebar"><p class="side-kicker">IN THIS STORY</p><nav class="toc" aria-label="文章目录"></nav><div class="side-foot"><span id="reading-meta"></span><br>图表可点击放大<a class="download" href="article-01.txt" download>下载文稿 ↓</a></div></aside><main>
<article id="article-1" class="article" role="tabpanel" aria-labelledby="tab-1">ARTICLE_ONE<button class="article-end" data-next="1"><span><small>继续阅读 / 02</small>换张目标图，机器人换种收纳法</span><span>→</span></button></article>
<article id="article-2" class="article" role="tabpanel" aria-labelledby="tab-2" hidden>ARTICLE_TWO<button class="article-end" data-next="0"><span><small>回到上一篇 / 01</small>人类与机器人经验共同扩展</span><span>→</span></button></article>
</main></div><footer class="footer"><span>Open-HumanScale · 文稿与配图预览</span><span>HUMAN + ROBOT EXPERIENCE → CAPABILITY</span></footer>
<dialog id="image-dialog" aria-labelledby="image-caption"><div class="dialog-top"><span id="image-caption"></span><button aria-label="关闭图片">×</button></div><img alt=""></dialog><div class="toast" role="status" aria-live="polite" hidden></div>
</body></html>'''
site_url = 'https://jiankai-ss.github.io/open-humanscale'
share_metadata = f'''<link rel="canonical" href="{site_url}/"><meta property="og:type" content="website"><meta property="og:url" content="{site_url}/"><meta property="og:title" content="Open-HumanScale · 两篇研究解读"><meta property="og:description" content="从人类与机器人混合数据Scaling，到零样本操作、视觉目标ICL与长程任务。"><meta property="og:image" content="{site_url}/assets/zero-shot-tasks-zoom.jpg">'''
(DIST / 'index.html').write_text(template.replace('</head>', share_metadata + '</head>').replace('ARTICLE_ONE', articles[0]).replace('ARTICLE_TWO', articles[1]))

class ExtractText(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts = []; self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ['p','h1','h2','figcaption','div','aside','section']: self.parts.append('\n\n')
        if tag == 'br': self.parts.append('\n')
        if tag == 'tr': self.parts.append('\n')
        if tag in ['td','th']: self.parts.append('\t')
        if tag in ['script','style','button','video','nav']: self.skip += 1
    def handle_endtag(self, tag):
        if tag in ['p','h1','h2','figcaption']: self.parts.append('\n\n')
        if tag in ['script','style','button','video','nav']: self.skip -= 1
    def handle_data(self, data):
        if not self.skip: self.parts.append(data)
for i, article in enumerate(articles, 1):
    parser=ExtractText();parser.feed(article)
    text = re.sub(r'\n\s*\n(?:\s*\n)+', '\n\n', ''.join(parser.parts)).strip()
    text += '\n\n论文：https://arxiv.org/pdf/2611.06817\n项目：https://dagroup-pku.github.io/open-humanscale/\n'
    (DIST / f'article-{i:02}.txt').write_text(text+'\n')
    print(f'Article {i}: {len(re.sub(r"\s", "", text))} characters')
print('Built', DIST / 'index.html')
