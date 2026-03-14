#!/usr/bin/env node

/**
 * AI 改写模块
 * 支持两种模式：
 * - direct: 直接调用 AI API（OpenAI/Anthropic/本地模型）
 * - agent: 通过 sessions_spawn 调用其他 agent（适用于多 agent 架构）
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 加载环境变量
require('dotenv').config({ path: path.join(__dirname, '../.env') });

const REWRITE_MODE = process.env.REWRITE_MODE || 'direct';

/**
 * 模式 A：直接调用 AI API
 */
async function rewriteWithDirectAI(note) {
  const AI_PROVIDER = process.env.AI_PROVIDER || 'openai';
  const AI_MODEL = process.env.AI_MODEL || 'gpt-4';
  const AI_API_KEY = process.env.AI_API_KEY;
  const AI_BASE_URL = process.env.AI_BASE_URL;

  if (!AI_API_KEY) {
    throw new Error('AI_API_KEY 未配置，请在 .env 中设置');
  }

  // 构建提示词
  const imageInfo = note.imageAnalysis && note.imageAnalysis.length > 0
    ? `\n\n图片分析结果：\n${note.imageAnalysis.map((img, i) => 
        `图片 ${i + 1}:\n- 内容描述: ${img.vision || '无'}\n- 文字内容: ${img.ocr || '无'}`
      ).join('\n\n')}`
    : '';

  const prompt = `请帮我改写以下小红书笔记，要求：
1. 保持原意，但用不同的表达方式
2. 风格轻松活泼，适合年轻人阅读
3. 标题控制在 30 字以内，正文控制在 500 字以内
4. 使用 emoji 增加趣味性
5. 参考图片分析结果（如有），确保内容与图片一致
6. 提取 3-5 个相关标签

原标题：${note.title}
原内容：${note.content}${imageInfo}

请以 JSON 格式返回，包含以下字段：
{
  "title": "改写后的标题",
  "content": "改写后的正文",
  "tags": ["标签1", "标签2", "标签3"]
}`;

  try {
    let result;

    if (AI_PROVIDER === 'openai') {
      // 使用 OpenAI API
      const apiUrl = AI_BASE_URL || 'https://api.openai.com/v1';
      const response = await callOpenAI(apiUrl, AI_API_KEY, AI_MODEL, prompt);
      result = JSON.parse(response);
    } else if (AI_PROVIDER === 'anthropic') {
      // 使用 Anthropic API
      const apiUrl = AI_BASE_URL || 'https://api.anthropic.com/v1';
      const response = await callAnthropic(apiUrl, AI_API_KEY, AI_MODEL, prompt);
      result = JSON.parse(response);
    } else if (AI_PROVIDER === 'local') {
      // 使用本地模型（如 Ollama）
      const apiUrl = AI_BASE_URL || 'http://localhost:11434';
      const response = await callLocalModel(apiUrl, AI_MODEL, prompt);
      result = JSON.parse(response);
    } else {
      throw new Error(`不支持的 AI_PROVIDER: ${AI_PROVIDER}`);
    }

    return {
      title: result.title,
      content: result.content,
      tags: result.tags || [],
    };

  } catch (error) {
    console.error(`[AI 改写] 失败: ${error.message}`);
    throw error;
  }
}

/**
 * 调用 OpenAI API
 */
async function callOpenAI(apiUrl, apiKey, model, prompt) {
  const https = require('https');
  const http = require('http');

  return new Promise((resolve, reject) => {
    const url = new URL(`${apiUrl}/chat/completions`);
    const client = url.protocol === 'https:' ? https : http;

    const postData = JSON.stringify({
      model: model,
      messages: [
        { role: 'user', content: prompt }
      ],
      temperature: 0.7,
    });

    const options = {
      hostname: url.hostname,
      port: url.port,
      path: url.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'Content-Length': Buffer.byteLength(postData),
      },
    };

    const req = client.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.error) {
            reject(new Error(json.error.message));
          } else {
            const content = json.choices[0].message.content;
            // 提取 JSON（可能包含在 markdown 代码块中）
            const jsonMatch = content.match(/```json\n([\s\S]*?)\n```/) || content.match(/\{[\s\S]*\}/);
            resolve(jsonMatch ? jsonMatch[1] || jsonMatch[0] : content);
          }
        } catch (error) {
          reject(error);
        }
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

/**
 * 调用 Anthropic API
 */
