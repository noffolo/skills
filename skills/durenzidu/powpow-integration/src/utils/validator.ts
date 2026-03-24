/**
 * 输入验证工具类
 * 提供各种验证和清理功能
 */

import { VALIDATION_CONFIG } from './constants';

export interface ValidationResult {
  valid: boolean;
  error?: string;
}

export class Validator {
  /**
   * 验证邮箱格式
   */
  static validateEmail(email: string): ValidationResult {
    if (!email || typeof email !== 'string') {
      return { valid: false, error: 'Email is required' };
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return { valid: false, error: 'Invalid email format' };
    }

    if (email.length > 254) {
      return { valid: false, error: 'Email is too long (max 254 characters)' };
    }

    return { valid: true };
  }

  /**
   * 验证用户名
   */
  static validateUsername(username: string): ValidationResult {
    if (!username || typeof username !== 'string') {
      return { valid: false, error: 'Username is required' };
    }

    if (username.length < VALIDATION_CONFIG.USERNAME_MIN) {
      return { 
        valid: false, 
        error: `Username must be at least ${VALIDATION_CONFIG.USERNAME_MIN} characters` 
      };
    }

    if (username.length > VALIDATION_CONFIG.USERNAME_MAX) {
      return { 
        valid: false, 
        error: `Username must be less than ${VALIDATION_CONFIG.USERNAME_MAX} characters` 
      };
    }

    // 只允许字母、数字、下划线和连字符
    if (!/^[a-zA-Z0-9_-]+$/.test(username)) {
      return { 
        valid: false, 
        error: 'Username can only contain letters, numbers, underscores, and hyphens' 
      };
    }

    return { valid: true };
  }

  /**
   * 验证密码
   */
  static validatePassword(password: string): ValidationResult {
    if (!password || typeof password !== 'string') {
      return { valid: false, error: 'Password is required' };
    }

    if (password.length < VALIDATION_CONFIG.PASSWORD_MIN) {
      return { 
        valid: false, 
        error: `Password must be at least ${VALIDATION_CONFIG.PASSWORD_MIN} characters` 
      };
    }

    if (password.length > VALIDATION_CONFIG.PASSWORD_MAX) {
      return { 
        valid: false, 
        error: `Password must be less than ${VALIDATION_CONFIG.PASSWORD_MAX} characters` 
      };
    }

    // 检查密码强度（至少包含一个大写字母、一个小写字母和一个数字）
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);

    if (!hasUpperCase || !hasLowerCase || !hasNumbers) {
      return { 
        valid: false, 
        error: 'Password must contain at least one uppercase letter, one lowercase letter, and one number' 
      };
    }

    return { valid: true };
  }

  /**
   * 验证数字人名称
   */
  static validateDigitalHumanName(name: string): ValidationResult {
    if (!name || typeof name !== 'string') {
      return { valid: false, error: 'Name is required' };
    }

    if (name.length < VALIDATION_CONFIG.NAME_MIN) {
      return { valid: false, error: 'Name cannot be empty' };
    }

    if (name.length > VALIDATION_CONFIG.NAME_MAX) {
      return { 
        valid: false, 
        error: `Name must be less than ${VALIDATION_CONFIG.NAME_MAX} characters` 
      };
    }

    return { valid: true };
  }

  /**
   * 验证数字人描述
   */
  static validateDescription(description: string): ValidationResult {
    if (!description || typeof description !== 'string') {
      return { valid: false, error: 'Description is required' };
    }

    if (description.length > VALIDATION_CONFIG.DESCRIPTION_MAX) {
      return { 
        valid: false, 
        error: `Description must be less than ${VALIDATION_CONFIG.DESCRIPTION_MAX} characters` 
      };
    }

    return { valid: true };
  }

  /**
   * 验证坐标
   */
  static validateCoordinates(lat: number, lng: number): ValidationResult {
    if (typeof lat !== 'number' || typeof lng !== 'number') {
      return { valid: false, error: 'Coordinates must be numbers' };
    }

    if (lat < -90 || lat > 90) {
      return { valid: false, error: 'Latitude must be between -90 and 90' };
    }

    if (lng < -180 || lng > 180) {
      return { valid: false, error: 'Longitude must be between -180 and 180' };
    }

    return { valid: true };
  }

  /**
   * 验证数字人ID
   */
  static validateDigitalHumanId(dhId: string): ValidationResult {
    if (!dhId || typeof dhId !== 'string') {
      return { valid: false, error: 'Digital human ID is required' };
    }

    // 检查是否为有效的UUID格式（简化检查）
    const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
    if (!uuidRegex.test(dhId) && !/^dh_[a-zA-Z0-9]+$/.test(dhId)) {
      return { valid: false, error: 'Invalid digital human ID format' };
    }

    return { valid: true };
  }

  /**
   * 清理字符串（防止XSS）
   */
  static sanitizeString(input: string): string {
    if (!input || typeof input !== 'string') {
      return '';
    }

    return input
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#x27;')
      .replace(/\//g, '&#x2F;');
  }

  /**
   * 清理对象中的所有字符串属性
   */
  static sanitizeObject<T extends Record<string, unknown>>(obj: T): T {
    const sanitized = { ...obj };
    
    for (const key of Object.keys(sanitized)) {
      const value = sanitized[key];
      if (typeof value === 'string') {
        (sanitized as Record<string, unknown>)[key] = this.sanitizeString(value);
      }
    }
    
    return sanitized;
  }

  /**
   * 验证消息内容
   */
  static validateMessage(message: string): ValidationResult {
    if (!message || typeof message !== 'string') {
      return { valid: false, error: 'Message is required' };
    }

    if (message.trim().length === 0) {
      return { valid: false, error: 'Message cannot be empty' };
    }

    if (message.length > 2000) {
      return { valid: false, error: 'Message is too long (max 2000 characters)' };
    }

    return { valid: true };
  }
}
