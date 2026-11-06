# 地狱也得下班 · After Hours in Hell

把职场里的甩锅、审批和「再开五分钟」变成可以闯过去的地狱关卡。

**从 Godot 原生离线 3D 游戏开发中整理可复用工具与工作流的版本化仓库**，后续逐步发布经过实际验证的 Skill。围绕 Aholo / Lux3D 生成底模、Blender 精修与 rigging、character animation、game UI 和引擎接入开展 AI-assisted game development。After Hours in Hell 是本仓库的英文说明名。

A versioned home for reusable tools and workflows from a work-in-progress 3D game development project. Visible 3D assets originate from Aholo/Lux3D and are refined in Blender; Godot runs the native offline prototype. The current release contains a validated rules example, a repository validator and technical documentation. Packaged Skills are planned but have not been released; no MCP server or hosted API is provided.

[网页过程与案例](https://after-hours-18-progress.meoworangecat.chatgpt.site/#diary) · [版本状态](status/current.json) · [构建与运行](docs/build-and-run.md) · [AI 入口](docs/for-ai.md) · [素材来源](assets/provenance.json)

## 可复用内容与技术索引

| 内容 | 实际入口 | 交付与适用范围 |
| --- | --- | --- |
| Godot 规则示例 | [examples/godot-rules](examples/godot-rules/) | 已验证 13 组后台检查；可用于阅读、复现规则与测试方法，数值仍与本关有关 |
| 公开目录验证脚本 | [tools/validate.py](tools/validate.py) | 已验证；检查本仓库白名单、索引、哈希和敏感模式，移用时需审核目标仓库规则 |
| 构建与验收工作流说明 | [构建运行](docs/build-and-run.md) / [架构](docs/architecture.md) / [更新规则](docs/updating.md) | 已有技术文档；不等于一键制作完整游戏的工具 |
| 可安装 Skill | 暂无 | 后续正式制作时使用 skill-creator，并在真实任务中验证后版本化发布 |
| MCP / 远程 API | 暂无 | 当前可调用入口只有文档所列本地命令 |

调试过程、灰模前后对比和完整制作图文主要保存在 [项目网页](https://after-hours-18-progress.meoworangecat.chatgpt.site/#diary)，方便录视频时讲解。回忆册的专用案例链接待网站交付并核验后补入；GitHub 保留与复用有关的技术摘要和链接，不重复搬运网页完整日记。

## 保留的游戏版本与证据

首版记录保留：**2026-11-06** 的制作基线 `character-showcase-3d-20261106-v001`。以下状态仅对应此版本，后续资产完成不自动改写这个冻结包的验收结论：

| 范围 | 已有证据 | 边界 |
| --- | --- | --- |
| Windows 离线样片 | 锅仔、小默可选；实时 3D 选角、出发、角色引导与游戏流程已接通 | 可玩包尚未在本仓库分发 |
| 锅仔 Guozai | 反弹技能、基础动作已接入；对应版本后台流程检查通过 | 最新持锅动作候选仍待游戏内验收 |
| 小默 Xiaomo | 替身诱敌流程已接入；对应版本后台流程检查通过 | 新动作/技能资源与游戏当前包分别记录 |
| 椅哥 Yige | 角色和躺平技能资产继续制作 | 当前选角禁用，不能据设计稿声称可玩 |
| 4K 与 game UI | Windows 最终资源包已有 3840×2160 Vulkan 选角画面取证 | 不等于 4K60、物理键盘或实际听感验收 |
| macOS | 较早候选已导出，并在 Windows 上做静态/资源检查 | 最新 Windows 选角补丁未同步；Mac 真机未验收 |

本仓库的 [Godot 逻辑示例](examples/godot-rules/) 可以独立运行 **13 组后台检查**，不需要模型、音频或网络。它覆盖规则对照、检查点种子、机关时序和小默受伤规则；它不是完整 3D 游戏、渲染演示或全关可达性证明。

## 玩法与制作方向

- 固定斜俯视，键盘为主；取证 → 提交 → 停机 → 下班。
- 三英雄方向：锅仔反弹、椅哥躺平闪避后加速、小默替身诱敌。上述基线只有锅仔、小默开放。
- 优先打磨一关完整体验；十八层是故事框架，尚未制作完十八关。
- 制作链：确认三视图 → Aholo / Lux3D 底模 → Blender 形体、材质、rigging 与 character animation → Godot 接入 → 分项验收。
- 按 3840×2160、16:9 准备 Windows 离线展示；macOS 为另一条适配线。进度网站用于展示记录，正式游戏不是网页版。

## 尚未完成

椅哥可玩接入、部分新资产的原生场景验收、正式开场视频接入、真实设备键盘与音频检查、4K60 性能和长时稳定性测试。开场镜头已实际生成并编码为视频，尚未接入当前游戏包；画面采样审查不等于最终听感或引擎播放验收。通关领取可打印模型是规划，当前没有领取 API、邮箱发奖服务或通过打印验收的奖励。

比赛报名、组队和选题已完成；最终作品交付与提交尚未完成。

## 快速开始

安装 Python 3.10+ 可检查公开索引；安装 Godot **4.7.2 标准版**可复现本次逻辑检查。在仓库根目录执行：

```sh
python tools/validate.py
godot --headless --path examples/godot-rules --script res://tests/parity.gd
```

`godot` 指本机 Godot 可执行文件；Windows PowerShell 可使用 `& '你的Godot可执行文件'`。程序输出 JSON 并返回退出码，`passed: true`、`cases: 13` 表示此示例检查通过。命令只运行无画面逻辑，不启动前台窗口。

完整游戏的源码、模型和音频未随此仓库发布，因此不能从这里构建完整试玩包。完整工程持有者的构建前提与已存在的命令见 [构建说明](docs/build-and-run.md)。

## 给开发者与 AI 的目录索引

| 入口 | 用途 |
| --- | --- |
| [project.json](project.json) | 可复用内容清单、Skill 实际交付状态、关键词、实际命令与目录索引 |
| [AGENTS.md](AGENTS.md) / [AI 阅读说明](docs/for-ai.md) | 证据边界、读写范围与本地调用示例 |
| [status/current.json](status/current.json) | 当前制作版本、平台、角色和未验收项目 |
| [status/history.json](status/history.json) / [devlog](devlog/2026-11-06.md) | 保留首版历史；后续记录可复用内容的实质版本变化 |
| [assets/provenance.json](assets/provenance.json) | 素材来源与公开分发状态；不包含模型文件 |
| [examples/godot-rules](examples/godot-rules/) | 来自现有游戏的规则与测试数据快照 |
| [docs/architecture.md](docs/architecture.md) | 制作链、逻辑接口和游戏接入边界 |
| [docs/updating.md](docs/updating.md) | 可复用内容的每日审核规则；无实质变化不提交 |
| [项目网页案例](https://after-hours-18-progress.meoworangecat.chatgpt.site/#diary) | 调试过程、前后对比与制作图文；专用回忆册链接待核验 |

中英文关键词与 GitHub topics 用于帮助检索和理解，不保证搜索引擎或其他 AI 收录。机器可读文件和本地脚本是当前可用入口，没有托管推理或游戏服务。

## 使用与权利

这是公开展示与技术记录仓库，当前未授予统一开源许可证。代码、文字、模型、字体和音频的权利应分别确认；请阅读 [RIGHTS.md](RIGHTS.md)。未确认再分发许可的模型、贴图、音频和大型构建包不包含在这里。
