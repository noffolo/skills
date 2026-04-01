// OpenClaw PowPow OpenClaw - Test Skill (1.0.0)
// In-memory mock implementation to mirror the interface surface of the real skill
import { Skill } from '@openclaw/core';

type UserRecord = {
  userId: string;
  token?: string;
  badges: number;
  digits?: DigitHuman[];
};

type DigitHuman = {
  id: string;
  name: string;
  description?: string;
  lat?: number;
  lng?: number;
  locationName?: string;
  expiresAt?: string;
};

class InMemoryStore {
  users = new Map<string, UserRecord>();
}

const store = new InMemoryStore();

export class PowpowOpenclawSkill implements Skill {
  name = 'powpow_openclaw';
  description = 'Independent test skill mirroring PowPow integration capabilities (OpenClaw)';
  version = '1.0.0';

  private store = store; // shared across instances

  private ensureUser(userId: string): UserRecord {
    if (!this.store.users.has(userId)) {
      this.store.users.set(userId, { userId, badges: 0, digits: [] });
    }
    // @ts-ignore
    return this.store.users.get(userId);
  }

  public async initialize(context: any): Promise<void> {
    // No-op for test skeleton
  }

  // Simple handlers emulating the surface of the real skill
  async register(params: { username: string }, context: any): Promise<string> {
    const userId = `user_${Date.now()}`;
    const rec: UserRecord = { userId, badges: 3 };
    this.store.users.set(context.userId ?? userId, rec);
    return `✅ Registered. UserID: ${userId}, badges: 3`;
  }

  async login(params: { username: string }, context: any): Promise<string> {
    const userId = `user_${Date.now()}`;
    const rec: UserRecord = { userId, token: `token_${userId}`, badges: 3 };
    this.store.users.set(context.userId ?? userId, rec);
    return `✅ Logged in. UserID: ${userId}, token: ${rec.token}`;
  }

  async createDigitalHuman(params: { name: string; description: string; lat?: number; lng?: number; locationName?: string }, context: any): Promise<string> {
    const user = this.ensureUser(context.userId);
    if (user.badges < 2) return '❌ 徽章不足';
    const dh: DigitHuman = { id: `dh_${Date.now()}`, name: params.name, description: params.description, lat: params.lat, lng: params.lng, locationName: params.locationName, expiresAt: new Date(Date.now() + 30 * 24 * 3600 * 1000).toISOString() };
    user.digits = user.digits ?? [];
    user.digits.push(dh);
    user.badges -= 2;
    return `✅ DigitalHuman created: ${dh.name} (id: ${dh.id})`;
  }

  async listDigitalHumans(params: any, context: any): Promise<string> {
    const user = this.store.users.get(context.userId) ?? { digits: [] } as any;
    const list = (user.digits ?? []);
    if (list.length === 0) return '没有数字人';
    return '数字人列表:\n' + list.map((d: DigitHuman, i: number) => ` ${i+1}. ${d.name} (${d.id})`).join('\n');
  }

  async chat(params: { dhId: string; message: string }, context: any): Promise<string> {
    return `对话模拟：收到来自 ${params.dhId} 的信息 → ${params.message}`;
  }

  async renew(params: { dhId: string }, context: any): Promise<string> {
    const user = this.store.users.get(context.userId) as UserRecord;
    if (!user) return '未找到用户';
    user.badges += 1;
    // not actually changing expires in this skeleton; just a placeholder
    return `续期成功，当前徽章：${user.badges}`;
  }

  async checkBadges(context: any): Promise<string> {
    const user = this.store.users.get(context.userId) as UserRecord;
    const count = user?.badges ?? 0;
    return `徽章余额: ${count}`;
  }

  async help(): Promise<string> {
    return '可用命令: register, login, createDigitalHuman, listDigitalHumans, chat, renew, checkBadges, help';
  }
}

export default PowpowOpenclawSkill;
