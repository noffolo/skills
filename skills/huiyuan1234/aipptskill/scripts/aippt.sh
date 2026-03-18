#!/bin/bash
# ============================================================================
# AiPPT API 集成脚本 v2.0
# 官方文档: https://open.aippt.cn/docs/zh/
# 作者: 小龙 🐉 for OpenClaw | 版本: 2.0.0 (2026-03-10)
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
ENV_FILE="${SKILL_DIR}/.env"
TOKEN_CACHE="${SKILL_DIR}/.token_cache.json"
BASE_URL="https://co.aippt.cn"

[ -f "$ENV_FILE" ] && source "$ENV_FILE"
APP_KEY="${AIPPT_APP_KEY:-}"
SECRET_KEY="${AIPPT_SECRET_KEY:-}"
UID_VALUE="${AIPPT_UID:-openclaw_default}"

die() { echo "{\"error\": \"$1\"}" >&2; exit 1; }

generate_signature() {
    local sign_str="${1}@${2}@${3}"
    echo -n "$sign_str" | openssl dgst -sha1 -hmac "$SECRET_KEY" -binary | base64
}

get_token() {
    local now=$(date +%s)
    if [ -f "$TOKEN_CACHE" ]; then
        local t=$(python3 -c "import json;d=json.load(open('$TOKEN_CACHE'));print(d.get('token',''))" 2>/dev/null)
        local e=$(python3 -c "import json;d=json.load(open('$TOKEN_CACHE'));print(d.get('expire_time',0))" 2>/dev/null)
        [ -n "$t" ] && [ "$e" -gt "$now" ] 2>/dev/null && { echo "$t"; return 0; }
    fi
    local ts=$(date +%s)
    local sig=$(generate_signature "GET" "/api/grant/token/" "$ts")
    local resp=$(curl -s "${BASE_URL}/api/grant/token/" \
        -H "x-api-key: ${APP_KEY}" -H "x-timestamp: ${ts}" -H "x-signature: ${sig}" \
        --data-urlencode "uid=${UID_VALUE}")
    local token=$(echo "$resp" | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['token'])")
    local exp=$(echo "$resp" | python3 -c "import sys,json;d=json.load(sys.stdin)['data'];print(int(d.get('time_stamp',0))+int(d.get('expire',0)))")
    python3 -c "import json;json.dump({'token':'$token','expire_time':$exp,'cached_at':$(date +%s)},open('$TOKEN_CACHE','w'),indent=2)"
    echo "$token"
}

api_get() {
    local path="$1"; shift
    local token=$(get_token)
    eval curl -s "\"${BASE_URL}${path}\"" -H "'x-api-key: ${APP_KEY}'" -H "'x-channel;'" -H "'x-token: ${token}'" "$@"
}

api_post() {
    local path="$1"; shift
    local token=$(get_token)
    eval curl -s -X POST "\"${BASE_URL}${path}\"" -H "'x-api-key: ${APP_KEY}'" -H "'x-channel;'" -H "'x-token: ${token}'" "$@"
}

# === 命令 ===

cmd_auth() {
    [ -n "$APP_KEY" ] && [ -n "$SECRET_KEY" ] || die "未设置 AIPPT_APP_KEY / AIPPT_SECRET_KEY"
    local ts=$(date +%s)
    local sig=$(generate_signature "GET" "/api/grant/token/" "$ts")
    curl -s "${BASE_URL}/api/grant/token/" \
        -H "x-api-key: ${APP_KEY}" -H "x-timestamp: ${ts}" -H "x-signature: ${sig}" \
        --data-urlencode "uid=${UID_VALUE}"
}

cmd_create() {
    local title="${1:?用法: create <标题> [type]}"
    local type="${2:-1}"
    api_post "/api/ai/chat/v2/task" --data-urlencode "title=${title}" --data-urlencode "type=${type}"
}

