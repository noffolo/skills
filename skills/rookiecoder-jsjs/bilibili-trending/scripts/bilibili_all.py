"""
Bilibili 热门数据抓取与分析自动化脚本

完整流程：
1. 抓取数据
2. 自动调用子 Agent 分析
3. 自动保存报告
"""

import requests
import json
import time
import random
import os
import re
import argparse
import sys
from datetime import datetime
from collections import Counter

# ========== 配置 ==========
script_dir = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
JSON_OUTPUT_DIR = os.path.join(WORKSPACE, "json")
ANALYSIS_DIR = os.path.join(WORKSPACE, "memory", "bilibili-analysis")
TREND_FILE = os.path.join(ANALYSIS_DIR, "trend.json")

os.makedirs(JSON_OUTPUT_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)

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


def fetch_ranking_v2(rid):
    """抓取普通视频排行榜"""
    url = "https://api.bilibili.com/x/web-interface/ranking/v2"
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"rid": rid, "type": "all", "pn": 1, "ps": 30}
    
    time.sleep(random.uniform(1, 3))
    response = requests.get(url, headers=headers, params=params, timeout=10)
    raw_data = response.json()
    
    if raw_data.get("code") != 0:
        raise Exception(f"API错误: {raw_data.get('message')}")
    return raw_data


def fetch_pgc_ranking(season_type):
    """抓取PGC内容排行榜"""
    url = "https://api.bilibili.com/pgc/season/rank/list"
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"season_type": season_type}
    
    time.sleep(random.uniform(1, 3))
    response = requests.get(url, headers=headers, params=params, timeout=10)
    raw_data = response.json()
    
    if raw_data.get("code") != 0:
        raise Exception(f"API错误: {raw_data.get('message')}")
    return raw_data


def process_ranking_v2(raw_data):
    """处理普通视频数据"""
    video_list = raw_data["data"]["list"]
    processed = []
    
    for idx, v in enumerate(video_list):
        view = v["stat"]["view"]
        danmaku = v["stat"]["danmaku"]
        reply = v["stat"]["reply"]
        like = v["stat"]["like"]
        
        processed.append({
            "rank": idx + 1,
            "title": v.get("title", "").strip(),
            "tname": v.get("tname"),
            "view": view,
            "danmaku": danmaku,
            "reply": reply,
            "like": like,
            "interaction_rate": round((danmaku + reply) / max(view, 1) * 100, 3),
        })
    
    total_views = sum(v["stat"]["view"] for v in video_list)
    zone_dist = {}
    for v in video_list:
        tname = v.get("tname")
        zone_dist[tname] = zone_dist.get(tname, 0) + 1
    
    return processed, {
        "total_videos": len(processed),
        "total_views": total_views,
        "avg_interaction_rate": round(sum(p["interaction_rate"] for p in processed) / len(processed), 3),
        "top_zone": max(zone_dist.items(), key=lambda x: x[1])[0] if zone_dist else "",
        "zone_distribution": zone_dist,
    }


def load_trend():
    """加载趋势数据"""
    if os.path.exists(TREND_FILE):
        with open(TREND_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"records": [], "keywords": {}, "zones": {}}


def save_trend(rank_type, top_zone, keywords, avg_interaction):
    """保存趋势数据"""
    trend = load_trend()
    trend["records"].append({
        "time": datetime.now().strftime("%Y-%m-%d-%H%M%S"),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "rank_type": rank_type,
        "top_zone": top_zone,
        "avg_interaction": avg_interaction,
        "keywords": keywords,
    })
    
    for kw in keywords:
        trend["keywords"][kw] = trend["keywords"].get(kw, 0) + 1
    if top_zone:
        trend["zones"][top_zone] = trend["zones"].get(top_zone, 0) + 1
    
    trend["records"] = trend["records"][-60:]
    
    with open(TREND_FILE, "w", encoding="utf-8") as f:
        json.dump(trend, f, ensure_ascii=False, indent=2)


