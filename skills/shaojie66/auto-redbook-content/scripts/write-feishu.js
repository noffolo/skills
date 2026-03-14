#!/usr/bin/env node

/**
 * 写入飞书多维表格
 * 使用 OpenClaw feishu_bitable_create_record
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

/**
 * 加载配置
 */
function loadConfig() {
  const envPath = path.join(__dirname, '..', '.env');
  
  if (!fs.existsSync(envPath)) {
    throw new Error('配置文件不存在: .env');
  }
  
  const envContent = fs.readFileSync(envPath, 'utf-8');
  const config = {};
  
  envContent.split('\n').forEach(line => {
    const match = line.match(/^([^=]+)=(.*)$/);
    if (match) {
      config[match[1].trim()] = match[2].trim();
    }
  });
  
  if (!config.FEISHU_APP_TOKEN || !config.FEISHU_TABLE_ID) {
    throw new Error('配置缺失: FEISHU_APP_TOKEN 或 FEISHU_TABLE_ID');
  }
  
  return config;
}

/**
 * 构建飞书表格字段
 */
function buildFields(note, rewritten) {
  const fields = {
    '原标题': note.title,
    '原文链接': {
      text: note.title,
      link: note.url,
    },
    '作者': note.author,
    '点赞数': note.likes,
    '评论数': note.comments,
    '收藏数': note.shares,
    '抓取时间': Date.now(),
    '状态': '待审核',
  };
  
  if (rewritten) {
    fields['改写后标题'] = rewritten.title;
    fields['改写后正文'] = rewritten.content;
    fields['提取标签'] = rewritten.tags.join(', ');
  }
  
  return fields;
}

/**
 * 写入飞书表格
 * @param {Object} note - 原始笔记
 * @param {Object} rewritten - 改写结果
 * @returns {Promise<string>} record_id
 */
async function writeToFeishu(note, rewritten) {
  console.log(`[飞书] 写入表格: ${note.title}`);
  
  try {
    const config = loadConfig();
    const fields = buildFields(note, rewritten);
    
    // 安全验证：确保配置有效
    if (!config.FEISHU_APP_TOKEN || !config.FEISHU_TABLE_ID) {
      throw new Error('飞书配置缺失');
    }
    
    // 验证 token 和 table_id 格式
    if (!/^(bascn|cli)_[a-zA-Z0-9_-]+$/.test(config.FEISHU_APP_TOKEN)) {
      throw new Error('FEISHU_APP_TOKEN 格式无效');
    }
    
    if (!/^tbl[a-zA-Z0-9]+$/.test(config.FEISHU_TABLE_ID)) {
      throw new Error('FEISHU_TABLE_ID 格式无效');
    }
    
    // 使用 spawn 而非 execSync，避免 shell 注入
    const { spawnSync } = require('child_process');
    const fieldsJson = JSON.stringify(fields);
    
    const result = spawnSync('openclaw', [
      'feishu-bitable',
      'create-record',
      '--app-token',
      config.FEISHU_APP_TOKEN,
      '--table-id',
      config.FEISHU_TABLE_ID,
      '--fields',
      fieldsJson
    ], {
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'pipe'],
      timeout: 30000
    });
    
    if (result.error) {
      throw result.error;
    }
    
    if (result.status !== 0) {
      throw new Error(result.stderr || '飞书写入失败');
    }
    
    const response = result.stdout;
    
    // 提取 record_id
    const match = response.match(/record_id["\s:]+([a-zA-Z0-9_-]+)/);
    if (!match) {
      throw new Error('未能从响应中提取 record_id');
    }
    
    const recordId = match[1];
    console.log(`[飞书] 成功写入，record_id: ${recordId}`);
    return recordId;
    
  } catch (error) {
    console.error(`[飞书] 写入失败:`, error.message);
    throw error;
  }
}

module.exports = { writeToFeishu };

// 如果直接运行此脚本
if (require.main === module) {
  const testNote = {
    title: '测试标题',
    url: 'https://www.xiaohongshu.com/explore/test',
    author: '测试作者',
    likes: 100,
    comments: 20,
    shares: 10,
  };
  
  const testRewritten = {
    title: '改写后的标题',
    content: '改写后的正文',
    tags: ['标签1', '标签2'],
  };
  
  writeToFeishu(testNote, testRewritten)
    .then(recordId => {
      console.log(`Record ID: ${recordId}`);
    })
    .catch(error => {
      console.error(error);
      process.exit(1);
    });
}
