# 📡 Social Content Monitor Skills

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-open%20format-5B5BD6.svg)](https://agentskills.io)
[![License MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

#### 盯住创作者的新作品，提取视频口播，再把结果送进飞书

这个仓库解决一件很具体的事。你给 Agent 一组抖音、小红书或其他平台的账号，它负责发现新作品、核对作者、避免重复采集、转写视频口播，最后把作品信息和文案写进飞书多维表格。

只想处理一个视频也可以。丢给 Agent 一个视频链接、本地视频或录音，它会生成带时间戳的文字稿和 SRT 字幕。

仓库遵循 [Agent Skills 开放格式](https://agentskills.io)。Claude Code、Codex 以及其他兼容 `SKILL.md` 的 Agent 都可以加载。不同客户端提供的浏览器、飞书连接器和定时任务能力并不相同，完整监控需要这些能力配合。

> 第一次安装建议看 [从安装到首次运行](docs/getting-started.md)。里面写了原生安装、手动安装和不支持 Skill 时的用法。

## 📋 这里有两个 Skill

| 名字 | 一句话说明 | 可以单独使用 |
| --- | --- | --- |
| [video-audio-transcribe](skills/video-audio-transcribe) | 下载或读取音视频，生成文字稿和 SRT 字幕 | 可以 |
| [social-content-monitor-to-lark](skills/social-content-monitor-to-lark) | 监控多平台账号，把新作品、互动数据和口播文案写入飞书 | 可以，但转写视频时需要上面的 Skill |

两个 Skill 拆开以后，单次转写不用碰飞书，账号监控也可以把转写当成独立步骤调用。下载或识别失败时，已经采集到的作品信息仍会保留，修复后可以继续处理同一条记录。

```mermaid
flowchart LR
    A[创作者账号] --> B[发现新作品]
    B --> C[核对作者并去重]
    C --> D[写入飞书作品信息]
    D --> E[调用转写 Skill]
    E --> F[回填同一条飞书记录]
```

## 📦 安装

### 支持 Agent Skills 的客户端

在 Claude Code、Codex 或其他支持 Agent Skills 的工具里，直接发送下面这段话。

```text
请帮我安装下面两个 Agent Skill，并在安装后检查是否能够识别。

https://github.com/wulitou-shubing/social-content-monitor-skills/tree/main/skills/video-audio-transcribe
https://github.com/wulitou-shubing/social-content-monitor-skills/tree/main/skills/social-content-monitor-to-lark
```

只做视频转文字时，安装第一个即可。

### 客户端不能从链接安装

下载对应的完整 Skill 文件夹，放进客户端规定的 Skills 目录，再重新加载客户端。不要只下载 `SKILL.md`，因为转写 Skill 还要使用同目录中的脚本和参考文件。

不同客户端的安装目录和启用方法各不相同，请以当前客户端文档为准。Skill 文件夹的名称要保持不变。

### 客户端没有原生 Skill 功能

把完整 Skill 文件夹放进项目，再让 Agent 阅读对应的 `SKILL.md` 并照着执行。它仍然需要能够读取文件、运行脚本和访问所需服务。若客户端不能运行本地命令，视频下载与转写脚本就无法工作。

更完整的判断方法见 [兼容性与安装教程](docs/getting-started.md#先判断你的-agent-能做到哪一步)。

## 🎙️ video-audio-transcribe

> 给它一个视频链接或媒体文件，拿回可以复核的时间戳文字稿。

它会按任务选择最短流程。在线视频先下载，本地视频可以直接识别，需要 MP3 时再单独提取音频。原始时间戳稿会保留，后续清理文案时不会覆盖证据稿。

它能处理下面这些请求。

- 下载 Agent 能正常访问且用户有权使用的在线视频
- 从本地视频中提取 MP3
- 识别视频或录音中的中文及其他语言
- 输出带时间戳的 TXT 文字稿
- 输出可以导入剪辑软件的 SRT 字幕
- 标出需要人工复核的人名、数字、品牌和专业词

可以直接这样说。

```text
提取这个视频的口播文案，保留时间戳文字稿，并生成 SRT 字幕。

这里换成视频链接或本地文件路径
```

```text
把这个录音转成中文文字稿。人名和数字听不清时标出来，不要猜。

这里换成本地音频路径
```

需要 Python 3.10 或更高版本、`ffmpeg` 和 [requirements.txt](skills/video-audio-transcribe/requirements.txt) 中的依赖。首次使用某个 Whisper 模型时通常需要下载模型。

## 🛰️ social-content-monitor-to-lark

> 给它一组账号和一个飞书表格，它只处理经过核对的新作品。

这个 Skill 负责账号监控的整个过程。它先从创作者自己的作品区找候选，再核对作者名称和稳定账号 ID。确认是新作品以后，它先在飞书保存作品信息，再调用转写 Skill，最后把口播文案写回同一条记录。

它能完成下面这些工作。

- 同时管理多个平台和多个创作者账号
- 排除置顶内容、推荐内容和其他作者的作品
- 使用稳定内容 ID 或规范化链接去重
- 保存标题、发布时间、链接、原始文案和可读取的互动数据
- 为视频作品提取口播文案
- 为没有语音的图文作品标记 `not_applicable`
- 为失败任务保留原因，下一次更新原记录
- 手动验证成功后再按用户要求创建定时监控

第一次建议这样说。

```text
请使用 social-content-monitor-to-lark 监控下面的公开账号，并把新作品写入我的飞书多维表格。

账号主页
这里填写平台名称和主页链接

飞书多维表格
这里填写链接

先检查环境和字段，只测试一个账号。首次运行只建立基线，不导入历史作品，也不要创建定时任务。
```

目前写有抖音、小红书、TikTok 和 YouTube 的平台适配指导。其他平台也能接入，但要先确认稳定账号 ID、稳定内容 ID、创作者自己的作品区域、置顶规则和下载权限。

## 🧩 兼容性

Agent Skills 是开放格式，Skill 能被加载，不代表每个客户端都具备相同工具。可以先用这张表判断自己能做到哪一步。

| 客户端具备的能力 | 单个视频转写 | 完整账号监控 |
| --- | --- | --- |
| 能读取文件并运行 Python | 可以处理本地媒体 | 不够 |
| 还能访问网络并运行 `ffmpeg` | 可以处理受支持的视频链接 | 不够 |
| 还能使用已登录浏览器或平台官方 API | 可以 | 可以发现新作品 |
| 还能调用飞书 OpenAPI、连接器或 `lark-cli` | 可以 | 可以写入飞书 |
| 还有定时任务能力 | 可以 | 可以按计划自动运行 |

在 Codex 中，可以使用 `lark-shared` 和 `lark-base` 完成飞书授权与多维表格操作。其他客户端可以使用自己的飞书连接器、MCP、官方 OpenAPI 或 `lark-cli`。没有定时任务能力时，手动触发监控仍然可用。

## 🗂️ 飞书会保存什么

推荐至少准备下面这些字段。

| 字段 | 用途 |
| --- | --- |
| 唯一键 | 判断作品是否已经入库 |
| 平台 | 保存内容来源 |
| 内容 ID | 保存平台作品编号 |
| 内容类型 | 区分视频、图文和其他类型 |
| 标题 | 保存作品标题 |
| 发布日期 | 保存作品发布时间 |
| 链接 | 返回原作品 |
| 作者 | 保存创作者名称 |
| 原始文案 | 保存作品发布时自带的文字 |
| 口播文案 | 保存语音转写结果 |
| 转写状态 | 显示等待、完成、不适用或失败 |
| 失败原因 | 留下可以用于重试的信息 |

点赞、评论、收藏、分享和播放量可以按需增加。实际字段名称通过 `field_map` 配置，不要求照搬中文名称。

## 🔒 使用边界

这两个 Skill 只处理用户有权访问和使用的内容。它们不会执行下面这些操作。

- 绕过验证码、登录验证、频率限制、私密账号或付费限制
- 模拟或伪造浏览器指纹
- 自动点赞、关注、评论、私信或发布内容
- 未经授权下载、转写或传播他人的内容
- 导出、打印或提交浏览器 Cookie

遇到验证码、安全验证、访问频繁或登录失效时，监控会停止。用户恢复正常会话后才能继续。

## 🧱 仓库结构

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

`agents/openai.yaml` 提供 OpenAI 客户端的界面信息，不影响其他 Agent 读取标准的 `SKILL.md`。

## 🌟 反馈与许可

有问题或想增加新的平台，可以在 [Issues](https://github.com/wulitou-shubing/social-content-monitor-skills/issues) 中提出。使用顺利的话，也欢迎点一个 Star。

本仓库使用 [MIT License](LICENSE)。平台内容不会因为这份开源许可证而改变版权或使用条件。
