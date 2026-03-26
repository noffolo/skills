#!/usr/bin/env node
/**
 * NewsToday — 早报推送 prompt 生成器
 * 由 openclaw cron 驱动，每日 08:00 执行
 * 输出内容由 Claude 通过 WebSearch 完成
 */

const now = new Date();
const dateStr = now.toLocaleDateString('zh-CN', {
  year: 'numeric', month: 'long', day: 'numeric', weekday: 'long'
});

console.log(`请生成今日早报。当前日期：${dateStr}

执行步骤：
1. 搜索「今日重要新闻 ${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}」
2. 搜索「今日国际新闻」
3. 搜索「今日财经新闻」
4. 综合去重，选取10条覆盖不同领域（重要/财经/国际/科技/社会各至少1条）

输出格式：
📰 今日早报 · ${dateStr}
━━━━━━━━━━━━━━━━━━━━━━━
（10条新闻，每条含标题、来源、2句摘要，按领域分组）
━━━━━━━━━━━━━━━━━━━━━━━
💡 回复序号可深读该条新闻详情`);
