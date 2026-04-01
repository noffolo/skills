---
name: zmt-account-launcher
version: 1.0.0
description: ZMT多账号浏览器启动工具。用于启动本地多账号管理工具中的浏览器实例，获取浏览器端口等信息以便后续控制。支持账号名模糊匹配、分组过滤。
---

# ZMT多账号浏览器启动工具

ZMT多账号浏览器启动与管理工具，用于程序化控制账号的启动、关闭及信息查询。

## 服务地址

`http://localhost:1008`

## 核心概念

### 账号索引（Index）
- 所有操作基于**账号索引**（从 `"1"` 开始）
- `获取所有账号信息` 返回的是**下标**（从 `"0"` 开始）
- **转换关系**：索引 = 下标 + 1

| 下标（API返回） | 索引（操作使用） |
|----------------|-----------------|
| "0"            | "1"             |
| "1"            | "2"             |
| "2"            | "3"             |

### API 列表

1. **获取所有分组** - 获取所有分组名称
2. **获取所有账号信息** - 获取账号名到下标的映射
3. **获取指定分组** - 获取分组内的账号索引
4. **启动** - 根据索引启动账号
5. **关闭** - 根据索引关闭账号
6. **指定账号所有数据** - 获取账号详细信息（含端口等）

## 使用方法

### 1. 直接调用脚本

```bash
python scripts/launcher.py --action start --account "账号名"
python scripts/launcher.py --action stop --account "账号名"
python scripts/launcher.py --action list
python scripts/launcher.py --action get --account "账号名"
```

### 2. Python API

```python
from scripts.launcher import ZMTLauncher

launcher = ZMTLauncher("http://localhost:1008")

# 列出所有账号
accounts = launcher.get_all_accounts()

# 启动账号（支持精确/模糊匹配）
launcher.start_account("654645645")

# 关闭账号
launcher.stop_account("654645645")

# 启动指定分组下的账号
launcher.start_account("654645645", group="默认分组")
```

## 启动后浏览器信息说明

当使用 `--action start` 启动浏览器后，可通过 `--action get` 获取以下浏览器信息：

### 返回信息字段

| 字段名 | 说明 | 示例值 | 用途 |
|--------|------|--------|------|
| `端口占用` / `端口` | 浏览器CDP调试端口 | `"35247"` | **最重要** - 用于连接和控制浏览器 |
| `进程id` | 浏览器进程ID | `"38312"` | 用于进程管理、监控 |
| `唯一id` | 账号唯一标识 | `"VJZYMKCDVP"` | 区分不同账号实例 |
| `指纹环境` | 浏览器User-Agent | `"Mozilla/5.0..."` | 了解浏览器环境配置 |
| `ck路径` | Cookie文件路径 | `".\软件缓存\ck\..."` | 读取/管理Cookie |
| `账号名` | 账号显示名称 | `"654645645"` | 账号识别 |
| `分组` | 所属分组 | `"默认分组"` | 分组管理 |

### 如何使用端口控制浏览器

**步骤1：获取端口号**
启动后从返回数据中获取 `端口` 字段的值，如 `35247`。

**步骤2：构建CDP连接地址**
```
http://127.0.0.1:35247
```

**步骤3：使用Playwright连接**
```python
from playwright.sync_api import sync_playwright

port = "35247"  # 从启动返回信息中获取
cdp_url = f"http://127.0.0.1:{port}"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(cdp_url)
    page = browser.new_page()
    
    # 现在可以控制浏览器了
    page.goto("https://example.com")
    page.screenshot(path="screenshot.png")
    
    browser.close()
```

**步骤4：执行浏览器操作**
获得 `page` 对象后，可以执行：
- `page.goto(url)` - 导航到指定网址
- `page.click(selector)` - 点击元素
- `page.fill(selector, text)` - 输入文本
- `page.screenshot(path)` - 截图
- `page.evaluate(js_code)` - 执行JavaScript

### 完整示例流程

```bash
# 1. 启动浏览器并获取信息
python scripts/launcher.py --action start --account "654645645"

# 2. 获取浏览器详细信息（包含端口）
python scripts/launcher.py --action get --account "654645645"
# 输出中包含: 端口: 35247

# 3. 使用该端口进行CDP连接（在其他脚本或技能中）
# CDP地址: http://127.0.0.1:35247

# 4. 完成操作后关闭浏览器
python scripts/launcher.py --action stop --account "654645645"
```

### 注意事项

- **端口唯一性**：每个账号启动后都有独立的端口号，不会冲突
- **端口生命周期**：浏览器关闭后，该端口会被释放
- **本地连接**：CDP连接仅限本地 (127.0.0.1)，不对外开放
- **进程管理**：可通过 `进程id` 在系统中查看和管理浏览器进程

## 账号匹配策略

1. **优先精确匹配**：先尝试完全匹配账号名
2. **模糊匹配兜底**：精确匹配失败时，进行子串匹配
3. **多匹配确认**：模糊匹配到多个结果时，返回候选列表

## 分组过滤

当指定分组时：
1. 先获取该分组内的所有账号索引
2. 在这些索引中匹配账号名
3. 仅操作匹配到的账号

## 脚本参数

```
python scripts/launcher.py --help

Options:
  --action {start,stop,list,get}  操作类型
  --account TEXT                  账号名（支持模糊匹配）
  --group TEXT                    指定分组
  --port INTEGER                  服务端口（默认1008）
  --host TEXT                     服务地址（默认localhost）
```

## 示例

```bash
# 启动账号（精确匹配）
python scripts/launcher.py --action start --account "654645645"

# 启动账号（模糊匹配）
python scripts/launcher.py --action start --account "654"

# 启动指定分组下的账号
python scripts/launcher.py --action start --account "654645645" --group "默认分组"

# 关闭账号
python scripts/launcher.py --action stop --account "654645645"

# 列出所有账号
python scripts/launcher.py --action list

# 获取账号详情（含端口信息）
python scripts/launcher.py --action get --account "654645645"
```

## 返回值说明

- `启动` / `关闭` 接口返回当前**操作的账号总数**
- 实际状态以软件界面为准

## 错误处理

- 账号不存在：返回错误信息
- 多匹配情况：返回候选账号列表供选择
- 连接失败：检查服务是否启动在指定端口

## 注意事项

1. 修改端口后需要取消勾选再重新勾选启动
2. 索引范围由 `获取所有账号信息` 返回的账号数量决定
3. 避免同时从多个客户端操作同一账号

## 依赖

```
requests>=2.25.0
```

## 参考文档

- 软件官网介绍页：https://zmt.scys6688.com/
- 飞书文档：https://feishu.cn/docx/RR0QdOStCooF5hxyb1GcfdFhnnb
