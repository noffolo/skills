import requests
import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter

# ========== 路径配置 ==========
# 从 scripts 目录向上 3 层到达 workspace
script_dir = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))

JSON_OUTPUT_DIR = os.path.join(WORKSPACE, "json")
ANALYSIS_DIR = os.path.join(WORKSPACE, "memory", "bilibili-analysis")
TREND_FILE = os.path.join(ANALYSIS_DIR, "trend.json")

os.makedirs(JSON_OUTPUT_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)

# 榜单配置
RANK_CONFIG = {
    "all": {"api_type": "ranking", "rid": 0, "name": "全站"},
    "anime": {"api_type": "pgc", "season_type": 1, "name": "番剧"},
    "guochuang": {"api_type": "pgc", "season_type": 4, "name": "国创"},
    "documentary": {"api_type": "pgc", "season_type": 3, "name": "纪录片"},
    "movie": {"api_type": "pgc", "season_type": 2, "name": "电影"},
    "tv": {"api_type": "pgc", "season_type": 5, "name": "电视剧"},
    "douga": {"api_type": "ranking", "rid": 1, "name": "动画"},
    "game": {"api_type": "ranking", "rid": 4, "name": "游戏"},
    "kichiku": {"api_type": "ranking", "rid": 119, "name": "鬼畜"},
    "music": {"api_type": "ranking", "rid": 3, "name": "音乐"},
    "dance": {"api_type": "ranking", "rid": 129, "name": "舞蹈"},
    "cinephile": {"api_type": "ranking", "rid": 181, "name": "影视"},
    "ent": {"api_type": "ranking", "rid": 5, "name": "娱乐"},
    "knowledge": {"api_type": "ranking", "rid": 36, "name": "知识"},
    "tech": {"api_type": "ranking", "rid": 188, "name": "科技数码"},
    "food": {"api_type": "ranking", "rid": 211, "name": "美食"},
    "car": {"api_type": "ranking", "rid": 223, "name": "汽车"},
    "fashion": {"api_type": "ranking", "rid": 155, "name": "时尚美妆"},
    "sports": {"api_type": "ranking", "rid": 234, "name": "体育运动"},
    "animal": {"api_type": "ranking", "rid": 217, "name": "动物"},
}


def get_json_path(rank_type="all"):
    """获取 JSON 输出路径"""
    return os.path.join(JSON_OUTPUT_DIR, f"output_{rank_type}.json")


def load_json_data(rank_type="all"):
    """加载最新数据"""
    json_path = get_json_path(rank_type)
    if not os.path.exists(json_path):
        # 兼容旧版本
        json_path = os.path.join(JSON_OUTPUT_DIR, "output.json")
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"文件不存在: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_trend():
    """加载趋势数据"""
    if os.path.exists(TREND_FILE):
        with open(TREND_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"records": [], "keywords": {}, "zones": {}, "rank_stats": {}}


