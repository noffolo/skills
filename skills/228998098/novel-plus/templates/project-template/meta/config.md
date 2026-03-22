# Phase 2 模型分工配置

| 角色 | 模型 | 职责 |
|------|------|------|
| 主控/协调 | MiniMax M2.7 (本Agent) | 整体调度、存档管理、用户汇报 |
| 主笔/初稿 | Kimi k2.5 | 完成章节初稿 |
| 润色/氛围 | Kimi k2.5 | 优化语言、氛围、感官细节 |
| OOC守护 | Qwen 3 Max / Qwen3.5 Plus | 一致性检查（常规章节抽样+条件触发） |
| 战斗/动作 | Gemini 3.1 Pro | **仅高强度/复杂战斗，详见战斗调用条件** |
| 情感节点 | MiniMax M2.7 / Claude 4.6 Opus | 本章情感规划 |
| 终稿三审 | Claude 4.6 Opus | 逻辑/情感/节奏/语言终审 |
| 读者模拟 | Doubao seed 2.0 pro | 读者视角反馈 |

## 关键章节配置（动态生成）

| 字段 | 内容 |
|------|------|
| key_chapters | [1, 10, 20, 30, 40, 50] |
| act_boundaries | {"act1_end": 10, "act2_end": 30, "act3_end": 50} |
| total_chapters | 50 |
| batch_mode | false |

## 自动推进配置（默认）

| 字段 | 默认值 | 说明 |
|------|--------|------|
| auto_advance_chapters | 4 | 一次自动写4章，节奏舒适 |
| write_interval_seconds | 6 | API缓冲 + 阅读思考时间 |
| auto_confirm | false | 保留手动安全感 |

## 战斗Agent调用条件

满足以下任一条件时调用 Gemini 3.1 Pro：
- 细纲/本章规划标注"高强度/复杂/多方战斗"
- 需要专业动作/物理/兵器描写
- 大规模战役场景

不满足上述条件时，战斗描写由 Kimi k2.5 完成。
