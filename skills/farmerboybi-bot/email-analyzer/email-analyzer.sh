#!/usr/bin/env bash
# Email Analyzer - 邮件分析技能调用脚本
# 固化版 - 改动需 Wood 哥书面同意

set -e

SKILL_DIR="/Users/lobster/.openclaw/workspace/skills/email-analyzer"
WORKSPACE="/Users/lobster/.openclaw/workspace"

cd "$SKILL_DIR"

# 显示帮助
show_help() {
    echo "📧 Email Analyzer - Wood 哥邮箱分析技能"
    echo ""
    echo "用法:"
    echo "  $0 analyze <start-date> <end-date>  # 分析指定日期范围"
    echo "  $0 backup <uids-file> <output>      # 备份待删除 UID"
    echo "  $0 delete <uids-file>               # 执行删除（需二次确认）"
    echo "  $0 verify                           # 验证删除结果"
    echo ""
    echo "示例:"
    echo "  $0 analyze 2021-02-26 2021-08-26"
    echo "  $0 backup analysis_report.json batch8_backup.json"
    echo "  $0 delete analysis_report.json"
    echo ""
}

# 检查参数
if [ $# -lt 1 ]; then
    show_help
    exit 1
fi

MODE=$1

case $MODE in
    analyze)
        if [ $# -lt 3 ]; then
            echo "❌ 分析模式需要 start-date 和 end-date 参数"
            echo "用法：$0 analyze <start-date> <end-date>"
            exit 1
        fi
        START_DATE=$2
        END_DATE=$3
        OUTPUT="$WORKSPACE/analysis_$(date +%Y%m%d_%H%M%S).json"
        
        echo "📊 分析邮件：$START_DATE ~ $END_DATE"
        python3 email_analyzer.py \
            --start-date "$START_DATE" \
            --end-date "$END_DATE" \
            --output "$OUTPUT" \
            --mode analyze
        
        echo ""
        echo "✅ 分析完成！报告：$OUTPUT"
        echo "⚠️  请 Wood 哥确认后回复'删除'执行删除操作"
        ;;
    
    backup)
        if [ $# -lt 3 ]; then
            echo "❌ 备份模式需要 uids-file 和 output 参数"
            echo "用法：$0 backup <uids-file> <output>"
            exit 1
        fi
        UIDS_FILE=$2
        OUTPUT=$3
        
        echo "💾 备份 UID：$UIDS_FILE → $OUTPUT"
        python3 backup.py \
            --uids-file "$UIDS_FILE" \
            --output "$OUTPUT"
        ;;
    
    delete)
        if [ $# -lt 2 ]; then
            echo "❌ 删除模式需要 uids-file 参数"
            echo "用法：$0 delete <uids-file>"
            exit 1
        fi
        UIDS_FILE=$2
        
        echo "⚠️  警告：即将执行删除操作！"
        echo "请确认已备份，然后输入 'yes' 继续："
        read -r CONFIRM
        
        if [ "$CONFIRM" != "yes" ]; then
            echo "❌ 删除已取消"
            exit 1
        fi
        
        python3 delete.py \
            --uids-file "$UIDS_FILE" \
            --confirm
        ;;
    
    verify)
        echo "📊 验证删除结果..."
        python3 verify.py
        ;;
    
    *)
        echo "❌ 未知模式：$MODE"
        show_help
        exit 1
        ;;
esac
