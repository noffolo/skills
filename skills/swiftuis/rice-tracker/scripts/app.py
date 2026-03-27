#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大米消耗采购提醒系统 - Flask Web App
运行方式：
  python3 app.py
  然后浏览器打开 http://localhost:5001
"""

import json
import os
from datetime import date, timedelta
from flask import Flask, request, jsonify, render_template_string, redirect, url_for
from pathlib import Path

app = Flask(__name__)

DATA_FILE = Path.home() / ".openclaw" / "workspace" / "rice-shop-records.json"
PORT = 5001
HOST = "0.0.0.0"   # 改为 0.0.0.0 手机也能访问

# ── 数据读写 ────────────────────────────────────────────────────────────────

def load_records():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_records(records):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

def days_left(record):
    """计算剩余天数（-1=已吃完）"""
    today = date.today()
    purchased = date.fromisoformat(record["purchase_date"])
    consumed_per_day = record["daily_rate"]  # 斤/人/天
    freq = record.get("frequency", "daily")
    people = record["people"]

    if freq == "workdays":
        # 从购买日到今天的工作日天数 × 人均日消耗
        days = (today - purchased).days + 1
        workdays = sum(1 for i in range(days)
                       if (purchased + timedelta(i)).weekday() < 5)
        total_consumed = workdays * people * consumed_per_day
    elif freq == "weekends":
        days = (today - purchased).days + 1
        weekends = sum(1 for i in range(days)
                       if (purchased + timedelta(i)).weekday() >= 5)
        total_consumed = weekends * people * consumed_per_day
    else:  # daily
        total_consumed = (today - purchased).days * people * consumed_per_day

    remaining = record["quantity"] - total_consumed
    if remaining <= 0:
        return -1
    if freq == "workdays":
        # 估算剩余工作日吃完的天数
        days_per_consumed = 1.0 / (people * consumed_per_day)  # 每斤需要多少工作日天
        return round(remaining * days_per_consumed)
    elif freq == "weekends":
        days_per_consumed = 1.0 / (people * consumed_per_day)
        return round(remaining * days_per_consumed * (7/2))  # 按周末频率折算
    else:
        return round(remaining / (people * consumed_per_day))

def expected_date(record):
    d = days_left(record)
    if d < 0:
        return "已吃完"
    return (date.today() + timedelta(days=d)).strftime("%Y-%m-%d")

# ── HTML 模板 ────────────────────────────────────────────────────────────────

CSS = """
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
    background: #f0f2f5;
    color: #1a1a2e;
    min-height: 100vh;
}
.container { max-width: 900px; margin: 0 auto; padding: 20px; }

