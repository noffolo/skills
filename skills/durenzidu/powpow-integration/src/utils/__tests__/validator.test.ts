/**
 * 验证器单元测试
 */

import { Validator } from '../validator';

describe('Validator', () => {
  describe('validateEmail', () => {
    it('should validate correct email addresses', () => {
      expect(Validator.validateEmail('test@example.com').valid).toBe(true);
      expect(Validator.validateEmail('user.name@domain.co.uk').valid).toBe(true);
      expect(Validator.validateEmail('user+tag@example.com').valid).toBe(true);
    });

    it('should reject invalid email addresses', () => {
      expect(Validator.validateEmail('').valid).toBe(false);
      expect(Validator.validateEmail('invalid').valid).toBe(false);
      expect(Validator.validateEmail('@example.com').valid).toBe(false);
      expect(Validator.validateEmail('test@').valid).toBe(false);
      expect(Validator.validateEmail('test@.com').valid).toBe(false);
    });

    it('should reject too long email addresses', () => {
      const longEmail = 'a'.repeat(250) + '@example.com';
      expect(Validator.validateEmail(longEmail).valid).toBe(false);
    });
  });

  describe('validateUsername', () => {
    it('should validate correct usernames', () => {
      expect(Validator.validateUsername('alice').valid).toBe(true);
      expect(Validator.validateUsername('user_123').valid).toBe(true);
      expect(Validator.validateUsername('test-user').valid).toBe(true);
    });

    it('should reject usernames that are too short', () => {
      expect(Validator.validateUsername('ab').valid).toBe(false);
      expect(Validator.validateUsername('').valid).toBe(false);
    });

    it('should reject usernames that are too long', () => {
      expect(Validator.validateUsername('a'.repeat(51)).valid).toBe(false);
    });

    it('should reject usernames with invalid characters', () => {
      expect(Validator.validateUsername('user@name').valid).toBe(false);
      expect(Validator.validateUsername('user name').valid).toBe(false);
      expect(Validator.validateUsername('user.name').valid).toBe(false);
    });
  });

  describe('validatePassword', () => {
    it('should validate strong passwords', () => {
      expect(Validator.validatePassword('Password123').valid).toBe(true);
      expect(Validator.validatePassword('MyP@ssw0rd').valid).toBe(true);
    });

    it('should reject passwords that are too short', () => {
      expect(Validator.validatePassword('Pass1').valid).toBe(false);
    });

    it('should reject passwords without uppercase letters', () => {
      expect(Validator.validatePassword('password123').valid).toBe(false);
    });

    it('should reject passwords without lowercase letters', () => {
      expect(Validator.validatePassword('PASSWORD123').valid).toBe(false);
    });

    it('should reject passwords without numbers', () => {
      expect(Validator.validatePassword('PasswordABC').valid).toBe(false);
    });
  });

  describe('validateDigitalHumanName', () => {
    it('should validate correct names', () => {
      expect(Validator.validateDigitalHumanName('AI助手').valid).toBe(true);
      expect(Validator.validateDigitalHumanName('Test Bot').valid).toBe(true);
    });

    it('should reject empty names', () => {
      expect(Validator.validateDigitalHumanName('').valid).toBe(false);
    });

    it('should reject names that are too long', () => {
      expect(Validator.validateDigitalHumanName('a'.repeat(101)).valid).toBe(false);
    });
  });

  describe('validateCoordinates', () => {
    it('should validate correct coordinates', () => {
      expect(Validator.validateCoordinates(39.9042, 116.4074).valid).toBe(true);
      expect(Validator.validateCoordinates(-90, -180).valid).toBe(true);
      expect(Validator.validateCoordinates(90, 180).valid).toBe(true);
    });

    it('should reject invalid latitudes', () => {
      expect(Validator.validateCoordinates(91, 0).valid).toBe(false);
      expect(Validator.validateCoordinates(-91, 0).valid).toBe(false);
    });

    it('should reject invalid longitudes', () => {
      expect(Validator.validateCoordinates(0, 181).valid).toBe(false);
      expect(Validator.validateCoordinates(0, -181).valid).toBe(false);
    });
  });

  describe('sanitizeString', () => {
    it('should sanitize HTML characters', () => {
      expect(Validator.sanitizeString('<script>')).toBe('&lt;script&gt;');
      expect(Validator.sanitizeString('"test"')).toBe('&quot;test&quot;');
      expect(Validator.sanitizeString("'test'")).toBe('&#x27;test&#x27;');
    });

    it('should handle empty strings', () => {
      expect(Validator.sanitizeString('')).toBe('');
    });

    it('should handle non-string inputs', () => {
      expect(Validator.sanitizeString(null as unknown as string)).toBe('');
      expect(Validator.sanitizeString(undefined as unknown as string)).toBe('');
    });
  });
});
