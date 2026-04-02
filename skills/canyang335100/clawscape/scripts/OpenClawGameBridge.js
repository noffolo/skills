/**
 * OpenClawGameBridge - 游戏桥接服务
 * 
 * 功能：
 * 1. 接收游戏客户端的连接注册
 * 2. 保存客户端连接（playerUid -> ws）
 * 3. 转发OpenClaw的指令到客户端
 */

const WebSocket = require('ws');

class OpenClawGameBridge {
    constructor(port = 18765) {
        this.port = port;
        this.wss = null;
        this.clients = new Map();
        this.heartbeatInterval = null;
        this.perceptions = new Map(); // 存储客户端感知数据
        this.currentMapId = null; // 当前地图ID

        this.startServer();
    }
    
    startServer() {
        this.wss = new WebSocket.Server({ port: this.port });
        
        // 心跳定时器
        this.heartbeatInterval = setInterval(() => {
            for (const [playerUid, clientWs] of this.clients) {
                if (clientWs.readyState === WebSocket.OPEN) {
                    // 发送ping保持连接
                    clientWs.ping();
                }
            }
        }, 30000); // 每30秒发送一次ping
        
        this.wss.on('connection', (ws) => {
            console.log('[Bridge] 新客户端连接');
            
            ws.isAlive = true;
            
            ws.on('pong', () => {
                ws.isAlive = true;
            });
            
            ws.on('message', (data) => {
                try {
                    const msg = JSON.parse(data);
                    console.log('[Bridge] 收到消息:', msg.type, JSON.stringify(msg).substring(0, 200));
                    this.handleMessage(msg, ws);
                } catch (error) {
                    console.error('[Bridge] 消息解析错误:', error);
                }
            });
            
            ws.on('close', () => {
                //console.log('[Bridge] 客户端断开,');
                for (const [playerUid, clientWs] of this.clients) {
                    if (clientWs === ws) {
                        this.clients.delete(playerUid);
                        console.log('[Bridge] 已移除客户端:', playerUid);
                        break;
                    }
                }
            });
            
            ws.on('error', (error) => {
                console.error('[Bridge] WebSocket错误:', error);
            });
        });
        
        this.wss.on('error', (error) => {
            console.error('[Bridge] 服务器错误:', error);
        });
        
        console.log(`[Bridge] 游戏桥接服务已启动: ws://localhost:${this.port}`);
    }
    
    handleMessage(msg, ws) {
        switch (msg.type) {
            case 'ai_register':
                this.onClientRegister(msg, ws);
                break;
                
            case 'ai_unregister':
                this.onClientUnregister(msg);
                break;
                
            case 'ai_perception':
                this.onClientPerception(msg);
                break;
                
            // AI控制端发送指令到指定玩家
            case 'ai_send_to_player':
                this.onSendToPlayer(msg);
                break;
                
            // AI控制端请求感知数据
            case 'ai_request_perception':
                this.onRequestPerception(msg);
                break;
                
            // AIController主动上报的感知数据
            case 'ai_perception_data':
                this.onPerceptionData(msg);
                break;
                
            // AIController发送的命令（包含地图信息等）
            case 'send_command':
                this.onSendCommand(msg);
                break;

            // AIController发送的地图信息（单独一个消息类型）
            case 'send_map_info':
                this.onSend_map_info(msg);
                break;

            // AI控制端请求地图信息更新
            case 'ai_request_map_update':
                this.onRequestMapUpdate(msg);
                break;
        }
    }
    
    // 处理命令消息（来自AIController）
    onSendCommand(msg) {
        const playerUid = msg.player_uid;
        const mapInfor = msg.mapInfor;
        
        if (!mapInfor) return;
        
        if (mapInfor.cmd === 'map_info') {
            // 存储地图信息
            this.mapInfo = this.mapInfo || {};
            this.mapInfo[mapInfor.map_id] = {
                mapId: mapInfor.map_id,
                mapWidth: mapInfor.map_width,
                mapHeight: mapInfor.map_height,
                gridInfo: mapInfor.grid_info
            };
            // 设置为当前地图
            this.currentMapInfo = this.mapInfo[mapInfor.map_id];
            console.log(`[Bridge] 收到地图信息: mapId=${mapInfor.map_id}, size=${mapInfor.map_width}x${mapInfor.map_height}`);
        }
    }
    
    // 处理地图信息（来自AIController，单独消息类型）
    onSend_map_info(msg) {
        const playerUid = msg.player_uid;
        const mapInfor = msg.mapInfor;
        
        if (!mapInfor) return;
        
        // 只在 mapId 变化时更新
        if (this.currentMapId !== mapInfor.map_id) {
            this.currentMapId = mapInfor.map_id;
            this.mapInfo = this.mapInfo || {};
            this.mapInfo[mapInfor.map_id] = {
                mapId: mapInfor.map_id,
                mapWidth: mapInfor.map_width,
                mapHeight: mapInfor.map_height,
                gridInfo: mapInfor.grid_info
            };
            this.currentMapInfo = this.mapInfo[mapInfor.map_id];
            console.log(`[Bridge] 地图信息更新: mapId=${mapInfor.map_id}, size=${mapInfor.map_width}x${mapInfor.map_height}`);
            
            // 通知 OpenClaw 地图已切换
            const openClawClient = this.clients.get('OPENCLAW');
            if (openClawClient && openClawClient.readyState === WebSocket.OPEN) {
                openClawClient.send(JSON.stringify({
                    type: 'ai_map_changed',
                    mapId: mapInfor.map_id,
                    mapWidth: mapInfor.map_width,
                    mapHeight: mapInfor.map_height
                }));
            }
        } else {
            console.log(`[Bridge] 地图未切换，跳过更新: mapId=${mapInfor.map_id}`);
        }
    }

