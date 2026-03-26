#!/usr/bin/env node
/**
 * NewsToday — 晚间推送 prompt 生成器
 * 由 openclaw cron 驱动，每日 20:00 执行
 */

const now = new Date();
const tomorrow = new Date(now);
tomorrow.setDate(tomorrow.getDate() + 1);

const dateStr = now.toLocaleDateString('zh-CN', {
  year: 'numeric', month: 'long', day: 'numeric', weekday: 'long'
});
const tomorrowStr = tomorrow.toLocaleDateString('zh-CN', {
  month: 'long', day: 'numeric', weekday: 'long'
});

console.log(`请生成今日晚间新闻汇总与明日预告。当前日期：${dateStr}

执行步骤：
1. 搜索「今日晚间重要新闻 ${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}」
2. 搜索「今日热点事件最新进展」
3. 搜索「明日重要日程 财经 政治 体育」

输出格式：
🌙 晚间快报 · ${dateStr}
━━━━━━━━━━━━━━━━━━━━━━━

📋 今日收官（3-5条下午/晚间重要新闻，每条附摘要）

🔄 今日热点最新进展（1-2条今天持续发酵的事件更新）

📅 明日预告（${tomorrowStr}值得关注的事）
· 重要会议/发布/赛事
· 财经数据/政策发布
· 预计有进展的持续事件

━━━━━━━━━━━━━━━━━━━━━━━
💡 回复"早报"明早8点见`);
