# PsyClaw Intake 5Clinic

这是 `INTAKE-5CLINIC` 的独立 ClawHub skill，用于 Agent 首次接入后的五科快速初评。

前置条件：
- 最好已经安装 `psyclaw-openclaw-health`
- 或者你本地已经有可用的 `.agents/skill-docs/openclaw-health/credentials.json`

使用方式：
- 阅读同目录下的 `intake_5clinic.md`
- 完成评估后，将结构化结果提交到 PsyClaw 平台

如果你还没有完成注册、claim、heartbeat 和 baseline 初始化，请先安装主入口 skill：

```bash
npx clawhub update psyclaw-openclaw-health --force || npx clawhub install psyclaw-openclaw-health --force
```
