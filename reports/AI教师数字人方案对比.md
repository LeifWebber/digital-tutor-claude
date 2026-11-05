# 语音先行，数字人按需：AI 教师选型

> **11-05 实测已完成，最终推荐见 `../推荐方案.md`。** 实测结论：anam 离线视频和 anam 实时都可用；万相视频创作可以用，但不够自然；万相 2D 实时、百炼 wan2.7、Simli 三项淘汰。

> **2026-11-05 更新：本节优先于下文。** 正文是 11-04 的桌面调研版本，下面三条新信息改变了预渲染的结论。
>
> 1. **anam 离线视频（Avatar Videos API）按现有套餐的每分钟价计费。** 这条来自 anam 邮件回复，不是推算。按当前套餐算是 $0.11–0.16/分钟，Enterprise 低至 $0.04，比下表任何一家预渲染都便宜一个数量级（其他家最低约 $0.68/分钟）。允许把 MP4 存到自己的 CDN 无限回放。每个请求最多 20,000 字符，约 20–25 分钟口播。Growth 及以上套餐没有单段时长上限。分辨率为 Cara 4 的 1152×768（横）或 768×1152（竖），Cara 3 只有 720×480。没有亚太区域，但预渲染一次、之后存储回放，所以没有影响。
>    - 一节课 27 分钟全程出镜约 **$3–4.3（20–29 元）**；80 节课全部做成视频约 **$240–350（1,600–2,350 元）**，一次性支出（推算：27 分钟 × $0.11–0.16，汇率 6.69）。
>    - 视频里的形象和声音与实时答疑是同一个。
>    - 这直接动摇了决策 9 里"不做预渲染数字人视频"的成本前提，见下文"推荐组合（11-05 版）"。
> 2. **anam 会话 30 分钟断开是我们自己代码设的，不是套餐限制。** anam 回复写明 Growth 及以上套餐没有会话时长上限。代码里 `maxSessionLengthSeconds: 1800` 可以直接改成 2,700 以上。文末"待人工验证"表的第 4 条已有答案。
> 3. **与第一轮调研结论有冲突的地方，11-05 回到官方页面逐条核实，结果如下。**第一轮结论只作线索，下面每条都以官方页面或实际文件为准。
>
>    | 说法 | 核实结果 | 依据 |
>    |---|---|---|
>    | 万相数字人"视频创作"能输出透明背景 | ✅ 成立，修正本报告。下文"所有照片+音频模型都没有透明背景"不适用于它 | 官方 API 参数 `mode=ONLY_AVATAR`：仅保留数字人通道，输出 webm（含透明通道），只对透明背景形象有效（[CreateBroadcastVideoFromTemplate](https://help.aliyun.com/zh/avatar/avatar-application/developer-reference/api-lingmou-2025-05-27-createbroadcastvideofromtemplate)）。本地样片用 ffprobe 检查：VP9、1280×720、`ALPHA_MODE=1` |
>    | 视频创作 0.1 元/秒 | ✅ 成立 | 官方："6元/分钟（精确到秒，即0.1元/秒）"，按量后付费，发起后不退款；控制台为 1 积分/秒，积分包 0.085–0.1 元/积分（[视频创作计费](https://help.aliyun.com/zh/avatar/avatar-application/product-overview/avatar-video-pricing)；[会员与积分](https://help.aliyun.com/zh/avatar/avatar-application/product-overview/avatar-membership-subscriptions-and-credits-packages)）。样片时长 34.0 / 36.5 秒，旧记录的 3.4 / 3.7 元与之吻合 |
>    | 视频创作渲染约 180 秒 | ⚠️ 只有旧记录，无法核实 | 需要在 T2 中重新计时 |
>    | 水印可以关闭 | ⚠️ 部分成立 | API 的 `watermark` 默认 True，可以传 False；控制台去水印要标准会员（100 元/月）及以上 |
>    | 百炼新人免费额度已下架 | ✅ 成立 | 官方"新人免费额度"页的下架列表（标注 2026-10-29）含 wan2.2-s2v、emo、liveportrait、wan2.7-i2v、cosyvoice 全系；videoretalk 不在列表中；只有北京地域有免费额度（[新人免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)）。旧版写的"10-30 更新"在页面上找不到，页面没有标注更新日期 |
>    | EMO 和 LivePortrait 已下线 | ⚠️ 疑似 | 两者的 API 文档页现在跳转到模型总览，VideoRetalk 的页面仍然在；但免费额度页还列着它们。不再测试 |
>    | CosyVoice 印尼语 | ✅ v3-flash、v3.5-flash、v3.5-plus 支持，v3-plus 不支持；⚠️ 新加坡地域是否每个模型都能复刻，官方没有逐个写明 | [声音复刻 API](https://help.aliyun.com/zh/model-studio/voice-clone-design-http-api)。旧版"系统音色只有北京的 loongindah_v3"本次没有核实 |
>    | 汇率 | 旧版按 6.75，本报告按 7.1，人民币数字会差约 5% | — |
>
> 4. **补充 X 社区评价（用 Grok 检索，原文见 `research_notes/AI教师数字人方案对比/06_X社区评价.md`），同样逐条核实：**
>
>    | 说法 | 核实结果 | 对结论的影响 |
>    |---|---|---|
>    | 汇率约 6.68 | ✅ open.er-api.com 2026-11-05 为 1 USD = 6.685 CNY | 正文按 7.1 算的人民币数字**偏高约 6%**；本节和任务文件已改按 6.69 |
>    | anam 连接要 4–10 秒 | ✅ 出自 anam 官方 FAQ："usually 4-5 seconds, but can be up to 10 seconds"（[anam FAQ](https://anam.ai/docs/resources/faq)） | 与 anam 基准里首帧 1.42 秒的说法冲突，以实测为准（T4） |
>    | 万相实时的打断主要靠人设里的"打断关键词" | ⚠️ 出自官方云渲染全链路指南；旧版调研另称 SDK 的 `interrupt()` 在思考、回答状态下可用 | T3 里两种都试 |
>    | "通义灵眸"已改名为"万相数字人"（约 2025-12） | ⚠️ 只有第三方来源 | 可以解释"虚拟数字人（文档停止维护）"指的是旧 DVH 文档树，不一定是产品要停；仍需阿里客服确认 |
>    | 开源 LongCat-Video-Avatar 在 X 上被频繁拿来对比 HeyGen 订阅价 | ✅ 有 1.5 版，主页仓库为 MIT 许可（MeiGen-AI/LongCat-Video-Avatar-1.5-Page），有 RunPod / ComfyUI 部署 | 自建要 GPU 和工程投入，单价也未必低于 anam 离线视频的 $0.11/分钟；只作远期压成本选项，不进 MVP |
>    | HeyGen LiveAvatar 实时线不该因 HeyGen 预渲染贵而一起排除 | ✅ 成立，但要修正口径：LITE 约 $0.09/分钟，不含语音识别和合成，补上后约 $0.10–0.13，与 anam 持平；FULL 约 $0.18，比 anam 贵。官网没有降价说明 | 作为与 anam 谈价的参照，MVP 不测 |
>    | X 上的共识：AI 教师 = 口播讲课 + 实时问答两件事，评测要包含打断和恢复讲课 | 观点，非事实 | 与本文组合 A/B/C 的拆法一致；T3、T4 已包含打断 |
>
> **推荐组合（11-05 版，待实测确认）**
>
> | 组合 | 讲课（预渲染） | 答疑（实时） | 一节课成本 | 适合 |
> |---|---|---|---|---|
> | **A. anam 一家通吃**（首推） | anam Avatar Videos，形象和声音与实时相同 | anam 实时（现状） | 视频约 $3–4.3，一次性；答疑按分钟 $0.11–0.16 | 改动最小、最省钱；讲课和答疑是同一个老师 |
> | **B. 阿里讲课 + anam 答疑** | 万相数字人视频创作，透明 WebM 叠在幻灯片上 | anam 实时；万相 2D 云渲染测试达标的话再换 | 视频约 162 元（全程）或 40 元（25% 出镜），一次性 | 阿里方案；画面能透明叠加在幻灯片上 |
> | **C. 实时最省**（后续优化项） | 同 A 或 B | Simli 音频驱动，吃我们的 ElevenLabs 音频 | 答疑约 $0.01/分钟 | 实时用量大了以后再换；需要开发接入 |
>
> 语音保留 ElevenLabs。TTS 在任何组合里都只占几分钱，不值得为省这点钱换供应商。百炼 wan2.2-s2v、wan2.7-i2v 每分钟 30–60 元，而且每段最长 15–20 秒，不推荐批量用，只作为"阿里视频模型"的样片对照。

对 maic-avatar 来说，成本和风险都最低的组合是：用预渲染的 ElevenLabs 神经语音打底，只在需要互动的场合开实时数字人。这与 2026-11-01 的决策 9 方向一致。按项目自己的用量画像算，一节 45 分钟的课约有 23–27 分钟口播，英语约 1.87 万字符，整课预渲染语音每节约 **$0.75–0.82（5.3–5.8 元）**。数字人视频最便宜的一档是 **$0.14–0.68/分钟**（腾讯、百度时长包，阿里 VideoRetalk，托管 LatentSync），前提是先有老师视频或定制形象；只用一张照片生成要 **$1.8–9.6/分钟**。全程出镜一节课，主流方案要 $18–150（OmniHuman 1.5 高达 $240）；只让老师出镜 25%（A-roll），一节课也要 $5–60。仓库估算一所 3 万学生的学校每月生成约 6,000 节课，如果全部预渲染视频，每月是 3 万到 36 万美元量级，所以视频只能用在固定的精品课目录上。实时档的格局已经变了。只做渲染、直接吃我方音频的厂商（**Simli $0.009/分钟、bitHuman $0.02–0.04、HeyGen LiveAvatar LITE 约 $0.085**）标价都低于 anam Professional 的 $0.11。但它们不含语音识别和合成，加上 ElevenLabs 后，HeyGen LiveAvatar 约 $0.10–0.13/分钟，与 anam 持平。HeyGen "贵"指的是预渲染（Avatar V 官方 $7.20/分钟），实时产品是另一条产品线、另一套价格，不是降价（11-05 核实，见"推荐组合与一所学校的月账"表下的参考行）。国内实时数字人按"路/月"包月，**2,400–3,500 元/路/月**。只有每一路每个上学日都跑满约 3 节课以上，才比 anam 标准价便宜；在上学时段里，它始终追不上 anam 企业价 $0.04。阿里云的长处在预渲染 API：wan2.7-i2v 有新加坡地域，VideoRetalk 是最便宜的一档，照片输入也不用训练。实时方面阿里只有"万相数字人 2D 云渲染"一条自营路线，有 Web SDK，也有"音频驱动"模式，但传输协议、延迟、海外可用性都没有公开数据，旧文档目录还标着"停止维护"，所以只能列为待测备选。本文推荐预渲染三档、实时三档。延迟、印尼语口型和所有需要商务洽谈的价格，都要人工实测后才能定案。

> 口径说明：汇率统一按 1 USD = 7.1 CNY、€1 ≈ $1.15（假设值）。表中"官方"指厂商定价页或文档原价；"第三方"指聚合站、转售商或评测文章；"推算"指本文根据官方单价和项目用量自行计算。用量基准全部来自仓库：一节标准课 45 分钟、32–33 个场景、约 23 分钟口播（成本口径 27 分钟，60% 讲解占比未确认）([CLAUDE.md](https://github.com/Kunbyte-AI/maic-avatar/blob/deploy/prod-diagram-fix/CLAUDE.md#L68))。本文取 25 分钟作为讲话分钟，45 分钟作为实时连接分钟。

## 预渲染：整课语音约 $0.8，加上数字人视频就是 $5–240

预渲染的成本几乎全由视频决定。HeyGen 实测已经说明了这一点："Speech is ~20x cheaper than video… the video share decides the bill"，团队按钱包扣款解出视频约 **$0.102/秒（约 $6.1/分钟）**，语音约 $0.0055/秒，渲染耗时约为实时的 10 倍 ([README-teacher-clips](https://github.com/Kunbyte-AI/maic-avatar/blob/deploy/prod-diagram-fix/scripts/README-teacher-clips.md))。ElevenLabs 现在的低延迟档（Flash v2.5 / v4 Turbo / v3 Conversational）官方价是 **$0.04/千字符**，高质量档（v4 / v3 / Multilingual v2）是 $0.08，大档订阅只是预付，单价不降 ([ElevenLabs API Pricing](https://elevenlabs.io/pricing/api))。项目旁白用的是 `eleven_v4_turbo`。按 g7-01 课件的字符数（英 18,712、印尼 20,617、中文约 5,282）算，一节课的语音分别是 $0.75、$0.82、$0.21。80 节课约 150 万字符，全部预渲染一次大约 **$60（约 426 元）**（推算）。

下表把各家预渲染方案统一换算成每输出分钟的价格。

| 方案 | 输入 | USD/分钟 | CNY/分钟 | 口径 | 关键限制 |
|---|---|---|---|---|---|
| ElevenLabs v4 Turbo（仅语音） | 文本 | 0.036（英）/ 0.040（印尼） | 0.26 / 0.28 | 官方单价，每分钟为推算 | 实测会忽略语速设置 ([commit c7b3cffd](https://github.com/Kunbyte-AI/maic-avatar/commit/c7b3cffd)) |
| 阿里 VideoRetalk | 老师视频 + 我方音频 | 0.68 | 4.8 | 官方 ([videoretalk](https://help.aliyun.com/zh/model-studio/videoretalk)) | 仅北京地域，并发 1，要正面清晰视频 |
| 阿里 万相数字人视频创作（控制台） | 训练好的形象 + 上传音频 | 0.72–0.85 | 5.1–6.0 | 官方积分价（1 积分/秒），折算为推算 ([会员与积分](https://help.aliyun.com/zh/avatar/avatar-application/product-overview/avatar-membership-subscriptions-and-credits-packages)) | API 价未公开；免费会员有水印 |
| 阿里 wan2.2-s2v 480P / 720P | 照片 + 音频 | 4.23 / 7.61 | 30 / 54 | 官方 ([wan-s2v api](https://help.aliyun.com/zh/model-studio/wan-s2v-api)) | 每段 <20 秒，并发 1，每段 5–10 分钟，仅北京，16 fps |
| 阿里 wan2.7-i2v（driving_audio）720P / 1080P | 照片 + 音频 | 北京 5.16 / 8.60；新加坡 6.0 / 9.0 | 北京 36.6 / 61.1（推算）；新加坡 42.6 / 63.9 | 官方美元价 ([Intl pricing](https://www.alibabacloud.com/help/en/model-studio/model-pricing)) | 每段视频 2–15 秒，每段 1–5 分钟，30 fps |
| 百度曦灵 2D 小样本 | 定制形象 | 0.42 | 3.0 | 官方时长包 ([曦灵价格](https://xiling.cloud.baidu.com/doc/AI_DH/s/Vlysgbz88)) | 能否吃外部音频未确认；形象 1,000 元 |
| 腾讯 2D 小样本（≤10 包 → ≥50 包） | 定制形象 | 0.47 → 0.14 | 3.33 → 1.0 | 官方 ([腾讯价格指南](https://cloud.tencent.com/document/product/1240/101944)) | 能否吃外部音频未确认；形象 2,500 元 |
| 火山 克隆数字人 | 老师视频形象 + 音频 | 0.85 | 6.0 | 官方，页面 2025-08 ([火山智能视觉](https://docs.volcengine.com/docs/Intelligentvisionservices/Abilitytointroduce-19?lang=zh)) | 单次 ≤12 分钟；创建形象 2,599 元 |
| InfiniteTalk（WaveSpeed）480p / 720p | 照片 + 音频 | 1.80 / 3.60 | 12.8 / 25.6 | 官方托管价 ([WaveSpeed](https://wavespeed.ai/models/wavespeed-ai/infinitetalk)) | 开源 Apache-2.0；图生视频超过约 1 分钟会色偏 |
| Kling AI Avatar v2 Std / Pro（fal） | 照片 + 音频 | 3.37 / 6.90 | 23.9 / 49.0 | fal 标价 ([fal](https://fal.ai/models/fal-ai/kling-video/ai-avatar/v2/standard)) | Std 讲话单段约 1 分钟（第三方） |
| OmniHuman 2.0（BytePlus）/ 1.5（fal） | 照片 + 音频 | 4.20 / 9.60 | 29.8 / 68.2 | 官方 ([BytePlus](https://www.byteplus.com/product/OmniHuman))；[fal](https://fal.ai/models/fal-ai/bytedance/omnihuman/v1.5) | 2.0 为 720p、单段 30–300 秒 |
| LatentSync（fal，两段式中的对口型步骤） | 老师视频 + 音频 | 约 0.30 | 约 2.1 | 推算（≤40 秒 $0.20，超出 $0.005/秒）([fal](https://fal.ai/models/fal-ai/latentsync)) | 要先有一段老师视频底板 |
| D-ID API | 平台形象 | 0.99–1.13 | 7.0–8.0 | 第三方核查 ([toolcolumn](https://www.toolcolumn.com/pricing/d-id-pricing)) | 套餐分钟不结转，形象属上一代 |
| Synthesia 配音对口型 API | 平台形象 + 音频 | 0.80 | 5.7 | 官方 ([Synthesia](https://www.synthesia.io/api-pricing)) | 自定义形象 $1,000/年 |
| HeyGen（参考） | 照片或分身 + 音频 | 团队实测 Avatar V 约 6.1；API Avatar IV 约 3.0 | 43.5 / 21.3 | 项目实测 / 第三方 ([anam 博客](https://anam.ai/blog/heygen-pricing)) | 已因价格排除；透明 WebM 只能在 Chrome 播放 |
| Anam 离线 Avatar Videos | 与实时同一分身（输入文本，由 anam 合成语音） | 0.11–0.16（Enterprise 低至 0.04） | 0.78–1.14 | **anam 邮件回复（11-05）**：等于套餐每分钟价 | 允许自存、无限回放；每次最多 2 万字符；1152×768；下载链接 1 小时过期，需及时转存 |

阿里的预渲染能力是真实可用的，但每个模型都带着工程限制，单价表里看不出来。**wan2.2-s2v** 一次只接受 20 秒以内的音频，主账号和子账号共享"同时处理中任务数 1"，每段要 5–10 分钟，结果 URL 只保留 24 小时，而且只开在北京地域 ([wan-s2v api](https://help.aliyun.com/zh/model-studio/wan-s2v-api))。80 节课按 25% 出镜计约 500 分钟视频，至少要切 1,500 段；在 1 并发下串行，需要 125–250 小时（推算）。全程出镜要四倍时间，不申请提高并发就无法批量生产。**wan2.7-i2v** 是阿里目前最适合本项目的生成式选项：在 `media` 里传 `driving_audio`，模型会把它"用作口型同步和动作节奏的驱动源"，支持 1080P、30 fps，北京和新加坡都能用 ([Intl image-to-video API](https://www.alibabacloud.com/help/model-studio/image-to-video-general-api-reference))；代价是每段只有 15 秒，拼接处的一致性要实测。**VideoRetalk** 每分钟只要 4.8 元，比生成式便宜一个数量级，前提是老师先录一段正面讲课视频，同样只有北京地域和 1 并发 ([videoretalk](https://help.aliyun.com/zh/model-studio/videoretalk))。万相数字人控制台的"视频创作"可以直接上传音频作为成片音轨 ([视频创作指南](https://help.aliyun.com/zh/avatar/avatar-application/user-guide/avatar-video-operation-guide))，按积分算每分钟只要 5–6 元，但 API 调用方式和价格都没有查到。质量方面，Wan-S2V 论文称优于 Hunyuan-Avatar 和 OmniHuman，这是作者自报 ([arXiv 2508.18621](https://arxiv.org/html/2508.18621v1))，中文社区没有找到可信的独立横评。

海外的"照片 + 音频"模型已经是 2026 年的主流形态。Kling Avatar v2 和 OmniHuman 是口型最稳的一档，不过结论来自托管商的自测博客：PiAPI 称 Kling 情绪更丰富、OmniHuman 动作更稳 ([PiAPI](https://piapi.ai/en/blogs/omnihuman-1-5-vs-kling-ai-avatar))。InfiniteTalk 最便宜，弱点是侧脸、密集辅音和超过 1 分钟后的色偏 ([InfiniteTalk GitHub](https://github.com/MeiGen-AI/InfiniteTalk))。另一种"两段式"做法更省钱：先用照片模型或真人实拍得到一段老师视频底板，之后每张幻灯片只做重新对口型。LatentSync 托管价约 $0.30/分钟，许可证是 Apache-2.0 ([LatentSync GitHub](https://github.com/bytedance/LatentSync))；sync.so 的模型不接受静态图片 ([sync docs](https://sync.so/docs/models))。所有调研到的"照片 + 音频"模型都没有标注原生透明背景输出。所以决策 9 里"透明 WebM 只支持 Chrome"那条反对理由，换掉 HeyGen 并不能解决：只能把背景烘进 MP4，或者自己抠像。

## 实时：标价之外，利用率决定包月是否划算

海外厂商按会话分钟收费，国内厂商按并发"路"包月，两种计价不能直接比，必须先假设利用率。下表把两类价格都换算到每会话分钟和每节 45 分钟课。包月价按每路每月 1,980 / 5,940 / 10,560 连接分钟折算，分别对应每个上学日 2 节、6 节、8 小时满载（每月 22 个上学日）。

| 方案 | 计费方式 | USD/会话分钟 | CNY/会话分钟 | 一节 45 分钟课 | 口径 | 驱动方式 |
|---|---|---|---|---|---|---|
| anam Professional（现用） | $999/月含 8,000 分钟，超额 $0.11，10 并发 | 0.11（10k–50k 分钟实付 0.112–0.122） | 0.78 | $4.95 / 35 元 | 官方 ([anam pricing](https://anam.ai/pricing)) | 文本（现用），音频直通为 beta |
| anam Enterprise | 起价，100 并发起 | 0.04 | 0.28 | $1.80 / 12.8 元 | 官方"起价"，需洽谈 | 同上 |
| Simli Scale | $249/月含 27,500 分钟，50 并发 | 0.009 | 0.064 | $0.41 / 2.9 元 | 官方 ([Simli](https://www.simli.com/pricing)) | 音频 |
| bitHuman 云端 / 自托管 | credits | 0.04 / 0.02（自托管只算说话秒数） | 0.28 / 0.14 | $1.80 / $0.50（按 25 分钟说话） | 官方 ([bitHuman](https://www.bithuman.ai/pricing)) | 音频 |
| HeyGen LiveAvatar LITE / FULL | 1 / 2 credits/分钟，超额 $0.09–0.095/credit | 0.084–0.089 / 0.174–0.18 | 0.60–0.63 / 1.24–1.28 | $3.8–4.0 / $7.8–8.1 | 官方 credits 价，折算为推算 ([LiveAvatar FAQ](https://docs.liveavatar.com/docs/faq/credits)) | LITE 为音频，自带 LLM/TTS |
| Beyond Presence Speech-to-Video | €349 含 4,000 分钟，超额 €0.0875 | ≈0.10 | ≈0.71 | ≈$4.5 | 官方欧元价 ([bey](https://www.beyondpresence.ai/pricing)) | 音频（推荐走 LiveKit） |
| Synthesia Interactive（只要头像） | 按量 | 0.10 | 0.71 | $4.50 | 官方 ([Synthesia](https://www.synthesia.io/api-pricing)) | 音频（只支持 LiveKit Python） |
| Runway Characters | 每 6 秒 2 credits | 0.20 | 1.42 | $9.0（单次 ≤30 分钟） | 官方 ([Runway help](https://help.runwayml.com/hc/en-us/articles/49557780326163-Runway-Characters)) | — |
| Tavus Business | $975 含 4,000 分钟，超额 $0.26 | ≈0.26 | ≈1.85 | ≈$11.7 | 官方 ([Tavus](https://www.tavus.io/pricing)) | 文本/音频 Echo 模式 |
| D-ID Agents | 套餐 | 0.35–0.56 | 2.5–4.0 | $16–25 | 第三方 | — |
| 阿里 万相 2D 云渲染·音频驱动 | 2,400 元/路/月（日付 = 月价 ÷ 30） | 0.171 / 0.057 / 0.032 | 1.21 / 0.40 / 0.23 | 54.5 / 18.2 / 10.2 元 | 官方月价 ([price-videochat-2d](https://help.aliyun.com/zh/avatar/avatar-application/product-overview/price-videochat-2d))，折算为推算 | 音频 |
| 阿里 万相 2D 云渲染·全链路 | 3,000 元/路/月 | 0.213 / 0.071 / 0.040 | 1.52 / 0.51 / 0.28 | 68.2 / 22.7 / 12.8 元 | 同上 | 内置 ASR+LLM+TTS |
| 腾讯 交互数智人 云渲染 2D | 3,500 元/路/月（年付折合 2,250） | 0.249 / 0.083 / 0.047（年付 0.160 / 0.053 / 0.030） | 1.77 / 0.59 / 0.33 | 79.5 / 26.5 / 14.9 元 | 官方 ([腾讯价格指南](https://cloud.tencent.com/document/product/1240/101944)) | 文本，可接自有 LLM |
| 百度曦灵 云渲染 2D | 2,400 元/路/月 | 与阿里音频驱动相同 | 同左 | 同左 | 官方 ([曦灵](https://xiling.cloud.baidu.com/doc/AI_DH/s/Vlysgbz88)) | 未确认 |
| 讯飞 虚拟人交互 | 约 28,000 元/路/年 | 0.166 / 0.055 / 0.031 | 1.18 / 0.39 / 0.22 | 53 / 17.7 / 9.9 元 | 第三方转载 ([yiban](https://ad.yiban.io/operate/tool/1201)) | 文本或音频 |

这张表有三点结论。第一，**包月不等于便宜**。阿里音频驱动每路每月 2,400 元，约合 $338。要比 anam Professional 便宜，每路每个上学日要跑 3.1 节课；要比 anam 企业价 $0.04 便宜，每天要跑 8.5 节，一个上学日排不下（推算）。阿里唯一按分钟计费的选项是 2D 端渲染，每分钟 0.06 元，但它只支持 iOS 和 Android SDK，网页用不了 ([price-videochat-2d](https://help.aliyun.com/zh/avatar/avatar-application/product-overview/price-videochat-2d))。第二，**连接分钟和讲话分钟相差约 1.8 倍**。现在的代码让会话贯穿整节课，测验和练习时间也在计费。只有 bitHuman 自托管明确"只计角色说话的秒数" ([bitHuman](https://www.bithuman.ai/pricing))，其他厂商按连接计费时，在测验场景主动断开会话是一个省钱杠杆，代价是要再承受一次首帧延迟。第三，对音频驱动的厂商来说，**TTS 不是主要成本**：ElevenLabs Flash / v4 Turbo 每讲话分钟 $0.036–0.040，折到每会话分钟只有 $0.015–0.025 ([ElevenLabs API Pricing](https://elevenlabs.io/pricing/api))。课件旁白还能直接复用预渲染好的音频。

延迟方面目前**没有中立的第三方基准**，这是实时档最大的空白。anam 在 2026-10-16 发布过自测：60 人、960 场对话，各家用默认全管线，回复延迟 p50/p95 为 anam 1.24/1.84 秒、HeyGen 1.82/2.52、Tavus 1.86/3.62、LemonSlice 2.10/3.06；连接首帧（TTFF）p50 为 anam 1.42 秒、HeyGen 3.66、Tavus 5.00、LemonSlice 9.72。但在共享 LiveKit 管线、只换头像的对照中，anam（2.12 秒）和 Synthesia（2.20 秒）没有显著差异，anam 自己也承认存在利益冲突 ([anam latency benchmark](https://anam.ai/tools/latency-benchmark))。LemonSlice 的自测则称自己与 Simli、LiveAvatar 无显著差异，比 anam Cara-3 快 ([LemonSlice blog](https://lemonslice.com/blog/lemonslice-flash))。由此推断：端到端延迟主要由 STT、LLM、TTS 决定，头像层在共享管线下只差 0.1–0.5 秒；首帧差距（1.4 秒对 5–10 秒）才直接影响"翻到这一页就开讲"的体验。国内厂商只有营销口径，例如火山称延迟 500ms、口型准确率 98.5%，来自搜索摘要 ([火山虚拟数字人](https://www.volcengine.com/product/avatar))；阿里所有渠道都没有给出首帧或端到端数据。还要注意区域：anam 只有 EU 和 US 两个引擎区域，区域选择限 Enterprise 套餐 ([anam regions](https://anam.ai/personas/session/regions))。目前没有任何从雅加达或中国发起的实测。

阿里实时线的细节决定了它目前只能当备选。万相数字人 2D 实时对话分"云渲染"和"端渲染"，集成方式分"全链路"（ASR+LLM+TTS+驱动一体）和"音频驱动"（已有语音链路的客户只买口型驱动）([2D 实时对话](https://help.aliyun.com/zh/avatar/avatar-application/user-guide/avatar-2dchat/))。音频驱动模式理论上可以接我们自己的 LLM 和 ElevenLabs，但文档没有说明 Web SDK 是不是 WebRTC，也没说能否接收外部 PCM 流，全链路模式能否替换成第三方 LLM 同样没写。试用是 7 天、最多 10 个 2D 项目，只能在控制台里对话，要调 SDK 必须购买。按日付价（月价 ÷ 30）买一路音频驱动只要 80 元/天，实测门槛很低。IMS 的 AI 实时互动工作流支持打断和自研模型，但数字人节点只能接"阿里灵境"（要提工单）或第三方"相芯"；"通义星尘"数字人已于 2025-08-31 下线 ([数字人集成](https://help.aliyun.com/zh/ims/user-guide/digital-human-integration))。千问 Omni Realtime 适合做语音对话本身：技术报告称支持低延迟流式，但没有公布延迟数字 ([Qwen3.5-Omni report](https://arxiv.org/html/2604.15804v2))。另外，平台文档的印尼语一栏可能只标了"Text"（表头没抓全，此判断不确定）([qianwenai s2s](https://docs.platform.qianwenai.com/developer-guides/speech/s2s-models))。

## 按硬性要求筛选：能原样替换 anam 的现成选项只有两三家

仓库里的 `LectureAvatar` 单例实际上就是一个隐式接口。对外暴露 `connect`、`speak(text) → ended|interrupted|timeout`、`interrupt` 等方法；服务端只把 `sessionToken` 发给浏览器；Anam 自带的 LLM 被关掉（`CUSTOMER_CLIENT_V1`）；每句话以 `endOfSpeech` 作为结束信号 ([lecture-avatar.ts](https://github.com/Kunbyte-AI/maic-avatar/blob/deploy/prod-diagram-fix/lib/avatar/lecture-avatar.ts#L46-L387))。从代码反推，实时档的硬性要求有七条：浏览器端 WebRTC、服务端签发令牌、文本驱动（自有 LLM）或音频驱动、可靠的"说完"和打断、会话 ≥45 分钟或能续接、en/id/zh 语音、用照片建分身。下表中，✅ 表示已确认，⚠️ 表示有条件满足，❓ 表示未查到，❌ 表示不满足。

| 厂商 | 浏览器 WebRTC / Web SDK | 服务端令牌 | 文本或音频驱动 | 说完事件 + 打断 | ≥45 分钟 / 续接 | en/id/zh 语音 | 照片建分身 |
|---|---|---|---|---|---|---|---|
| anam（现用） | ✅ | ✅ | ✅ 文本；音频直通 beta ([cookbook](https://anam.ai/cookbook/python-audio-passthrough-tts)) | ✅（打断后不触发中断事件，代码已绕过） | ⚠️ 代码设 30 分钟；定价页称 Growth 及以上单次 2 小时；已有重连 | ✅ id/zh 靠导入 ElevenLabs 音色 | ✅ 单张照片，约 80 秒 |
| Simli | ✅ JS SDK | ✅ 后端签发 session token ([Simli SDKs](https://docs.simli.com/simli-sdks)) | ✅ 音频（16kHz PCM） | ⚠️ 由我方管线控制，清空缓冲的接口未核实 | ❓ | ✅ 外接 ElevenLabs | ✅ 上传图片（流程细节未核实） |
| HeyGen LiveAvatar LITE | ✅ JS SDK | ❓ | ✅ 音频，自带 LLM/TTS ([LITE](https://docs.liveavatar.com/docs/lite-mode/overview)) | ❓ | ❓ | ✅ 外接 | ❓ |
| Beyond Presence | ⚠️ 官方推荐 LiveKit 插件 ([bey](https://docs.bey.dev/integrations/speech-to-video.md)) | ✅（LiveKit） | ✅ 音频 | ⚠️ 我方管线 | ❓ | ✅ 外接 | ❓ |
| Synthesia Interactive | ⚠️ 只有 LiveKit Python 插件 | ✅（LiveKit） | ✅ 音频 | ⚠️ | ❓ | ✅ 外接 | ❓ |
| bitHuman | ⚠️ LiveKit / Pipecat | ✅ | ✅ 音频 | ⚠️ | ✅ 自托管不限会话数 | ✅ 外接 | ✅ Essence 2 $5，几分钟 |
| Tavus | ✅ Daily WebRTC | ❓ | ✅ Text/Audio Echo ([modes](https://docs.tavus.io/sections/conversational-video-interface/modes-and-layers)) | ❓ | ❓ | ✅ | ❌ 需要视频 + 本人口述授权，训练 3–5 小时 |
| Runway Characters | ❓ | ❓ | ❓ | ❓ | ❌ 单次 ≤30 分钟 | ❓ | ✅ 单图 |
| 阿里 万相 2D 云渲染 | ✅ Web SDK（协议未知） | ❓ | ⚠️ 有音频驱动模式；全链路能否换 LLM 未知 | ❓ | ❓（包月不按时长计） | ⚠️ 音频驱动可外接；内置语种未知 | ✅ 图片训练版 39 元，约 0.5 小时 |
| 阿里 IMS 工作流 | ⚠️ 走阿里 RTC | ❓ | ✅ 自研模型、TTS 标准接口 | ✅ 打断 | ❓ | ⚠️ | ⚠️ 只能用灵境（工单）或相芯 |
| 腾讯 交互数智人 | ✅ 云渲染 H5 SDK（协议未写）([H5 SDK](https://cloud.tencent.cn/document/product/1240/104050)) | ❓ | ✅ 文本驱动，"支持客户侧自行开发接入其他大模型" | ⚠️ 端渲染有 `IVH.stop()`，云渲染未写 | ❓ | ✅ 语种表含 id-ID ([语种列表](https://www.tencentcloud.com/zh/document/product/1211/67803)) | ✅ 照片 19.9 元 |
| 百度曦灵 | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ✅ 照片 20 元 |
| 火山 veRTC + 数字人 | ⚠️ RTC 方案 | ❓ | ⚠️ 可用 UpdateVoiceChat 注入文本 ([火山 RTC](https://www.volcengine.com/docs/6348/1568689))；外部 TTS 未知 | ❓ | ❓ | ❓ | ❓ |
| 讯飞 | ✅ 服务端 API 输出视频流，适用 Web/H5 ([讯飞](https://virtual-man.xfyun.cn/interaction)) | ❓ | ✅ 文本或音频 | ✅ 支持打断 | ❓ | ❓ | ❓ |

预渲染档的硬性要求是四条：能用我方音频驱动、输出能在 Safari 和 Android 播放、有书面的缓存和再分发权利、下载链接过期前我们能转存。

| 方案 | 我方音频驱动 | 输出与播放 | 缓存 / 再分发权利 | 吞吐与地域 |
|---|---|---|---|---|
| 阿里 wan2.2-s2v / wan2.7-i2v / VideoRetalk | ✅ mp3/wav | ❓ 格式未写（推测为 MP4）；无透明背景 | ❓ 条款未查到；结果保留 24 小时；s2v 要先过 detect 合规检测 | s2v 和 VideoRetalk 并发 1、仅北京；wan2.7 有新加坡 |
| 阿里 万相数字人视频创作 | ✅ 上传音频 | ✅ `ONLY_AVATAR` 输出透明 WebM（官方文档 + 样片 ALPHA_MODE=1）；Safari 能否播放透明 WebM 需验证 | ⚠️ API 可关水印，控制台要会员；授权条款未查到 | API 按量 0.1 元/秒；渲染速度待实测 |
| 火山克隆 / 百度 / 腾讯播报 | 火山 ✅；百度、腾讯 ❓ | ❓ | ❓ | 国内地域 |
| Kling / OmniHuman / InfiniteTalk（fal、WaveSpeed） | ✅ | ❓（推测为 MP4）；无透明背景 | ✅ fal 页面标注商用；WaveSpeed 称取决于模型许可证 | 海外；InfiniteTalk 可自部署 |
| HeyGen | ✅ `audio_asset_id` | ⚠️ 透明 WebM 只能在 Chrome 播放 | ❓ | 约 10 倍实时 |
| Anam 离线 Avatar Videos | ⚠️ 输入文本，由 anam 合成语音（可选导入的 ElevenLabs 音色） | ✅ MP4 | ✅ 邮件书面确认可自存、无限回放 | 链接 1 小时过期；无亚太区域，但预渲染不受影响 |
| LatentSync / MuseTalk 自部署 | ✅ | ✅ 自控 | ✅ Apache-2.0 / MIT | 自控；需要视频底板 |

筛完以后，**浏览器 SDK + 服务端令牌 + 音频驱动 + 照片建分身**四项都已确认的只有 Simli；HeyGen LiveAvatar LITE 有 JS SDK，令牌和分身流程还没查清。其他海外厂商大多以 LiveKit/Pipecat 服务端插件为主。不过反过来看，如果团队愿意加一个 LiveKit Agents 服务端，就能用同一套代码在 anam、Simli、bey、Synthesia、LemonSlice、Keyframe、Tavus、LiveAvatar 之间随意切换；LiveKit 现在支持 16 家头像插件 ([LiveKit avatar models](https://docs.livekit.io/agents/models/avatar/))，这也是做人工 A/B 测试成本最低的方式。国内厂商中，腾讯是唯一在官方文档里同时写明"文本驱动 + 自带 LLM"和 id-ID 语种的；阿里的 Web SDK 最接近现有架构，但关键接口都还是 ❓。

另有几家已经停服或存在长期风险，选型时要排除或打折扣。**Hedra Realtime** 已于 2026-04-15 下线，LiveKit 插件失效 ([LiveKit Hedra](https://docs.livekit.io/agents/models/avatar/plugins/hedra.md))。**Soul Machines** 2026-02-05 进入破产接管 ([NBR](https://www.nbr.co.nz/tech/soul-machines-in-receivership))，9 月据报被 AppDirect 收购（单一来源）。**阿里 EMO（emo-v1）和 LivePortrait** 据下线列表搜索摘要已于 2026-10-10 下线，animate-anyone-gen2 由 wan2.7-r2v 替代；官方页面没有直接列出模型名，但相关文档已跳转或返回 404 ([模型下线](https://help.aliyun.com/zh/model-studio/model-depreciation)；[公告 118344](https://www.aliyun.com/notice/118344))。**万相数字人**的旧"虚拟数字人"文档目录标注"文档停止维护"，最后更新于 2025-08-11；产品以"通义万相数字人"的名字继续销售 ([产品概览](https://help.aliyun.com/zh/avatar/avatar-application/product-overview/))，"停止维护"是否预示产品线收缩，需要商务确认。fal 上的 InfiniteTalk 端点已标记 deprecated（WaveSpeed 仍在售）([fal infinitalk](https://fal.ai/models/fal-ai/infinitalk))。ElevenLabs Turbo v2.5 已弃用，由 Flash v2.5 替代 ([ElevenLabs models](https://elevenlabs.io/docs/overview/models))。

## 老师分身：从一张照片 80 秒到视频训练 10 天

在"用真实老师照片创建分身"这件事上，各家门槛差别很大。整体分成三档。**按次传照片、不用训练**的有百炼 s2v / wan2.7、Kling、OmniHuman、InfiniteTalk，上手最快，肖像同意的合规责任完全在我方。**单张照片上传后几十秒到半小时出分身**的有 anam、阿里图片训练版、腾讯和百度的照片数字人、bitHuman。**需要老师录视频甚至口述授权**的有 Tavus、HeyGen 分身、阿里高精度版、腾讯和百度小样本、火山克隆、VideoRetalk。

| 方案 | 素材 | 耗时 | 费用 | 来源 |
|---|---|---|---|---|
| anam one-shot | 方形照片 ≥1152px、≤4.5MB，人脸清晰、手不入镜；要过审核 | 同步约 80 秒 | 所有套餐不限数量 | [anam custom avatars](https://anam.ai/docs/personas/avatars/custom-avatars)；[custom/route.ts](https://github.com/Kunbyte-AI/maic-avatar/blob/deploy/prod-diagram-fix/app/api/avatar/custom/route.ts#L7-L24) |
| 阿里 百炼 s2v / wan2.7 | 每次调用传一张照片（s2v 要先过 detect，0.004 元/张） | 不用训练 | 无 | [wan-s2v overview](https://help.aliyun.com/zh/model-studio/wan-s2v-overview/) |
| 阿里 万相 图片训练版 | 单人站姿、双肩完整、正脸偏转 <15°、9:16，不戴帽子 | 约 0.5 小时 | 控制台 390 积分；API 39 元；免训练版 100 积分 | [2D 图片形象定制](https://help.aliyun.com/zh/avatar/avatar-application/user-guide/customized-digital-2d-image-avatar/) |
| 阿里 万相 小样本 / 高精度 | 10 秒–2 分钟视频 / 5 分钟视频 | 未查到 | 小样本未查到；高精度 39,990 积分（约 3,400–4,000 元，推算） | [会员与积分](https://help.aliyun.com/zh/avatar/avatar-application/product-overview/avatar-membership-subscriptions-and-credits-packages) |
| 阿里 VideoRetalk | 老师正面讲课视频 | 不用训练 | 无 | [videoretalk](https://help.aliyun.com/zh/model-studio/videoretalk) |
| 腾讯 | 照片；小样本需 3 分钟口播 + 100 句语音（2023 年数据） | 小样本 24 小时内交付（2023 年数据） | 照片 19.9 元；小样本 2,500 元 + 9.9 元/月；高精 20,000 元 | [腾讯价格指南](https://cloud.tencent.com/document/product/1240/101944)；[界面新闻](https://www.jiemian.com/article/9312569.html) |
| 百度曦灵 | 照片 / 视频 | 未查到 | 照片 20 元；小样本 1,000 元；专属口型 2,000 元 | [曦灵价格](https://xiling.cloud.baidu.com/doc/AI_DH/s/Vlysgbz88) |
| 火山 克隆数字人 | 一段单人视频 | 未查到 | 2,599 元/次 | [火山智能视觉](https://docs.volcengine.com/docs/Intelligentvisionservices/Abilitytointroduce-19?lang=zh) |
| bitHuman | 照片 | Essence 2 几分钟 | $5（Expression 2 $20） | [bitHuman](https://www.bithuman.ai/pricing) |
| Tavus Phoenix-4 | 30 秒说话 + 30 秒倾听视频 + 本人口述授权 | 3–5 小时 | Business 含 15 个 | [Tavus replica training](https://docs.tavus.io/sections/replica/replica-training) |
| Synthesia Studio 头像 | 视频 | 最长 10 天 | $1,000/年 | [Synthesia pricing](https://www.synthesia.io/pricing) |

用于"像本人"的分身，难点在授权，技术上不难。仓库的合规要求写明：教师照片和声音模型存放在供应商处，同意书由业务方签；渲染出的 MP4 能否存到客户云和课堂主机上回放，必须拿到书面确认 ([tech-stack-and-cost.md §9, §12](https://github.com/Kunbyte-AI/maic-avatar/blob/deploy/prod-diagram-fix/dev-and-design/tech-stack-and-cost.md))。阿里图片训练版的页面没有提到任何授权书要求；只有 Tavus 把本人口述授权写进了流程。国内厂商定制真人形象，通常要本人授权和身份核验（推断，各家材料清单都没查到）。还有一个容易忽略的约束：wan2.2-s2v、VideoRetalk、CosyVoice v3.5 都只在北京地域。老师的照片和讲课音频会因此出境到中国大陆，这与"公立学校阶段学生数据必须在印尼境内"并不直接冲突（这些是教师素材，不是学生数据），但实时问答会把学生的问题内容送到供应商，要单独评估。

## 推荐组合与一所学校的月账

下面的组合都按同一用量计算。预渲染以"每节课每种语言"计，A-roll 按 25% 出镜约 6.25 分钟视频，全程出镜约 25 分钟。实时档设两个学校场景：**试点校**高峰同时 5 个班投屏，每班每个上学日 2 节 AI 课，每月 220 节；**规模校**高峰 20 个班，每班每天 6 节，每月 2,640 节。投屏时只有老师端拉一路流，所以并发等于同时上课的班级数 ([live-class/bridge.ts](https://github.com/Kunbyte-AI/maic-avatar/blob/deploy/prod-diagram-fix/lib/live-class/bridge.ts#L1-L15))。音频驱动方案的旁白复用预渲染音频，只给问答算实时 TTS，按每节课约 3 分钟老师回答、$0.11 估（假设）。以上全部是推算。

| 组合 | 单节课成本 | 示例月成本 | 适用与风险 |
|---|---|---|---|
| **P1 ElevenLabs v4 Turbo 整课旁白，不出数字人视频**（决策 9 现状） | 英 $0.75 / 印尼 $0.82 / 中 $0.21（5.3 / 5.8 / 1.5 元） | 80 节目录一次性约 $60（426 元）；每月新增 100 节约 $78（约 550 元）；若每月 6,000 节生成课全部预渲染，约 $4,500–4,900（3.2–3.5 万元） | 默认档；兼容所有浏览器；音频每次观看约 12 MB，每校每月约 3 TB 流量（推算） |
| **P2 P1 + 照片生成的 25% 出镜**（Kling v2 Std；阿里备选 wan2.7-i2v 新加坡 720P） | Kling $21.9（155 元）；wan2.7 $38.3（272 元）；全程出镜 $85 / $151 | 80 节目录 A-roll $1,750 / $3,060（1.2 / 2.2 万元）；每月新增 100 节 $2,190 / $3,830 | 只适合精品课和介绍视频；每段 ≤15–60 秒，正好按句子切；无透明背景 |
| **P3 P1 + 老师真人视频底板对口型**（阿里 VideoRetalk；备选火山克隆、LatentSync） | VideoRetalk 35.5 元（$5.0）；全程 125.5 元（$17.7）；火山 43 元，另加 2,599 元/老师 | 80 节目录 A-roll 2,840 元（$400）；每月新增 100 节 3,550 元（$500） | 每分钟最便宜；要老师录 30–60 秒正面视频；VideoRetalk 仅北京、并发 1 |
| **R1 维持 anam（文本驱动）+ 导入的 ElevenLabs 音色**，洽谈企业价 | 试点 $5.49（39 元，Professional）；规模 $1.80（12.8 元，Enterprise $0.04） | 试点 $1,208（8,580 元）；规模 $4,752（3.37 万元）+ 平台费（未知）；规模校 20 并发超出 Professional 的 10 并发 | 零改造；首帧在自测中最快；区域只有 EU/US |
| **R2 Simli Trinity + ElevenLabs**（旁白用 P1 音频，问答实时调 Flash / v4 Turbo） | 试点 $1.24（8.8 元）；规模 $0.52（3.7 元） | 试点 $273（1,940 元）；规模 $1,361（9,660 元） | 最便宜、最接近原样替换；口碑认为待机动作偏弱，要盲测 ([meet-cody](https://meet-cody-website-xr0tt.kinsta.page/blog/real-time-ai-avatar-models-compared/)) |
| **R3 阿里万相 2D 云渲染（音频驱动）+ ElevenLabs 或 CosyVoice**；文本驱动的替代是腾讯交互数智人（年付） | 阿里：试点 55.3 元（$7.79）；规模 19.0 元（$2.67）。腾讯：51.1 / 17.0 元 | 阿里：试点 12,170 元（$1,714）；规模 50,060 元（$7,051）；另加 39 元/老师。腾讯：11,250 / 45,000 元 | 中文市场或国内部署的首选验证对象；海外可用性、协议、延迟都待测 |
| 参考：HeyGen LiveAvatar LITE + ElevenLabs | 试点 $3.86；规模 $4.14 | 试点 $850；规模 $10,917 | 加上自带语音后与 anam 持平，不是更便宜；Essential/Business 不限并发，Business 单次会话最长 60 分钟，额外自定义形象每个 $49/月；可作为谈判参照 |

语音组件建议保留 ElevenLabs：它是唯一同时确认 en/id/zh、音色能跨模型使用、并且已经在项目里通过听感检查的选项（印尼语 Citra、Mahaputra，中文 Amy）([personas.ts](https://github.com/Kunbyte-AI/maic-avatar/blob/deploy/prod-diagram-fix/lib/avatar/personas.ts#L34-L48))。要压成本，有两个现成的替代。一是 **MiniMax speech-2.8-turbo**：$60/M 字符，官方 `language_boost` 列出 Indonesian，快速复刻每个音色 $1.5 ([MiniMax pricing](https://platform.minimax.io/docs/pricing/overview))。二是阿里 **CosyVoice**：cosyvoice-v3.5-flash 每万字符 0.8 元，约为 ElevenLabs 的四分之一，官方写明支持印尼语，但只开在北京 ([cosyvoice-v3.5-flash](https://help.aliyun.com/zh/model-studio/cosyvoice-v3-5-flash))。cosyvoice-v3-flash 在中文 TTS 模型列表中写着系统音色和复刻音色都支持印尼语、并有新加坡地域 ([TTS 模型列表](https://help.aliyun.com/zh/model-studio/tts-model))，但国际站页面没有给出语种表，两份调研的结论不一致，要在新加坡控制台核实。上游 OpenMAIC 本来就内置了 qwen-tts、doubao-tts、minimax-tts 等 11 个 TTS 提供方 ([lib/audio/constants.ts](https://github.com/Kunbyte-AI/maic-avatar/blob/deploy/prod-diagram-fix/lib/audio/constants.ts))，换 TTS 的代码成本很低，真正的门槛是印尼语听感。学生端 ASR 不要用阿里 Paraformer，它不支持印尼语 ([paraformer-realtime-v2](https://help.aliyun.com/zh/model-studio/paraformer-realtime-v2))；ElevenLabs Scribe v2 Realtime 是 $0.39/小时 ([ElevenLabs API Pricing](https://elevenlabs.io/pricing/api))，可以和 TTS 统一账单。

这些发现与决策 9 的关系如下。决策 9 定的是预渲染神经语音、不用预渲染数字人视频，目前只预渲染一节课和介绍视频 ([course-content-platform-design.md §11](https://github.com/Kunbyte-AI/maic-avatar/blob/deploy/ma-reports-1103/dev-and-design/course-content-platform-design.md))。本次调研从成本上支持这个决定：视频每分钟比语音贵约 4–250 倍（主流照片生成方案在 45 倍以上），按生成课的规模每月要多付几万到几十万美元；而且第一节提到的 Safari 问题，换掉 HeyGen 也无法根本解决。有两点值得注意。第一，整套 80 节课的语音全量预渲染只要约 $60，所以限制只做一节课的因素应该在质检和发布流程，不在成本。第二，音频驱动的实时厂商（Simli、LiveAvatar LITE、bey，以及阿里的音频驱动模式）能直接吃已经预渲染好的旁白音频。现在引擎把"预生成音频"和"实时数字人"当成互斥（[engine.ts#L708-L737](https://github.com/Kunbyte-AI/maic-avatar/blob/deploy/prod-diagram-fix/lib/playback/engine.ts#L708-L737)），换成音频驱动的厂商后，这里就变成接口：录音模式和实时模式用同一把声音，只有问答需要实时 TTS。这正好满足仓库要求的"同一个分身、同一把声音"。决策 9 的投入因此不会浪费，反而是 R2、R3 两条路线的前置条件。

## 待人工验证的关键问题

| # | 问题 | 为什么关键 | 建议的验证方式 | 涉及对象 |
|---|---|---|---|---|
| 1 | 实时首帧（TTFF）和问答端到端延迟，从雅加达和国内网络各测一次 | 唯一的对比数据是 anam 自测；代码里每句最多等 12 秒（[engine.ts#L65](https://github.com/Kunbyte-AI/maic-avatar/blob/deploy/prod-diagram-fix/lib/playback/engine.ts#L65)）；anam 只有 EU/US 区域 | 冷启动 20 次记 TTFF；30 轮以上问答算 p50/p95；加上 1.5Mbps 和 500ms 抖动的弱网测试 | anam、Simli、LiveAvatar LITE、阿里 2D 云渲染、腾讯 |
| 2 | 印尼语（以及中文、中英混读）的口型 | 没有任何厂商发布印尼语评测；InfiniteTalk、EchoMimic 用的是中文 wav2vec2 编码器 | 用 4 段 ElevenLabs MP3（EN/ID × 15 秒/45 秒）配同一张老师照片，重点看 p/b/m 闭唇音、快语速、45 秒末尾的身份漂移和牙齿伪影 | 所有预渲染候选和音频驱动实时候选 |
| 3 | 音频驱动模式下的"说完"和打断 | 引擎依赖 `speak → ended/interrupted`，打断后状态必须干净 | 插话后 300ms 内闭嘴；连续打断 10 次看有没有残音或状态错乱 | Simli、LiveAvatar LITE、阿里音频驱动 |
| 4 | ~~anam 的 30 分钟是套餐限制还是代码设置~~ **已解决（11-05）：是代码设置，Growth 及以上无上限** | 定价页称 Growth 及以上单次会话 2 小时；代码把 `maxSessionLengthSeconds` 设成 1,800 来控制计费（[session/route.ts](https://github.com/Kunbyte-AI/maic-avatar/blob/deploy/prod-diagram-fix/app/api/avatar/session/route.ts#L33-L34)） | 查当前账户套餐，在测试环境设成 2,700 跑满一节课 | anam |
| 5 | 阿里万相 Web SDK 的真实能力 | 决定 R3 能否成立 | 7 天试用加日付 80 元买一路：确认是否 WebRTC、能否接收外部 PCM、全链路能否接自有 LLM、印尼能否访问、国际站有没有这个产品、"停止维护"的含义 | 阿里（客服 4008013260） |
| 6 | 需要商务洽谈的价格 | 表中多个关键数字是"起价"或未公开 | anam 企业价（$0.04 起）、平台费和 APAC 区域；anam 离线渲染单价和回放权；阿里 3D 实时、小样本视频版价格、s2v 提高并发；腾讯和百度的试用路数；讯飞官方年包；火山数字人在 RTC 方案里的单价；万相视频创作的 API 价 | anam、阿里、腾讯、百度、讯飞、火山 |
| 7 | 预渲染吞吐和实际渲染倍率 | s2v 和 VideoRetalk 并发 1，大多数商业 API 不公布速度 | 记录提交到完成的墙钟时间，换算成"渲染 1 分钟需要几分钟"；以 80 节课 A-roll 约 500 分钟为基准估算总工期 | 阿里三模型、Kling、OmniHuman、InfiniteTalk |
| 8 | 国内播报 API 能否吃外部 MP3 | 决定百度（3 元/分钟）、腾讯（3.33 元/分钟）能否沿用 ElevenLabs 的声音 | 用 19.9–20 元的照片数字人加时长包测试上传音频 | 百度、腾讯 |
| 9 | 输出格式、背景和再分发权利 | Safari/Android 播放、课堂主机离线播放都依赖这些 | 在 Safari 和 Android Chrome 播放样片；检查编码和背景是否便于抠像；要供应商书面确认缓存和再分发权利 | 全部预渲染候选 |
| 10 | 计费口径：连接分钟还是讲话分钟 | 两者相差约 1.8 倍 | 在账单里对照会话日志 | Simli、LiveAvatar、bey、anam |
| 11 | TTS 印尼语听感与地域 | 阿里 CosyVoice 新加坡地域是否支持印尼语，两份资料矛盾；ElevenLabs v4 Turbo 会忽略语速设置 | 用同一段勾股定理讲稿（EN/ID，各约 45 秒）盲听 A/B，包括公式读法 | ElevenLabs、MiniMax、CosyVoice、Fun-Realtime-TTS |
| 12 | 老师肖像和声音授权，以及数据出境 | 北京地域模型会让教师素材出境；实时问答会让学生内容进入供应商 | 收集各家授权材料要求；法务确认同意书模板 | 阿里、腾讯、百度、火山、Tavus |

## 结论

这次对比改变了一个前提：团队原来把"数字人贵"当成一个整体问题，其实它分成两笔性质完全不同的账。预渲染视频按分钟线性增长，而且是生成课数量的倍数，再便宜的供应商也没法让它进入基础套餐，只能限定在少量精品目录上。实时数字人的单价已经被只做渲染的厂商压到每分钟 1 美分到 10 美分，真正的成本变量变成了连接时长、并发路数和利用率。也就是说，决定账单的是会话怎么开、什么时候断开，选哪家反而是次要的。国内包月产品只在高利用率的投屏场景里有意义，对按需开启的学生端并不划算。

由此得出的行动顺序是：先把决策 9 的预渲染音频铺满全部 80 节课，成本可以忽略；再把引擎里"录音和实时互斥"的逻辑改成"录音驱动实时头像"，为音频驱动厂商留好接口；然后用 1–2 周、几百美元做三组并行实测，分别是 anam 企业报价、Simli 和 LiveAvatar LITE 的音频驱动接入、阿里或腾讯的一路日付试用。拿到雅加达实测延迟和印尼语口型的盲测结果后，再决定实时档的主供应商。在此之前，任何供应商切换都只是价格表上的推演。
