# 《地狱也得下班》开发踩坑复盘

这是一个 AI 辅助制作的单人 3D 游戏。项目先用群核 Lux3D 生成底模，经 Blender 修整，再把道具和角色接入游戏。下面的制作记录跨越早期 Godot 原型和 Unreal Engine 试玩版，每条按实际取证版本注明。

| 遇到的坑 | 当时怎么处理 | 证据到哪一步 |
| --- | --- | --- |
| 打印机外观成立，飞出的文件还需要独立控制 | 三视图先定出纸口。在 Blender 修整机身和纸面，将纸包单独导出，出纸位置交给机关逻辑。 | 机身和纸包的导出件有独立网格。11 月 16 日的 Godot 候选已有两个资产和出纸逻辑。[打印机案例与对照图](https://github.com/huangxin-design/after-hours-hell-godot/blob/v011/docs/lux3d/deadline-printer.md) |
| 模型站着没问题，做技能时接触点才露馅 | 锅仔靠右手挂点固定锅柄，椅哥在后仰及回正中检查身体和椅背，小默抬手时调整肩肘蒙皮，再查看本体和替身的受击对象。 | Blender 姿态图和早期实机采样分别记录。Windows v011 另有椅哥选中后开场的坐姿，以及椅哥、小默技能的运行记录。[角色动作案例](https://github.com/huangxin-design/after-hours-hell-godot/blob/v011/docs/lux3d/characters.md) · [v011 验收范围](https://github.com/huangxin-design/after-hours-hell-godot/blob/v011/status/current.json) |
| 锅仔卡片停稳后看不出问题，首帧仍可能出现异常 | 先给选角模型应用采样姿态，再让肖像贴图在展示前就绪。冷进入、从小默切回、激活锅仔卡片时分别取连续帧。 | v011 在 720p、4K 两种显示下各查三个入口，每个入口取 16 帧。六组序列里脸、眼睛和衣领均完整。 |
| 中文按钮在设计图里够粗，进游戏却不好读 | 早期原型调整可变字体字重和运行时轴设置，用导出包中的实际选角画面确认。 | 对应 Godot Windows 候选有字重检查和 4K 画面。v011 另覆盖最长题干、菜单、错误反馈和结算。[Godot 候选记录](https://github.com/huangxin-design/after-hours-hell-godot/blob/v011/status/godot-20261106.json) · [v011 验收范围](https://github.com/huangxin-design/after-hours-hell-godot/blob/v011/status/current.json) |
| 看过机关动画，仍不知道挨打和重试后能不能过桥 | 从正常路线接近审批桥，记录受击、跳跃、失败、重试和反弹，再从同版 Windows 包做一次到结算的流程。 | v011 留有 13 次定向运行记录，其中一条完成路线约 67 米，结算时剩 3 点生命。这次记录覆盖跑通与状态，手感由试玩另评。[v011 版本记录](https://github.com/huangxin-design/after-hours-hell-godot/blob/v011/devlog/2026-11-18.md) |

## 用 Skill 回看一次真实问题

以“切回锅仔卡片时，第一帧的姿势和材质是否正常”为输入，按 Skill 选择首帧检查。现有 v011 记录给出了三个操作入口和两种分辨率。改动也可分开核对，骨骼初始姿态决定首帧轮廓，肖像贴图就绪影响首帧材质。验收对象是这六组连续帧，结果写入交付时只覆盖该包、该角色和已检查入口。

这套做法也适用于自己的项目。记录故障画面来自哪一帧、哪份包，以及哪种输入，再把“视觉异常消失”和“事件状态正确”各自对应到可重看的证据。