def save_analysis(analysis_content, trend_data, rank_type="all"):
    """保存单次分析结果"""
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    
    # 保存报告
    report_path = os.path.join(ANALYSIS_DIR, f"{rank_type}_{timestamp}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(analysis_content)
    
    # 更新趋势
    trend = load_trend()
    record = {
        "time": timestamp,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "rank_type": rank_type,
        "top_zone": trend_data.get("top_zone", ""),
        "avg_interaction": trend_data.get("avg_interaction_rate", 0),
        "keywords": trend_data.get("keywords", []),
    }
    trend["records"].append(record)
    
    # 更新关键词
    for kw in trend_data.get("keywords", []):
        trend["keywords"][kw] = trend["keywords"].get(kw, 0) + 1
    
    # 更新分区
    zone = trend_data.get("top_zone", "")
    if zone:
        trend["zones"][zone] = trend["zones"].get(zone, 0) + 1
    
    # 更新榜单统计
    if rank_type not in trend["rank_stats"]:
        trend["rank_stats"][rank_type] = 0
    trend["rank_stats"][rank_type] += 1
    
    trend["records"] = trend["records"][-60:]
    
    with open(TREND_FILE, "w", encoding="utf-8") as f:
        json.dump(trend, f, ensure_ascii=False, indent=2)
    
    return report_path


def analyze_trend(rank_type=None):
    """生成趋势报告"""
    trend = load_trend()
    
    if rank_type:
        # 单榜单分析
        filtered = [r for r in trend["records"] if r.get("rank_type") == rank_type]
        if len(filtered) < 3:
            return f"{RANK_CONFIG.get(rank_type, {}).get('name', rank_type)} 数据不足"
        
        zone_counter = {}
        kw_counter = {}
        for r in filtered:
            zone = r.get("top_zone", "")
            if zone:
                zone_counter[zone] = zone_counter.get(zone, 0) + 1
            for kw in r.get("keywords", []):
                kw_counter[kw] = kw_counter.get(kw, 0) + 1
        
        report = f"# {RANK_CONFIG.get(rank_type, {}).get('name', rank_type)} 趋势分析\n\n"
        report += f"分析次数: {len(filtered)} 次\n\n"
        report += "## 热门分区\n"
        for zone, count in sorted(zone_counter.items(), key=lambda x: x[1], reverse=True)[:5]:
            report += f"- {zone}: {count} 次\n"
        report += "\n## 高频关键词\n"
        for kw, count in sorted(kw_counter.items(), key=lambda x: x[1], reverse=True)[:10]:
            report += f"- {kw}: {count} 次\n"
        return report
    
    # 全局趋势
    if len(trend["records"]) < 3:
        return "数据不足，需要至少 3 次记录"
    
    report = "# Bilibili 全站趋势分析\n\n"
    
    report += "## 各榜单热度统计\n"
    for rank, count in sorted(trend.get("rank_stats", {}).items(), key=lambda x: x[1], reverse=True):
        rank_name = RANK_CONFIG.get(rank, {}).get("name", rank)
        report += f"- {rank_name}: {count} 次\n"
    
    report += "\n## 热门分区 TOP 5\n"
    for zone, count in sorted(trend["zones"].items(), key=lambda x: x[1], reverse=True)[:5]:
        report += f"- {zone}: {count} 次登顶\n"
    
    report += "\n## 高频关键词 TOP 10\n"
    for kw, count in sorted(trend["keywords"].items(), key=lambda x: x[1], reverse=True)[:10]:
        report += f"- {kw}: {count} 次\n"
    
    return report


def generate_weekly_summary(rank_type=None):
    """生成周总结"""
    trend = load_trend()
    now = datetime.now()
    week_ago = now - timedelta(days=7)
    
    records = trend["records"]
    if rank_type:
        records = [r for r in records if r.get("rank_type") == rank_type]
    
    weekly_records = []
    for r in records:
        try:
            r_date = datetime.strptime(r.get("date", ""), "%Y-%m-%d")
            if r_date >= week_ago:
                weekly_records.append(r)
        except:
            continue
    
    if not weekly_records:
        return "本周无数据"
    
    zone_counter = {}
    kw_counter = {}
    interactions = []
    
    for r in weekly_records:
        zone = r.get("top_zone", "")
        if zone:
            zone_counter[zone] = zone_counter.get(zone, 0) + 1
        for kw in r.get("keywords", []):
            kw_counter[kw] = kw_counter.get(kw, 0) + 1
        interactions.append(r.get("avg_interaction", 0))
    
    avg_interaction = sum(interactions) / len(interactions) if interactions else 0
    
    rank_name = RANK_CONFIG.get(rank_type, {}).get("name", rank_type) if rank_type else "全站"
    
    report = f"# 周总结 - {rank_name} ({week_ago.strftime('%Y-%m-%d')} ~ {now.strftime('%Y-%m-%d')})\n\n"
    report += f"- 分析次数: {len(weekly_records)} 次\n"
    report += f"- 平均互动率: {avg_interaction:.2f}%\n\n"
    report += "## 热门分区\n"
    for zone, count in sorted(zone_counter.items(), key=lambda x: x[1], reverse=True)[:3]:
        report += f"- {zone}: {count} 次\n"
    
    report += "\n## 热门关键词\n"
    for kw, count in sorted(kw_counter.items(), key=lambda x: x[1], reverse=True)[:5]:
        report += f"- {kw}: {count} 次\n"
    
    prefix = f"weekly-{rank_type}" if rank_type else "weekly"
    weekly_path = os.path.join(ANALYSIS_DIR, f"{prefix}-{now.strftime('%YW%W')}.md")
    with open(weekly_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    return report


def generate_monthly_summary(rank_type=None):
    """生成月总结"""
    trend = load_trend()
    now = datetime.now()
    month_ago = now - timedelta(days=30)
    
    records = trend["records"]
    if rank_type:
        records = [r for r in records if r.get("rank_type") == rank_type]
    
    monthly_records = []
    for r in records:
        try:
            r_date = datetime.strptime(r.get("date", ""), "%Y-%m-%d")
            if r_date >= month_ago:
                monthly_records.append(r)
        except:
            continue
    
    if not monthly_records:
        return "本月无数据"
    
    zone_counter = {}
    kw_counter = {}
    interactions = []
    
    for r in monthly_records:
        zone = r.get("top_zone", "")
        if zone:
            zone_counter[zone] = zone_counter.get(zone, 0) + 1
        for kw in r.get("keywords", []):
            kw_counter[kw] = kw_counter.get(kw, 0) + 1
        interactions.append(r.get("avg_interaction", 0))
    
    avg_interaction = sum(interactions) / len(interactions) if interactions else 0
    
    rank_name = RANK_CONFIG.get(rank_type, {}).get("name", rank_type) if rank_type else "全站"
    
    report = f"# 月总结 - {rank_name} ({month_ago.strftime('%Y-%m-%d')} ~ {now.strftime('%Y-%m-%d')})\n\n"
    report += f"- 分析次数: {len(monthly_records)} 次\n"
    report += f"- 平均互动率: {avg_interaction:.2f}%\n\n"
    report += "## 分区排名\n"
    for zone, count in sorted(zone_counter.items(), key=lambda x: x[1], reverse=True)[:5]:
        report += f"- {zone}: {count} 次登顶\n"
    
    report += "\n## 关键词排行\n"
    for kw, count in sorted(kw_counter.items(), key=lambda x: x[1], reverse=True)[:10]:
        report += f"- {kw}: {count} 次\n"
    
    report += "\n## 趋势洞察\n"
    if kw_counter:
        top_kw = max(kw_counter.items(), key=lambda x: x[1])[0]
        report += f"- 下月预测: {top_kw} 相关内容可能持续火热\n"
    
    prefix = f"monthly-{rank_type}" if rank_type else "monthly"
    monthly_path = os.path.join(ANALYSIS_DIR, f"{prefix}-{now.strftime('%Y-%m')}.md")
    with open(monthly_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    return report


def list_ranks():
    """列出所有榜单"""
    print("\n可用榜单列表:")
    print("-" * 40)
    for key, config in RANK_CONFIG.items():
        print(f"  {key:15} - {config['name']}")
    print("-" * 40)
    print(f"共 {len(RANK_CONFIG)} 个榜单\n")


def run_workflow(rank_type="all"):
    """运行工作流"""
    json_data = load_json_data(rank_type)
    videos = json_data["data"]["videos"]
    summary = json_data["data"]["summary"]
    rank_name = json_data["data"].get("rank_name", RANK_CONFIG.get(rank_type, {}).get("name", rank_type))
    
    # 提取关键词
    keywords = []
    for v in videos[:10]:
        title = v.get("title", "")
        words = re.findall(r'[\u4e00-\u9fa5]{2,4}', title)
        keywords.extend(words[:3])
    
    kw_counter = Counter(keywords)
    top_keywords = [kw for kw, _ in kw_counter.most_common(5)]
    
    trend_data = {
        "top_zone": summary.get("top_zone", ""),
        "avg_interaction_rate": summary.get("avg_interaction_rate", 0),
        "keywords": top_keywords,
    }
    
    analysis_prompt = f"""## {rank_name} 数据概览
- 总视频数: {summary.get('total_videos', 0)}
- 总播放: {summary.get('total_views', 0):,}
- 平均互动率: {summary.get('avg_interaction_rate', 0)}%
- 最热分区: {summary.get('top_zone', '')}

请分析并输出报告：
1. 热门内容分析
2. 分区热度
3. 关键词趋势
4. 下期预测"""

    print(analysis_prompt)
    return {"status": "ready", "prompt": analysis_prompt, "trend_data": trend_data, "rank_type": rank_type}


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "list":
            list_ranks()
        elif sys.argv[1] == "weekly":
            rank = sys.argv[2] if len(sys.argv) > 2 else None
            print(generate_weekly_summary(rank))
        elif sys.argv[1] == "monthly":
            rank = sys.argv[2] if len(sys.argv) > 2 else None
            print(generate_monthly_summary(rank))
        elif sys.argv[1] == "trend":
            rank = sys.argv[2] if len(sys.argv) > 2 else None
            print(analyze_trend(rank))
        else:
            run_workflow(sys.argv[1])
    else:
        run_workflow("all")
