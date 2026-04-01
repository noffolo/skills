#!/bin/bash
# publish.sh - 一键发布 Skill 到所有平台
# 用法: ./publish.sh <slug> [--platforms=clawhub,github,coze,...]
#
# 首次使用会自动引导配置 Token

set -e
WORKSPACE="/home/node/.openclaw/workspace"
SKILL_DIR="${WORKSPACE}/skills/${1:?用法: $0 <slug> [平台]}"
ENV_FILE="$(dirname $0)/../.env"
SKILL="${1}"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 加载 .env
load_env() {
  if [ -f "$ENV_FILE" ]; then
    set -a
    source "$ENV_FILE"
    set +a
  fi
}

# 检查 Token
check_token() {
  local name=$1
  local token=$2
  if [ -z "$token" ]; then
    warn "$name Token 未配置"
    return 1
  fi
  log "$name Token ✓"
  return 0
}

# 首次运行引导
first_run() {
  if [ ! -f "$ENV_FILE" ]; then
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  Skill Publisher - 首次使用${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "检测到首次使用，正在启动 Token 配置向导..."
    echo ""
    python "$(dirname $0)/setup_tokens.py"
    echo ""
    read -p "按 Enter 继续发布流程..."
  fi
}

# 预检查
preflight() {
  echo ""
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${BLUE}  发布前检查${NC}"
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  
  load_env
  
  echo ""
  log "检查 Skill 目录: ${SKILL_DIR}"
  if [ ! -d "$SKILL_DIR" ]; then
    error "Skill 目录不存在: ${SKILL_DIR}"
    exit 1
  fi
  
  local ver=$(node -p "require('${SKILL_DIR}/_meta.json').version" 2>/dev/null || echo "1.0.0")
  local name=$(node -p "require('${SKILL_DIR}/_meta.json').name" 2>/dev/null || echo "$SKILL")
  echo ""
  log "Skill: ${name}"
  log "版本: v${ver}"
  log "目录: ${SKILL_DIR}"
  
  echo ""
  echo "检查 Token..."
  local has_clawhub=0
  local has_github=0
  
  check_token "ClawHub" "$CLAWHUB_TOKEN" && has_clawhub=1
  check_token "GitHub" "$GITHUB_TOKEN" && has_github=1
  
  echo ""
}

# 发布到 ClawHub
publish_clawhub() {
  log "→ 发布到 ClawHub..."
  cd "${WORKSPACE}/skills/${SKILL}"
  local ver=$(node -p "require('./_meta.json').version" 2>/dev/null || echo "1.0.0")
  local changelog=$(node -p "require('./_meta.json').changelog" 2>/dev/null || echo "Update")
  npx -y clawhub publish . --slug ${SKILL} --version ${ver} --changelog "${changelog}" --tags latest
  echo -e "${GREEN}✓ ClawHub 发布完成${NC}"
}

# 发布到 GitHub
publish_github() {
  log "→ 发布到 GitHub..."
  local git_dir="${WORKSPACE}/${SKILL}-github"
  
  if [ -d "$git_dir" ]; then
    cd ${git_dir}
    cp ${SKILL_DIR}/SKILL.md ${SKILL_DIR}/_meta.json . 2>/dev/null || true
    find ${SKILL_DIR} -maxdepth 3 \( -name "*.js" -o -name "*.json" -o -name "*.md" \) 2>/dev/null \
      | head -50 | while read f; do
        [ -f "$f" ] && cp "$f" . 2>/dev/null || true
      done
    git add -A && git commit -m "${changelog}" 2>/dev/null && \
    GIT_TOKEN=${GITHUB_TOKEN} git push 2>/dev/null && \
    echo -e "${GREEN}✓ GitHub 推送完成${NC}" || \
    echo -e "${YELLOW}⚠ GitHub 无更新或推送失败${NC}"
  else
    warn "GitHub 目录不存在: ${git_dir}"
    echo "  创建新仓库: ${git_dir}"
    mkdir -p ${git_dir}
    cd ${git_dir}
    cp ${SKILL_DIR}/SKILL.md ${SKILL_DIR}/_meta.json . 2>/dev/null || true
    find ${SKILL_DIR} -maxdepth 3 \( -name "*.js" -o -name "*.json" -o -name "*.md" \) 2>/dev/null \
      | head -50 | while read f; do
        [ -f "$f" ] && cp "$f" . 2>/dev/null || true
      done
    git init && git config user.email "publisher@skill.com" && git config user.name "Skill Publisher"
    git add -A && git commit -m "Initial commit: ${SKILL}"
    git remote add origin "https://github.com/ryanbihai/${SKILL}.git"
    GIT_TOKEN=${GITHUB_TOKEN} git push -u origin main 2>/dev/null && \
    echo -e "${GREEN}✓ GitHub 仓库创建并推送完成${NC}" || \
    echo -e "${YELLOW}⚠ GitHub 推送失败，请手动检查${NC}"
  fi
}

# 生成手动平台提交文本
generate_manual_text() {
  log "→ 生成手动平台提交文本..."
  python "$(dirname $0)/gen_submission.py" ${SKILL}
}

# 主流程
main() {
  first_run
  preflight
  
  echo ""
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${BLUE}  开始发布: ${SKILL}${NC}"
  echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  
  # 自动平台
  echo -e "${GREEN}━━━ 自动平台 ━━━${NC}"
  
  load_env
  
  if [ -n "$CLAWHUB_TOKEN" ]; then
    publish_clawhub
  else
    warn "跳过 ClawHub（未配置 Token）"
  fi
  
  if [ -n "$GITHUB_TOKEN" ]; then
    publish_github
  else
    warn "跳过 GitHub（未配置 Token）"
  fi
  
  # 手动平台
  echo ""
  echo -e "${YELLOW}━━━ 手动平台 ━━━${NC}"
  echo "以下平台需要手动操作，生成提交文本..."
  generate_manual_text
  
  # 完成
  echo ""
  echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${GREEN}  发布完成！${NC}"
  echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
  echo "💡 提示："
  echo "  • 查看所有平台状态: python scripts/check_status.py ${SKILL}"
  echo "  • 重新配置 Token: python scripts/setup_tokens.py"
  echo "  • 查看详细文档: cat docs/PLATFORM_RESEARCH.md"
  echo ""
}

main