cmd_create_with_file() {
    local file="${1:?用法: create_with_file <文件路径> [type]}"
    local type="${2:-}"
    [ -f "$file" ] || die "文件不存在: $file"
    if [ -z "$type" ]; then
        case "${file##*.}" in
            doc|docx) type=3;; xmind) type=4;; mm) type=5;; md) type=7;;
            pdf) type=8;; txt) type=9;; ppt|pptx) type=10;;
            *) die "无法推断文件类型, 请指定type (3=Word,4=XMind,5=FreeMind,7=Markdown,8=PDF,9=TXT,10=PPTX)";;
        esac
    fi
    api_post "/api/ai/chat/v2/task" -F "file=@${file}" -F "type=${type}"
}

cmd_create_from_url() {
    local url="${1:?用法: create_from_url <URL>}"
    api_post "/api/ai/chat/v2/task" --data-urlencode "type=16" --data-urlencode "link=${url}"
}

cmd_outline() {
    local task_id="${1:?用法: outline <task_id>}"
    local token=$(get_token)
    curl -s --max-time 120 -N "${BASE_URL}/api/ai/chat/outline?task_id=${task_id}" \
        -H "x-api-key: ${APP_KEY}" -H "x-channel;" -H "x-token: ${token}"
}

cmd_content() {
    local task_id="${1:?用法: content <task_id> [template_id]}"
    local tpl="${2:-}"
    local url="/api/ai/chat/v2/content?task_id=${task_id}"
    [ -n "$tpl" ] && url="${url}&template_id=${tpl}"
    api_get "$url"
}

cmd_check() {
    local ticket="${1:?用法: check <ticket> (注意: 参数是ticket, 不是task_id!)}"
    api_get "/api/ai/chat/v2/content/check?ticket=${ticket}"
}

cmd_wait() {
    local ticket="${1:?用法: wait <ticket> [timeout_seconds]}"
    local timeout="${2:-120}"
    local elapsed=0
    while [ "$elapsed" -lt "$timeout" ]; do
        local resp=$(cmd_check "$ticket")
        local status=$(echo "$resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('data',{}).get('status',''))" 2>/dev/null)
        if [ "$status" = "2" ]; then
            echo "$resp"
            return 0
        fi
        sleep 3; elapsed=$((elapsed + 3))
    done
    die "等待内容生成超时 (${timeout}秒)"
}

cmd_options() {
    api_get "/api/template_component/suit/select"
}

cmd_templates() {
    local page="${1:-1}" size="${2:-10}" color="${3:-}" style="${4:-}"
    local url="/api/template_component/suit/search?page=${page}&size=${size}"
    [ -n "$color" ] && url="${url}&color=${color}"
    [ -n "$style" ] && url="${url}&style=${style}"
    api_get "$url"
}

cmd_save() {
    local task_id="${1:?用法: save <task_id> <template_id> [name]}"
    local tpl_id="${2:?用法: save <task_id> <template_id> [name]}"
    local name="${3:-}"
    local args="--data-urlencode 'task_id=${task_id}' --data-urlencode 'template_id=${tpl_id}'"
    [ -n "$name" ] && args="${args} --data-urlencode 'name=${name}'"
    eval api_post "/api/design/v2/save" ${args}
}

cmd_export() {
    local design_id="${1:?用法: export <design_id> [format] [edit]}"
    local format="${2:-ppt}" edit="${3:-true}"
    api_post "/api/download/export/file" -d "id=${design_id}" -d "format=${format}" -d "edit=${edit}" -d "files_to_zip=false"
}

cmd_export_result() {
    local task_key="${1:?用法: export_result <task_key>}"
    api_post "/api/download/export/file/result" -d "task_key=${task_key}"
}

