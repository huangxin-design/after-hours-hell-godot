# 制作链与规则接口

可见模型经 Aholo / Lux3D 生成，再在 Blender 中修整形体、材质、骨骼与动作。
Godot 负责原生场景、输入、UI、状态和音频接入。模型在 Blender 中通过检查，
并不自动代表游戏内尺度、朝向、握持、碰撞、动画混合或性能合格。

当前作品是固定斜俯视的单关样片。三英雄使用不同技能，分享取证、提交、停机、
出口和检查点规则。椅哥仍在制作；逻辑里的默认分支不能用来宣称椅哥已实现。

## 可阅读和调用的示例

`examples/godot-rules/scripts/simulation.gd` 是现有 GDScript 规则文件的原样快照。
它继承 `RefCounted`，读取同示例下 `data/migration.json`。地图数据只保留这份
代码实际读取的字段，测试向量只保留执行所需数据与说明。

| 函数 | 含义 |
| --- | --- |
| `create_state(checkpoint, evidence, run_seed, hero)` | 创建状态，当前英雄 ID 为 `guozai` 或 `xiaomo` |
| `tick(state, input, dt, use_navigation)` | 原地更新状态并返回；将 dt 限制在 0–0.05 秒 |
| `objective(state)` | 返回当前中文目标文字 |
| `can_stand(x, y, cleared, use_navigation)` | 查询规则中的地面/导航约束 |

`input` 是字典，支持 `x`、`y`、`guard`、`interact`。地图平面 x/y 与独立地面高度
使用米，时间使用秒。每个 tick 重置并产生 `events`；事件用于接入表现，本示例
不播放音效或动画。以下 GDScript 调用可在 Godot 项目脚本中使用：

```gdscript
var sim = load("res://scripts/simulation.gd").new()
var state = sim.create_state(false, false, 0, "guozai")
sim.tick(state, {"guard": true}, 1.0 / 60.0)
print(sim.objective(state))
```

规则数值是开发中的初版，尚未通过平衡测试。来源哈希与公开提取范围见
`examples/godot-rules/source-manifest.json`。独立跑通此示例不等于完整工程可构建。
