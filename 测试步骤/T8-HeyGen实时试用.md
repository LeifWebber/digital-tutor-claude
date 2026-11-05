# T8 HeyGen 实时（LiveAvatar）试用

P1 · 20 分钟

**为什么做**：HeyGen 的实时产品 LiveAvatar 价格和 anam 持平。只渲染画面的模式约 $0.09/分钟，加上自带语音后约 $0.10–0.13/分钟。所以换不换，只看画面是否明显比 anam 好。这一项只回答一个问题：**它的画面和反应速度，值不值得我们花开发量切换过去？**

## 免费额度能做什么

依据官方定价和文档：
- 免费账号有 10 credits。全托管模式 2 credits/分钟，所以够聊约 5 分钟。
- 每次会话最长 2 分钟，带水印，同时只能开 1 路。
- 不能用照片做自定义分身。自定义分身要 Essential 套餐，$99/月，含 1 个 720p 分身。

所以这次用官方形象、全托管模式，在网页控制台里直接聊，不写代码。全托管模式用的是 HeyGen 自带的语音和大模型，回答内容不用在意，**只看画面、口型和反应速度**。

## 步骤

1. 打开 https://app.liveavatar.com 注册登录。
2. 在控制台新建一个对话，菜单名称以实际界面为准，通常叫 Agent 或 Avatar。选一个官方形象，模式选 FULL，语言先选英语。
3. 开始会话，用手机秒表记**首帧时间**：从点开始到画面出现。
4. 依次问这 3 个问题，每题记"问完到开口"的时间：
   - "What is the Pythagorean theorem?"
   - "Why do we square the two short sides first?"
   - "Can you give me another example?"
5. 在它说话时插话，看能不能停下来。
6. 新开一次会话，把语言改成中文，问一句"勾股定理可以用在非直角三角形吗？"。语言列表里有印尼语的话，再试一句："Apakah teorema ini berlaku untuk segitiga yang bukan siku-siku?"
7. 录屏，存到 `测试结果/HeyGen/`。

每次会话 2 分钟就会自动断开，第 4–6 步可以分 2–3 次会话做完。

## 记录

在 `测试记录.csv` 的 T8 行填写：首帧时间、回答延迟中位数、能否打断、3 项打分、中文和印尼语能否听懂。

## 判定

和 T4（anam 实时，3 / 3 / 4）对比：
- **自然度比 anam 高 1 分以上，且延迟不更慢**：值得花 $99 开一个月 Essential，用照片做分身，再测一次。之后作为组合 A 答疑部分的替代候选。
- **否则**：结论为"画面与 anam 同档，不值得切换"，只保留作谈价参照。

参考：[LiveAvatar 积分说明](https://docs.liveavatar.com/docs/faq/credits)、[沙箱模式说明](https://docs.liveavatar.com/docs/sandbox-mode.md)（开发调试用，只有一个形象，约 1 分钟断开，不扣积分）
