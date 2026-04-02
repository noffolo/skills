# Bilibili 全榜单数据分析工作流

## 支持 21 个榜单

| 类型 | 榜单 |
|------|------|
| **普通视频** | 全站、动画、游戏、音乐、舞蹈、鬼畜、影视、娱乐、知识、科技数码、美食、汽车、时尚美妆、体育运动、动物 |
| **PGC 内容** | 番剧、国创、纪录片、电影、电视剧 |

## 完整自动化流程

### Step 1: 抓取数据（自动）
```bash
python skills/Bilibili-trending/scripts/bilibili_all.py --rank game
```

脚本自动完成：
1. 调用 B 站 API 抓取数据
2. 提取关键词（正则 2-4 字中文，统计词频）
3. 计算统计数据（播放、互动率等）
4. 保存 JSON 到 `json/output_{rank_type}.json`
5. 更新趋势数据到 `trend.json`
6. 生成分析 prompt

### Step 2: 子 Agent 分析（自动）
脚本自动 spawn 子 Agent，发送分析 prompt

### Step 3: 保存报告（自动）
分析完成后，报告自动保存为：
```
memory/bilibili-analysis/{时间}_{榜单名称}.md
```
例如：`20260402-2327_游戏.md`

### Step 4: 查看趋势
```bash
python skills/Bilibili-trending/scripts/bili_trend.py trend
python skills/Bilibili-trending/scripts/bili_trend.py trend game
```

### Step 5: 周/月总结
```bash
python skills/Bilibili-trending/scripts/bili_trend.py weekly
python skills/Bilibili-trending/scripts/bili_trend.py monthly
python skills/Bilibili-trending/scripts/bili_trend.py monthly game
```

## 关键词提取逻辑

```python
# 1. 正则提取 2-4 字中文
words = re.findall(r'[\u4e00-\u9fa5]{2,4}', title)

# 2. 统计词频
kw_counter = Counter(words)

# 3. 取 Top 5
top_keywords = [kw for kw, _ in kw_counter.most_common(5)]
```

## 数据存储

```
{workspace}/json/
└── output_{rank_type}.json     # 原始数据

{workspace}/memory/bilibili-analysis/
├── trend.json                  # 趋势累计数据
├── 20260402-2327_游戏.md      # 自动生成的报告
├── 20260402-2315_动画.md
├── weekly-2026-W14.md         # 周总结
└── monthly-2026-04.md         # 月总结
```

## 预测目标

通过长期积累（30+ 次），分析：
- 各榜单热门分区变化
- 关键词频次趋势
- 新兴关键词信号
- 下期热门题材预测
