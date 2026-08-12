# Social Content Monitor Skills

一组配合使用的 Codex Skills，用于监控多个内容平台的创作者账号，把新内容、互动数据和视频口播文案保存到飞书多维表格。

仓库包含两个独立 Skill：

1. `video-audio-transcribe`：下载在线视频、提取音频、使用 faster-whisper 生成带时间戳的文字稿和 SRT。
2. `social-content-monitor-to-lark`：监控抖音、小红书等平台的新内容，完成作品归属校验、去重、转写编排和飞书回填。

## 为什么拆成两个 Skill

转写能力可以独立处理本地视频、录音和单个视频链接；监控能力则负责多个平台、多个账号、定时任务和飞书数据生命周期。上层监控 Skill 调用底层转写 Skill，避免重复代码，也避免用户只想转写一个文件时误触发飞书流程。

```text
社交平台账号
  ↓
平台适配与作品归属校验
  ↓
唯一键去重
  ↓
飞书创建元数据记录
  ↓
video-audio-transcribe
  ↓
按同一个 record_id 回填口播文案
```

## 支持范围

当前设计包含以下适配指导：

- 抖音
- 小红书
- TikTok
- YouTube
- 其他能够通过浏览器、官方 API 或连接器可靠读取的平台

平台页面结构会变化，因此 Skill 不把易失效的 CSS 选择器写死在公共流程里。新增平台时，需要明确稳定账号 ID、稳定内容 ID、创作者自有内容区域、置顶规则和下载授权策略。

## 安装

可以让 Codex 直接从以下两个地址安装：

```text
https://github.com/wulitou-shubing/social-content-monitor-skills/tree/main/skills/video-audio-transcribe
https://github.com/wulitou-shubing/social-content-monitor-skills/tree/main/skills/social-content-monitor-to-lark
```

两个 Skill 应同时安装。监控 Skill 还需要：

- Codex 中可用的浏览器控制能力，或目标平台的官方连接器/API
- 飞书官方 `lark-cli`
- `lark-shared` 和 `lark-base` Skills
- Python 3.10+
- `ffmpeg`
- `video-audio-transcribe/requirements.txt` 中的 Python 包
- 用户正常登录且获准使用的目标平台和飞书会话

## 配置

复制示例配置到 Skill 文件夹之外：

```bash
cp skills/social-content-monitor-to-lark/assets/config.example.json ./monitor.config.json
```

修改账号、飞书表格、字段映射、时区和检查时间后进行校验：

```bash
python skills/social-content-monitor-to-lark/scripts/validate_config.py ./monitor.config.json
```

示例账号默认全部为停用状态，必须替换占位符并显式启用。

不要把真实配置提交到 Git。真实配置可能包含私人账号列表、飞书分享链接和本地工作路径。

## 推荐的飞书字段

至少准备以下字段：

- 唯一键
- 平台
- 内容ID
- 内容类型
- 标题
- 发布日期
- 链接
- 作者
- 原始文案
- 口播文案
- 转写状态
- 失败原因

点赞、评论、收藏、分享和播放量可按需增加。实际字段名称通过 `field_map` 配置，不要求使用中文名称。

## 数据可靠性

- 使用 `<平台>:<内容ID>` 作为主要去重键。
- 只从目标创作者自己的作品区域读取候选。
- 详情页作者名称和稳定作者 ID 必须同时通过校验。
- 先创建元数据，再下载和转写。
- 下载或转写失败时保留原记录并标记失败，不创建重复行。
- 小红书图文等没有可转写语音的内容仍可入库，转写状态记为 `not_applicable`。
- Whisper 结果是听写草稿，专业名词、人名和数字仍需人工核对。

## 安全边界

这些 Skills 不提供也不应被用于：

- 绕过验证码、登录验证、频率限制、私密账号或付费限制
- 模拟或伪造浏览器指纹
- 自动点赞、关注、评论、私信或发布
- 未经授权下载、转写或传播内容
- 导出、打印或提交浏览器 Cookie

遇到验证码、安全验证、访问频繁或登录失效时，监控流程会停止并请求用户恢复正常会话。

## 仓库结构

```text
social-content-monitor-skills/
├── README.md
├── LICENSE
├── .gitignore
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

MIT License。平台内容本身不因本仓库的许可证而改变其版权或使用条件。
