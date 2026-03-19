---
description: 微信公众号HTML文章生成规范
alwaysApply: true
---

# 微信公众号 HTML 文章生成规范

## 1. 基础结构

**单html文件，文件名YYYYMMDD_related_name.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>标题</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Microsoft YaHei', 'PingFang SC', Arial, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="design-container">
        <!-- 内容 -->
    </div>
</body>
</html>
```

---

## 2. 容器规范

### 公众号文章容器（默认宽度 677px）

```css
.design-container {
    width: 677px;
    max-width: 100%;
    margin: 0 auto;
    padding: 0;
    box-sizing: border-box;
    background-color: #fff;
}
```

### 图文卡片容器（宽度 375px）

```css
.card-container {
    width: 375px;
    max-width: 100%;
    margin: 0 auto;
    padding: 0;
    box-sizing: border-box;
}
```

---

## 3. 字体规范

```css
/* 正文 */
p { font-size: clamp(15px, 1.4vw, 16px); line-height: 1.8; }

/* 一级标题 */
h1 { font-size: clamp(18px, 2vw, 20px); font-weight: bold; text-align: center; }

/* 二级标题 */
h2 { font-size: clamp(17px, 1.8vw, 18px); font-weight: bold; }

/* 三级标题 */
h3 { font-size: clamp(15px, 1.6vw, 16px); font-weight: bold; }

