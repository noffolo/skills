// @ts-nocheck
/**
 * OpenClaw POWPOW Integration Skill
 * 
 * 功能：
 * 1. POWPOW用户注册/登录
 * 2. 数字人创建与管理
 * 3. 与数字人实时通信
 * 
 * 修复内容：
 * 1. 添加输入验证和XSS防护
 * 2. 添加速率限制
 * 3. 添加会话过期清理
 * 4. 优化错误处理
 * 5. 添加结构化日志
 * 
 * @author OpenClaw Team
 * @version 1.1.0
 */

import { Skill, SkillContext } from '@openclaw/core';
import { PowpowClient, PowpowAPIError, DigitalHuman, Logger } from './powpow-client';
import { Validator } from './utils/validator';
import { RateLimiter } from './utils/rate-limiter';
import { SESSION_CONFIG } from './utils/constants';

// Skill配置接口
export interface PowpowSkillConfig {
  powpowBaseUrl: string;
  powpowApiKey?: string;
  defaultLocation?: {
    lat: number;
    lng: number;
    name: string;
  };
}

// 用户会话状态
interface UserSession {
  powpowUserId?: string;
  powpowToken?: string;
  currentDigitalHuman?: DigitalHuman;
  isChatting: boolean;
  lastActivity: number;
}

export class PowpowSkill implements Skill {
  name = 'powpow-integration';
  description = 'Integration with POWPOW platform for digital human management and communication';
  version = '1.0.3';

  private client: PowpowClient;
  private config: PowpowSkillConfig;
  private userSessions: Map<string, UserSession> = new Map();
  private rateLimiter: RateLimiter;
  private cleanupInterval?: NodeJS.Timeout;
  private logger: Logger;

  // 能力定义
  capabilities = [
    {
      name: 'register',
      description: 'Register a new POWPOW account',
      parameters: {
        username: { type: 'string', required: true, description: 'Username for POWPOW (3-50 chars, alphanumeric)' },
      },
      handler: this.handleRegister.bind(this),
    },
    {
      name: 'login',
      description: 'Login to existing POWPOW account',
      parameters: {
        username: { type: 'string', required: true },
      },
      handler: this.handleLogin.bind(this),
    },
    {
      name: 'createDigitalHuman',
      description: 'Create a digital human on POWPOW map (requires 2 badges)',
      parameters: {
        name: { type: 'string', required: true, description: 'Digital human name (1-100 chars)' },
        description: { type: 'string', required: true, description: 'Description/personality (max 500 chars)' },
        lat: { type: 'number', required: false, description: 'Latitude (-90 to 90)' },
        lng: { type: 'number', required: false, description: 'Longitude (-180 to 180)' },
        locationName: { type: 'string', required: false, description: 'Location name' },
      },
      handler: this.handleCreateDigitalHuman.bind(this),
    },
    {
      name: 'listDigitalHumans',
      description: 'List all your digital humans',
      parameters: {},
      handler: this.handleListDigitalHumans.bind(this),
    },
    {
      name: 'chat',
      description: 'Start chatting with a digital human',
      parameters: {
        dhId: { type: 'string', required: true, description: 'Digital human ID' },
        message: { type: 'string', required: true, description: 'Message to send (max 2000 chars)' },
      },
      handler: this.handleChat.bind(this),
    },
    {
      name: 'renew',
      description: 'Renew a digital human for 30 days (requires 1 badge)',
      parameters: {
        dhId: { type: 'string', required: true, description: 'Digital human ID to renew' },
      },
      handler: this.handleRenew.bind(this),
    },
    {
      name: 'checkBadges',
      description: 'Check your badge balance',
      parameters: {},
      handler: this.handleCheckBadges.bind(this),
    },
    {
      name: 'help',
      description: 'Show available commands',
      parameters: {},
      handler: this.handleHelp.bind(this),
    },
  ];

