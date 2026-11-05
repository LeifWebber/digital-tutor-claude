# 语音 TTS 与 ASR 选型：ElevenLabs 与中外替代方案对比（截至 2026-11-04）

> **换算假设**（全文统一）：
> - 每分钟语音的字符数：英语约 **900 字符/分钟**，印尼语约 **1000 字符/分钟**（印尼语单词更长、语速相近，所以多算约 10%）。中文没有算（约 250–300 汉字/分钟，按字计费时每分钟成本会低很多）。
> - 汇率按 **1 USD ≈ 7.0 CNY** 计。阿里云自己的换算并不一致：新加坡 0.954101 CNY 标为 $0.13（≈7.34），北京 1 CNY 标为 $0.143353（≈6.98）。
> - 每分钟成本只算 TTS 合成本身，不含 LLM、数字人渲染、网络和并发费用。
> - 标注"（第三方）"的数据来自聚合站或博客，没有在官方页核实。官方页抓取时部分价格被遮挡（Azure）或没能抓到（Google、阿里云总价目表的 TTS 段），这些都在 Gaps 里注明了。

---

## 1. ElevenLabs（现用方案）：API 价格、档位、印尼语、延迟、Agents 每分钟价格

### Takeaway
ElevenLabs 已经推出 **v4 / v4 Turbo**。按官方 API 价：低延迟模型（Flash v2.5 / v4 Turbo / v3 Conversational）是 **$0.04/1k 字符**，约 **英语 $0.036/分钟、印尼语 $0.040/分钟**；高质量模型（v4 / v3 / Multilingual v2）是 **$0.08/1k**，约 $0.072–0.080/分钟。所有主力模型都支持印尼语。订阅档位本质上是按同一单价预付，买大档不会降低每字符单价。

