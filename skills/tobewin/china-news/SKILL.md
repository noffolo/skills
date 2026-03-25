---
name: china-news
description: 中国新闻资讯聚合工具。Use when user wants to get latest news from Chinese sources. Supports multiple news sites (Sina, Sohu, NetEase, Tencent) via browser automation and RSS. Generates categorized news reports. 新闻资讯、热点新闻、每日新闻。
version: 1.0.0
license: MIT-0
metadata: {"openclaw": {"emoji": "📰", "requires": {"bins": ["curl", "python3"], "env": []}, "minVersion": "2026.3.22", "needsBrowser": true}}
---

# China News

中国新闻资讯聚合工具，通过浏览器自动化和RSS订阅获取各大新闻网站内容，生成分类新闻报告。

## Features

- 📰 **多源聚合**: 新浪、搜狐、网易、腾讯等主流媒体
- 📂 **智能分类**: 时事、财经、科技、体育、娱乐
- 🔄 **双模式**: 浏览器自动化 + RSS订阅
- 🎨 **精美排版**: 专业新闻报告格式
- ⚡ **实时更新**: 获取最新新闻
- 🌍 **多语言**: 中英文输出

## Trigger Conditions

- "给我今天的新闻" / "Today's news"
- "有什么热点新闻" / "What's trending"
- "看看科技新闻" / "Tech news"
- "财经新闻" / "Financial news"
- "china-news"

## News Sources (新闻来源)

### 浏览器自动化模式

| 来源 | 网址 | 内容 |
|------|------|------|
| 新浪新闻 | news.sina.com.cn | 综合新闻 |
| 搜狐新闻 | news.sohu.com | 深度报道 |
| 网易新闻 | news.163.com | 热点新闻 |
| 腾讯新闻 | news.qq.com | 快讯 |

### RSS订阅模式

| 来源 | RSS地址 | 内容 |
|------|---------|------|
| 新浪新闻 | rss.sina.com.cn | 综合 |
| 搜狐新闻 | rss.sohu.com | 综合 |
| 凤凰新闻 | rss.ifeng.com | 时政 |

## Prerequisites

### OpenClaw版本要求
- OpenClaw v2026.3.22+ (浏览器自动化)

### 浏览器配置
- 配置好browser工具
- 无需登录（新闻网站通常无需登录）

---

## Step 1: 获取新闻

### 方式A：浏览器自动化（推荐）

```javascript
// 打开新浪新闻
await browser.open({
  url: "https://news.sina.com.cn"
})

// 等待页面加载
await browser.wait({ timeout: 5000 })

// 提取新闻标题
const news = await browser.evaluate(() => {
  const items = []
  
  // 提取头条新闻
  document.querySelectorAll('.main-title a, .top-news a, .headline a').forEach(el => {
    if (el.innerText && el.innerText.length > 10) {
      items.push({
        title: el.innerText.trim(),
        url: el.href,
        source: '新浪'
      })
    }
  })
  
  return items.slice(0, 10)
})
```

### 方式B：RSS订阅

```python
import requests
import xml.etree.ElementTree as ET

def fetch_rss(url):
    """获取RSS订阅内容"""
    response = requests.get(url, timeout=10)
    root = ET.fromstring(response.content)
    
    items = []
    for item in root.findall('.//item'):
        title = item.find('title')
        link = item.find('link')
        pub_date = item.find('pubDate')
        
        if title is not None:
            items.append({
                'title': title.text,
                'url': link.text if link is not None else '',
                'date': pub_date.text if pub_date is not None else ''
            })
    
    return items[:10]

# 获取新闻
news = fetch_rss('https://rss.sina.com.cn/news/china/roll.xml')
```

---

## Step 2: 新闻分类

```python
def categorize_news(news_list):
    """智能分类新闻"""
    
    categories = {
        '时事': ['政治', '国际', '外交', '政策', '政府', '两会', '选举'],
        '财经': ['股市', '基金', '经济', '金融', '投资', '银行', '房产'],
        '科技': ['AI', '人工智能', '芯片', '手机', '互联网', '新能源'],
        '体育': ['足球', '篮球', '奥运', '世界杯', 'NBA', '中超'],
        '娱乐': ['明星', '电影', '音乐', '综艺', '八卦', '热播'],
        '社会': ['事故', '案件', '民生', '教育', '医疗', '疫情']
    }
    
    categorized = {cat: [] for cat in categories}
    categorized['其他'] = []
    
    for news in news_list:
        matched = False
        for category, keywords in categories.items():
            if any(kw in news['title'] for kw in keywords):
                categorized[category].append(news)
                matched = True
                break
        if not matched:
            categorized['其他'].append(news)
    
    # 移除空分类
    return {k: v for k, v in categorized.items() if v}
```

---

## Step 3: 生成报告