  /**
   * Skill初始化
   */
  async initialize(context: SkillContext): Promise<void> {
    this.config = context.getConfig('powpow') as PowpowSkillConfig;
    
    if (!this.config?.powpowBaseUrl) {
      throw new Error('POWPOW base URL is required in skill configuration');
    }

    // 初始化日志
    this.logger = {
      debug: (msg, meta) => context.logger.debug(`[POWPOW] ${msg}`, meta),
      info: (msg, meta) => context.logger.info(`[POWPOW] ${msg}`, meta),
      warn: (msg, meta) => context.logger.warn(`[POWPOW] ${msg}`, meta),
      error: (msg, err, meta) => context.logger.error(`[POWPOW] ${msg}`, err, meta),
    };

    // 初始化客户端
    this.client = new PowpowClient({
      baseUrl: this.config.powpowBaseUrl,
      apiKey: this.config.powpowApiKey,
      logger: this.logger,
    });

    // 初始化速率限制器
    this.rateLimiter = new RateLimiter();

    // 启动会话清理定时器
    this.cleanupInterval = setInterval(() => {
      this.cleanupExpiredSessions();
    }, SESSION_CONFIG.CLEANUP_INTERVAL);

    this.logger.info('POWPOW skill initialized', {
      baseUrl: this.config.powpowBaseUrl,
      hasApiKey: !!this.config.powpowApiKey,
    });
  }

  /**
   * 获取或创建用户会话
   */
  private getSession(userId: string): UserSession {
    if (!this.userSessions.has(userId)) {
      this.userSessions.set(userId, { 
        isChatting: false,
        lastActivity: Date.now()
      });
    } else {
      // 更新活动时间
      const session = this.userSessions.get(userId)!;
      session.lastActivity = Date.now();
    }
    return this.userSessions.get(userId)!;
  }

  /**
   * 清理过期会话
   */
  private cleanupExpiredSessions(): void {
    const now = Date.now();
    let cleanedCount = 0;

    for (const [userId, session] of this.userSessions.entries()) {
      if (now - session.lastActivity > SESSION_CONFIG.TIMEOUT) {
        // 如果正在聊天，先断开连接
        if (session.isChatting) {
          this.client.disconnect();
        }
        this.userSessions.delete(userId);
        cleanedCount++;
      }
    }

    if (cleanedCount > 0) {
      this.logger.info(`Cleaned up ${cleanedCount} expired sessions`);
    }
  }

  /**
   * 检查速率限制
   */
  private checkRateLimit(userId: string, action: string): string | null {
    if (!this.rateLimiter.isAllowed(userId)) {
      const resetTime = this.rateLimiter.getResetTime(userId);
      const waitSeconds = resetTime ? Math.ceil((resetTime - Date.now()) / 1000) : 60;
      return `❌ Rate limit exceeded. Please try again in ${waitSeconds} seconds.`;
    }
    return null;
  }

  /**
   * 处理用户注册
   */
  private async handleRegister(
    params: { username: string },
    context: SkillContext
  ): Promise<string> {
    // 速率限制检查
    const rateLimitError = this.checkRateLimit(context.userId, 'register');
    if (rateLimitError) return rateLimitError;

    // 验证用户名
    const usernameValidation = Validator.validateUsername(params.username);
    if (!usernameValidation.valid) {
      return `❌ ${usernameValidation.error}`;
    }

    this.logger.info('Processing registration', { 
      username: params.username,
      openclawUserId: context.userId 
    });

    try {
      const result = await this.client.registerUser({
        username: Validator.sanitizeString(params.username),
        email: '', // 不再使用
        password: '', // 不再使用
        source: 'openclaw',
        openclawUserId: context.userId,
      });

      // 保存会话
      const session = this.getSession(context.userId);
      session.powpowUserId = result.userId;

      // 清除速率限制记录（注册成功）
      this.rateLimiter.clearForKey(context.userId);

      this.logger.info('Registration successful', { 
        powpowUserId: result.userId,
        openclawUserId: context.userId 
      });

      return `✅ Registration successful!\n` +
        `👤 User ID: ${result.userId}\n` +
        `🏅 Initial badges: ${result.badges}\n` +
        `\nYou can now create digital humans using the 'createDigitalHuman' command.`;
    } catch (error) {
      if (error instanceof PowpowAPIError) {
        this.logger.error('Registration failed', error, { 
          username: params.username,
          status: error.statusCode 
        });
        return `❌ Registration failed: ${error.message}`;
      }
      this.logger.error('Unexpected registration error', error as Error);
      return '❌ An unexpected error occurred during registration.';
    }
  }

