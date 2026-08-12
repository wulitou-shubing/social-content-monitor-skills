# Social Content Monitor Skills

[![License MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Codex Skills](https://img.shields.io/badge/Codex-Skills-blue.svg)](https://github.com/openai/codex)

一套可以配合使用的 Codex Skills。它能盯住抖音、小红书等平台的指定账号，发现新作品后采集作品信息，提取视频口播文案，再把结果写入飞书多维表格。

你也可以只使用其中的转写 Skill，把一个视频链接、本地视频或录音转成带时间戳的文字稿和字幕。

> 第一次使用建议先看 [从安装到首次运行](docs/getting-started.md)。教程按小白能够照着完成的顺序编写。

## 它能做什么

- 监控多个平台上的多个创作者账号
- 识别新发布的作品并避免重复入库
- 保存标题、作者、发布时间、链接和互动数据
- 下载有权限访问的视频并提取口播文案
- 把作品信息和文案写进同一条飞书多维表格记录
- 保留失败状态，方便以后重试，不会因为转写失败重复建行
- 单独处理一个视频链接、本地视频或音频文件

## 两个 Skill 怎样配合

仓库里有两个可以独立安装的 Skill。

| Skill | 负责的事情 | 适合什么时候用 |
| --- | --- | --- |
| `video-audio-transcribe` | 下载视频、提取音频、生成文字稿和 SRT 字幕 | 转写单个链接、本地视频或录音 |
| `social-content-monitor-to-lark` | 监控账号、判断新作品、去重、安排转写、写入飞书 | 长期收集多个账号的新内容 |

监控 Skill 会在需要转写时调用转写 Skill。这样只想处理一个视频的人不用配置飞书，想做长期监控的人也不用重新写一套转写流程。

```mermaid
flowchart LR
    A[创作者账号] --> B[发现并确认新作品]
    B --> C[检查是否已经入库]
    C --> D[在飞书创建作品记录]
    D --> E[下载并转写音视频]
    E --> F[把口播文案写回同一条记录]
```

## 适合谁

- 想持续收集竞品或行业账号内容的人
- 想把视频口播文案整理并保存到飞书的人
- 同时关注抖音、小红书或其他平台的人
- 希望先手动验证，再逐步改成定时监控的人
- 想给自己的 Codex 增加视频转文字能力的人

它不是一个面向普通消费者的一键式网页产品。使用者需要在 Codex 中完成安装，并准备正常可用的平台账号、飞书多维表格和本地运行环境。详细步骤已经放进 [使用教程](docs/getting-started.md)。

## 支持范围

目前提供以下平台的适配思路。

- 抖音
- 小红书
- TikTok
- YouTube
- 其他能够通过浏览器、官方 API 或已授权连接器可靠读取的平台

各平台页面会变化，所以公共流程没有写死容易失效的页面位置。接入新平台时，需要先确认稳定账号 ID、稳定内容 ID、创作者自己的作品区域、置顶规则和下载权限。

## 快速安装

把下面这段话发给 Codex 即可。

```text
请帮我安装下面两个 Skill，并在安装后检查它们是否可用。

https://github.com/wulitou-shubing/social-content-monitor-skills/tree/main/skills/video-audio-transcribe
https://github.com/wulitou-shubing/social-content-monitor-skills/tree/main/skills/social-content-monitor-to-lark
```

如果你只需要视频转文字，可以只安装第一个 Skill。

安装完成后，建议先用一个有权访问的视频链接测试。

```text
请提取这个视频的口播文案，保留带时间戳的文字稿，并同时生成 SRT 字幕。

这里换成你的视频链接
```

需要监控账号时，可以这样告诉 Codex。

```text
请使用 social-content-monitor-to-lark 帮我监控这些公开账号。

平台和账号链接
这里填写

飞书多维表格链接
这里填写

先手动运行一次并建立基线，不要导入历史作品，也不要创建定时任务。完成后告诉我发现了什么、写入了什么，以及还有哪些配置需要确认。
```

完整的飞书建表、配置文件、首次运行、定时监控和排错步骤见 [从安装到首次运行](docs/getting-started.md)。

## 运行前需要准备什么

- Codex
- Python 3.10 或更高版本
- `ffmpeg`
- 转写依赖文件中列出的 Python 包
- 飞书官方 `lark-cli`
- Codex 中可用的 `lark-shared` 和 `lark-base` Skills
- 可正常登录且有权访问的平台与飞书账号
- 浏览器控制能力、官方 API 或已授权的平台连接器

这些依赖只需要准备一次。Skill 不会在没有征得同意时安装系统软件或读取浏览器登录信息。

## 飞书中会保存什么

建议至少准备以下字段。

| 字段 | 用途 |
| --- | --- |
| 唯一键 | 判断一条作品是否已经入库 |
| 平台 | 记录作品来自哪个平台 |
| 内容 ID | 保存平台提供的稳定作品编号 |
| 内容类型 | 区分视频、图文和其他类型 |
| 标题 | 保存作品标题 |
| 发布日期 | 保存发布时间 |
| 链接 | 返回原作品 |
| 作者 | 保存创作者名称 |
| 原始文案 | 保存作品发布时自带的文字 |
| 口播文案 | 保存语音转写结果 |
| 转写状态 | 显示等待、成功、不适用或失败 |
| 失败原因 | 保存可以用于排错的信息 |

点赞、评论、收藏、分享和播放量可以按需增加。字段不必使用上表中的中文名称，配置文件里的 `field_map` 会把你的字段和流程对应起来。

## 数据怎样避免混乱

- 使用 `<平台>:<内容ID>` 作为主要去重键
- 只读取目标创作者自己的作品区域
- 同时核对作者名称和稳定账号 ID
- 先保存作品信息，再进行耗时较长的下载和转写
- 转写失败时保留原记录和失败原因
- 重试时更新原记录，不重复创建一行
- 没有语音的图文内容仍可入库，转写状态记为 `not_applicable`

Whisper 生成的是听写草稿。人名、品牌、专业词和数字仍建议人工核对。

## 使用边界

这些 Skills 不会帮助使用者做以下事情。

- 绕过验证码、登录验证、频率限制、私密账号或付费限制
- 模拟或伪造浏览器指纹
- 自动点赞、关注、评论、私信或发布内容
- 未经授权下载、转写或传播他人的内容
- 导出、打印或提交浏览器 Cookie

遇到验证码、安全验证、访问频繁或登录失效时，监控应当停止，等使用者恢复正常会话后再继续。

## 仓库结构

```text
social-content-monitor-skills/
├── README.md
├── LICENSE
├── docs/
│   └── getting-started.md
└── skills/
    ├── video-audio-transcribe/
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   ├── requirements.txt
    │   ├── references/
    │   └── scripts/
    └── social-content-monitor-to-lark/
        ├── SKILL.md
        ├── agents/openai.yaml
        ├── assets/config.example.json
        ├── references/
        └── scripts/validate_config.py
```

## License

本仓库使用 [MIT License](LICENSE)。平台内容本身不会因为这份开源许可证而改变版权或使用条件。