### Cited Findings
- 官方 API 定价页（2026-11 抓取）：v4 $0.08/1k 字符；**v4 Turbo $0.04/1k，约 100ms**；v3 $0.08/1k；**v3 Conversational $0.04/1k，约 280ms**；v2 Multilingual $0.08/1k；**Flash / Turbo $0.04/1k，约 75ms**。页面注明 API 按美元计费，不按 credits。— [ElevenLabs API Pricing](https://elevenlabs.io/pricing/api)
- 档位与含量（按表格顺序推断对应档位）：Free 1 万字符（$0.08 档模型）/ 2 万（$0.04 档）；Starter $6/月，7.5 万 / 15 万；Creator $22/月，27.5 万 / 55 万；**Pro $99/月，123.8 万 / 247.5 万**；Scale $299/月，373.8 万 / 747.5 万；Business $990/月，1237.5 万 / 2475 万。换算下来每档都等于 $0.04 或 $0.08/1k，大档没有单价折扣。— [ElevenLabs API Pricing](https://elevenlabs.io/pricing/api)
- **价格冲突**：Cartesia 写的对比文给出 Flash/Turbo $0.05/1k、Multilingual v2/v3 $0.10/1k，可能是旧价，也可能是竞品引用有误。以官方页 $0.04/$0.08 为准。— [Cartesia: ElevenLabs pricing 2026](https://www.cartesia.ai/learn/elevenlabs-pricing)
- 模型文档：**Flash v2.5 支持 32 种语言（含印尼语 id），中位延迟约 100ms（不含应用和网络），单次 4 万字符**，官方推荐用于实时语音 Agent；**v4 Turbo 支持 90+ 语言（含印尼语），中位约 100ms**，推荐给 Agents Platform 用来获得"最有表现力"的效果；v3 Conversational 支持 70+ 语言，约 165ms（与定价页的 280ms 不一致）；Multilingual v2 支持 29 种语言，含印尼语，延迟和成本都高于 Flash；**Turbo v2.5 已弃用**，由 Flash v2.5 替代。v3 和 v3 Conversational 被标为上一代。— [ElevenLabs Models docs](https://elevenlabs.io/docs/overview/models)
- Agents（原 Conversational AI）：**Speech Engine $0.08/分钟**，突发价 $0.16/分钟。各档含 15 / 75 / 275 / 1,238 / 3,738 / 12,375 分钟，并发 4 / 6 / 10 / 20 / 30 / 40。**Realtime v1 Mini**（端到端语音模型）$0.08/连接音频分钟，另加 token 费（输入 $0.20/M，输出 $6/M），首音 620ms；**Realtime v1 Max** $0.08/分钟，另加输入 $1.80/M、输出 $9/M，首音 570ms。— [ElevenLabs API Pricing](https://elevenlabs.io/pricing/api)
- 第三方说法：Agents 按通话分钟 $0.08 计费，LLM 和电话另计。— [Cartesia: ElevenLabs pricing 2026](https://www.cartesia.ai/learn/elevenlabs-pricing)

### Inferences
- 数字人老师场景中，老师大约只有 40–60% 的会话时间在说话。按 Flash/v4 Turbo 算，**每会话分钟的 TTS 成本约 $0.015–0.025**，远低于 anam 数字人的 $0.11–0.16/分钟，所以 TTS 不是主要成本项。
- 如果要换模型，优先试 **v4 Turbo**：价格与 Flash 相同，语言更多（90+），表现力更强。

### Gaps
- 定价页没有给 v4 / v3 / Multilingual v2 的延迟数字，也没有印尼语专项的质量或延迟评测。
- 定价表没有档位名标签，档位与行的对应关系是按顺序推断的。

---

## 2. 阿里云百炼：CosyVoice、Qwen-TTS、Fun-Realtime-TTS、Omni Realtime、声音复刻

### Takeaway
阿里系 TTS 单价约为 ElevenLabs 的 **1/3 到 1/4**：qwen3-tts-flash-realtime 国际版 $0.13/万字符，约 **$0.012–0.013/分钟**；cosyvoice-v3.5-flash 0.8 元/万字符，约 $0.010–0.011/分钟。**Fun-Realtime-TTS 在 2026-06 登上 Artificial Analysis 榜首**（Elo 1219，$27.59/M 字符）。不过**能明确确认支持印尼语的只有 cosyvoice-v3.5-plus / v3.5-flash，而且这两款只在北京地域提供**；新加坡地域的模型都没有确认印尼语。百炼已上线 qwen-audio-3.1-tts-plus/flash 这一新代模型，但没查到价格。

### Cited Findings
- 百炼模型列表（2026-11）里，TTS 主推 **qwen-audio-3.1-tts-plus / qwen-audio-3.1-tts-flash**（实时和非实时都支持，适用场景含"虚拟人"）；语音到语音有 qwen-audio-3.1-realtime-plus/flash、qwen3.5-omni-plus、qwen3.8-omni-flash-realtime；ASR 有 qwen-audio-3.1-asr-flash 系列。页面没有价格。— [百炼 模型列表](https://help.aliyun.com/zh/model-studio/models)
- 国际站（新加坡）可用的 TTS：qwen-audio-3.1/3.0-tts-plus/flash、cosyvoice-v3-plus、cosyvoice-v3-flash、qwen3-tts-flash-realtime。页面没有给完整语种表，新加坡地域的模型也**没有确认支持印尼语**。印尼语只出现在 cosyvoice-v3.5-plus/flash（北京）的指令语种中，列表为"中、英、法、德、日、韩、俄、葡、泰、印尼、越"。支持流式（WebSocket）和声音复刻，复刻音色只能用于创建它时指定的目标模型。— [Alibaba Cloud: Text-to-speech](https://www.alibabacloud.com/help/en/model-studio/text-to-speech)
- **qwen3-tts-flash-realtime**：新加坡 **$0.13/万字符**，北京 $0.143353/万字符；只按输入字符计费，输出音频不收费；RPM 180；页面没有列具体语种和延迟数字。— [qwen3-tts-flash-realtime 模型页](https://www.alibabacloud.com/help/en/model-studio/qwen3-tts-flash-realtime)
- 同系列其他型号：qwen3-tts-instruct-flash-realtime 新加坡 $0.143/万字符，离线 qwen3-tts-flash 新加坡 $0.10/万字符；新账户有 1 万字符免费额度（90 天）。— [Alibaba Cloud model pricing](https://www.alibabacloud.com/help/en/model-studio/model-pricing)；[qwen3-tts-flash](https://www.alibabacloud.com/help/en/model-studio/qwen3-tts-flash)
- CosyVoice 原价（元/万字符）：**cosyvoice-v3-plus 北京 2 元 / 新加坡 1.9082 元**（主打复刻，音质和相似度更好）；**cosyvoice-v3-flash 北京 1 元 / 新加坡 0.9541 元**；**cosyvoice-v3.5-plus 北京 1.5 元**；**cosyvoice-v3.5-flash 北京 0.8 元**。— [cosyvoice-v3-plus](https://help.aliyun.com/zh/model-studio/cosyvoice-v3-plus)；[cosyvoice-v3-flash](https://help.aliyun.com/zh/model-studio/cosyvoice-v3-flash)；[cosyvoice-v3.5-plus](https://help.aliyun.com/zh/model-studio/cosyvoice-v3-5-plus)；[cosyvoice-v3.5-flash](https://help.aliyun.com/zh/model-studio/cosyvoice-v3-5-flash)
- **cosyvoice-v3.5-flash** 原文写明支持"中、英、德、法、俄、日、韩、葡、泰、印尼、越南"的实时合成，首包延迟"较之前版本大幅减少"（没有给数字）；价格只列北京地域 0.8 元/万字符，没有单列复刻或声音设计费用。— [cosyvoice-v3.5-flash](https://help.aliyun.com/zh/model-studio/cosyvoice-v3-5-flash)
- **Fun-Realtime-TTS（阿里）**：2026-06-03 登上 Artificial Analysis Speech Arena **第 1 名，Elo 1,219（±16，962 次对战）**，**$27.59/M 字符**；支持实时生成、声音复刻、声音设计、多语言和方言口音；前代 Fun-Realtime-TTS-Preview 排第 7。— [Artificial Analysis, 2026-06-03](https://artificialanalysis.ai/de/articles/fun-realtime-tts-new-text-to-speech-model-topping-artificial-analysis-leaderboard)
- **Omni Realtime（语音到语音）** 百炼价（元/百万 token），按"输入文本 / 输入音频 / 输出文本 / 输出音频"顺序：qwen3.8-omni-flash-realtime 北京 1.5 / 6 / 4.5 / **12**，新加坡 1.677 / 6.781 / 5.104 / **13.636**；qwen3.5-omni-flash-realtime 北京 3.3 / 27 / 20 / 107；qwen3.5-omni-plus-realtime 北京 10 / 80 / 60 / 300，新加坡 15.74 / 123.65 / 92.93 / 464.64。qwen3.5-omni realtime 系列的文本输出不收费。另外 qwen-audio-turbo 只剩免费额度，官方建议改用 Omni。（抓取时表头有些不清，列的对应关系按表序推断。）— [百炼 模型价格](https://help.aliyun.com/zh/model-studio/model-pricing)

### Inferences
- 每分钟成本：qwen3-tts-flash-realtime 英语 ≈ $0.0117、印尼语 ≈ $0.013；cosyvoice-v3-flash（新加坡）≈ $0.0123 / $0.0136；cosyvoice-v3-plus（新加坡）≈ $0.0245 / $0.0273；cosyvoice-v3.5-flash（北京）≈ $0.0103 / $0.0114；cosyvoice-v3.5-plus（北京）≈ $0.0193 / $0.0214；Fun-Realtime-TTS ≈ $0.0248 / $0.0276。
- **合规与地域风险**：能确认支持印尼语的 v3.5 只在北京地域。面向印尼学生时，从北京调用会带来跨境延迟（印尼到北京的 RTT 通常 >100ms）和数据出境问题。实测前应在新加坡控制台确认 v3.5 或 qwen-audio-3.1 是否已上线、是否支持印尼语。
- 声音复刻：复刻音色和目标模型绑定，换模型要重新复刻。ElevenLabs 的音色则可以跨模型使用。

### Gaps
- **qwen-audio-3.1-tts-plus/flash 和 Fun-Realtime-TTS 在百炼的具体单价、地域、语种**都没抓到（总价目表的 TTS 段可能是动态加载，三次分段抓取都没拿到）。
- **声音复刻（qwen-voice-enrollment / CosyVoice 复刻）的创建费用**在已抓取页面中没有说明。
- Omni 输出音频的 token 与秒的换算没查到，所以没法折算成每分钟价格。
- 阿里数字人是否内置 TTS、是否支持印尼语，没有查到。

---

## 3. 火山引擎 豆包语音合成 2.0 / 声音复刻 2.0

### Takeaway
官方按量价格为 **3 元/万字符**（合成 2.0 和复刻 2.0 同价），约 **$0.039/分钟（英）、$0.043/分钟（印尼）**，与 ElevenLabs Flash 基本持平；预付费资源包最低约 2.1 元/万字符。印尼语支持只有第三方资料提到。

### Cited Findings
- 官方计费说明：**豆包语音合成模型 2.0 和豆包声音复刻模型 2.0 的 API 调用都是 3 元/万字符，不分阶梯**；资源包（1 年有效）10 万字 28 元、2000 万字 5400 元（2.7 元/万字符），更大档位最低约 2.1 元/万字符；复刻音色的槽位费在首次合成时收取，每个预付费音色可上传 15 次音频重新复刻。（价格来自搜索摘要，同时引用了官方计费页。）— [火山引擎 豆包语音 计费说明](https://www.volcengine.com/docs/DoubaoVoice/Billinginstructions-21)；[文档中心 6561/1359370](https://docs.volcengine.com/docs/6561/1359370?lang=zh)
- **冲突**：火山开发者社区的几篇文章写"1.3 元/千字"、"150 元/年/音色"，与官方页不一致，以官方为准。— [火山开发者社区 2026 评测](https://developer.volcengine.com/articles/7631415579070136370)
- 印尼语：pyvideotrans 文档称火山 TTS 支持 8 种配音语言，包括中、英、日、葡、西、泰、越、**印尼**。这是第三方集成文档，不等于官方的 2.0 语种清单。— [pyvideotrans: Volcengine TTS](https://doc.pyvideotrans.com/en/volcenginetts)

### Inferences
- 豆包的优势在中文情感表现和国内低延迟。对印尼语课程来说，没有明显的价格优势，印尼语质量也未经验证，适合作为"中文课程"的备选。

### Gaps
- 没有官方的语种清单，也没有官方的首包延迟数据。火山国际版（BytePlus）的价格和可用性没有查。

---

## 4. MiniMax Speech（国际版 platform.minimax.io）

### Takeaway
**speech-2.8-turbo $60/M 字符**（约 $0.054/分钟英、$0.060/分钟印尼），HD 版 $100/M。官方 API 的 `language_boost` 明确列出 **Indonesian**，快速复刻 **$1.5/音色**，复刻门槛最低。

### Cited Findings
- 官方价格：speech-2.8-hd $100/M 字符，**speech-2.8-turbo $60/M 字符**（同步和异步同价）；旧型号 speech-2.6/02-turbo $60/M，hd $100/M；**快速复刻 $1.5/音色，首次用于合成时才扣费**。— [MiniMax Pricing Overview](https://platform.minimax.io/docs/pricing/overview)
- API 文档：`language_boost` 枚举值包含 **Indonesian**、Malay、Vietnamese、Thai 等 40 种语言以及 auto；支持 `stream` 流式输出（流式时只输出 hex 格式）；文档没有给延迟数字。— [MiniMax T2A HTTP API](https://platform.minimax.io/docs/api-reference/speech-t2a-http)
- 第三方渠道价格冲突：有平台列 speech-2.6-turbo 为 $30/M（Together AI 等），与官方 $60/M 不一致。— [Together AI: MiniMax Speech 2.6 Turbo](https://www.together.ai/models/minimax-speech-2-6-turbo)

### Inferences
- 在国际厂商中，MiniMax 是"明确支持印尼语、复刻便宜、中文也强"的少数选项，适合英、印尼、中三语共用一个复刻老师音色。

### Gaps
- MiniMax 中国站（minimaxi.com）的人民币价格没有抓取。首包延迟没有官方或独立数据。

---

## 5. 国际云厂商与独立 TTS：Google、Azure、OpenAI、Cartesia、Fish Audio、Deepgram

### Takeaway
国际选项每分钟成本大致在 $0.013–0.06 之间。最便宜的是 Fish Audio、Azure、OpenAI tts-1，约 $0.0135–0.015/分钟。Google Gemini 3.1 Flash TTS 在榜单上居前（Elo 1214，$18.3/M），性价比突出。Cartesia 主打延迟（官方称约 40–90ms），但实测中位约 166ms。

### Cited Findings
- **Google Cloud TTS**：Chirp 3 HD $30/M 字符，每月 100 万字符免费；Standard / WaveNet $4/M；Neural2 / Polyglot $16/M；Chirp 3 HD 不支持 SSML，也不能调音高和语速。（第三方汇总，官方页抓取失败。）— [Synthorai: Chirp 3 HD](https://synthorai.io/models/google-tts-chirp3-hd/)；[diyai.io Google TTS pricing 2026](https://diyai.io/ai-tools/audio-generation/google-cloud-text-to-speech-pricing/)
- **Gemini 3.1 Flash TTS**：Artificial Analysis Elo 1,214，$18.3/M 字符（2026-06 榜单第 2）。— [Artificial Analysis, 2026-06-03](https://artificialanalysis.ai/de/articles/fun-realtime-tts-new-text-to-speech-model-topping-artificial-analysis-leaderboard)
- **Azure Neural TTS**：官方页的价格被遮挡（显示为"$-"）；免费层 F0 每月 50 万字符 TTS、5 小时实时 STT；Personal Voice 创建免费，按合成字符和音色档案存储收费；Custom Neural Voice 另收端点托管费（按模型按小时）。第三方称 Neural 约 $15/M 字符、STT 约 $1/小时。— [Azure Speech pricing](https://azure.microsoft.com/en-us/pricing/details/speech/)；[aloa.co 对比](https://aloa.co/ai/comparisons/ai-voice-comparison/elevenlabs-vs-google-cloud-tts)
- **OpenAI**（官方定价页）：gpt-4o-mini-tts 文本输入 $0.60/M token，**音频输出 $12/M token**；tts-1 $15/M 字符；tts-1-hd $30/M 字符。Realtime：**gpt-realtime-2.1 / 2 / 1.5 / gpt-realtime 音频输入 $32/M、输出 $64/M**；**gpt-realtime-2.1-mini / gpt-realtime-mini 输入 $10/M、输出 $20/M**。— [OpenAI API Pricing](https://developers.openai.com/api/docs/pricing)
- gpt-4o-mini-tts 约 **$0.015/分钟**（第三方按约 1,500 音频 token/分钟估算）；模型页标为 deprecated。— [OpenAI gpt-4o-mini-tts 模型页](https://developers.openai.com/api/docs/models/gpt-4o-mini-tts)；[TokenMix](https://tokenmix.ai/blog/gpt-4o-mini-tts-cheapest-tts-api-2026)
- **Cartesia Sonic-3 / 3.5 / 3.6**：约 1 credit/字符，Pro Voice Clone 1.5 credit/字符，折合约 $33–65/M（取决于档位）；档位 Free 2 万 credits、Pro $5（10 万）、Startup $49（125 万）、Scale $299（800 万），各来源说法不一；首音延迟官方或宣传口径约 90ms（Turbo 约 40ms），**Vapi 实测中位 166ms**；Sonic-3.6 宣称覆盖 44 种语言、<90ms；有来源称支持印尼语。Sonic 3.5 在 AA 榜 Elo 1,203，$39/M。— [eesel.ai Cartesia Sonic 3 pricing](https://www.eesel.ai/blog/cartesia-sonic-3-pricing)；[Vapi Humanness Index](https://humannessindex.vapi.ai/models/cartesia-sonic-3)；[therundown Sonic 3.6](https://www.therundown.ai/tools/sonic-3-5-ink-2)；[Artificial Analysis](https://artificialanalysis.ai/de/articles/fun-realtime-tts-new-text-to-speech-model-topping-artificial-analysis-leaderboard)
- **Fish Audio**：s2.1-pro **$15/M UTF-8 字节**（另有免费的 s2.1-pro-free）；s2-pro 和 s1 同价；按量付费。Fish Audio S2 Pro 是 AA 榜上最高的开源权重模型（Elo 1121）。— [Fish Audio API Pricing](https://docs.fish.audio/developer-guide/models-pricing/pricing-and-rate-limits)；[Artificial Analysis Leaderboard](https://artificialanalysis.ai/text-to-speech/leaderboard)
- **Deepgram Aura-2**：按量 $0.030/1k 字符，Growth 档 $0.027/1k；Aura-1 $0.015/1k（资料采集于 2026-05 至 07）。— [Deepgram TTS](https://www.deepgram.com/TTS)；[happyrobot Deepgram pricing](https://www.happyrobot.ai/hub/deepgram-pricing)
- **榜单现状**：AA Speech Arena 头部模型的 Elo 集中在 1,200–1,222，2026 年榜首多次易主（Fun-Realtime-TTS、Gemini 3.1 Flash TTS、Inworld Realtime TTS 1.5 Max / TTS-2、Speechify Simba 3.2 自称第一）。另有二手资料称 Eleven v3 约 1,178，排第 3（日期不明）。— [Artificial Analysis Leaderboard](https://artificialanalysis.ai/text-to-speech/leaderboard)；[okmiku 评论](https://okmiku.com/blog/inworld-passes-eleven-v3-naturalness)
- PlayHT：本次没有检索到 2026 年的有效信息（未专门检索，按低优先级跳过）。

### Inferences
- 每分钟成本（英 900 字符 / 印尼 1000 字符）：Chirp 3 HD $0.027 / $0.030；Gemini 3.1 Flash TTS $0.0165 / $0.0183；Azure Neural 约 $0.0135 / $0.015；OpenAI tts-1 $0.0135 / $0.015；gpt-4o-mini-tts 约 $0.015；Cartesia $0.030–0.059 / $0.033–0.065；Fish Audio $0.0135 / $0.015（印尼语基本是 ASCII，字节数约等于字符数）；Deepgram Aura-2 $0.027 / $0.030。
- OpenAI Realtime 的音频输出按约 1,250 token/分钟估算（由 gpt-4o-mini-tts $12/M 对应 $0.015/分钟反推）：gpt-realtime-2.1 ≈ **$0.08/分钟**输出音频，mini ≈ $0.025/分钟。这是推算，不是官方数字。
- Azure id-ID 有 Neural 音色（据既有知识为 id-ID-ArdiNeural / GadisNeural），Google Chirp 3 HD 有 id-ID 音色。这两点本次**没有在页面上核实**。

### Gaps
- Google 和 Azure 官方页的价格没有直接抓到（Google 页面被截断，Azure 价格被遮挡）。
- Gemini 3.1 Flash TTS 是否支持印尼语、流式延迟，以及 Deepgram Aura-2 是否支持印尼语，都没有核实。
- **腾讯云 TTS 的价格和印尼语支持没有检索**（受工具调用预算限制）。
- 没有找到 2025–2026 年的独立**印尼语** TTS 质量评测。所有榜单都以英语为主。

---

## 6. 数字人厂商是否捆绑 TTS（只记录检索中遇到的信息）

### Takeaway
anam.ai 按会话分钟计费：$0.16 → $0.11/分钟，企业版最低 $0.04/分钟。各档"包含 Custom Voice"，宣称 70+ 语言，但没有确认印尼语。第三方称 anam 支持自带 TTS。Tavus、Simli、阿里数字人、腾讯数智人这次没查到可用信息。

### Cited Findings
- anam 定价：Free $0，30 分钟，1 并发；Starter $12/月，50 分钟，超出 $0.16/分钟；Explorer $49，250 分钟，$0.14；Growth $299，2,000 分钟，$0.12，5 并发；Professional $999，8,000 分钟，$0.11，10 并发；Enterprise 定制，**超出部分 $0.04 起**，并发 100 到不限。页面写着"Custom Voice is included in every plan"和"70+ languages"，没有提到自带 TTS/LLM。— [anam.ai Pricing](https://anam.ai/pricing)
- 第三方：anam 支持 bring-your-own-TTS，可以把 ElevenLabs 音频接到 anam 渲染；也可以用 anam 内置的 TTS 管线；按秒计费。（同一篇文章内部对计费方式的描述有矛盾。）— [toughtongueai: Anam vs ElevenLabs Avatars](https://www.toughtongueai.com/blog/anam-vs-elevenlabs-avatars-2026)
- Cartesia 也提供托管 Agents（第三方称 $0.03–0.06/分钟，说法有冲突），TTS 从套餐 credits 中扣。— [Cartesia: ElevenLabs pricing](https://www.cartesia.ai/learn/elevenlabs-pricing)；[Dasha](https://dasha.ai/blog/elevenlabs-alternatives)

### Inferences
- 如果 anam 内置 TTS 的费用已经含在 $0.11–0.16/分钟里，那么继续用 ElevenLabs 外接，每会话分钟大约多出 $0.015–0.04。只有当 anam 内置音色的印尼语质量够好时，才值得省掉这部分。需要实测 anam 内置音色的印尼语效果。

### Gaps
- anam 内置 TTS 背后用的是哪家引擎、是否支持印尼语、外接 TTS 是否单独计费，都没有确认。
- Tavus、Simli、阿里数字人、腾讯数智人的 TTS 捆绑情况没有检索到。

---

## 7. 学生端实时 ASR / STT：价格与印尼语

### Takeaway
实时 ASR 每分钟成本都在 **$0.002–0.008**，相对数字人费用可以忽略。印尼语方面，ElevenLabs Scribe v2 Realtime（$0.39/小时，约 150ms）和 Deepgram Nova-3 Multilingual 比较稳妥；阿里 Paraformer 不支持印尼语，Fun-ASR 实时版是否支持印尼语没有确认。

### Cited Findings
- **ElevenLabs Scribe v2 Realtime $0.39/小时**（≈ $0.0065/分钟），约 150ms；Scribe v2 批量 $0.22/小时；keyterm prompting 另加 $0.05–0.08/小时。— [ElevenLabs API Pricing](https://elevenlabs.io/pricing/api)
- **Deepgram Nova-3**：流式 Monolingual $0.0048/分钟、Multilingual $0.0058/分钟（标为促销价）；常规 Monolingual 流式 $0.0077/分钟；预录 $0.0043 / $0.0052 每分钟。印尼语是否在 Multilingual 档内没有确认。— [scored.tools Deepgram 2026](https://scored.tools/blog/deepgram-pricing-plans-2026/)；[Gladia: Deepgram pricing](https://www.gladia.io/blog/deepgram-pricing)
- **OpenAI**：gpt-4o-transcribe $0.006/分钟，gpt-4o-mini-transcribe $0.003/分钟。— [OpenAI API Pricing](https://developers.openai.com/api/docs/pricing)
- **阿里百炼（北京原价）**：fun-asr-realtime 0.00033 元/秒（≈1.19 元/小时，约 $0.0028/分钟）；paraformer-realtime-v2 0.00024 元/秒（≈0.86 元/小时），语种为中文（含方言）、英、日、韩，**不含印尼语**；fun-asr-flash-8k-realtime 0.00022 元/秒（电话场景）。— [fun-asr-realtime](https://help.aliyun.com/zh/model-studio/fun-asr-realtime)；[paraformer-realtime-v2](https://help.aliyun.com/zh/model-studio/paraformer-realtime-v2)
- 有代码仓库称 Fun-ASR 覆盖 31 种语言，但没有说明实时版是否包含印尼语。— [gitee FunASR](https://gitee.com/weyee/FunASR)
- 百炼新一代 ASR 为 qwen-audio-3.1-asr-flash（含 streaming）系列，价格没有抓到。— [百炼 模型列表](https://help.aliyun.com/zh/model-studio/models)
- Azure 实时 STT 免费层每月 5 小时，付费价被遮挡；第三方称约 $1/小时。— [Azure Speech pricing](https://azure.microsoft.com/en-us/pricing/details/speech/)；[aloa.co](https://aloa.co/ai/comparisons/ai-voice-comparison/elevenlabs-vs-google-cloud-tts)

### Inferences
- 如果 TTS 留在 ElevenLabs，同时用 Scribe v2 Realtime 可以统一账单和 SDK。如果改走阿里方案，印尼语 ASR 需要另找（qwen-audio-3.1-asr 或 Deepgram），因为 Paraformer 不支持印尼语。

### Gaps
- Fun-ASR 实时版、qwen-audio-3.1-asr 是否支持印尼语以及新加坡地域价格；各家印尼语 WER 的独立评测，都没有找到。

---

## 汇总表：每分钟语音成本（USD，仅 TTS）

| 方案 | 单价（原始单位） | 英语/分钟（900 字符） | 印尼语/分钟（1000 字符） | 印尼语 | 实时/延迟 | 复刻 | 来源 |
|---|---|---|---|---|---|---|---|
| ElevenLabs Flash v2.5 / v4 Turbo | $0.04/1k | $0.036 | $0.040 | ✅ 官方 | 约 75–100ms（官方中位） | 即时/专业复刻，音色跨模型可用 | [1](https://elevenlabs.io/pricing/api) [2](https://elevenlabs.io/docs/overview/models) |
| ElevenLabs v4 / v3 / Multilingual v2 | $0.08/1k | $0.072 | $0.080 | ✅ | 较高（未给数字） | 同上 | [1](https://elevenlabs.io/pricing/api) |
| ElevenLabs Agents Speech Engine | $0.08/会话分钟 | — | — | ✅ | — | — | [1](https://elevenlabs.io/pricing/api) |
| 阿里 qwen3-tts-flash-realtime（新加坡） | $0.13/万字符 | $0.0117 | $0.013 | ❓ 未确认 | WebSocket 流式 | 有（费用未知） | [link](https://www.alibabacloud.com/help/en/model-studio/qwen3-tts-flash-realtime) |
| 阿里 cosyvoice-v3.5-flash（仅北京） | 0.8 元/万字符 | $0.0103 | $0.0114 | ✅ 官方 | 首包"大幅降低" | 有 | [link](https://help.aliyun.com/zh/model-studio/cosyvoice-v3-5-flash) |
| 阿里 cosyvoice-v3.5-plus（仅北京） | 1.5 元/万字符 | $0.0193 | $0.0214 | ✅ 官方（指令语种） | 流式 | 有 | [link](https://help.aliyun.com/zh/model-studio/cosyvoice-v3-5-plus) |
| 阿里 cosyvoice-v3-plus（新加坡） | 1.9082 元/万字符 | $0.0245 | $0.0273 | ❓ | 流式 | 主打复刻 | [link](https://help.aliyun.com/zh/model-studio/cosyvoice-v3-plus) |
| 阿里 Fun-Realtime-TTS | $27.59/M | $0.0248 | $0.0276 | ❓ | 实时 | 有 | [AA](https://artificialanalysis.ai/de/articles/fun-realtime-tts-new-text-to-speech-model-topping-artificial-analysis-leaderboard) |
| 火山 豆包 TTS 2.0 / 复刻 2.0 | 3 元/万字符（包年最低约 2.1） | $0.039 | $0.043 | ⚠️ 仅第三方 | — | 复刻 2.0 同价，另收槽位费 | [link](https://www.volcengine.com/docs/DoubaoVoice/Billinginstructions-21) |
| MiniMax speech-2.8-turbo | $60/M | $0.054 | $0.060 | ✅ 官方 | 流式 | $1.5/音色 | [link](https://platform.minimax.io/docs/pricing/overview) |
| MiniMax speech-2.8-hd | $100/M | $0.090 | $0.100 | ✅ | 流式 | $1.5/音色 | 同上 |
| Google Chirp 3 HD | $30/M（第三方） | $0.027 | $0.030 | ❓（据知有 id-ID） | 流式 | Instant custom voice | [link](https://synthorai.io/models/google-tts-chirp3-hd/) |
| Google Gemini 3.1 Flash TTS | $18.3/M | $0.0165 | $0.0183 | ❓ | — | — | [AA](https://artificialanalysis.ai/de/articles/fun-realtime-tts-new-text-to-speech-model-topping-artificial-analysis-leaderboard) |
| Azure Neural | 约 $15/M（第三方） | $0.0135 | $0.015 | ❓（据知有 id-ID） | 流式 | Personal / Custom Voice | [link](https://azure.microsoft.com/en-us/pricing/details/speech/) |
| OpenAI gpt-4o-mini-tts | $12/M 音频 token | 约 $0.015 | 约 $0.015 | ❓ | 流式 | 无 | [link](https://developers.openai.com/api/docs/pricing) |
| OpenAI gpt-realtime-2.1 / mini（输出音频） | $64 / $20 每 M token | 约 $0.08 / $0.025（推算） | 同左 | ❓ | 端到端 | 无 | 同上 |
| Cartesia Sonic-3.x | 约 1 credit/字符（$33–65/M） | $0.030–0.059 | $0.033–0.065 | ⚠️ 第三方称支持 | 宣称 40–90ms；实测中位 166ms | Pro clone 1.5 倍 credits | [link](https://www.eesel.ai/blog/cartesia-sonic-3-pricing) [Vapi](https://humannessindex.vapi.ai/models/cartesia-sonic-3) |
| Fish Audio s2.1-pro | $15/M 字节 | $0.0135 | $0.015 | ❓ | — | 有 | [link](https://docs.fish.audio/developer-guide/models-pricing/pricing-and-rate-limits) |
| Deepgram Aura-2 | $0.030/1k | $0.027 | $0.030 | ❓ | 面向 Agent | — | [link](https://www.deepgram.com/TTS) |

---

## 8. 人工任务：A/B 试听清单（对照 ElevenLabs）

### Takeaway
建议用同一段英语和同一段印尼语勾股定理讲解脚本（各约 45 秒），把以下 4 个方案与 **ElevenLabs v4 Turbo / Flash v2.5** 做盲听 A/B：
1. **阿里 CosyVoice v3.5-flash / plus 或 Fun-Realtime-TTS**：便宜、榜首、官方确认印尼语，但只在北京地域。
2. **MiniMax speech-2.8-turbo**：官方确认印尼语，复刻 $1.5，中文也强。
3. **Google Gemini 3.1 Flash TTS 或 Chirp 3 HD id-ID**：榜单高、便宜、东南亚覆盖好。
4. **Cartesia Sonic-3.6**：延迟最低档，用来检验印尼语是否可用。

可选第 5 个：火山豆包 2.0，只在中文课程场景下测。

### Cited Findings
- 各候选的价格和印尼语依据见上文第 2、4、5 节：[cosyvoice-v3.5-flash](https://help.aliyun.com/zh/model-studio/cosyvoice-v3-5-flash)、[MiniMax T2A](https://platform.minimax.io/docs/api-reference/speech-t2a-http)、[AA 榜单](https://artificialanalysis.ai/text-to-speech/leaderboard)、[Cartesia Sonic 3.6](https://www.therundown.ai/tools/sonic-3-5-ink-2)。

### Inferences
- **试听入口**（根据既有知识列出，本次没有逐一打开核实，多数需要登录，由人工完成）：
  - ElevenLabs：https://elevenlabs.io/app/speech-synthesis
  - 阿里百炼（国内）：https://bailian.console.aliyun.com/ → 模型广场 / 语音合成体验；国际：https://modelstudio.console.alibabacloud.com/
  - MiniMax Audio：https://www.minimax.io/audio （国际）
  - Google：AI Studio 语音生成 https://aistudio.google.com/generate-speech （Gemini TTS）；Cloud TTS 页面内有 demo https://cloud.google.com/text-to-speech
  - Cartesia：https://play.cartesia.ai
  - （可选）Fish Audio：https://fish.audio ；火山豆包语音控制台：https://console.volcengine.com/speech
- **评分维度**（1–5 分）：发音准确度（尤其是 "Pythagoras"、"hipotenusa"、"a² + b² = c²" 等数字和公式的读法）；印尼语重音和语调是否自然；是否像老师（语速、停顿）；在复刻同一位老师音色后的一致性；首音延迟（API 流式实测，从首个文本 chunk 到首个音频 chunk，测 10 次取中位）。
- **测试脚本草稿**（约 45 秒，可直接使用）：
  - EN：*"Today we're going to explore one of the most famous ideas in mathematics: the Pythagorean theorem. Imagine a right triangle — a triangle with one perfect ninety-degree corner. The two shorter sides are called the legs, and we'll name them a and b. The longest side, opposite the right angle, is called the hypotenuse, or c. The theorem says that a squared plus b squared equals c squared. Let's try it. If one leg is three centimeters and the other is four, then three squared is nine, four squared is sixteen, and nine plus sixteen is twenty-five. The square root of twenty-five is five, so the hypotenuse is five centimeters. Pretty neat, right? Now it's your turn: what if the legs are six and eight?"*
  - ID：*"Hari ini kita akan belajar salah satu ide paling terkenal dalam matematika, yaitu teorema Pythagoras. Bayangkan sebuah segitiga siku-siku, yaitu segitiga yang memiliki satu sudut tepat sembilan puluh derajat. Dua sisi yang lebih pendek disebut sisi siku-siku, kita beri nama a dan b. Sisi terpanjang, yang berada di depan sudut siku-siku, disebut hipotenusa atau sisi miring, kita sebut c. Teorema ini mengatakan bahwa a kuadrat ditambah b kuadrat sama dengan c kuadrat. Mari kita coba. Jika satu sisi panjangnya tiga sentimeter dan sisi lainnya empat sentimeter, maka tiga kuadrat adalah sembilan, empat kuadrat adalah enam belas, dan sembilan ditambah enam belas sama dengan dua puluh lima. Akar dari dua puluh lima adalah lima, jadi sisi miringnya lima sentimeter. Sekarang giliranmu: bagaimana jika sisinya enam dan delapan?"*
  - 另做一个"公式原文版"：把数字和公式写成 "3² + 4² = 25" 的形式，测试各引擎的文本正则化能力。

### Gaps
- 试听入口 URL 没有在本次逐一验证，可能已改版或需要登录。
- 阿里 v3.5 和 Fun-Realtime-TTS 在国际控制台是否可用，需要人工确认。
