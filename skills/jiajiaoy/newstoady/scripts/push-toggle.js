#!/usr/bin/env node
/**
 * NewsToday — 推送开关
 *
 * 用法:
 *   node push-toggle.js on <userId>   开启推送
 *   node push-toggle.js off <userId>  关闭推送
 *   node push-toggle.js status <userId>  查看状态
 *
 * 选项:
 *   --morning HH:MM   早报时间（默认 08:00）
 *   --evening HH:MM   晚报时间（默认 20:00）
 *   --channel <name>  推送渠道（默认 telegram）
 */

const fs = require('fs');
const path = require('path');

const USERS_DIR = path.join(__dirname, '../data/users');

function loadUser(userId) {
  const f = path.join(USERS_DIR, `${userId}.json`);
  if (!fs.existsSync(f)) return null;
  return JSON.parse(fs.readFileSync(f, 'utf8'));
}

function saveUser(userId, data) {
  fs.mkdirSync(USERS_DIR, { recursive: true });
  fs.writeFileSync(path.join(USERS_DIR, `${userId}.json`), JSON.stringify(data, null, 2), 'utf8');
}

function enablePush(userId, opts = {}) {
  const morning = opts.morning || '08:00';
  const evening = opts.evening || '20:00';
  const channel = opts.channel || 'telegram';

  const [mh, mm] = morning.split(':');
  const [eh, em] = evening.split(':');

  const morningCron = `${mm} ${mh} * * *`;
  const eveningCron = `${em} ${eh} * * *`;

  const sessionKey = `agent:main:${channel}:direct:${userId}`;

  // 早报 cron
  const morningConfig = {
    name: `newstoday-morning-${userId}`,
    cronExpr: morningCron,
    tz: 'Asia/Shanghai',
    session: 'isolated',
    sessionKey,
    channel,
    to: userId,
    announce: true,
    timeoutSeconds: 120,
    message: `node ${path.join(__dirname, 'morning-push.js')}`
  };
  console.log(`__OPENCLAW_CRON_ADD__:${JSON.stringify(morningConfig)}`);

  // 晚报 cron
  const eveningConfig = {
    name: `newstoday-evening-${userId}`,
    cronExpr: eveningCron,
    tz: 'Asia/Shanghai',
    session: 'isolated',
    sessionKey,
    channel,
    to: userId,
    announce: true,
    timeoutSeconds: 120,
    message: `node ${path.join(__dirname, 'evening-push.js')}`
  };
  console.log(`__OPENCLAW_CRON_ADD__:${JSON.stringify(eveningConfig)}`);

  // 保存用户推送设置
  saveUser(userId, {
    pushEnabled: true,
    morningTime: morning,
    eveningTime: evening,
    channel,
    enabledAt: new Date().toISOString()
  });

  console.log(`
✅ 每日推送已开启

⏰ 早报：每天 ${morning}（今日要闻10条）
🌙 晚报：每天 ${evening}（收官+明日预告）
📡 渠道：${channel}

关闭推送：node push-toggle.js off ${userId}`);
}

function disablePush(userId) {
  const user = loadUser(userId);
  if (!user) {
    console.log(`❌ 未找到用户 ${userId} 的推送记录`);
    return;
  }

  console.log(`__OPENCLAW_CRON_RM__:newstoday-morning-${userId}`);
  console.log(`__OPENCLAW_CRON_RM__:newstoday-evening-${userId}`);

  saveUser(userId, { ...user, pushEnabled: false, disabledAt: new Date().toISOString() });
  console.log(`✅ 推送已关闭`);
}

function showStatus(userId) {
  const user = loadUser(userId);
  if (!user) {
    console.log(`❌ 未找到用户 ${userId} 的推送记录`);
    return;
  }
  console.log(`
📡 推送状态 — ${userId}
━━━━━━━━━━━━━━━━━━━━━━━
状态：${user.pushEnabled ? '✅ 开启中' : '❌ 已关闭'}
早报：${user.morningTime || '08:00'}
晚报：${user.eveningTime || '20:00'}
渠道：${user.channel || 'telegram'}
开启于：${user.enabledAt ? user.enabledAt.split('T')[0] : '未知'}
━━━━━━━━━━━━━━━━━━━━━━━`);
}

module.exports = { enablePush, disablePush, showStatus };

if (require.main !== module) return;

const args = process.argv.slice(2);
const command = args[0];
const userId = args[1];

if (!command || !userId) {
  console.log(`用法:
  node push-toggle.js on <userId> [--morning 08:00] [--evening 20:00] [--channel telegram] [--no-breaking]
  node push-toggle.js off <userId>
  node push-toggle.js status <userId>`);
  process.exit(1);
}

const opts = {};
const mi = args.indexOf('--morning');
if (mi !== -1) opts.morning = args[mi + 1];
const ei = args.indexOf('--evening');
if (ei !== -1) opts.evening = args[ei + 1];
const ci = args.indexOf('--channel');
if (ci !== -1) opts.channel = args[ci + 1];
if (args.includes('--no-breaking')) opts.breaking = false;

switch (command) {
  case 'on':     enablePush(userId, opts); break;
  case 'off':    disablePush(userId); break;
  case 'status': showStatus(userId); break;
  default:
    console.log(`❌ 未知命令: ${command}`);
    process.exit(1);
}
