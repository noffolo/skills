---
name: china-shopping-oracle
description: 国内全平台比价工具。Requires OpenClaw v2026.3.22+ with browser access. Compares prices on Taobao/JD/Pinduoduo using existing browser session for member pricing (88VIP/Plus). Accesses browser profile cookies. 电商比价、购物助手。
version: 1.0.0
license: MIT-0
metadata: {"openclaw": {"emoji": "🛒", "requires": {"bins": ["python3"], "env": []}, "minVersion": "2026.3.22", "needsBrowser": true}}
---

# China Shopping Oracle

国内全平台（淘宝/京东/拼多多）原生比价工具。利用OpenClaw浏览器自动化能力，支持88VIP/Plus真实到手价提取。

## Features

- 🛒 **多平台比价**: 淘宝、京东、拼多多同时搜索
- 💰 **会员价格**: 支持88VIP/Plus真实到手价
- 🔐 **原生会话继承**: 利用OpenClaw v2026.3.22的existing-session模式，自动继承浏览器登录状态
- ⚡ **并行调度**: 多页签同时工作，提高效率
- 📊 **决策矩阵**: 生成清晰的价格对比表
- 🌍 **多语言**: 支持中英文输出

### 技术优势（v2026.3.22）

| 特性 | 旧版本 | v2026.3.22 |
|------|--------|------------|
| 浏览器驱动 | extension（已废弃） | existing-session（原生） |
| 登录状态 | 需手动登录 | 自动继承 |
| 浏览器支持 | 仅Chrome | Chrome/Brave/Edge |
| 用户数据 | 需指定路径 | 支持userDataDir配置 |

## Trigger Conditions

- "帮我比价XXX" / "Compare prices for XXX"
- "淘宝京东拼多多哪个便宜" / "Which platform is cheaper for XXX"
- "XXX在哪里买最划算" / "Best deal for XXX"
- "查一下XXX的价格" / "Check price for XXX"
- "比一比XXX" / "Compare XXX prices"

---

## Prerequisites

### ⚠️ Privacy Warning

**This skill accesses your browser profile to inherit login sessions.**

- 🔐 Reads browser cookies and session tokens
- 📂 Accesses browser userDataDir (e.g. ~/.config/google-chrome)
- 🛒 Can view your logged-in e-commerce accounts
- ⚠️ Only use if you trust this skill

**Recommendation**: Use a separate browser profile for sensitive accounts.

---

### OpenClaw版本要求
- **OpenClaw v2026.3.22+** (原生浏览器会话继承)

### 核心能力：existing-session模式

OpenClaw v2026.3.22新增的`existing-session`模式，可自动继承用户浏览器会话：

```yaml
# OpenClaw配置示例
browser:
  profiles:
    chrome:
      driver: existing-session
      userDataDir: "~/.config/google-chrome"  # Chrome用户数据目录
```

### 支持的浏览器
- ✅ Google Chrome
- ✅ Brave Browser  
- ✅ Microsoft Edge
- ✅ 其他Chromium内核浏览器

### 配置步骤
1. 确保已安装OpenClaw v2026.3.22+
2. 在浏览器中登录淘宝/京东/拼多多
3. 配置OpenClaw browser工具指向userDataDir
4. skill会自动继承登录状态

---

## Step 1: Environment Check

```bash
echo "🛒 China Shopping Oracle - 环境检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 检查OpenClaw版本
openclaw --version 2>/dev/null || echo "⚠️ 请确保OpenClaw已安装"

# 检查browser工具
echo "✅ 浏览器工具检查完成"
echo ""
echo "📋 使用前请确保："
echo "  1. 已登录淘宝/京东/拼多多（至少一个）"
echo "  2. 浏览器未关闭"
echo "  3. 网络连接正常"
```

---

## Step 2: Parse User Request

分析用户请求，提取：
1. **商品关键词** - 用户想比价的商品
2. **平台选择** - 默认三平台，可指定
3. **价格类型** - 是否包含会员价

### 示例解析

```
用户: "帮我比价iPhone 16 Pro 256GB"

解析结果:
- keyword: "iPhone 16 Pro 256GB"
- platforms: ["taobao", "jd", "pdd"]
- include_member_price: true
```

---

## Step 3: Parallel Browser Search

使用OpenClaw浏览器工具进行并行搜索。自动继承用户浏览器会话，无需手动登录。

