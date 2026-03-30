#!/usr/bin/env node
/**
 * 代码质量分析系统 - 安装脚本
 * 
 * 用法：npm run setup
 * 
 * 此脚本会：
 * 1. 解压前后端代码
 * 2. 检查环境（Node.js、PostgreSQL）
 * 3. 安装依赖
 * 4. 初始化数据库
 * 5. 创建配置文件
 */

const { execSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

const SKILL_DIR = path.join(__dirname, '..');
const CONFIG_FILE = path.join(SKILL_DIR, 'config.json');
const CONFIG_EXAMPLE = path.join(SKILL_DIR, 'config.example.json');
const BACKEND_DIR = path.join(SKILL_DIR, 'backend');
const FRONTEND_DIR = path.join(SKILL_DIR, 'frontend');
const BACKEND_ZIP = path.join(SKILL_DIR, 'backend.zip');
const FRONTEND_ZIP = path.join(SKILL_DIR, 'frontend.zip');
const ENV_FILE = path.join(BACKEND_DIR, '.env');
const ENV_EXAMPLE = path.join(BACKEND_DIR, '.env.example');

const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  reset: '\x1b[0m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function checkCommand(command, name) {
  try {
    execSync(`${command} --version`, { stdio: 'ignore' });
    log(`✅ ${name} 已安装`, 'green');
    return true;
  } catch {
    log(`❌ ${name} 未安装`, 'red');
    return false;
  }
}

function unzipFiles() {
  log('\n📦 解压代码文件...', 'blue');
  
  // 检查压缩包是否存在
  if (!fs.existsSync(BACKEND_ZIP)) {
    log('   ⚠️ backend.zip 不存在，可能已解压', 'yellow');
  } else {
    try {
      log('   解压 backend.zip...');
      execSync(`unzip -o "${BACKEND_ZIP}" -d "${SKILL_DIR}"`, { stdio: 'inherit' });
      log('   ✅ 后端代码已解压', 'green');
    } catch (err) {
      log('   ❌ 解压失败: ' + err.message, 'red');
      return false;
    }
  }
  
  if (!fs.existsSync(FRONTEND_ZIP)) {
    log('   ⚠️ frontend.zip 不存在，可能已解压', 'yellow');
  } else {
    try {
      log('   解压 frontend.zip...');
      execSync(`unzip -o "${FRONTEND_ZIP}" -d "${SKILL_DIR}"`, { stdio: 'inherit' });
      log('   ✅ 前端代码已解压', 'green');
    } catch (err) {
      log('   ❌ 解压失败: ' + err.message, 'red');
      return false;
    }
  }
  
  return true;
}

function installDependencies() {
  log('\n📦 安装依赖...', 'blue');
  
  if (!fs.existsSync(BACKEND_DIR)) {
    log('   ❌ backend 目录不存在，请先解压代码', 'red');
    return false;
  }
  
  if (!fs.existsSync(FRONTEND_DIR)) {
    log('   ❌ frontend 目录不存在，请先解压代码', 'red');
    return false;
  }
  
  try {
    log('   安装后端依赖...');
    execSync('npm install', { cwd: BACKEND_DIR, stdio: 'inherit' });
    log('   ✅ 后端依赖安装完成', 'green');
  } catch (err) {
    log('   ❌ 后端依赖安装失败', 'red');
    return false;
  }
  
  try {
    log('   安装前端依赖...');
    execSync('npm install', { cwd: FRONTEND_DIR, stdio: 'inherit' });
    log('   ✅ 前端依赖安装完成', 'green');
  } catch (err) {
    log('   ❌ 前端依赖安装失败', 'red');
    return false;
  }
  
  return true;
}

function initDatabase() {
  log('\n🗄️ 初始化数据库...', 'blue');
  
  try {
    log('   生成 Prisma Client...');
    execSync('npx prisma generate', { cwd: BACKEND_DIR, stdio: 'inherit' });
    
    log('   运行数据库迁移...');
    execSync('npx prisma migrate deploy', { cwd: BACKEND_DIR, stdio: 'inherit' });
    
    log('   ✅ 数据库初始化完成', 'green');
    return true;
  } catch (err) {
    log('   ❌ 数据库初始化失败', 'red');
    log('   请确保数据库已创建：createdb code_quality', 'yellow');
    return false;
  }
}