/* 辅助文字 */
.secondary { font-size: clamp(14px, 1.3vw, 15px); color: #666; }

/* 注释说明 */
.note { font-size: clamp(13px, 1.2vw, 14px); color: #999; }
```

**字体规则：**
- ❌ 禁止输出文章标题（页面已有 `<title>`）
- ❌ 禁止输出 `<header>` 标签
- ❌ 禁止用左边框（`border-left`）装饰标题
- ❌ 禁止在标题下方加横线装饰
- ✅ 标题编号：H1 用"一、二、三"，H2 用"1.1、1.2"，H3 用"1.1.1"

---

## 4. 布局规范

```css
/* Flex 布局 */
.flex { display: flex; gap: clamp(10px, 2vw, 20px); }

/* Grid 自适应 */
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: clamp(10px, 2vw, 20px);
}

/* 卡片 */
.card { padding: clamp(10px, 2vw, 20px); border-radius: 8px; }
```

**布局限制：**
- ❌ 禁止 `position: absolute` / `position: fixed`
- ✅ 只能使用 `position: relative`
- ❌ 禁止 `top` `left` `right` `bottom` 定位
- ❌ 禁止 `float`

---

## 5. 文章内容规范

### 段落边距规则

```css
/* 内容容器，零边距 */
.content-container { padding: 0; margin: 0; }

/* 无背景色段落：只允许上下内边距 */
p, h1, h2, h3 { padding-left: 0; padding-right: 0; }

/* 有背景色段落：四个方向都可以设置内边距 */
.highlight { padding: clamp(10px, 2vw, 16px); }
```

### 表格规范

```css
.table { width: 100%; border-collapse: collapse; font-size: clamp(13px, 1.1vw, 14px); }
.table th { background-color: #d6eaf8; padding: 8px; text-align: left; }
.table td { padding: 8px; border-bottom: 1px solid #eee; }
/* 斑马纹 */
.table tr:nth-child(even) td { background-color: #f9f9f9; }
```

---

## 6. 图文卡片（分页）规范

**宽度 375px，默认 3:4 竖图比例，高度 500px**

### 尺寸对照

| 比例 | 高度计算 | 示例（375px） |
|------|----------|--------------|
| 1:1  | 宽 × 1   | 375px        |
| 3:4  | 宽 × 4/3 | 500px        |
| 4:3  | 宽 × 3/4 | 281px        |

### HTML 结构规则

- ✅ 文字内容只用 `<p>` 标签（JS 分页依赖此标签）
- ✅ `.pagination` 直接子元素只能是扁平块级元素
- ❌ 禁止在 `.pagination` 内套 wrapper / inner 等额外容器
- ❌ 禁止用 `<div>` 承载纯文字内容

```html
<!-- ✅ 正确 -->
<div class="pagination">
    <p class="title">标题文字</p>
    <p class="para">正文段落</p>
    <img src="..." alt="...">
</div>

<!-- ❌ 错误 -->
<div class="pagination">
    <div class="content-block">
        <p>内容</p>
    </div>
</div>
```

### CSS 规范

```css
.pagination {
    width: 375px;
    max-width: 100%;
    height: 500px; /* 3:4 比例，按需调整 */
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
    overflow: hidden;
    outline: 1px solid #f5f5f5;
}
.pagination * { max-width: 100%; box-sizing: border-box; }
.pagination img { width: 100%; height: auto; max-height: 40%; object-fit: cover; }
```

### 自动分页脚本（放在 `</body>` 前）

```javascript
(function() {
    var pages = document.querySelectorAll('.pagination');
    if (!pages.length) return;
    var pageHeight = pages[0].offsetHeight;

    function getOrCreateNextPage(page) {
        var next = page.nextElementSibling;
        if (!next || !next.classList.contains('pagination')) {
            next = document.createElement('div');
            next.className = page.className;
            page.parentNode.insertBefore(next, page.nextSibling);
        }
        return next;
    }

    function isUnsplittable(el) {
        return ['IMG','TABLE','UL','OL','DIV'].includes(el.tagName);
    }

    function splitElement(el, page) {
        if (isUnsplittable(el) || el.tagName !== 'P') return false;
        var text = el.textContent;
        if (!text.trim()) { el.remove(); return true; }
        var pageTop = page.getBoundingClientRect().top;
        var lo = 0, hi = text.length;
        while (lo < hi - 1) {
            var mid = Math.floor((lo + hi) / 2);
            el.textContent = text.slice(0, mid);
            el.getBoundingClientRect().bottom - pageTop > pageHeight ? hi = mid : lo = mid;
        }
        var firstPart = text.slice(0, lo), secondPart = text.slice(lo);
        if (!firstPart.trim()) { el.textContent = text; return false; }
        el.textContent = firstPart;
        if (secondPart.trim()) {
            var next = getOrCreateNextPage(page);
            var newEl = document.createElement('P');
            newEl.className = el.className;
            newEl.textContent = secondPart;
            next.appendChild(newEl);
        }
        return true;
    }

    var maxIter = 10000, count = 0, i = 0;
    while (i < document.querySelectorAll('.pagination').length && count < maxIter) {
        count++;
        var page = document.querySelectorAll('.pagination')[i];
        Array.from(page.children).forEach(function(c) {
            if (!c.textContent.trim() && c.tagName !== 'IMG') c.remove();
        });
        if (page.scrollHeight > pageHeight) {
            var children = Array.from(page.children), handled = false;
            var pageTop = page.getBoundingClientRect().top;
            for (var j = 0; j < children.length; j++) {
                if (children[j].getBoundingClientRect().bottom - pageTop > pageHeight) {
                    if (!splitElement(children[j], page)) {
                        getOrCreateNextPage(page).appendChild(children[j]);
                    }
                    handled = true; break;
                }
            }
            if (!handled) i++;
        } else { i++; }
    }
})();
```

---

## 7. CSS 限制

| 禁止 | 替代方案 |
|------|----------|
| `:hover` `:active` `:focus` `::before` `::after` | CSS 渐变背景 / 实际 `<div>` 元素 |
| `backdrop-filter` | 半透明背景 `rgba` |
| `filter` | `box-shadow` / `text-shadow` |
| `position: absolute/fixed` | `position: relative` |
| `top/left/right/bottom` 定位 | Flex / Grid 布局 |
| `float` | Flex / Grid 布局 |

---

## 8. HTML 标签限制

| 禁止 | 替代 |
|------|------|
| `<button>` | `<div>` |
| `<i>` + Font Awesome | Emoji 或内联 SVG |
| `<form>` `<input>` `<label>` | — |
| `<iframe>` `<embed>` | — |

---

## 9. JavaScript 限制

- ❌ 禁止所有事件监听器（`addEventListener`、`onclick`、`onload` 等）
- ✅ 允许用于初始化渲染（图表初始化、DOM 操作）