    // AI控制端请求地图信息更新
    onRequestMapUpdate(msg) {
        const playerUid = msg.playerUid;
        const targetWs = this.clients.get(playerUid);
        if (targetWs && targetWs.readyState === WebSocket.OPEN) {
            targetWs.send(JSON.stringify({ type: 'ai_request_map_update' }));
            console.log(`[Bridge] 请求 ${playerUid} 更新地图信息`);
        }
    }
    
    // 检查坐标是否可通行
    isWalkable(mapId, x, y) {
        const map = this.mapInfo ? this.mapInfo[mapId] : null;
        if (!map || !map.gridInfo) return true; // 无数据默认可通行
        
        const grid = map.gridInfo;
        if (x < 0 || x >= map.mapWidth || y < 0 || y >= map.mapHeight) return false;
        
        // gridInfo格式：[x][y] = true可通行，false障碍
        if (grid[x] && grid[x][y] !== undefined) {
            return grid[x][y] === true;
        }
        return true;
    }
    
    // 查找距离指定坐标最近的可行走位置
    findNearestWalkable(x, y, map) {
        const range = 5;
        for (let d = 1; d <= range; d++) {
            for (let dx = -d; dx <= d; dx++) {
                for (let dy = -d; dy <= d; dy++) {
                    const nx = x + dx;
                    const ny = y + dy;
                    if (this.isWalkable(map.mapId, nx, ny)) {
                        return { x: nx, y: ny };
                    }
                }
            }
        }
        return null;
    }
    
    // AI控制端发送指令到指定玩家
    onSendToPlayer(msg) {
        const targetPlayerUid = msg.targetPlayerUid;
        const command = msg.command;
        
        // 如果是移动指令，检查目标是否可通行
        if (command.type === 'move' && this.currentMapInfo) {
            const x = Math.round(command.x);
            const y = Math.round(command.y);
            
            if (!this.isWalkable(this.currentMapInfo.mapId, x, y)) {
                console.log(`[Bridge] 目标 ${x},${y} 不可通行，查找最近可行走位置`);
                const nearest = this.findNearestWalkable(x, y, this.currentMapInfo);
                if (nearest) {
                    console.log(`[Bridge] 已调整为最近可行走位置: ${nearest.x},${nearest.y}`);
                    command.x = nearest.x;
                    command.y = nearest.y;
                } else {
                    console.warn(`[Bridge] 附近无可行走位置`);
                    return; // 不发送不可通行的移动
                }
            }
        }
        
        const targetWs = this.clients.get(targetPlayerUid);
        if (targetWs && targetWs.readyState === WebSocket.OPEN) {
            targetWs.send(JSON.stringify({
                type: 'ai_control',
                command: command
            }));
            console.log(`[Bridge] ✅ 转发指令到 ${targetPlayerUid}:`, command);
        } else {
            console.warn(`[Bridge] ❌ 玩家 ${targetPlayerUid} 不在线或连接无效`);
        }
    }
    
    onClientRegister(msg, ws) {
        // 处理空的playerUid
        let playerUid = msg.playerUid;
        if (!playerUid || playerUid === '') {
            playerUid = 'player_001';
            console.log(`[Bridge] ⚠️ 玩家ID为空，已自动设置为: player_001`);
        }
        
        this.clients.set(playerUid, ws);
        console.log(`[Bridge] ⭐ 客户端注册: playerUid=${playerUid}, ws=${ws.readyState}`);
        console.log(`[Bridge] 当前保存的客户端:`, Array.from(this.clients.keys()));
        
        ws.send(JSON.stringify({
            type: 'ai_registered',
            playerUid: playerUid,
            status: 'ok'
        }));
        
        // 如果是游戏客户端注册，通知OpenClaw
        // 检查是否有OpenClaw控制端连接
        const openClawClient = this.clients.get('OPENCLAW');
        if (openClawClient && openClawClient.readyState === WebSocket.OPEN) {
            openClawClient.send(JSON.stringify({
                type: 'ai_client_connected',
                playerUid: playerUid
            }));
        }
        
        console.log(`[Bridge] 已通知OpenClaw：玩家 ${playerUid} 已准备好`);
    }
    
    onClientUnregister(msg) {
        const playerUid = msg.playerUid;
        if (this.clients.has(playerUid)) {
            this.clients.delete(playerUid);
            console.log(`[Bridge] 客户端取消注册: ${playerUid}`);
        }
    }
    