cmd_wait_export() {
    local task_key="${1:?用法: wait_export <task_key> [timeout_seconds]}"
    local timeout="${2:-120}"
    local elapsed=0
    while [ "$elapsed" -lt "$timeout" ]; do
        local resp=$(cmd_export_result "$task_key")
        local parsed=$(echo "$resp" | python3 -c "
import sys,json
d=json.load(sys.stdin)
code=d.get('code','')
msg=d.get('msg','')
data=d.get('data',[])
if code==20003:
    print('QUEUE_FULL')
elif code==0:
    if isinstance(data,list) and data and isinstance(data[0],str) and data[0].startswith('http'):
        print(data[0])
    elif isinstance(data,str) and data.startswith('http'):
        print(data)
    else:
        print('PENDING')
else:
    print(f'ERROR:{code}:{msg}')
" 2>/dev/null)
        case "$parsed" in
            http*)
                echo "$parsed"
                return 0
                ;;
            QUEUE_FULL)
                echo '{"step":"wait_export","msg":"导出队列已满，等待中..."}' >&2
                sleep 5; elapsed=$((elapsed + 5))
                ;;
            PENDING)
                sleep 3; elapsed=$((elapsed + 3))
                ;;
            ERROR:*)
                die "导出失败: $parsed"
                ;;
            *)
                sleep 3; elapsed=$((elapsed + 3))
                ;;
        esac
    done
    die "等待导出超时 (${timeout}秒)"
}

verify_file() {
    local file="$1" format="$2"
    [ -f "$file" ] || return 1
    local size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
    [ "$size" -gt 1000 ] 2>/dev/null || return 1  # 文件太小，可能是错误页
    local magic=$(head -c 4 "$file" | xxd -p 2>/dev/null)
    case "$format" in
        ppt)  [[ "$magic" == "504b0304" ]] || return 1 ;;  # PK (zip)
        pdf)  [[ "$magic" == "25504446" ]] || return 1 ;;  # %PDF
        *)    return 0 ;;  # png/word 不检查
    esac
}

cmd_download() {
    local task_id="${1:?用法: download <task_id> <template_id> <output_path> [format] [name]}"
    local tpl_id="${2:?用法: download <task_id> <template_id> <output_path> [format] [name]}"
    local output="${3:?用法: download <task_id> <template_id> <output_path> [format] [name]}"
    local format="${4:-ppt}"
    local name="${5:-}"

    echo '{"step":"save","msg":"正在生成PPT作品..."}' >&2
    local save_resp=$(cmd_save "$task_id" "$tpl_id" "$name")
    local design_id=$(echo "$save_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('data',{}).get('id',''))" 2>/dev/null)
    [ -n "$design_id" ] && [ "$design_id" != "" ] || die "生成PPT作品失败: $save_resp"
    echo "{\"step\":\"save_done\",\"design_id\":\"${design_id}\"}" >&2

    echo '{"step":"export","msg":"正在导出文件..."}' >&2
    local export_resp=$(cmd_export "$design_id" "$format")
    local export_code=$(echo "$export_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('code',''))" 2>/dev/null)
    local task_key=$(echo "$export_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('data',''))" 2>/dev/null)
    
    # 如果队列满, 等待后重试 (最多3次)
    local retries=0
    while [ "$export_code" = "20003" ] && [ "$retries" -lt 3 ]; do
        echo '{"step":"export","msg":"导出队列已满，等待10秒后重试..."}' >&2
        sleep 10
        export_resp=$(cmd_export "$design_id" "$format")
        export_code=$(echo "$export_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('code',''))" 2>/dev/null)
        task_key=$(echo "$export_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('data',''))" 2>/dev/null)
        retries=$((retries + 1))
    done
    [ -n "$task_key" ] && [ "$task_key" != "" ] || die "触发导出失败: $export_resp"

    echo '{"step":"wait_export","msg":"等待导出完成..."}' >&2
    local download_url=$(cmd_wait_export "$task_key" 180)
    [ -n "$download_url" ] || die "获取下载链接失败"

    echo '{"step":"downloading","msg":"正在下载文件..."}' >&2
    curl -sL -o "$output" "$download_url" || die "下载失败"
    
    # 验证下载文件
    if ! verify_file "$output" "$format"; then
        local actual_size=$(stat -f%z "$output" 2>/dev/null || stat -c%s "$output" 2>/dev/null || echo "0")
        die "文件验证失败: 格式不正确或文件损坏 (size=${actual_size}字节)"
    fi
    
    local size=$(ls -l "$output" | awk '{print $5}')
    echo "{\"step\":\"done\",\"file\":\"${output}\",\"size\":${size},\"design_id\":\"${design_id}\"}"
}

