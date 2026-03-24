/**
 * 速率限制器
 * 防止暴力破解和滥用
 */

import { RATE_LIMIT_CONFIG } from './constants';

interface RateLimitEntry {
  attempts: number[];
}

export class RateLimiter {
  private attempts = new Map<string, RateLimitEntry>();

  /**
   * 检查是否允许请求
   * @param key 标识符（如用户ID或IP）
   * @returns 是否允许
   */
  isAllowed(key: string): boolean {
    const now = Date.now();
    const windowStart = now - RATE_LIMIT_CONFIG.WINDOW_MS;

    // 获取或创建条目
    let entry = this.attempts.get(key);
    if (!entry) {
      entry = { attempts: [] };
      this.attempts.set(key, entry);
    }

    // 清理过期记录
    entry.attempts = entry.attempts.filter(time => time > windowStart);

    // 检查是否超过限制
    if (entry.attempts.length >= RATE_LIMIT_CONFIG.MAX_ATTEMPTS) {
      return false;
    }

    // 记录本次尝试
    entry.attempts.push(now);
    return true;
  }

  /**
   * 获取剩余尝试次数
   */
  getRemainingAttempts(key: string): number {
    const now = Date.now();
    const windowStart = now - RATE_LIMIT_CONFIG.WINDOW_MS;

    const entry = this.attempts.get(key);
    if (!entry) {
      return RATE_LIMIT_CONFIG.MAX_ATTEMPTS;
    }

    const recentAttempts = entry.attempts.filter(time => time > windowStart);
    return Math.max(0, RATE_LIMIT_CONFIG.MAX_ATTEMPTS - recentAttempts.length);
  }

  /**
   * 获取下次重置时间
   */
  getResetTime(key: string): number | null {
    const entry = this.attempts.get(key);
    if (!entry || entry.attempts.length === 0) {
      return null;
    }

    const oldestAttempt = Math.min(...entry.attempts);
    return oldestAttempt + RATE_LIMIT_CONFIG.WINDOW_MS;
  }

  /**
   * 清理所有记录
   */
  clear(): void {
    this.attempts.clear();
  }

  /**
   * 清理特定用户的记录
   */
  clearForKey(key: string): void {
    this.attempts.delete(key);
  }
}
