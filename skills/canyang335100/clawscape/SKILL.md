---
name: game-takeover
description: 接管游戏角色控制。当需要：接管游戏角色、发送移动指令、发送聊天消息、与NPC交互、获取感知数据时使用。游戏为「口袋冒险大陆」，通过WebSocket桥接（端口18765）控制AI角色。项目路径 F:\maoxiandalu\。
---

# Game Takeover

通过 OpenClaw 接管「口袋冒险大陆」游戏角色的控制权。

## 游戏信息

| 项目 | 值 |
|------|-----|
| 游戏 URL | `https://www.mxdl.online/index2.html` |
| 桥接端口 | 18765（WebSocket） |
| 玩家 UID | `280181a14_10001` |
| 地图信息 | `gridInfo[x][y] = true` 可通行，`false` 障碍 |
| 示例地图 | mapId=5004, size=100×110 |

## 准备工作

### ⚠️ 操作顺序（必须严格遵守）

1. **先启动桥接服务**（端口 18765）
2. **再打开游戏**
3. **玩家点托管**（由用户手动操作）

> 顺序错误会导致玩家无法连接桥接。

### 1. AI 自动启动桥接

收到「接管游戏」指令时，**第一步**先启动桥接：

```bash
cd <skill目录>/scripts
npm install
node start_game_bridge.js
```

等待桥接就绪（约 1-2 秒）。

### 2. AI 自动打开游戏

桥接启动后，第二步打开游戏：

```
游戏 URL：https://www.mxdl.online/index2.html
```

### 3. 用户操作（AI 打开游戏后）

1. 在浏览器中登录自己的账号
2. 点击游戏内的「托管」按钮，让 AIController 连接桥接服务

> **注意**：必须由用户在游戏内主动点击「托管」，这一步无法由 AI 代完成。

### 2. 获取玩家 UID

AI 注册时使用 `OPENCLAW`，但这只是标识符。游戏客户端的真实 UID 由桥接服务通知：

```
{ "type": "ai_client_connected", "playerUid": "280181a14_10001", ... }
```

后续发送指令时需使用这个真实 UID。

## 自动启动桥接流程

**每次收到控制指令时，AI 会自动按此流程执行：**

### Step 1：检查桥接是否运行

```javascript
const net = require('net');
const isPortInUse = (port) => new Promise((resolve) => {
    const client = new net.Socket();
    client.once('connect', () => { client.destroy(); resolve(true); });
    client.once('error', () => resolve(false));
    client.connect(port, '127.0.0.1');
});
```

### Step 2：桥接未运行则启动

```bash
cd <skill目录>/scripts
npm install
node start_game_bridge.js
```

### Step 3：等待桥接就绪后注册

```json
{ "type": "ai_register", "playerUid": "OPENCLAW" }
```

等待 `ai_client_connected` 消息，记录真实 `playerUid`（如 `8b7c7119c_10001`）。

### Step 4：感知当前位置

发 `get_perception` 获取 `self.position`，这是角色的当前坐标，**移动指令必须基于此坐标在 ±20 范围内**。

> ⚠️ 如果有多个游戏客户端同时连接，**以桥接日志中最新注册的客户端为准**。日志中 `当前保存的客户端: [...]` 列表的最后一项就是最新加入的。

## 控制指令

### 移动指令

```json
{
  "type": "ai_send_to_player",
  "targetPlayerUid": "280181a14_10001",
  "command": { "type": "move", "x": 12, "y": 39 }
}
```

> ⚠️ **移动前必须先感知当前位置**（get_perception 获取 self.position），A* 寻路单次移动范围建议控制在 ±20 格以内。

### 聊天指令

```json
{
  "type": "ai_send_to_player",
  "targetPlayerUid": "280181a14_10001",
  "command": { "type": "sendDialogue", "message": "大家好！" }
}
```

### NPC 交互

```json
{
  "type": "ai_send_to_player",
  "targetPlayerUid": "280181a14_10001",
  "command": { "type": "interact", "npcId": "npc_001" }
}
```

### 获取感知数据

```json
{
  "type": "ai_send_to_player",
  "targetPlayerUid": "280181a14_10001",
  "command": { "type": "get_perception" }
}
```

返回周围玩家、怪物、NPC 等信息。

## 完整通信流程

```
OpenClaw → Bridge(18765) → AIController → 游戏客户端
                                    ↓
                              执行指令（移动/聊天/交互）
```

1. OpenClaw 发送 `ai_register` 到 Bridge
2. Bridge 转发到游戏客户端
3. 游戏客户端回复 `ai_client_connected`（含真实UID）
4. OpenClaw 发送 `ai_send_to_player` + `command` 控制游戏角色
5. 如需感知数据，发送 `get_perception`

## 注意事项

1. **必须用户先点击托管**：AI 无法替代用户在游戏内操作
2. **gridInfo 格式**：`true` = 可通行，`false` = 障碍
3. **playerUid 每次可能不同**：重新连接后需重新获取真实 UID
4. **聊天字段名**：用 `content`，不是 `message`
5. **地图切换**：桥接收到 `ai_map_changed` 消息时表示地图已切换，gridInfo 会自动更新

## 资源

### scripts/

- `OpenClawGameBridge.js` - 桥接核心（WebSocket 服务端）
- `start_game_bridge.js` - 启动脚本
- `package.json` - 依赖配置（ws）