cmd_generate() {
    local title="${1:?用法: generate <标题> [template_id] [output_dir] [formats]}"
    local tpl_id="${2:-}"
    local output_dir="${3:-$SKILL_DIR}"
    local formats="${4:-ppt}"  # 逗号分隔: ppt,pdf,word,png

    echo '{"step":"create","msg":"创建任务..."}' >&2
    local create_resp=$(cmd_create "$title")
    local task_id=$(echo "$create_resp" | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['id'])" 2>/dev/null)
    [ -n "$task_id" ] || die "创建任务失败: $create_resp"
    echo "{\"step\":\"created\",\"task_id\":\"${task_id}\"}" >&2

    echo '{"step":"outline","msg":"生成大纲..."}' >&2
    cmd_outline "$task_id" > /dev/null 2>&1

    echo '{"step":"content","msg":"生成内容..."}' >&2
    local content_resp=$(cmd_content "$task_id" "$tpl_id")
    local ticket=$(echo "$content_resp" | python3 -c "import sys,json;print(json.load(sys.stdin)['data'])" 2>/dev/null)
    [ -n "$ticket" ] || die "触发内容生成失败: $content_resp"
    echo "{\"step\":\"content_triggered\",\"ticket\":\"${ticket}\"}" >&2

    echo '{"step":"wait_content","msg":"等待内容生成完成..."}' >&2
    cmd_wait "$ticket" > /dev/null
    echo '{"step":"content_done","msg":"内容生成完成"}' >&2

    # 如果没有指定模板, 选推荐第一个
    if [ -z "$tpl_id" ]; then
        echo '{"step":"pick_template","msg":"选择推荐模板..."}' >&2
        tpl_id=$(cmd_templates 1 1 | python3 -c "import sys,json;d=json.load(sys.stdin);items=d.get('data',{}).get('list',[]);print(items[0]['id'] if items else '')" 2>/dev/null)
        [ -n "$tpl_id" ] || die "无法获取模板"
        echo "{\"step\":\"template_picked\",\"template_id\":\"${tpl_id}\"}" >&2
    fi

    # 生成 PPT 作品 (只需一次)
    echo '{"step":"save","msg":"正在生成PPT作品..."}' >&2
    local save_resp=$(cmd_save "$task_id" "$tpl_id" "$title")
    local design_id=$(echo "$save_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('data',{}).get('id',''))" 2>/dev/null)
    [ -n "$design_id" ] && [ "$design_id" != "" ] || die "生成PPT作品失败: $save_resp"
    echo "{\"step\":\"save_done\",\"design_id\":\"${design_id}\"}" >&2

    local safe_title=$(echo "$title" | tr '/:*?"<>|\\' '_')
    mkdir -p "$output_dir"
    local results="["

    # 按格式顺序导出 (不能并行, 会导致队列满)
    IFS=',' read -ra FMT_ARRAY <<< "$formats"
    for fmt in "${FMT_ARRAY[@]}"; do
        fmt=$(echo "$fmt" | tr -d ' ')
        local ext="pptx"
        case "$fmt" in
            ppt)  ext="pptx" ;;
            pdf)  ext="pdf" ;;
            word) ext="docx" ;;
            png)  ext="png" ;;
        esac
        local outfile="${output_dir}/${safe_title}.${ext}"

        echo "{\"step\":\"export\",\"msg\":\"导出${fmt}...\"}" >&2
        
        # 触发导出 (带重试)
        local export_resp export_code task_key retries=0
        while true; do
            export_resp=$(cmd_export "$design_id" "$fmt")
            export_code=$(echo "$export_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('code',''))" 2>/dev/null)
            task_key=$(echo "$export_resp" | python3 -c "import sys,json;print(json.load(sys.stdin).get('data',''))" 2>/dev/null)
            if [ "$export_code" = "20003" ] && [ "$retries" -lt 5 ]; then
                echo "{\"step\":\"export\",\"msg\":\"导出队列已满，等待后重试(${retries})...\"}" >&2
                sleep 10
                retries=$((retries + 1))
            else
                break
            fi
        done
        [ -n "$task_key" ] && [ "$task_key" != "" ] || { echo "{\"step\":\"error\",\"msg\":\"${fmt}导出触发失败\"}" >&2; continue; }

        echo "{\"step\":\"wait_export\",\"msg\":\"等待${fmt}导出完成...\"}" >&2
        local download_url=$(cmd_wait_export "$task_key" 180)
        if [ -z "$download_url" ]; then
            echo "{\"step\":\"error\",\"msg\":\"${fmt}导出超时\"}" >&2
            continue
        fi

        curl -sL -o "$outfile" "$download_url"
        if verify_file "$outfile" "$fmt"; then
            local fsize=$(ls -l "$outfile" | awk '{print $5}')
            echo "{\"step\":\"downloaded\",\"format\":\"${fmt}\",\"file\":\"${outfile}\",\"size\":${fsize}}" >&2
            results="${results}{\"format\":\"${fmt}\",\"file\":\"${outfile}\",\"size\":${fsize}},"
        else
            echo "{\"step\":\"error\",\"msg\":\"${fmt}文件验证失败\"}" >&2
            rm -f "$outfile"
        fi
    done

    results="${results%,}]"
    echo "{\"step\":\"done\",\"task_id\":\"${task_id}\",\"design_id\":\"${design_id}\",\"template_id\":\"${tpl_id}\",\"files\":${results}}"
}