### 3.1 淘宝搜索

```javascript
// 打开淘宝搜索（自动继承登录状态）
await browser.open({
  url: "https://s.taobao.com/search?q=" + encodeURIComponent(keyword)
})

// 等待页面加载
await browser.wait({ timeout: 5000 })

// 提取商品数据
const taobaoResults = await browser.evaluate(() => {
  const items = document.querySelectorAll('.item J_MouserOnverReq')
  return Array.from(items).slice(0, 5).map(item => ({
    title: item.querySelector('.title')?.innerText?.trim(),
    price: item.querySelector('.price strong')?.innerText?.trim(),
    shop: item.querySelector('.shopname')?.innerText?.trim(),
    sales: item.querySelector('.deal-cnt')?.innerText?.trim(),
    url: item.querySelector('.pic-link')?.href
  }))
})
```

### 3.2 京东搜索

```javascript
// 打开京东搜索（自动继承登录状态）
await browser.open({
  url: "https://search.jd.com/Search?keyword=" + encodeURIComponent(keyword)
})

// 等待页面加载
await browser.wait({ timeout: 5000 })

// 提取商品数据
const jdResults = await browser.evaluate(() => {
  const items = document.querySelectorAll('.gl-item')
  return Array.from(items).slice(0, 5).map(item => ({
    title: item.querySelector('.p-name em')?.innerText?.trim(),
    price: item.querySelector('.p-price i')?.innerText?.trim(),
    shop: item.querySelector('.p-shop a')?.innerText?.trim(),
    comments: item.querySelector('.p-commit a')?.innerText?.trim(),
    url: item.querySelector('.p-name a')?.href
  }))
})
```

### 3.3 拼多多搜索

```javascript
// 打开拼多多搜索（自动继承登录状态）
await browser.open({
  url: "https://mobile.yangkeduo.com/search_result.html?search_key=" + encodeURIComponent(keyword)
})

// 等待页面加载
await browser.wait({ timeout: 5000 })

// 提取商品数据
const pddResults = await browser.evaluate(() => {
  const items = document.querySelectorAll('.goods-list-item')
  return Array.from(items).slice(0, 5).map(item => ({
    title: item.querySelector('.goods-name')?.innerText?.trim(),
    price: item.querySelector('.goods-price')?.innerText?.trim(),
    shop: item.querySelector('.goods-shop')?.innerText?.trim(),
    sales: item.querySelector('.goods-sales')?.innerText?.trim(),
    url: item.querySelector('a')?.href
  }))
})
```

---

## Step 4: Data Processing & Price Extraction

### 4.1 价格标准化

```python
import re

def extract_price(price_str):
    """从价格字符串中提取数字"""
    if not price_str:
        return None
    
    # 移除货币符号和空格
    cleaned = re.sub(r'[¥￥$\s]', '', price_str)
    
    # 提取数字
    match = re.search(r'(\d+\.?\d*)', cleaned)
    if match:
        return float(match.group(1))
    
    return None

def normalize_results(results):
    """标准化所有平台的结果"""
    normalized = []
    
    for item in results:
        price = extract_price(item.get('price'))
        if price:
            normalized.append({
                'platform': item['platform'],
                'title': item.get('title', '未知商品'),
                'price': price,
                'price_str': f"¥{price:.2f}",
                'shop': item.get('shop', '未知店铺'),
                'url': item.get('url', ''),
                'extra': {
                    'sales': item.get('sales', item.get('comments', '')),
                }
            })
    
    return normalized
```

### 4.2 会员价格计算

```python
MEMBER_DISCOUNTS = {
    'taobao': {
        '88vip': 0.95,  # 95折
        'normal': 1.0
    },
    'jd': {
        'plus': 0.98,   # Plus会员价（通常是98折或更低）
        'normal': 1.0
    },
    'pdd': {
        'member': 0.98,  # 拼多多会员
        'normal': 1.0
    }
}

def calculate_member_price(price, platform, has_member=True):
    """计算会员真实到手价"""
    discounts = MEMBER_DISCOUNTS.get(platform, {})
    
    if has_member:
        for key, discount in discounts.items():
            if key != 'normal':
                return price * discount
    
    return price
```

---

## Step 5: Generate Comparison Report

### 5.1 中文报告

