# HunterMiner 安装说明

## 1. 安装 Python 3

- Windows 10/11：安装 Python 3.10+
- Linux：确保有 `python3`
- macOS：确保有 `python3`

## 2. 安装依赖

在技能目录下执行：

### Linux / macOS

```bash
cd hunterminer
python3 -m pip install -r requirements.txt
```

### Windows PowerShell

```powershell
cd hunterminer
py -3 -m pip install -r requirements.txt
```

## 3. 放到 OpenClaw 技能目录

你可以把整个 `hunterminer` 文件夹复制到以下任一位置：

- `~/.openclaw/skills/hunterminer`
- `~/.openclaw/workspace/skills/hunterminer`
- 或当前 OpenClaw 工作区的 `skills/hunterminer`

## 4. 刷新 OpenClaw

- 重启 OpenClaw
- 或让 OpenClaw 刷新 skills

## 5. 第一次使用前确认

- `config.local.json` 里已经预留了计费配置
- 你也可以改成环境变量 `SKILLPAY_API_KEY`
- 如果要让特征库自动远程合并，编辑 `indicators/remote_sources.json`

## 6. 免费更新特征库

### Linux / macOS

```bash
cd hunterminer
python3 hunterminer.py update-db
```

### Windows

```powershell
cd hunterminer
py -3 hunterminer.py update-db
```

## 7. 运行一次计费扫描

### Linux / macOS

```bash
cd hunterminer
python3 hunterminer.py scan --user-id YOUR_USER_ID
```

### Windows

```powershell
cd hunterminer
py -3 hunterminer.py scan --user-id YOUR_USER_ID
```

## 8. 查看报告

报告会生成在：

- `output/latest_report.json`
- `output/latest_report.md`

## 9. 处理扫描结果

先看报告里的 `finding id`，再执行：

### 先演练，不真正删除

```bash
python hunterminer.py remediate --report output/latest_report.json --finding-id FINDING_ID
```

### 隔离

```bash
python hunterminer.py remediate --report output/latest_report.json --finding-id FINDING_ID --action quarantine --yes
```

### 删除（必须你明确确认后再做）

```bash
python hunterminer.py remediate --report output/latest_report.json --finding-id FINDING_ID --action delete --yes
```

删除或隔离完成后，建议重启计算机。
