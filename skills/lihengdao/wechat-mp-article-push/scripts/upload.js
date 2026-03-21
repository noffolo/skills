#!/usr/bin/env node
/**
 * 上传脚本：推送到 GitHub 并/或发布到 ClawHub
 * 用法: node scripts/upload.js [github|clawhub]
 * 不传参数时先执行 github，再执行 clawhub
 */
const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const root = path.resolve(__dirname, '..');
const pkgPath = path.join(root, 'package.json');
const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
const version = pkg.version;
const slug = 'wechat-mp-article-push';
const GITHUB_REPO = 'https://github.com/lihengdao/wechat-mp-article-push.git';

// 若本目录不是独立仓库，则视为父仓库下的子目录，只推送该子目录
const isStandaloneRepo = fs.existsSync(path.join(root, '.git'));
const gitRepoRoot = isStandaloneRepo
  ? root
  : path.resolve(execSync('git rev-parse --show-toplevel', { encoding: 'utf8', cwd: root }).trim());
const SUBTREE_PREFIX = path.relative(gitRepoRoot, root).replace(/\\/g, '/');

function run(cmd, opts = {}) {
  console.log('\n$', cmd);
  return execSync(cmd, { stdio: 'inherit', cwd: root, ...opts });
}

function runInRepo(cmd, opts = {}) {
  console.log('\n$', cmd);
  return execSync(cmd, { stdio: 'inherit', cwd: gitRepoRoot, ...opts });
}

function uploadGitHub() {
  console.log('\n--- 推送到 GitHub ---');
  if (isStandaloneRepo) {
    run('git add -A');
    try {
      run('git diff --staged --quiet', { stdio: 'pipe' });
      console.log('没有新的更改，跳过 commit。');
    } catch {
      run(`git commit -m "chore: sync (v${version})"`);
      run(`git push ${GITHUB_REPO} main --force`);
    }
  } else {
    runInRepo(`git add ${SUBTREE_PREFIX}`);
    try {
      runInRepo('git diff --staged --quiet', { stdio: 'pipe' });
      console.log('没有新的更改，跳过 commit。');
    } catch {
      runInRepo(`git commit -m "chore: sync (v${version})"`);
      const subtreeBranch = 'subtree-push-temp';
      runInRepo(`git subtree split --prefix=${SUBTREE_PREFIX} -b ${subtreeBranch}`);
      try {
        runInRepo(`git push ${GITHUB_REPO} ${subtreeBranch}:main --force`);
      } finally {
        runInRepo(`git branch -D ${subtreeBranch}`);
      }
    }
  }
}

function uploadClawhub() {
  console.log('\n--- 发布到 ClawHub ---');
  run(`npx clawhub publish . --slug ${slug} --version ${version} --changelog "chore: sync (v${version})"`);
}

const arg = process.argv[2];
if (arg === 'github') {
  uploadGitHub();
} else if (arg === 'clawhub') {
  uploadClawhub();
} else {
  uploadGitHub();
  uploadClawhub();
}
console.log('\n完成。');