def generate_prompt(rank_type, videos, summary):
    """生成分析 prompt"""
    rank_name = RANK_CONFIG[rank_type]["name"]
    
    # 提取关键词
    keywords = []
    for v in videos[:10]:
        words = re.findall(r'[\u4e00-\u9fa5]{2,4}', v.get("title", ""))
        keywords.extend(words[:2])
    kw_counter = Counter(keywords)
    top_keywords = [kw for kw, _ in kw_counter.most_common(5)]
    
    top_videos = videos[:5]
    
    prompt = f"""请分析以下 Bilibili {rank_name} 热门视频数据：

## 数据概览
- 榜单: {rank_name}
- 总视频数: {summary.get('total_videos', 0)}
- 总播放: {summary.get('total_views', 0):,}
- 平均互动率: {summary.get('avg_interaction_rate', 0)}%
- 最热分区: {summary.get('top_zone', '')}

## Top 5 视频
{json.dumps(top_videos, ensure_ascii=False, indent=2)}

## 提取的关键词
{json.dumps(top_keywords, ensure_ascii=False)}

## 分区分布
{json.dumps(summary.get('zone_distribution', {}), ensure_ascii=False)}

请输出分析报告（Markdown 格式），包含：
1. 热门内容分析
2. 分区热度分析
3. 关键词趋势
4. 下期预测（什么题材可能火）

请用中文输出，直接输出报告内容。"""
    
    return prompt, top_keywords


def save_report(rank_type, content):
    """保存分析报告"""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    rank_name = RANK_CONFIG[rank_type]["name"]
    filename = f"{timestamp}_{rank_name}.md"
    filepath = os.path.join(ANALYSIS_DIR, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    return filepath


def main():
    parser = argparse.ArgumentParser(description="Bilibili 热门数据分析")
    parser.add_argument("--rank", "-r", type=str, default="all", help="榜单类型")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有榜单")
    parser.add_argument("--auto", "-a", action="store_true", help="自动完成整个流程")
    args = parser.parse_args()
    
    # 列出榜单
    if args.list:
        print("\n可用榜单:")
        for key, config in RANK_CONFIG.items():
            print(f"  {key:15} - {config['name']}")
        return
    
    rank_type = args.rank
    config = RANK_CONFIG[rank_type]
    rank_name = config["name"]
    
    print(f"\n{'='*50}")
    print(f"开始抓取 {rank_name} 榜单...")
    print("=" * 50)
    
    # Step 1: 抓取数据
    try:
        if config["api_type"] == "ranking":
            raw_data = fetch_ranking_v2(config["rid"])
            videos, summary = process_ranking_v2(raw_data)
        else:
            raw_data = fetch_pgc_ranking(config["season_type"])
            videos, summary = process_pgc_ranking_data(raw_data)
    except Exception as e:
        print(f"抓取失败: {e}")
        return
    
    print(f"✓ 成功抓取 {len(videos)} 条数据")
    print(f"  总播放: {summary['total_views']:,}")
    print(f"  平均互动率: {summary['avg_interaction_rate']}%")
    print(f"  最热分区: {summary['top_zone']}")
    
    # Step 2: 保存 JSON
    output_path = os.path.join(JSON_OUTPUT_DIR, f"output_{rank_type}.json")
    result = {
        "result": "success",
        "data": {
            "rank_type": rank_type,
            "rank_name": rank_name,
            "videos": videos,
            "summary": summary
        }
    }
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"✓ 数据已保存: {output_path}")
    
    # Step 3: 生成 prompt 并更新趋势
    prompt, top_keywords = generate_prompt(rank_type, videos, summary)
    save_trend(rank_type, summary.get("top_zone", ""), top_keywords, summary.get("avg_interaction_rate", 0))
    print(f"✓ 趋势数据已更新")
    
    # Step 4: 输出提示
    print(f"\n{'='*50}")
    print("下一步操作:")
    print("=" * 50)
    print("请将以下 prompt 发送给子 Agent 进行分析：")
    print("-" * 50)
    print(prompt)
    print("-" * 50)
    print(f"\n分析完成后，报告将自动保存为：")
    print(f"  memory/bilibili-analysis/{{时间}}_{rank_name}.md")
    print(f"\n趋势文件位置: {TREND_FILE}")


if __name__ == "__main__":
    main()