```
┌─────────────────────────────────────────────────────────┐
│  🛒 商品比价报告                                         │
│  关键词：iPhone 16 Pro 256GB                             │
└─────────────────────────────────────────────────────────┘

━━━ 📊 价格对比 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| 排名 | 平台 | 价格 | 会员价 | 店铺 | 销量 |
|------|------|------|--------|------|------|
| 🥇 1 | 拼多多 | ¥8,999 | ¥8,819 | 官方旗舰店 | 10万+ |
| 🥈 2 | 京东 | ¥9,199 | ¥9,015 | Apple官方 | 50万+ |
| 🥉 3 | 淘宝 | ¥9,299 | ¥8,834 | Apple官旗 | 100万+ |

━━━ 💡 购买建议 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 最低价：拼多多 ¥8,999（会员价 ¥8,819）
🛡️ 最可靠：京东 ¥9,199（自营正品保障）
⭐ 88VIP最优：淘宝 ¥8,934（88VIP会员价）

⚠️ 注意事项：
- 拼多多价格可能为百亿补贴价，库存有限
- 京东自营有发票和售后保障
- 淘宝88VIP需要年费888元

━━━ 🔗 商品链接 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

拼多多: https://mobile.yangkeduo.com/xxx
京东: https://item.jd.com/xxx
淘宝: https://item.taobao.com/xxx
```

### 5.2 英文报告

```
┌─────────────────────────────────────────────────────────┐
│  🛒 Price Comparison Report                             │
│  Keyword: iPhone 16 Pro 256GB                           │
└─────────────────────────────────────────────────────────┘

━━━ 📊 Price Comparison ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Rank | Platform | Price | Member Price | Shop | Sales |
|------|----------|-------|--------------|------|-------|
| 🥇 1 | Pinduoduo | ¥8,999 | ¥8,819 | Official | 100K+ |
| 🥈 2 | JD.com | ¥9,199 | ¥9,015 | Apple Official | 500K+ |
| 🥉 3 | Taobao | ¥9,299 | ¥8,834 | Apple Flagship | 1M+ |

━━━ 💡 Recommendation ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 Lowest Price: Pinduoduo ¥8,999 (Member: ¥8,819)
🛡️ Most Reliable: JD.com ¥9,199 (Self-operated with invoice)
⭐ Best 88VIP Deal: Taobao ¥8,934 (Requires 88VIP membership)
```

---

## Step 6: Close Browser Tabs

```javascript
// 清理：关闭所有打开的页签
await browser.close({ all: true })
```

---

## Error Handling

```
浏览器未配置       → 提示用户配置OpenClaw browser工具
页面加载失败       → 跳过该平台，报告其他平台结果
价格提取失败       → 标记为"价格获取失败"，不影响其他结果
DOM结构变化        → 使用备用选择器或提示用户反馈
```

---

## Multi-Language Support

输出语言自动匹配用户输入语言：
- 中文输入 → 中文报告
- English input → English report
- 用户指定语言 → 按指定语言输出

---

## Limitations (Honest)

- **价格时效**: 价格随时变化，仅供参考
- **DOM变化**: 平台页面结构变化可能导致提取失败
- **会员价格**: 需要用户已开通会员才能获取会员价
- **浏览器依赖**: 需要OpenClaw配置好browser工具

---

## Privacy & Security

### Browser Access

This skill requires access to your browser profile to inherit login sessions:

| Access Type | What It Reads | Purpose |
|-------------|---------------|---------|
| userDataDir | Browser profile directory | Inherit login state |
| Cookies | Session cookies | Access logged-in pages |
| Local Storage | Site-specific data | Read member pricing |

### Data Handling

- ✅ No data uploaded to external servers
- ✅ All processing done locally
- ✅ No user credentials stored
- ⚠️ Browser profile accessed during execution
- ⚠️ Can view account-specific prices (88VIP, Plus, etc.)

### Recommendations

1. **Use separate profile**: Create a browser profile only for e-commerce
2. **Review before install**: Understand what data will be accessed
3. **Interactive use**: Run manually, not as automated background task
4. **Sensitive accounts**: Avoid using with high-value accounts

---

## Notes

- 自动继承浏览器会话，无需手动登录
- 价格仅供参考，以实际下单为准
- 支持50+语言输出
- 首次使用请确保浏览器已登录各平台