```python
def generate_news_report(categorized_news, date_str):
    """生成精美新闻报告"""
    
    output = []
    output.append(f"┌{'─'*50}┐")
    output.append(f"│  📰 每日新闻速递")
    output.append(f"│  {date_str}")
    output.append(f"└{'─'*50}┘")
    output.append("")
    
    # 热点速递（取每个分类的第一条）
    output.append("🔥 热点速递")
    output.append("─" * 40)
    for category, news_list in categorized_news.items():
        if news_list and category != '其他':
            top_news = news_list[0]
            output.append(f"【{category}】{top_news['title']}")
    output.append("")
    
    # 分类详情
    for category, news_list in categorized_news.items():
        if news_list:
            output.append(f"📌 {category}新闻")
            output.append("─" * 40)
            for i, news in enumerate(news_list[:5], 1):
                output.append(f"{i}. {news['title']}")
                if news.get('source'):
                    output.append(f"   来源：{news['source']}")
            output.append("")
    
    return '\n'.join(output)
```

---

## Step 4: 完整流程

```bash
python3 << 'PYEOF'
import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

class ChinaNews:
    def __init__(self):
        self.rss_sources = {
            '新浪国内': 'https://rss.sina.com.cn/news/china/roll.xml',
            '新浪国际': 'https://rss.sina.com.cn/news/world/roll.xml',
            '新浪财经': 'https://rss.sina.com.cn/finance/roll.xml',
            '新浪科技': 'https://rss.sina.com.cn/tech/roll.xml',
            '搜狐新闻': 'https://news.sohu.com/rss/'
        }
        
        self.keywords = {
            '时事': ['政治', '国际', '外交', '政策', '政府', '两会', '外交'],
            '财经': ['股市', '基金', '经济', '金融', '投资', '银行', '房产', 'A股'],
            '科技': ['AI', '人工智能', '芯片', '手机', '互联网', '新能源', '科技'],
            '体育': ['足球', '篮球', '奥运', '世界杯', 'NBA', '中超', '体育'],
            '娱乐': ['明星', '电影', '音乐', '综艺', '八卦', '热播', '娱乐'],
            '社会': ['事故', '案件', '民生', '教育', '医疗', '社会']
        }
    
    def fetch_rss(self, url):
        """获取RSS内容"""
        try:
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
            })
            root = ET.fromstring(response.content)
            
            items = []
            for item in root.findall('.//item'):
                title = item.find('title')
                link = item.find('link')
                desc = item.find('description')
                
                if title is not None and title.text:
                    items.append({
                        'title': title.text.strip(),
                        'url': link.text if link is not None else '',
                        'desc': desc.text[:100] if desc is not None and desc.text else ''
                    })
            
            return items[:15]
        except Exception as e:
            print(f"⚠️ RSS获取失败: {e}")
            return []
    
    def categorize(self, news_list):
        """智能分类新闻"""
        categorized = {cat: [] for cat in self.keywords}
        categorized['其他'] = []
        
        for news in news_list:
            matched = False
            for category, kws in self.keywords.items():
                if any(kw in news['title'] for kw in kws):
                    categorized[category].append(news)
                    matched = True
                    break
            if not matched:
                categorized['其他'].append(news)
        
        return {k: v for k, v in categorized.items() if v}
    
    def generate_report(self, categorized_news, date_str):
        """生成新闻报告"""
        output = []
        output.append(f"┌{'─'*50}┐")
        output.append(f"│  📰 每日新闻速递")
        output.append(f"│  {date_str}")
        output.append(f"└{'─'*50}┘")
        output.append("")
        
        # 热点速递
        output.append("🔥 热点速递")
        output.append("─" * 40)
        for category, news_list in categorized_news.items():
            if news_list and category != '其他':
                top = news_list[0]
                output.append(f"【{category}】{top['title'][:40]}...")
        output.append("")
        
        # 分类详情
        for category, news_list in categorized_news.items():
            if news_list:
                output.append(f"📌 {category}新闻")
                output.append("─" * 40)
                for i, news in enumerate(news_list[:5], 1):
                    title = news['title'][:50]
                    output.append(f"{i}. {title}")
                output.append("")
        
        return '\n'.join(output)

# 执行
news_service = ChinaNews()

print("📰 正在获取新闻...")

# 获取多个来源的新闻
all_news = []
for name, url in news_service.rss_sources.items():
    print(f"   获取 {name}...")
    items = news_service.fetch_rss(url)
    for item in items:
        item['source'] = name
    all_news.extend(items)

print(f"   共获取 {len(all_news)} 条新闻")

# 分类
categorized = news_service.categorize(all_news)

# 生成报告
date_str = datetime.now().strftime('%Y年%m月%d日 %H:%M')
report = news_service.generate_report(categorized, date_str)

# 输出
print("\n" + "=" * 50)
print(report)

# 保存到文件
output_dir = os.environ.get('OPENCLAW_WORKSPACE', os.getcwd())
output_path = os.path.join(output_dir, f'news_{datetime.now().strftime("%Y%m%d")}.md')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(report)

print(f"\n📁 报告已保存: {output_path}")
PYEOF
```

---

## Security Notes

- ✅ No API keys required
- ✅ No data uploaded to external servers
- ✅ Local processing only
- ⚠️ Requires internet access to fetch news

---

## Notes

- RSS模式无需浏览器，curl即可
- 浏览器模式需要OpenClaw v2026.3.22+
- 新闻网站结构可能变化，需要维护
- 支持中英文输出