  /**
   * 处理用户登录
   */
  private async handleLogin(
    params: { username: string },
    context: SkillContext
  ): Promise<string> {
    // 速率限制检查
    const rateLimitError = this.checkRateLimit(context.userId, 'login');
    if (rateLimitError) return rateLimitError;

    // 验证用户名
    const usernameValidation = Validator.validateUsername(params.username);
    if (!usernameValidation.valid) {
      return `❌ ${usernameValidation.error}`;
    }

    this.logger.info('Processing login', { 
      username: params.username,
      openclawUserId: context.userId 
    });

    try {
      const result = await this.client.loginUser({
        username: Validator.sanitizeString(params.username),
        password: '', // 不再使用
      });

      // 保存会话
      const session = this.getSession(context.userId);
      session.powpowUserId = result.userId;
      session.powpowToken = result.token;
      this.client.setAuthToken(result.token);

      // 清除速率限制记录（登录成功）
      this.rateLimiter.clearForKey(context.userId);

      this.logger.info('Login successful', { 
        powpowUserId: result.userId,
        openclawUserId: context.userId 
      });

      return `✅ Login successful!\n` +
        `👤 User ID: ${result.userId}\n` +
        `🏅 Available badges: ${result.badges}`;
    } catch (error) {
      if (error instanceof PowpowAPIError) {
        this.logger.warn('Login failed', { 
          username: params.username,
          status: error.statusCode 
        });
        return `❌ Login failed: ${error.message}`;
      }
      this.logger.error('Unexpected login error', error as Error);
      return '❌ An unexpected error occurred during login.';
    }
  }

  /**
   * 处理创建数字人
   */
  private async handleCreateDigitalHuman(
    params: {
      name: string;
      description: string;
      lat?: number;
      lng?: number;
      locationName?: string;
    },
    context: SkillContext
  ): Promise<string> {
    const session = this.getSession(context.userId);

    // 检查是否已登录
    if (!session.powpowUserId) {
      return '⚠️ Please login first using: login username=<your_username> password=<your_password>';
    }

    // 验证名称
    const nameValidation = Validator.validateDigitalHumanName(params.name);
    if (!nameValidation.valid) {
      return `❌ ${nameValidation.error}`;
    }

    // 验证描述
    const descValidation = Validator.validateDescription(params.description);
    if (!descValidation.valid) {
      return `❌ ${descValidation.error}`;
    }

    // 验证坐标
    const lat = params.lat ?? this.config.defaultLocation?.lat ?? 39.9042;
    const lng = params.lng ?? this.config.defaultLocation?.lng ?? 116.4074;
    const coordValidation = Validator.validateCoordinates(lat, lng);
    if (!coordValidation.valid) {
      return `❌ ${coordValidation.error}`;
    }

    const locationName = params.locationName 
      ? Validator.sanitizeString(params.locationName)
      : this.config.defaultLocation?.name ?? 'Beijing';

    this.logger.info('Creating digital human', { 
      name: params.name,
      userId: session.powpowUserId 
    });

    try {
      const dh = await this.client.createDigitalHuman({
        name: Validator.sanitizeString(params.name),
        description: Validator.sanitizeString(params.description),
        lat,
        lng,
        locationName,
        userId: session.powpowUserId,
      });

      // 保存当前数字人
      session.currentDigitalHuman = dh;

      this.logger.info('Digital human created', { 
        dhId: dh.id,
        name: dh.name 
      });

      return `✅ Digital human created successfully!\n` +
        `🎭 Name: ${dh.name}\n` +
        `🆔 ID: ${dh.id}\n` +
        `📍 Location: ${dh.locationName} (${dh.lat}, ${dh.lng})\n` +
        `⏰ Expires at: ${new Date(dh.expiresAt).toLocaleString()}\n` +
        `\nYou can now chat with it using: chat dhId=${dh.id} message=<your_message>`;
    } catch (error) {
      if (error instanceof PowpowAPIError) {
        if (error.statusCode === 402) {
          return `❌ ${error.message}\n\n` +
            `You can check your badge balance using: checkBadges`;
        }
        this.logger.error('Failed to create digital human', error);
        return `❌ Failed to create digital human: ${error.message}`;
      }
      this.logger.error('Unexpected error creating digital human', error as Error);
      return '❌ An unexpected error occurred.';
    }
  }

