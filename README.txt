Open-HumanScale 双篇公众号文稿 / v2 / 2026-11-05

阅读：dist/index.html
文稿：dist/article-01.txt 与 dist/article-02.txt
编辑：article-01.html 与 article-02.html 是正文源文件。
重建：在本目录执行 python build.py。
预览：python -m http.server 8731 --bind 127.0.0.1 --directory dist
然后打开 http://127.0.0.1:8731

第一篇主线：纯人类数据Scaling → robot＋ego混合Scaling → zero-shot。
第二篇主线：视觉目标ICL → 人类视角目标 → 连续桌面与跨区域任务。

数据依据：用户提供的2026-11-05本地论文PDF，第3—6节。
图表：从同一论文目录中的原始PDF图导出。
视频与目标图：用户提供的公开项目页对应素材，保存在dist/assets。
项目：https://dagroup-pku.github.io/open-humanscale/
论文：https://arxiv.org/pdf/2611.06817

正式发布前可以进一步确认的材料：
1. 两条长程任务的真实执行时长、子目标输入及更新方式、是否人工干预。
2. 复杂ICL和长程任务后训练的数据量、重复测试次数及成功率。
3. 最终项目URL、团队署名、代码/数据/权重发布状态。
本版未对这些未核实信息作额外断言。

此项目为本地文稿预览，未创建云端站点。

v2更新：第一篇新增8段zero-shot demo，第二篇新增两组成对ICL视频；复用项目页两张雪山榜单动画，附完整成绩表。官方RoboTwin榜单数据核对于2026-11-05（数据自身更新时间2026-10-30）。

补充：加入同等时长人类/机器人预训练对比、少样本适应收益、RoboDojo结果与49维动作表示说明。共16段视频；本地素材引用、窄屏溢出、动画完成状态、开场视频播放、成对视频启动均已检查。

开场更新：移除两段独立真机视频，改为21段zero-shot录像拼接的56秒静音循环集锦。标题为“单一预训练模型，多项任务能力”。生成脚本：build_zero_montage.py；素材与排布：zero-montage-sources.json。

最新调整：开场改为20画面5×4网格，去掉重复的双瓶抓取例2；先单任务展示4秒，再用6秒缩放到完整网格。展示文案统一为“任务演示”。移除两张可展开完整成绩表；零样本Scaling处并列补入Task coverage图。

本轮文稿精简：SOTA表述改为“在RoboTwin 2.0上达到SOTA”；正文移除具体机器人型号、长程任务额外说明及所有折叠全文图表。第二篇第六节加入论文Fig.16架构图，并解释Goal condition设计与Scaling共同支撑能力。成功率与任务覆盖图在宽窄版均并排。
