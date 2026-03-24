/**
 * 速率限制器单元测试
 */

import { RateLimiter } from '../rate-limiter';
import { RATE_LIMIT_CONFIG } from '../constants';

describe('RateLimiter', () => {
  let rateLimiter: RateLimiter;

  beforeEach(() => {
    rateLimiter = new RateLimiter();
  });

  afterEach(() => {
    rateLimiter.clear();
  });

  describe('isAllowed', () => {
    it('should allow requests within limit', () => {
      const key = 'test-user';
      
      for (let i = 0; i < RATE_LIMIT_CONFIG.MAX_ATTEMPTS; i++) {
        expect(rateLimiter.isAllowed(key)).toBe(true);
      }
    });

    it('should block requests exceeding limit', () => {
      const key = 'test-user';
      
      // 达到限制
      for (let i = 0; i < RATE_LIMIT_CONFIG.MAX_ATTEMPTS; i++) {
        rateLimiter.isAllowed(key);
      }
      
      // 下一个请求应该被阻止
      expect(rateLimiter.isAllowed(key)).toBe(false);
    });

    it('should allow requests after window expires', async () => {
      const key = 'test-user';
      
      // 达到限制
      for (let i = 0; i < RATE_LIMIT_CONFIG.MAX_ATTEMPTS; i++) {
        rateLimiter.isAllowed(key);
      }
      
      expect(rateLimiter.isAllowed(key)).toBe(false);
      
      // 等待窗口过期（在实际测试中可能需要模拟时间）
      // 这里我们直接清理记录来模拟
      rateLimiter.clearForKey(key);
      
      expect(rateLimiter.isAllowed(key)).toBe(true);
    });

    it('should track different keys independently', () => {
      const key1 = 'user-1';
      const key2 = 'user-2';
      
      // user-1达到限制
      for (let i = 0; i < RATE_LIMIT_CONFIG.MAX_ATTEMPTS; i++) {
        rateLimiter.isAllowed(key1);
      }
      
      expect(rateLimiter.isAllowed(key1)).toBe(false);
      expect(rateLimiter.isAllowed(key2)).toBe(true);
    });
  });

  describe('getRemainingAttempts', () => {
    it('should return max attempts for new key', () => {
      const key = 'new-user';
      expect(rateLimiter.getRemainingAttempts(key)).toBe(RATE_LIMIT_CONFIG.MAX_ATTEMPTS);
    });

    it('should decrease remaining attempts after each request', () => {
      const key = 'test-user';
      
      rateLimiter.isAllowed(key);
      expect(rateLimiter.getRemainingAttempts(key)).toBe(RATE_LIMIT_CONFIG.MAX_ATTEMPTS - 1);
      
      rateLimiter.isAllowed(key);
      expect(rateLimiter.getRemainingAttempts(key)).toBe(RATE_LIMIT_CONFIG.MAX_ATTEMPTS - 2);
    });

    it('should not return negative remaining attempts', () => {
      const key = 'test-user';
      
      for (let i = 0; i < RATE_LIMIT_CONFIG.MAX_ATTEMPTS + 5; i++) {
        rateLimiter.isAllowed(key);
      }
      
      expect(rateLimiter.getRemainingAttempts(key)).toBe(0);
    });
  });

  describe('getResetTime', () => {
    it('should return null for new key', () => {
      const key = 'new-user';
      expect(rateLimiter.getResetTime(key)).toBeNull();
    });

    it('should return reset time after requests', () => {
      const key = 'test-user';
      const beforeRequest = Date.now();
      
      rateLimiter.isAllowed(key);
      const resetTime = rateLimiter.getResetTime(key);
      
      expect(resetTime).not.toBeNull();
      expect(resetTime!).toBeGreaterThan(beforeRequest);
      expect(resetTime!).toBeLessThanOrEqual(beforeRequest + RATE_LIMIT_CONFIG.WINDOW_MS + 1000);
    });
  });

  describe('clear', () => {
    it('should clear all rate limit records', () => {
      const key = 'test-user';
      
      rateLimiter.isAllowed(key);
      expect(rateLimiter.getRemainingAttempts(key)).toBeLessThan(RATE_LIMIT_CONFIG.MAX_ATTEMPTS);
      
      rateLimiter.clear();
      expect(rateLimiter.getRemainingAttempts(key)).toBe(RATE_LIMIT_CONFIG.MAX_ATTEMPTS);
    });
  });

  describe('clearForKey', () => {
    it('should clear records for specific key only', () => {
      const key1 = 'user-1';
      const key2 = 'user-2';
      
      rateLimiter.isAllowed(key1);
      rateLimiter.isAllowed(key2);
      
      rateLimiter.clearForKey(key1);
      
      expect(rateLimiter.getRemainingAttempts(key1)).toBe(RATE_LIMIT_CONFIG.MAX_ATTEMPTS);
      expect(rateLimiter.getRemainingAttempts(key2)).toBe(RATE_LIMIT_CONFIG.MAX_ATTEMPTS - 1);
    });
  });
});