  /**
   * 处理列出数字人
   */
  private async handleListDigitalHumans(
    params: {},
    context: SkillContext
  ): Promise<string> {
    const session = this.getSession(context.userId);

    if (!session.powpowUserId) {
      return '⚠️ Please login first using: login username=<your_username> password=<your_password>';
    }

    try {
      const dhs = await this.client.getUserDigitalHumans(session.powpowUserId);

      if (dhs.length === 0) {
        return '📭 You have no digital humans yet.\n' +
          'Create one using: createDigitalHuman name=<name> description=<description>';
      }

      let response = `🎭 You have ${dhs.length} digital human(s):\n\n`;
      
      dhs.forEach((dh, index) => {
        const daysLeft = Math.ceil(
          (new Date(dh.expiresAt).getTime() - Date.now()) / (1000 * 60 * 60 * 24)
        );
        const status = dh.isActive ? '✅' : '❌';
        
        response += `${index + 1}. ${status} ${dh.name}\n` +
          `   ID: ${dh.id}\n` +
          `   📍 ${dh.locationName}\n` +
          `   ⏰ ${daysLeft} days left\n` +
          `   💬 Chat: chat dhId=${dh.id} message=hello\n\n`;
      });

      return response;
    } catch (error) {
      if (error instanceof PowpowAPIError) {
        this.logger.error('Failed to list digital humans', error);
        return `❌ Failed to list digital humans: ${error.message}`;
      }
      this.logger.error('Unexpected error listing digital humans', error as Error);
      return '❌ An unexpected error occurred.';
    }
  }

  /**
   * 处理聊天
   */
  private async handleChat(
    params: { dhId: string; message: string },
    context: SkillContext
  ): Promise<string> {
    const session = this.getSession(context.userId);

    if (!session.powpowUserId) {
      return '⚠️ Please login first';
    }

    // 验证数字人ID
    const dhIdValidation = Validator.validateDigitalHumanId(params.dhId);
    if (!dhIdValidation.valid) {
      return `❌ ${dhIdValidation.error}`;
    }

    // 验证消息
    const messageValidation = Validator.validateMessage(params.message);
    if (!messageValidation.valid) {
      return `❌ ${messageValidation.error}`;
    }

    // 如果已经在聊天中，先断开
    if (session.isChatting) {
      this.client.disconnect();
      session.isChatting = false;
    }

    this.logger.info('Starting chat', { 
      dhId: params.dhId,
      userId: session.powpowUserId 
    });

    try {
      // 建立SSE连接
      this.client.connectToDigitalHuman(
        params.dhId,
        (message) => {
          // 收到数字人回复，通过OpenClaw发送给用户
          context.sendMessage({
            content: message.content,
            metadata: {
              sender: 'digital_human',
              timestamp: message.timestamp,
            },
          });
        },
        (error) => {
          this.logger.error('Chat connection error', error, { dhId: params.dhId });
          context.sendMessage({
            content: '⚠️ Connection lost. Please try again.',
          });
          session.isChatting = false;
        }
      );

      session.isChatting = true;

      // 发送用户消息
      await this.client.sendMessage(params.dhId, params.message);

      return `💬 Message sent to digital human. Waiting for response...`;
    } catch (error) {
      session.isChatting = false;
      if (error instanceof PowpowAPIError) {
        this.logger.error('Chat failed', error, { dhId: params.dhId });
        return `❌ Chat failed: ${error.message}`;
      }
      this.logger.error('Unexpected chat error', error as Error, { dhId: params.dhId });
      return '❌ An unexpected error occurred.';
    }
  }

