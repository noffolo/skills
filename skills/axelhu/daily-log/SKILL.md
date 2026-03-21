---
name: daily-log
version: 1.1.0
description: 每日工作日志生成技能。触发时机：每次会话结束前或完成重要任务后。输出位置：memory/daily/YYYY-MM-DD.md。使用方法：加载 skill 后读取 references/spec.md 获取详细规范。
---

# Daily Log

按规范生成每日工作日志，供后续知识提取。

## 输出位置

`memory/daily/YYYY-MM-DD.md`

## 核心流程

1. 读取 references/spec.md 获取详细规范
2. 读取当前日记（如已存在）
3. 按规范生成/整合日志
4. 写文件
5. 自检

## 触发时机

- 会话结束前
- 完成重要任务后
- 用户明确要求时

## 为什么要写日记

日记是记忆系统的核心输入：
- cron memory-review 扫描日记生成知识提案
- 没有日记，知识沉淀链条断裂
- 详细日记 → 更多可提取知识

## 常见错误

- 只写结果不写过程 → 无法提取经验
- 事后概括 → 丢失细节
- 过于简略 → 扫不出东西

## 与 Memory Review 联动

日记是记忆系统的核心输入：
- **daily-log** 负责写日记
- **memory-review** 负责扫描日记生成知识提案
- 两者配合：详细日记 → 更多可提取知识

详见 `skills/memory-review/SKILL.md`