async function callAnthropic(apiUrl, apiKey, model, prompt) {
  const https = require('https');

  return new Promise((resolve, reject) => {
    const url = new URL(`${apiUrl}/messages`);

    const postData = JSON.stringify({
      model: model,
      max_tokens: 2048,
      messages: [
        { role: 'user', content: prompt }
      ],
    });

    const options = {
      hostname: url.hostname,
      port: url.port || 443,
      path: url.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01',
        'Content-Length': Buffer.byteLength(postData),
      },
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.error) {
            reject(new Error(json.error.message));
          } else {
            const content = json.content[0].text;
            const jsonMatch = content.match(/```json\n([\s\S]*?)\n```/) || content.match(/\{[\s\S]*\}/);
            resolve(jsonMatch ? jsonMatch[1] || jsonMatch[0] : content);
          }
        } catch (error) {
          reject(error);
        }
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

/**
 * 调用本地模型（Ollama）
 */
async function callLocalModel(apiUrl, model, prompt) {
  const http = require('http');

  return new Promise((resolve, reject) => {
    const url = new URL(`${apiUrl}/api/generate`);

    const postData = JSON.stringify({
      model: model,
      prompt: prompt,
      stream: false,
    });

    const options = {
      hostname: url.hostname,
      port: url.port || 11434,
      path: url.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData),
      },
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.error) {
            reject(new Error(json.error));
          } else {
            const content = json.response;
            const jsonMatch = content.match(/```json\n([\s\S]*?)\n```/) || content.match(/\{[\s\S]*\}/);
            resolve(jsonMatch ? jsonMatch[1] || jsonMatch[0] : content);
          }
        } catch (error) {
          reject(error);
        }
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

/**
 * 模式 B：通过 sessions_spawn 调用其他 agent
 * 注意：此函数需要在 OpenClaw agent 环境中运行
 */
async function rewriteWithAgent(note) {
  const AGENT_ID = process.env.AGENT_ID || 'libu';

  const imageInfo = note.imageAnalysis && note.imageAnalysis.length > 0
    ? `\n\n图片分析结果：\n${note.imageAnalysis.map((img, i) => 
        `图片 ${i + 1}:\n- 内容描述: ${img.vision || '无'}\n- 文字内容: ${img.ocr || '无'}`
      ).join('\n\n')}`
    : '';

  const task = `请帮我改写以下小红书笔记，要求：
1. 保持原意，但用不同的表达方式
2. 风格轻松活泼，适合年轻人阅读
3. 标题控制在 30 字以内，正文控制在 500 字以内
4. 使用 emoji 增加趣味性
5. 参考图片分析结果（如有），确保内容与图片一致
6. 提取 3-5 个相关标签

原标题：${note.title}
原内容：${note.content}${imageInfo}

请以 JSON 格式返回，包含以下字段：
{
  "title": "改写后的标题",
  "content": "改写后的正文",
  "tags": ["标签1", "标签2", "标签3"]
}`;

  console.log(`[Agent 改写] 调用 ${AGENT_ID} 进行改写...`);
  console.log(`[Agent 改写] 任务: ${task.substring(0, 100)}...`);
  
  // 注意：这里只是示例，实际需要通过 OpenClaw 的 sessions_spawn 工具调用
  // 在 SKILL.md 中会有完整的调用示例
  throw new Error('Agent 模式需要在 OpenClaw agent 环境中通过 sessions_spawn 调用');
}

/**
 * 统一改写接口
 */
async function rewriteNote(note) {
  console.log(`[改写] 模式: ${REWRITE_MODE}`);
  
  if (REWRITE_MODE === 'direct') {
    return await rewriteWithDirectAI(note);
  } else if (REWRITE_MODE === 'agent') {
    return await rewriteWithAgent(note);
  } else {
    throw new Error(`不支持的 REWRITE_MODE: ${REWRITE_MODE}`);
  }
}

module.exports = { 
  rewriteNote, 
  rewriteWithDirectAI, 
  rewriteWithAgent,
  rewriteByLibu: rewriteNote  // 别名，兼容 run.js
};

// 如果直接运行此脚本（用于测试）
if (require.main === module) {
  const testNote = {
    title: 'AI绘画新手入门指南｜零基础也能画出大片',
    content: '最近迷上了AI绘画，从完全不会到现在能画出自己满意的作品...',
    imageAnalysis: [],
  };

  rewriteNote(testNote)
    .then(result => {
      console.log('\n[改写结果]');
      console.log(JSON.stringify(result, null, 2));
    })
    .catch(error => {
      console.error('[改写失败]', error.message);
      process.exit(1);
    });
}
