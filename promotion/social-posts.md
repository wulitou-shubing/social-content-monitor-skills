# 多渠道发布文案

下面的文案只使用已经公开且验证过的信息。发布时可按平台删掉说明文字，保留正文和项目链接即可。

## V2EX

标题

开源了两个 Agent Skill，用来监控创作者新作品、提取口播并写入飞书

正文

我最初只想做视频口播提取，后来又把账号监控和飞书入库接了进来。整理之后，我没把它做成一个巨大流程，而是拆成了两个可单独安装的 Agent Skill。

`video-audio-transcribe` 负责下载或读取媒体，用 faster-whisper 转写，输出带时间戳的 TXT 和 SRT。

`social-content-monitor-to-lark` 负责发现新作品、核对作者、用稳定内容 ID 去重，再把作品信息和口播文案写入飞书多维表格。下载或识别失败时，作品记录会保留，后面重试更新原记录，不会反复新建行。

目前写了抖音、小红书、TikTok 和 YouTube 的适配指导。它不绕过验证码、私密账号或频率限制，也不代替用户做点赞和评论。

我已经用 skills.sh CLI 从空目录做过完整安装测试，两个 Skill 都能被正常发现和安装。

```bash
npx skills add wulitou-shubing/social-content-monitor-skills
```

仓库里有中英文说明、脱敏演示、新手教程和安全边界。想看看这种拆分是不是合理，也欢迎帮我找真实安装问题。

https://github.com/wulitou-shubing/social-content-monitor-skills

## 即刻或朋友圈

我把“盯账号、听口播、填飞书”做成了两个开源 Agent Skill。

一个专门把视频和录音转成带时间戳的 TXT 和 SRT，另一个负责监控多平台创作者、核对作者、去重，最后把作品信息和口播文案写入飞书。

现在已经补齐中英文说明、脱敏演示、安全边界和真实安装测试。只想处理一条视频时，也可以只装转写 Skill。

https://github.com/wulitou-shubing/social-content-monitor-skills

## 技术群聊

我刚开源了一组内容监控 Agent Skill，适合做创作者跟踪、竞品内容收集和视频口播归档。

仓库分成两部分。转写 Skill 处理视音频、时间戳 TXT 和 SRT，监控 Skill 处理作者核验、稳定 ID 去重、飞书两阶段写入和失败恢复。已经用 skills.sh CLI 实际验证过安装。

如果你也在做小红书、抖音、TikTok 或 YouTube 的公开内容整理，欢迎帮我试一下安装和边界处理。

https://github.com/wulitou-shubing/social-content-monitor-skills

## X 中文

开源了两个可以配合使用的 Agent Skill。

一个把视音频转成带时间戳的 TXT 和 SRT，另一个监控抖音、小红书、TikTok、YouTube 创作者，核验和去重后写入飞书。

遵循 Agent Skills 开放格式，已用 skills.sh CLI 做过完整安装验证。

https://github.com/wulitou-shubing/social-content-monitor-skills

## X English

I open-sourced two composable Agent Skills.

One turns authorized video and audio into timestamped TXT and SRT. The other monitors creator feeds, verifies authorship, deduplicates stable content IDs, and writes post metadata plus transcripts to Lark Base.

Includes adapter guidance for Douyin, Xiaohongshu, TikTok, and YouTube. Installation was verified with the skills.sh CLI.

https://github.com/wulitou-shubing/social-content-monitor-skills
