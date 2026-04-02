---
name: Bilibili-trending
description: 获取 Bilibili 全榜单热门数据并分析趋势。支持 21 个榜单，自动调用子 Agent 分析并生成 MD 报告持久化储存。安全无隐私风险，仅调用公开 API。
---

# Bilibili Trending

获取 B 站热门数据 → 自动分析 → 持久化储存 → 趋势预测

## ⚠️ 安全说明

- **仅调用公开 API**：使用 B 站公开排行榜 API，不涉及登录、Cookie、用户信息
- **无个人信息**：只获取热门视频数据，不采集任何用户身份信息
- **本地存储**：数据保存在本地工作区，不上传到任何外部服务器
- **标准请求头**：仅使用标准 User-Agent，无特殊权限

## 环境要求

- Python 3.x
- `requests` 库

## 支持 21 个榜单

| 类型 | 榜单 |
|------|------|
| **普通视频** | 全站、动画、游戏、音乐、舞蹈、鬼畜、影视、娱乐、知识、科技数码、美食、汽车、时尚美妆、体育运动、动物 |
| **PGC 内容** | 番剧、国创、纪录片、电影、电视剧 |

---

## 运行流程（详细）

### Step 1: 选择榜单并抓取

```bash
# 查看所有榜单
python skills/Bilibili-trending/scripts/bilibili_all.py --list

# 抓取指定榜单（以游戏区为例）
python skills/Bilibili-trending/scripts/bilibili_all.py --rank game
```

**脚本自动执行**：
1. 调用 B 站 API 抓取数据
2. 处理数据（计算互动率、提取关键词）
3. 保存 JSON 到 `json/output_game.json`
4. 更新趋势数据到 `trend.json`

**输出示例**：
```
==================================================
开始抓取 游戏 榜单...
==================================================
✓ 成功抓取 97 条数据
  总播放: 243,732,632
  平均互动率: 0.503%
  最热分区: 手机游戏
✓ 数据已保存: .../json/output_game.json
✓ 趋势数据已更新
```

### Step 2: 子 Agent 分析

脚本输出分析 prompt 后，将其发送给子 Agent：

```
请分析以下 Bilibili 游戏 热门视频数据：

## 数据概览
- 榜单: 游戏
- 总视频数: 97
- 总播放: 243,732,632
- 平均互动率: 0.503%
- 最热分区: 手机游戏

## Top 5 视频
[...]

## 提取的关键词
["崩坏", "星穹铁道", "绝区零", "星徽骑士", "鸣潮"]

请输出分析报告（Markdown 格式），包含：
1. 热门内容分析
2. 分区热度分析
3. 关键词趋势
4. 下期预测
```

### Step 3: 保存报告

子 Agent 返回分析报告后，手动保存到：
```
memory/bilibili-analysis/{时间}_{榜单名称}.md
```
例如：`20260402-2327_游戏.md`

**报告内容结构**：
- 数据概览
- 热门内容分析
- 分区热度分析
- 关键词趋势
- 下期预测

### Step 4: 查看趋势

```bash
# 全局趋势
python skills/Bilibili-trending/scripts/bili_trend.py trend

# 单榜单趋势
python skills/Bilibili-trending/scripts/bili_trend.py trend game
```

### Step 5: 生成周/月总结

```bash
# 周总结
python skills/Bilibili-trending/scripts/bili_trend.py weekly

# 月总结
python skills/Bilibili-trending/scripts/bili_trend.py monthly
python skills/Bilibili-trending/scripts/bili_trend.py monthly game
```

---

## 关键词提取逻辑

```python
# 1. 正则提取 2-4 字中文
words = re.findall(r'[\u4e00-\u9fa5]{2,4}', title)

# 2. 统计词频
kw_counter = Counter(words)

# 3. 取 Top 5
top_keywords = [kw for kw, _ in kw_counter.most_common(5)]
```

---

## 输出文件

```
{workspace}/json/
└── output_{rank_type}.json     # 原始数据

{workspace}/memory/bilibili-analysis/
├── trend.json                  # 趋势累计数据
├── 20260402-2327_游戏.md      # 分析报告
├── weekly-2026-W14.md         # 周总结
└── monthly-2026-04.md         # 月总结
```

---

## 注意事项

- 频繁请求会触发 API 限流（-352 错误），建议添加登录 Cookie
- 趋势数据需长期积累（建议 30+ 次）才能形成可靠预测
- 子 Agent 分析完成后需手动保存报告文件
