/**
 * GitHub to Skill - Entry Point
 * 
 * Analyzes GitHub .zip downloads and converts them to OpenClaw skills.
 */

const { exec } = require('child_process');
const { promisify } = require('util');
const fs = require('fs').promises;
const path = require('path');

const execAsync = promisify(exec);

const SKILL_DIR = path.join(__dirname);
const ANALYZER_SCRIPT = path.join(SKILL_DIR, 'analyzer.py');

/**
 * Main function
 * @param {Object} options - Skill options
 * @param {string} options.input - .zip file path or project directory
 * @param {string} options.name - Custom skill name (optional)
 * @param {string} options.output - Output directory (default: ./skills)
 * @param {boolean} options.analyzeOnly - Only analyze, don't generate
 * @returns {Promise<Object>} - Result object
 */
async function run(options) {
  const {
    input,
    name,
    output,
    analyzeOnly = false,
    confirm = false,  // Require explicit confirmation
  } = options;

  if (!input) {
    throw new Error('Input file path is required');
  }

  // Security warning
  console.log(`\n[!] SECURITY WARNING / 安全警告`);
  console.log(`This skill will:`);
  console.log(`  1. Extract and analyze the .zip file you provide`);
  console.log(`  2. Copy source code to a new skill directory`);
  console.log(`  3. Execute Python analyzer script (read-only analysis)`);
  console.log(`\nSensitive files (passwords, keys, tokens) will be automatically excluded.`);
  console.log(`Only source code files will be copied.`);
  console.log(`\n[!] LICENSE WARNING / 许可证警告`);
  console.log(`  Please verify the license of the source project before reuse.`);
  console.log(`  Ensure you have the right to convert and use the code.`);
  console.log(`  Common open-source licenses: MIT, Apache-2.0, GPL, BSD.\n`);

  if (!confirm) {
    console.log(`❌ Execution cancelled. Use --confirm to proceed.`);
    console.log(`   执行已取消。使用 --confirm 参数确认执行。`);
    return {
      success: false,
      message: 'Execution cancelled: confirmation required / 执行已取消：需要确认',
      hint: 'Add --confirm to proceed / 添加 --confirm 参数继续'
    };
  }

  console.log(`🔧 GitHub to Skill Converter`);
  console.log(`   Input: ${input}`);
  console.log(`   Output: ${output || './skills'}`);

  try {
    // Verify input exists
    await fs.access(input);

    // Run analyzer
    const args = [
      `"${input}"`,
      output ? `-o "${output}"` : '',
      analyzeOnly ? '--analyze-only' : '',
    ].filter(Boolean).join(' ');

    const command = `python "${ANALYZER_SCRIPT}" ${args}`;

    const { stdout, stderr } = await execAsync(command, {
      cwd: SKILL_DIR,
      timeout: 600000, // 10 minutes
      maxBuffer: 50 * 1024 * 1024,
    });

    if (stderr && !stderr.includes('WARNING')) {
      console.warn('Analyzer warnings:', stderr);
    }

    // Parse output
    const jsonMatch = stdout.match(/\{[\s\S]*\}/);
    const projectInfo = jsonMatch ? JSON.parse(jsonMatch[0]) : {};

    return {
      success: true,
      input,
      projectInfo,
      skillPath: projectInfo.name ? path.join(output || './skills', projectInfo.name) : null,
      message: generateSummary(projectInfo, analyzeOnly),
    };
  } catch (error) {
    console.error('❌ GitHub to Skill failed:', error.message);
    return {
      success: false,
      input,
      error: error.message,
      suggestions: getTroubleshootingSuggestions(error),
    };
  }
}

/**
 * Generate summary message
 */
function generateSummary(projectInfo, analyzeOnly) {
  if (analyzeOnly) {
    return `✅ 分析完成！
项目名称：${projectInfo.name || 'N/A'}
语言：${projectInfo.language || 'Unknown'}
类型：${projectInfo.type || 'Unknown'}
入口：${projectInfo.entry_point || 'N/A'}
依赖：${projectInfo.dependencies?.length || 0} 个
函数：${projectInfo.functions?.length || 0} 个`;
  }

  return `✅ 技能生成完成！

项目名称：${projectInfo.name || 'N/A'}
位置：skills/${projectInfo.name || 'unknown'}/

下一步：
1. cd skills/${projectInfo.name || 'unknown'}/src
${projectInfo.language === 'python' ? '2. pip install -r requirements.txt (如果有)' : '2. npm install (如果有 package.json)'}
3. 在 OpenClaw 中测试技能`;
}

/**
 * Get troubleshooting suggestions
 */
function getTroubleshootingSuggestions(error) {
  const message = error.message.toLowerCase();
  
  if (message.includes('python') || message.includes('not found')) {
    return '检查 Python 是否正确安装：python --version';
  }
  if (message.includes('no such file') || message.includes('cannot access')) {
    return '检查输入文件路径是否正确';
  }
  if (message.includes('zip') || message.includes('extract')) {
    return '检查.zip 文件是否完整，尝试重新下载';
  }
  if (message.includes('module')) {
    return 'Python 模块缺失，尝试：pip install pathlib';
  }
  
  return '查看详细错误日志，或尝试 --analyze-only 先分析';
}

/**
 * Quick analyze function
 */
async function analyze(inputPath) {
  return run({ input: inputPath, analyzeOnly: true });
}

/**
 * Quick convert function
 */
async function convert(inputPath, outputDir) {
  return run({ input: inputPath, output: outputDir });
}

// Export for OpenClaw skill system
module.exports = {
  run,
  analyze,
  convert,
};