/* 标题栏 */
.header {
    background: linear-gradient(135deg, #1a1a2e, #0f3460);
    color: white;
    padding: 24px 28px;
    border-radius: 16px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
}
.header h1 { font-size: 1.4em; font-weight: 700; }
.header .subtitle { font-size: 0.85em; opacity: 0.7; margin-top: 2px; }
.header .stats {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}
.header .stat { text-align: center; }
.header .stat .num { font-size: 1.8em; font-weight: 800; }
.header .stat .label { font-size: 0.75em; opacity: 0.7; }

/* 报警横幅 */
.alert-bar {
    background: linear-gradient(90deg, #ff4757, #ff6b81);
    color: white;
    padding: 12px 20px;
    border-radius: 12px;
    margin-bottom: 16px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 10px;
}
.alert-bar.warn {
    background: linear-gradient(90deg, #ffa502, #ff6348);
}

/* 卡片 */
.card {
    background: white;
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,.06);
}

/* 表单 */
.form-title {
    font-size: 1.05em;
    font-weight: 700;
    color: #0f3460;
    margin-bottom: 16px;
    border-left: 4px solid #e94560;
    padding-left: 10px;
}
.form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
}
.form-grid .full { grid-column: 1 / -1; }
.form-grid label {
    font-size: 0.82em;
    color: #666;
    margin-bottom: 4px;
    display: block;
}
.form-grid input,
.form-grid select {
    width: 100%;
    padding: 9px 12px;
    border: 1.5px solid #e0e0e0;
    border-radius: 9px;
    font-size: 0.95em;
    font-family: inherit;
    transition: border-color 0.2s;
    background: #fafafa;
}
.form-grid input:focus,
.form-grid select:focus {
    outline: none;
    border-color: #0f3460;
    background: white;
}
.hint {
    font-size: 0.75em;
    color: #999;
    margin-top: 3px;
}
.btn-row {
    display: flex;
    gap: 10px;
    margin-top: 16px;
}
.btn {
    padding: 10px 22px;
    border: none;
    border-radius: 9px;
    font-size: 0.95em;
    font-weight: 600;
    cursor: pointer;
    font-family: inherit;
    transition: opacity 0.2s, transform 0.1s;
}
.btn:hover { opacity: 0.85; transform: translateY(-1px); }
.btn:active { transform: translateY(0); }
.btn-primary { background: linear-gradient(135deg, #e94560, #c73e54); color: white; }
.btn-secondary { background: #f0f2f5; color: #555; border: 1.5px solid #ddd; }
.btn-danger { background: #ff4757; color: white; padding: 6px 14px; font-size: 0.82em; }
.btn-sm { padding: 6px 14px; font-size: 0.82em; border-radius: 7px; }

/* 表格 */
.table-title {
    font-size: 1.05em;
    font-weight: 700;
    color: #0f3460;
    margin-bottom: 14px;
    border-left: 4px solid #0f3460;
    padding-left: 10px;
}
table { width: 100%; border-collapse: collapse; font-size: 0.88em; }
thead tr {
    background: #f5f5f5;
    color: #888;
}
th {
    text-align: left;
    padding: 9px 10px;
    font-weight: 500;
    font-size: 0.8em;
    border-bottom: 2px solid #e8e8e8;
}
td {
    padding: 11px 10px;
    border-bottom: 1px solid #f0f0f0;
    vertical-align: middle;
}
tr:last-child td { border-bottom: none; }
tr:hover td { background: #fafafa; }

/* 状态标签 */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.8em;
    font-weight: 600;
}
.badge-red { background: #ffe5e5; color: #d63031; }
.badge-orange { background: #fff3e0; color: #e17055; }
.badge-green { background: #e5f9ed; color: #00b894; }
.badge-blue { background: #e8f0fe; color: #1565c0; }
.badge-gray { background: #f0f0f0; color: #888; }

/* 剩余天数大字 */
.days-num {
    font-size: 1.3em;
    font-weight: 800;
    display: block;
    line-height: 1;
}
.days-label { font-size: 0.7em; color: #aaa; }

/* 删除确认 */
.delete-form { display: inline; }

/* 空状态 */
.empty {
    text-align: center;
    padding: 40px;
    color: #bbb;
    font-size: 0.95em;
}
.empty-icon { font-size: 3em; margin-bottom: 10px; }

/* 响应式 */
@media (max-width: 600px) {
    .form-grid { grid-template-columns: 1fr; }
    .header { flex-direction: column; align-items: flex-start; }
    table { font-size: 0.8em; }
    th:nth-child(5), td:nth-child(5) { display: none; }
}
"""

INDEX_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>大米消耗提醒系统</title>
</head>
<body>
""" + CSS + """
<div class="container">

<!-- 标题栏 -->
<div class="header">
  <div>
    <h1>🍚 大米消耗采购提醒系统</h1>
    <div class="subtitle">实时追踪每个买家的消耗进度与采购提醒</div>
  </div>
  <div class="stats">
    <div class="stat"><div class="num">{{ records|length }}</div><div class="label">客户总数</div></div>
    <div class="stat"><div class="num" style="color:#ff4757">{{ urgent_count }}</div><div class="label">待采购</div></div>
    <div class="stat"><div class="num" style="color:#00b894">{{ ok_count }}</div><div class="label">库存充足</div></div>
  </div>
</div>

<!-- 警告列表 -->
{% if urgent_records %}
<div class="alert-bar">
  🚨 <strong>紧急提醒</strong>：{{ urgent_records|length }} 位客户的大米预计 < 3 天后吃完，请及时采购！
</div>
{% endif %}

<!-- 添加记录表单 -->
<div class="card" id="form">
  <div class="form-title">📝 添加 / 编辑客户记录</div>
  <form method="post" action="/add">
    <div class="form-grid">
      <div>
        <label>户主姓名 *</label>
        <input name="owner" placeholder="如：张三" required>
      </div>
      <div>
        <label>手机号（选填）</label>
        <input name="phone" placeholder="方便联系">
      </div>
      <div>
        <label>购买日期 *</label>
        <input name="purchase_date" type="date" value="{{ today }}" required>
      </div>
      <div>
        <label>购买斤数 *</label>
        <input name="quantity" type="number" step="0.1" min="0.1" placeholder="如：40" required>
        <div class="hint">1斤 = 0.5kg，10kg ≈ 20斤</div>
      </div>
      <div>
        <label>家庭人口数 *</label>
        <input name="people" type="number" min="1" value="1" required>
      </div>
      <div>
        <label>人均每天消耗量（斤/人/天）</label>
        <input name="daily_rate" type="number" step="0.05" min="0.05" value="0.4" required>
        <div class="hint">一般 0.3~0.6 斤/人/天</div>
      </div>
      <div class="full">
        <label>消耗频率</label>
        <select name="frequency">
          <option value="daily">每天都吃</option>
          <option value="workdays">只在工作日吃（周一~周五）</option>
          <option value="weekends">只在周末吃（周六、周日）</option>
        </select>
      </div>
      <div class="full">
        <label>备注</label>
        <input name="note" placeholder="如：家里有老人/小孩，消耗较高">
      </div>
    </div>
    <div class="btn-row">
      <button type="submit" class="btn btn-primary">💾 添加记录</button>
      <button type="reset" class="btn btn-secondary">🔄 重置</button>
    </div>
  </form>
</div>

<!-- 记录列表 -->
<div class="card" id="records">
  <div class="table-title">📋 客户记录列表（共 {{ records|length }} 条）</div>
  {% if records %}
  <table>
    <thead>
      <tr>
        <th>户主</th>
        <th>购买日期</th>
        <th>购买量</th>
        <th>人口 / 频率</th>
        <th>预计吃完日期</th>
        <th>剩余天数</th>
        <th>状态</th>
        <th>操作</th>
      </tr>
    </thead>
    <tbody>
    {% for r in records %}
      <tr id="row-{{ loop.index0 }}">
        <td>
          <strong>{{ r.owner }}</strong>
          {% if r.phone %}<br><span style="font-size:0.78em;color:#999">{{ r.phone }}</span>{% endif %}
        </td>
        <td>{{ r.purchase_date }}</td>
        <td>{{ r.quantity }} 斤</td>
        <td>
          {{ r.people }} 人
          <br>
          <span class="badge badge-gray">
            {% if r.frequency == 'daily' %}每天都吃
            {% elif r.frequency == 'workdays' %}工作日吃
            {% else %}周末吃
            {% endif %}
          </span>
        </td>
        <td>{{ r.expected_date }}</td>
        <td style="text-align:center">
          {% set dl = r.days_left %}
          {% if dl < 0 %}
            <span class="days-num" style="color:#d63031">已吃完</span>
          {% else %}
            <span class="days-num" style="color:
              {% if dl <= 2 %}#d63031
              {% elif dl <= 7 %}#e17055
              {% else %}#00b894{% endif %}">
              {{ dl }}
            </span>
            <span class="days-label">天</span>
          {% endif %}
        </td>
        <td>
          {% set dl = r.days_left %}
          {% if dl < 0 %}
            <span class="badge badge-red">已吃完，请采购</span>
          {% elif dl <= 3 %}
            <span class="badge badge-orange">⚠️ 即将耗尽</span>
          {% elif dl <= 7 %}
            <span class="badge badge-blue">还剩{{ dl }}天</span>
          {% else %}
            <span class="badge badge-green">✅ 充足</span>
          {% endif %}
        </td>
        <td>
          <form method="post" action="/delete/{{ loop.index0 }}" style="display:inline"
                onsubmit="return confirm('确定删除【{{ r.owner }}】的记录？')">
            <button type="submit" class="btn-danger">🗑 删除</button>
          </form>
        </td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
  {% else %}
  <div class="empty">
    <div class="empty-icon">🍚</div>
    <div>暂无记录，请添加第一个客户</div>
  </div>
  {% endif %}
</div>

<!-- 底部 -->
<div style="text-align:center;color:#bbb;font-size:0.78em;padding:20px 0">
  数据保存在：{{ data_file }}<br>
  刷新页面查看最新状态 · 每晚 20:00 自动检查提醒
</div>
</div>
</body>
</html>"""

# ── 路由 ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    records = load_records()
    today_str = date.today().isoformat()
    for r in records:
        r["days_left"] = days_left(r)
        r["expected_date"] = expected_date(r)

    urgent_records = [r for r in records if 0 <= r["days_left"] <= 3]
    urgent_count = len(urgent_records)
    ok_count = len([r for r in records if r["days_left"] > 7])

    return render_template_string(
        INDEX_HTML,
        records=records,
        today=today_str,
        urgent_records=urgent_records,
        urgent_count=urgent_count,
        ok_count=ok_count,
        data_file=str(DATA_FILE),
    )

@app.route("/add", methods=["POST"])
def add():
    records = load_records()
    record = {
        "owner": request.form["owner"].strip(),
        "phone": request.form.get("phone", "").strip(),
        "purchase_date": request.form["purchase_date"],
        "quantity": float(request.form["quantity"]),
        "people": int(request.form["people"]),
        "daily_rate": float(request.form["daily_rate"]),
        "frequency": request.form.get("frequency", "daily"),
        "note": request.form.get("note", "").strip(),
        "created": date.today().isoformat(),
    }
    records.append(record)
    save_records(records)
    return redirect(url_for("index"))

@app.route("/delete/<int:idx>", methods=["POST"])
def delete(idx):
    records = load_records()
    if 0 <= idx < len(records):
        del records[idx]
        save_records(records)
    return redirect(url_for("index"))

@app.route("/api/records")
def api_records():
    records = load_records()
    for r in records:
        r["days_left"] = days_left(r)
        r["expected_date"] = expected_date(r)
    return jsonify(records)

@app.route("/api/alert")
def api_alert():
    """供定时任务调用的提醒接口"""
    records = load_records()
    alerts = []
    for r in records:
        dl = days_left(r)
        if dl < 0:
            alerts.append(f"🚨 【{r['owner']}】的大米已耗尽！请立即采购！")
        elif dl <= 3:
            alerts.append(f"⚠️ 【{r['owner']}】的大米预计 {dl} 天后（{expected_date(r)}）吃完，请提醒采购！")
    return jsonify({
        "has_alerts": len(alerts) > 0,
        "alerts": alerts,
        "checked_at": date.today().isoformat(),
    })

# ── 启动 ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"\n🍚 大米消耗提醒系统已启动")
    print(f"   本地访问：http://localhost:{PORT}")
    print(f"   手机访问：http://<本机IP>:{PORT}")
    print(f"   数据文件：{DATA_FILE}")
    print(f"   按 Ctrl+C 停止服务\n")
    app.run(host=HOST, port=PORT, debug=False)
