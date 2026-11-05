# T1 anam 离线视频出两段样片

P0 · 20 分钟

**为什么做**：anam 回信说离线视频按套餐分钟价计费，一节课约 $3–4，比其他预渲染方案便宜 10 倍以上。只要画面和印尼语口型过关，组合 A 就成立：讲课和答疑是同一张脸、同一个声音，项目也不用接新厂商。

## 步骤

1. 在 https://lab.anam.ai/api-keys 拿 API Key（公司现有账号）。在项目根目录新建 `.env`，写一行 `ANAM_API_KEY=...`。`.env` 已经加进 `.gitignore`。
2. 用线上同款形象 Layla 跑英语、印尼语各一段：
   ```bash
   python3 scripts/anam_video.py
   ```
   - 讲稿用 B 段。音色和线上一致：英语 Mia，印尼语 Citra（导入的 ElevenLabs 音色）。
   - 视频存到 `测试结果/anam/`，终端会打印渲染耗时。
   - 如果报 400 说尺寸不支持，说明 Layla 是 Cara 3 形象，加 `--model cara-3-latest` 重跑。
3. （可选，多 10 分钟）用测试者本人照片做分身：打开 https://lab.anam.ai/avatars ，新建形象，上传 `素材/teacher-1x1.jpg`，1–2 分钟生成。复制形象 ID 后运行：
   ```bash
   python3 scripts/anam_video.py --avatar-id <形象ID> --tag me
   ```
   这一步看的是"用老师照片做的分身"在视频里像不像本人。

## 记录

在 `测试记录.csv` 的 T1 行填渲染耗时和 3 项打分。顺便看两点：
- 印尼语里 p、b、m 开头的音，嘴唇有没有闭上；
- 背景是不是纯色。纯色背景可以用项目里现成的绿幕抠像叠到幻灯片上。

## 判定

印尼语一段"能上课"≥4 分，组合 A 就可以推荐。