  /**
   * 处理续期
   */
  private async handleRenew(
    params: { dhId: string },
    context: SkillContext
  ): Promise<string> {
    const session = this.getSession(context.userId);

    if (!session.powpowUserId) {
      return '⚠️ Please login first';
    }

    // 验证数字人ID
    const dhIdValidation = Validator.validateDigitalHumanId(params.dhId);
    if (!dhIdValidation.valid) {
      return `❌ ${dhIdValidation.error}`;
    }

    this.logger.info('Renewing digital human', { 
      dhId: params.dhId,
      userId: session.powpowUserId 
    });

    try {
      const dh = await this.client.renewDigitalHuman(params.dhId);
      
      this.logger.info('Digital human renewed', { 
        dhId: params.dhId,
        newExpiry: dh.expiresAt 
      });
      
      return `✅ Digital human renewed successfully!\n` +
        `🎭 Name: ${dh.name}\n` +
        `⏰ New expiration: ${new Date(dh.expiresAt).toLocaleString()}\n` +
        `📅 Extended by 30 days`;
    } catch (error) {
      if (error instanceof PowpowAPIError) {
        if (error.statusCode === 402) {
          return `❌ ${error.message}`;
        }
        this.logger.error('Failed to renew digital human', error);
        return `❌ Failed to renew: ${error.message}`;
      }
      this.logger.error('Unexpected error renewing digital human', error as Error);
      return '❌ An unexpected error occurred.';
    }
  }

  /**
   * 处理检查徽章
   */
  private async handleCheckBadges(
    params: {},
    context: SkillContext
  ): Promise<string> {
    const session = this.getSession(context.userId);

    if (!session.powpowUserId) {
      return '⚠️ Please login first';
    }

    try {
      const badges = await this.client.checkBadges(session.powpowUserId);
      
      return `🏅 Your badge balance:\n` +
        `   Count: ${badges.count}\n` +
        `   Type: ${badges.type}\n\n` +
        `💡 You need:\n` +
        `   • 2 badges to create a digital human\n` +
        `   • 1 badge to renew a digital human`;
    } catch (error) {
      if (error instanceof PowpowAPIError) {
        this.logger.error('Failed to check badges', error);
        return `❌ Failed to check badges: ${error.message}`;
      }
      this.logger.error('Unexpected error checking badges', error as Error);
      return '❌ An unexpected error occurred.';
    }
  }

  /**
   * 处理帮助
   */
  private async handleHelp(params: {}, context: SkillContext): Promise<string> {
    return `🎭 POWPOW Digital Human Skill - Available Commands\n\n` +
      `Authentication:\n` +
      `  • register username=<name> - Create new account\n` +
      `  • login username=<name> - Login to existing account\n\n` +
      `Digital Human Management:\n` +
      `  • createDigitalHuman name=<name> description=<desc> [lat=<lat> lng=<lng>] - Create (2 badges)\n` +
      `  • listDigitalHumans - List all your digital humans\n` +
      `  • renew dhId=<id> - Renew for 30 days (1 badge)\n\n` +
      `Communication:\n` +
      `  • chat dhId=<id> message=<text> - Chat with a digital human\n\n` +
      `Account:\n` +
      `  • checkBadges - Check your badge balance\n` +
      `  • help - Show this help message`;
  }

  /**
   * Skill清理
   */
  async destroy(): Promise<void> {
    // 停止会话清理定时器
    if (this.cleanupInterval) {
      clearInterval(this.cleanupInterval);
      this.cleanupInterval = undefined;
    }

    // 断开所有SSE连接
    this.client.disconnect();
    
    // 清理会话
    this.userSessions.clear();
    
    // 清理速率限制记录
    this.rateLimiter.clear();

    this.logger.info('POWPOW skill destroyed');
  }
}

// 导出Skill类
export default PowpowSkill;
