# 构建与运行 / Build and run

## 本仓库可直接运行的内容

`examples/godot-rules/` 是独立的 Godot 无素材规则示例。它不包含可视场景、
模型、音频或主菜单。无需导出模板；本次验证使用 Godot 4.7.2 标准版。

在仓库根目录运行：

```sh
python tools/validate.py
godot --headless --path examples/godot-rules --script res://tests/parity.gd
```

Python 3.10+，仅使用标准库。Godot 可执行文件名可能不同，请替换 `godot`；
PowerShell 使用 `&` 调用带空格的可执行文件路径。

成功时规则脚本退出码为 0，最后输出包含 `passed: true` 与 `cases: 13` 的 JSON。
它还会向 Godot 的此示例专用 `user://` 目录写入 `native-logic-tests.json`。
13 组包括 10 个规则对照向量、种子重试、机关时序和小默半透明时的受伤规则。
对照向量关闭导航检测；它们不能代替正式场景的通路、动画或碰撞验收。

验证脚本检查公开文件白名单、JSON、索引引用、示例哈希及常见敏感信息模式。
自动扫描不能代替内容和权利审查。

## 完整游戏：仅适用于已合法持有完整工程的人

完整工程和试玩包未在本仓库发布。以下是现有生产工程的构建接口记录，
**在本仓库中运行不会得到完整游戏**。

完整工程应包含 `project.godot`、`main.tscn`、脚本、UI、数据、模型、音频和字体，
并配有与 Godot 4.7.2 匹配的导出模板。把模板设置为自己机器上有效的位置；
本仓库不发布工作机器的路径或原始导出配置。

在完整工程根目录，已存在的导出预设名是 `Windows Desktop` 和 `macOS Universal`：

```sh
godot --headless --editor --path . --quit
godot --headless --path . --export-release "Windows Desktop" build/AfterHours.exe
godot --headless --path . --export-release "macOS Universal" build/AfterHours-macOS.zip
```

先创建 `build` 目录。Windows 当前使用独立 PCK，保留 EXE 与同名 PCK 同目录。
只有在明确安排交互试玩时才双击启动。macOS 包导出与静态检查不证明签名、
Gatekeeper、Metal 渲染、声音或键盘在 Mac 上通过；必须在目标设备单独验收。
本次公开发布只实际执行了上面的无素材示例，没有重新构建完整游戏。

官方命令参考：[Godot command line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)。
