# 微信 Cookie 自动监控系统

**创建时间**: 2026-03-20 18:37  
**版本**: 1.0.0

---

## 📋 功能说明

### 核心功能
- ✅ **定时检查 Cookie 状态**（每 12 小时）
- ✅ **Cookie 过期预警**（剩余 1 天时提醒）
- ✅ **过期紧急通知**（立即通知扫码）
- ✅ **自动记录登录时间**
- ✅ **预估过期时间**

---

## 📁 文件位置

| 文件 | 说明 |
|------|------|
| `wechat_cookie_monitor.py` | 监控脚本 |
| `wechat-cookie-status.json` | Cookie 状态文件 |
| `wechat-cookie-notification.md` | 通知文件 |
| `/tmp/wechat-cookie-monitor.log` | 日志文件 |

---

## ⏰ 定时任务

**执行频率**: 每 12 小时检查一次  
**Cron 表达式**: `0 */12 * * *`

**下次检查时间**: 2026-03-21 06:00:00

---

## 📬 通知方式

### 1. 通知文件
位置：`/home/admin/.openclaw/workspace/temp/wechat-cookie-notification.md`

### 2. 日志文件
位置：`/tmp/wechat-cookie-monitor.log`

### 3. 状态文件
位置：`/home/admin/.openclaw/workspace/temp/wechat-cookie-status.json`

---

## 🔧 使用方法

### 手动检查
```bash
python3 /home/admin/.openclaw/workspace/skills/wechat-fetch/scripts/wechat_cookie_monitor.py --check
```

### 查看状态
```bash
cat /home/admin/.openclaw/workspace/temp/wechat-cookie-status.json
```

### 查看通知
```bash
cat /home/admin/.openclaw/workspace/temp/wechat-cookie-notification.md
```

---

## 📊 状态说明

### cookie_valid: true
- ✅ Cookie 有效
- ✅ 可以正常抓取
- ✅ 无需操作

### cookie_valid: false
- ❌ Cookie 已过期
- ❌ 无法抓取文章
- ⚠️ 需要扫码登录

### 过期预警
- ⚠️ 剩余 1 天时发送提醒
- 🔴 已过期发送紧急通知

---

## 🎯 扫码登录流程

当收到过期通知时：

1. **访问**: https://mp.weixin.qq.com/
2. **扫码**: 使用微信扫码登录
3. **保持**: 不要关闭浏览器
4. **完成**: Cookie 已更新，有效期约 4 天

---

## 📝 日志示例

```
============================================================
微信 Cookie 状态检查
检查时间：2026-03-20 18:36:54
============================================================
正在检查 Cookie 状态...
✅ Cookie 有效，可以正常访问
距离上次登录：0 天
预计剩余有效：4 天
✅ Cookie 状态良好，下次检查：12 小时后
============================================================
```

---

## ⚠️ 注意事项

1. **Cookie 有效期**: 约 4 天
2. **检查频率**: 每 12 小时
3. **预警时间**: 剩余 1 天
4. **登录方式**: 必须扫码登录

---

## 🚀 后续优化

- [ ] 集成 MemOS 消息通知
- [ ] 支持邮件通知
- [ ] 支持微信通知
- [ ] 自动重新登录（需要图形界面）

---

**维护者**: OpenClaw Assistant  
**最后更新**: 2026-03-20
