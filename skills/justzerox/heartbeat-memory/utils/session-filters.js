#!/usr/bin/env node

/**
 * session-filters.js - Session 过滤工具
 * 
 * 负责过滤 sessions（日期范围、已处理、格式兼容性等）
 */

/**
 * 过滤 sessions（日期范围、已处理、格式兼容性）
 * 
 * @param {Array} sessions - sessions 列表
 * @param {Set} processedIds - 已处理的 session IDs
 * @param {Object} config - 配置对象
 * @returns {Object} { validSessions, newSessions, skippedCount }
 */
function filterSessions(sessions, processedIds, config) {
  // Issue #5 修复：兼容不同 OpenClaw 版本的 session 字段
  const validSessions = sessions.filter(s => {
    // 至少需要一个标识字段
    const hasId = s.sessionKey || s.sessionId || s.key || s.id;
    // 至少需要一个内容来源（transcriptPath 或 messages）
    const hasContent = s.transcriptPath || s.messages || s.history;
    return hasId && hasContent;
  });
  
  const skippedCount = sessions.length - validSessions.length;
  if (skippedCount > 0) {
    console.log(`⚠️  跳过 ${skippedCount} 个格式不兼容的 sessions`);
  }
  
  const newSessions = validSessions.filter(s => {
    const id = s.sessionKey || s.sessionId || s.key || s.id;
    if (!id || processedIds.has(id)) return false;
    
    // Issue #6 修复：日期范围过滤
    if (config.memorySave?.processSessionsAfter) {
      const cutoffDate = new Date(config.memorySave.processSessionsAfter);
      const sessionDate = s.updatedAt || s.modified || s.createdAt;
      if (sessionDate) {
        const sessionTime = new Date(sessionDate);
        if (sessionTime < cutoffDate) {
          console.log(`  ⏭️  跳过 ${id.substring(0, 20)}... (早于 ${config.memorySave.processSessionsAfter})`);
          return false;
        }
      }
    }
    
    return true;
  });

  return { validSessions, newSessions, skippedCount };
}

/**
 * 限制 sessions 处理数量（防止 OOM）
 * 
 * @param {Array} sessions - sessions 列表
 * @param {number} maxSessions - 最大处理数量
 * @returns {Object} { limitedSessions, remainingCount }
 */
function limitSessions(sessions, maxSessions = 50) {
  if (sessions.length <= maxSessions) {
    return { limitedSessions: sessions, remainingCount: 0 };
  }
  
  const remainingCount = sessions.length - maxSessions;
  console.log(`⚠️  限制处理数量：${maxSessions} 个（剩余 ${remainingCount} 个下次处理）`);
  
  return {
    limitedSessions: sessions.slice(0, maxSessions),
    remainingCount
  };
}

// 导出
module.exports = {
  filterSessions,
  limitSessions
};
