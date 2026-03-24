# OpenClaw PowPow Integration Skill

将 OpenClaw Agent 发布到 PowPow 地图平台，创建数字人并与用户实时对话。

## 功能

- **用户认证**: 注册/登录 PowPow 账号
- **数字人管理**: 创建、续期、列出数字人
- **实时通信**: 通过 SSE 与数字人聊天
- **徽章系统**: 使用徽章创建和续期数字人

## 安装

```bash
npm install
npm run build
```

## 配置

在 ClawHub 中配置：

```json
{
  "powpowBaseUrl": "https://global.powpow.online",
  "powpowApiKey": "可选",
  "defaultLocation": {
    "lat": 39.9042,
    "lng": 116.4074,
    "name": "Beijing"
  }
}
```

## 命令

| 命令 | 功能 | 所需徽章 |
|------|------|----------|
| `register` | 注册 PowPow 账号 | - |
| `login` | 登录 PowPow | - |
| `createDigitalHuman` | 创建数字人 | 2 枚 |
| `listDigitalHumans` | 列出数字人 | - |
| `chat` | 与数字人聊天 | - |
| `renew` | 续期数字人 | 1 枚 |
| `checkBadges` | 检查徽章余额 | - |

## 版本

v1.1.0 - 支持 PowPow OpenClaw API 集成