# === 入口 ===
cmd="${1:-help}"shift 2>/dev/null || true

case "$cmd" in
    auth)              cmd_auth "$@" ;;
    create)            cmd_create "$@" ;;
    create_with_file)  cmd_create_with_file "$@" ;;
    create_from_url)   cmd_create_from_url "$@" ;;
    outline)           cmd_outline "$@" ;;
    content)           cmd_content "$@" ;;
    check)             cmd_check "$@" ;;
    wait)              cmd_wait "$@" ;;
    options)           cmd_options "$@" ;;
    templates)         cmd_templates "$@" ;;
    save)              cmd_save "$@" ;;
    export)            cmd_export "$@" ;;
    export_result)     cmd_export_result "$@" ;;
    wait_export)       cmd_wait_export "$@" ;;
    download)          cmd_download "$@" ;;
    generate)          cmd_generate "$@" ;;
    help|*)
        cat <<EOF
AiPPT API 集成脚本 v2.1

一键生成 (推荐):
  generate <标题> [template_id] [output_dir] [formats]
    多格式一键生成PPT并下载。formats用逗号分隔: ppt,pdf,word,png
    示例: generate "年终总结" "" ~/Desktop "ppt,pdf"

分步操作:
  auth                                    获取/刷新 Token
  create <标题> [type]                    创建任务 (type: 1=智能生成)
  create_with_file <文件> [type]          从文件创建 (3=Word,7=MD,8=PDF,9=TXT,10=PPTX)
  create_from_url <URL>                   从网页创建
  outline <task_id>                       获取大纲 (SSE流式)
  content <task_id> [template_id]         触发内容生成 → 返回 ticket
  check <ticket>                          检查生成状态 (注意: 参数是ticket!)
  wait <ticket> [timeout]                 等待内容生成完成
  save <task_id> <template_id> [name]     生成PPT作品 → 返回 design_id
  export <design_id> [format] [edit]      触发导出 (ppt/pdf/png/word)
  export_result <task_key>                查询导出结果
  wait_export <task_key> [timeout]        等待导出完成 → 返回下载URL
  download <task_id> <tpl_id> <path>      save+export+下载三合一
  templates [page] [size] [color] [style] 搜索模板
  options                                 获取模板筛选选项

环境变量 (.env):
  AIPPT_APP_KEY      API Key (必需)
  AIPPT_SECRET_KEY   Secret Key (必需)
  AIPPT_UID          用户标识 (默认: openclaw_default)
EOF
        ;;
esac
