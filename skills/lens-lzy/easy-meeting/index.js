require('dotenv').config();
const express = require('express');
const FeishuService = require('./feishuService');
const dbStore = require('./dbStore');

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

const feishu = new FeishuService(
  process.env.FEISHU_APP_ID,
  process.env.FEISHU_APP_SECRET
);

/**
 * =========================================================
 * 供 OpenClaw Agent 调用的三组原子化 Skill 接口
 * =========================================================
 */

/**
 * 技能一：日历排期计算器
 * Agent 提取出人名单和期望时间段后，调用此接口索要 3 个左右空闲时间解
 */
app.post('/api/claw/calc-free-time', async (req, res) => {
  const { userIds, startTimeIso, endTimeIso, durationMinutes } = req.body;

  if (!userIds || !startTimeIso || !endTimeIso || !durationMinutes) {
    return res.status(400).json({ error: '缺少 userIds / startTimeIso / endTimeIso / durationMinutes' });
  }

  try {
    const timeOptions = await feishu.getCommonFreeTime(userIds, startTimeIso, endTimeIso, durationMinutes);
    res.json({
      success: true,
      message: timeOptions.length > 0 ? '找到了以下空闲时段' : '在给定时间内所有人无符合要求的共同空闲时段',
      data: { options: timeOptions }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

/**
 * 技能二：状态发包与意向收集单
 * Agent 利用第一步的结果自己生成了拟人化的话术，再调用此接口下发确认卡片，并开启一个 Session 挂起任务
 */
app.post('/api/claw/dispatch-cards', async (req, res) => {
  const { meetingTopic, userIds, timeSlots, agentMessage } = req.body;

  if (!meetingTopic || !userIds || !timeSlots || !agentMessage) {
    return res.status(400).json({ error: '参数缺失' });
  }

  try {
    // 1. 生成唯一事务 ID
    const sessionId = 'ses_' + Date.now() + '_' + Math.floor(Math.random() * 1000);

    // 2. 本地（持久化）存储事务状态
    dbStore.createSession(sessionId, {
      meetingTopic,
      userIds,
      timeSlots,
      agentMessage
    });

    // 3. 将包含 session_id 的独立带按钮卡片派给这几个人
    await feishu.sendPollCards(userIds, sessionId, meetingTopic, agentMessage, timeSlots);

    res.json({
      success: true,
      message: `已向 ${userIds.length} 人的飞书发送了排期卡片。此任务已建档挂起等待用户响应。`,
      data: { sessionId }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

const crypto = require('crypto');

/**
 * 校验飞书 Webhook 签名的工具函数
 * @returns {boolean|null} true: 校验通过; false: 校验失败; null: 未配置 Key 无法进行 HMAC 校验
 */
function verifyFeishuSignature(req) {
  const timestamp = req.headers['x-lark-request-timestamp'];
  const nonce = req.headers['x-lark-request-nonce'];
  const signature = req.headers['x-lark-signature'];
  const encryptKey = process.env.FEISHU_ENCRYPT_KEY;

  if (!encryptKey) return null; 
  
  const body = JSON.stringify(req.body);
  const content = timestamp + nonce + encryptKey + body;
  const hash = crypto.createHash('sha256').update(content).digest('hex');
  return hash === signature;
}

/**
 * 安全校验：校验 URL 是否合法，防止 SSRF
 */
function isSafeUrl(url) {
  if (!url) return false;
  try {
    const parsed = new URL(url);
    // 生产环境应增加更严格的域名白名单，此处至少确保是 HTTP(S) 且非极其异常输入
    return ['http:', 'https:'].includes(parsed.protocol);
  } catch (e) {
    return false;
  }
}

/**
 * =========================================================
 * 飞书卡片 Webhook，用于接管用户点击与后续决策
 * =========================================================
 */
app.post('/api/feishu/card-webhook', async (req, res) => {
  // 1. 安全校验逻辑 - 响应 OpenClaw 安全扫描关于“验证不足”的考量
  const signatureValid = verifyFeishuSignature(req);
  
  if (signatureValid === false) {
    console.error('[Security] HMAC Signature Match Failed');
    return res.status(403).send('Forbidden: Invalid Signature');
  } else if (signatureValid === null) {
    // 未配置密钥时，降级回 Verification Token，但必须匹配
    console.warn('[Security Warning] Running without FEISHU_ENCRYPT_KEY fallback to Token-based auth.');
    if (!process.env.FEISHU_VERIFICATION_TOKEN || req.body.token !== process.env.FEISHU_VERIFICATION_TOKEN) {
       console.error('[Security] Verification Token Missing or Mismatch');
       return res.status(403).send('Forbidden: Security Token Mismatch');
    }
  }

  // URL 验证（飞书后台配置时使用）
  if (req.body.type === 'url_verification') {
    return res.json({ challenge: req.body.challenge });
  }

  const actionObj = req.body.action;
  
  // 处理投递按钮点击逻辑
  if (actionObj && actionObj.value && actionObj.value.action === 'vote') {
    const { session_id, choice } = actionObj.value;
    const operatorId = req.body.open_id;

    console.log(`[Webhook] Session ${session_id} - User ${operatorId} clicked: ${choice}`);

    // 1. 更新此人的意向
    dbStore.updateParticipantState(session_id, operatorId, choice);

    // 2. 检查会话当前的共识状态
    const status = dbStore.checkSessionConsensus(session_id);

    // 回复给点击用户的局部视图 Toast 提示
    let toastMsg = '收到意向！请等待其他人反馈~';

    if (status.done) {
      if (status.result === 'agreed') {
        // ========== 全员同意，执行最终定档 ==========
        toastMsg = '你是最后一个确认者！全员意见统一，我正在执行系统排期...';
        
        const agreedSlot = JSON.parse(status.time);
        const sessionStore = dbStore.getSession(session_id);
        
        // 异步执行：创会并通知
        feishu.createMeeting(
          sessionStore.userIds, 
          sessionStore.meetingTopic, 
          agreedSlot.start_time, 
          agreedSlot.end_time
        ).catch(err => console.error('[Meeting Error]', err));
        
      } else if (status.result === 'conflict') {
        // ========== 唤醒唤醒端点：排期冲突，需 LLM 决策 ==========
        toastMsg = '由于存在冲突或有人没空，排期进程暂停。助手已记录并将寻求下一套方案！';

        console.log(`[ALERT] 排期冲突触发：会话 ${session_id} 需要回复人工或重议。`);
        
        // 关键唤醒逻辑：明确执行外部调用
        const wakeEndpoint = process.env.OPENCLAW_WAKE_ENDPOINT;
        if (isSafeUrl(wakeEndpoint)) {
          try {
            console.log(`[Wakeup] 正在主动唤醒 Agent 端点: ${wakeEndpoint}`);
            const response = await fetch(wakeEndpoint, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                sessionId: session_id,
                event: 'schedule_conflict',
                message: '大家排期时间无法协调，或者均选择了暂无时间。请你分析冲突情况，主动跟用户生成安抚话术或重新提出另外一周的时间方案进行斡旋。'
              })
            });
            const wakeData = await response.json();
            console.log(`[Wakeup] Agent 响应接收:`, JSON.stringify(wakeData));
          } catch (wakeErr) {
            console.warn(`[Wakeup Warning] 唤醒请求失败(非致命):`, wakeErr.message);
          }
        } else {
          console.warn('[Security/Config] OPENCLAW_WAKE_ENDPOINT 未配置或不合法，跳过唤醒。');
        }

      }
    }

    // 给飞书立刻回包
    return res.json({ toast: { type: 'success', content: toastMsg } });
  }

  res.status(200).send('ok');
});


app.listen(port, () => {
  console.log(`[OpenClaw Agent] 排期原子服务启动, 监听端口: ${port}`);
});