    onClientPerception(msg) {
        console.log(`[Bridge] 收到感知数据: ${msg.playerUid}`);
        // 存储感知数据
        if (msg.perception) {
            this.perceptions.set(msg.playerUid, msg.perception);
        }
        
        // 转发感知数据给OpenClaw控制端
        const openClawClient = this.clients.get('OPENCLAW');
        if (openClawClient && openClawClient.readyState === WebSocket.OPEN) {
            openClawClient.send(JSON.stringify({
                type: 'ai_perception_update',
                playerUid: msg.playerUid,
                perception: msg.perception
            }));
        }
    }
    
    // 处理感知数据（来自AIController的主动上报）
    onPerceptionData(msg) {
        console.log(`[Bridge] 收到AIController感知数据: playerUid=${msg.playerUid}`);
        console.log(`[Bridge] perception.self=`, msg.perception?.self);
        console.log(`[Bridge] perception.self.nodeName=`, msg.perception.self.nodeName);
        console.log(`[Bridge] perception.robots=`, msg.perception?.robots);
        
        // 转发给OpenClaw控制端
        const openClawClient = this.clients.get('OPENCLAW');
        if (openClawClient && openClawClient.readyState === WebSocket.OPEN) {
            try {
                // robots等字段可能是Map，需要转成数组
                const toArray = (v) => {
                    if (!v) return [];
                    if (Array.isArray(v)) return v;
                    if (v instanceof Map) return Array.from(v.entries()).map(([k, node]) => ({ playerUid: k, node: node ? node.name || k : null }));
                    return [];
                };
                const perceptionData = {
                    self: msg.perception?.self ? {
                        position: msg.perception.self?.position,
                        mapId: msg.perception.self?.mapId
                    } : null,
                    position: msg.perception?.position,
                    mapId: msg.perception?.mapId,
                    robots: toArray(msg.perception?.robots),
                    npcs: msg.perception?.npcs || [],
                    monsters: msg.perception?.monsters || [],
                    players: msg.perception?.players || []
                };
                openClawClient.send(JSON.stringify({
                    type: 'ai_perception_data',
                    playerUid: msg.playerUid,
                    perception: perceptionData
                }));
                console.log(`[Bridge] 感知数据转发成功`);
            } catch (e) {
                console.error(`[Bridge] 感知数据序列化失败:`, e.message);
                // 只发 robots 试试
                try {
                    openClawClient.send(JSON.stringify({
                        type: 'ai_perception_data',
                        playerUid: msg.playerUid,
                        perception: { robots: msg.perception?.robots || [] }
                    }));
                } catch (e2) {
                    console.error(`[Bridge] robots也发不出去:`, e2.message);
                }
            }
        }
    }
    
    // AI控制端请求感知数据
    onRequestPerception(msg) {
        const targetPlayerUid = msg.targetPlayerUid;
        const perception = this.perceptions.get(targetPlayerUid);
        
        if (perception) {
            console.log(`[Bridge] 转发感知数据到 OpenClaw: ${targetPlayerUid}`);
            // 这里可以通过某种方式通知OpenClaw，但目前WebSocket是客户端连接过来的
            // 所以感知数据会通过客户端的onMessage返回
            return perception;
        } else {
            console.log(`[Bridge] 没有 ${targetPlayerUid} 的感知数据`);
            return null;
        }
    }
    
    setAIMode(playerUid, enabled) {
        const ws = this.clients.get(playerUid);
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                type: 'ai_set_mode',
                enabled: enabled
            }));
            console.log(`[Bridge] 发送模式设置: ${playerUid} -> ${enabled}`);
            return true;
        } else {
            console.warn(`[Bridge] 玩家不在线: ${playerUid}`);
            return false;
        }
    }
    
    sendCommand(playerUid, command) {
        console.log(`[Bridge] ⭐ 尝试发送指令到 ${playerUid}`);
        console.log(`[Bridge] 当前保存的客户端:`, Array.from(this.clients.keys()));
        
        const ws = this.clients.get(playerUid);
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                type: 'ai_control',
                command: command
            }));
            console.log(`[Bridge] ✅ 发送指令成功到 ${playerUid}:`, command);
            return true;
        } else {
            console.warn(`[Bridge] ❌ 玩家不在线或ws无效: ${playerUid}, ws=${ws ? ws.readyState : 'undefined'}`);
            return false;
        }
    }
    
    requestSync(playerUid) {
        const ws = this.clients.get(playerUid);
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                type: 'ai_sync_request'
            }));
            return true;
        }
        return false;
    }
    
    getStatus() {
        return {
            port: this.port,
            clientCount: this.clients.size,
            clients: Array.from(this.clients.keys())
        };
    }
    
    stop() {
        if (this.heartbeatInterval) {
            clearInterval(this.heartbeatInterval);
            this.heartbeatInterval = null;
        }
        if (this.wss) {
            this.wss.close();
            this.wss = null;
        }
        console.log('[Bridge] 服务已停止');
    }
}

module.exports = OpenClawGameBridge;