function createConfigFiles() {
  log('\n📝 创建配置文件...', 'blue');
  
  // 创建 config.json
  if (!fs.existsSync(CONFIG_FILE)) {
    if (fs.existsSync(CONFIG_EXAMPLE)) {
      fs.copyFileSync(CONFIG_EXAMPLE, CONFIG_FILE);
      log('   ✅ 创建 config.json（请修改配置）', 'green');
    }
  } else {
    log('   ℹ️ config.json 已存在', 'yellow');
  }
  
  // 创建 .env
  if (fs.existsSync(BACKEND_DIR)) {
    const envExample = path.join(BACKEND_DIR, '.env.example');
    const envFile = path.join(BACKEND_DIR, '.env');
    if (!fs.existsSync(envFile) && fs.existsSync(envExample)) {
      fs.copyFileSync(envExample, envFile);
      log('   ✅ 创建 backend/.env（请修改数据库连接）', 'green');
    } else if (fs.existsSync(envFile)) {
      log('   ℹ️ backend/.env 已存在', 'yellow');
    } else {
      // 创建默认 .env
      const defaultEnv = `DATABASE_URL="postgresql://postgres:postgres@localhost:5432/code_quality?schema=public"
PORT=3000
NODE_ENV=development
JWT_SECRET=your-secret-key-change-in-production`;
      fs.writeFileSync(envFile, defaultEnv);
      log('   ✅ 创建 backend/.env（请修改数据库连接）', 'green');
    }
  }
  
  // 创建前端 .env
  if (fs.existsSync(FRONTEND_DIR)) {
    const frontendEnvFile = path.join(FRONTEND_DIR, '.env');
    if (!fs.existsSync(frontendEnvFile)) {
      const defaultFrontendEnv = 'VITE_API_BASE_URL=http://localhost:3000/api/v1';
      fs.writeFileSync(frontendEnvFile, defaultFrontendEnv);
      log('   ✅ 创建 frontend/.env', 'green');
    } else {
      log('   ℹ️ frontend/.env 已存在', 'yellow');
    }
  }
  
  return true;
}

function printNextSteps() {
  log('\n========================================', 'blue');
  log('  ✅ 安装完成！', 'green');
  log('========================================\n');
  log('下一步操作：');
  log('1. 创建数据库：createdb code_quality');
  log('2. 修改配置文件：');
  log('   - config.json（代码目录、Teams、SMTP）');
  log('   - backend/.env（数据库连接）');
  log('3. 启动服务：');
  log('   - 后端：cd backend && npm run start:dev');
  log('   - 前端：cd frontend && npm run dev');
  log('4. 访问前端：http://localhost:5173');
  log('\n或者直接告诉 AI 助手：');
  log('  "帮我启动代码质量分析系统"\n');
}

async function main() {
  log('========================================', 'blue');
  log('  代码质量分析系统 - 安装向导', 'blue');
  log('========================================\n');
  
  // 检查环境
  log('🔍 检查环境...', 'blue');
  const nodeOk = checkCommand('node', 'Node.js');
  const npmOk = checkCommand('npm', 'npm');
  
  if (!nodeOk || !npmOk) {
    log('\n❌ 请先安装 Node.js: https://nodejs.org/', 'red');
    process.exit(1);
  }
  
  // 解压代码
  if (!unzipFiles()) {
    process.exit(1);
  }
  
  // 创建配置文件
  createConfigFiles();
  
  // 安装依赖
  if (!installDependencies()) {
    process.exit(1);
  }
  
  // 检查 PostgreSQL
  try {
    execSync('psql --version', { stdio: 'ignore' });
    log('\n✅ PostgreSQL 已安装', 'green');
    
    // 初始化数据库
    initDatabase();
  } catch {
    log('\n⚠️ PostgreSQL 未安装或未配置 PATH', 'yellow');
    log('   请先安装 PostgreSQL 并创建数据库', 'yellow');
  }
  
  // 打印下一步
  printNextSteps();
}

main().catch(console.error);