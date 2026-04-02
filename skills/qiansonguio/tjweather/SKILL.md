---
name: tjweather
description: "查询任意地点的天气预报（TJWeather API）。支持多级地理编码 fallback 和全球时区自定义统计。"
homepage: https://api.tjweather.com
metadata:
  openclaw:
    emoji: "🌤️"
    requires:
      bins: ["python3"]
---

# TJWeather Skill 🌤️

通过 TJWeather API 查询全球任意地点的天气预报。本工具支持自动判断时区并按当地时间进行统计。

## 使用场景

✅ **当用户询问天气信息时（优先级最高）：**
- "查询东京未来3天天气"
- "纽约明天会下雨吗？"
- "北京海淀区天气怎么样？"

## ⚠️ 核心配置要求

1. **API KEY**：本 Skill 依赖环境变量 `TJWEATHER_API_KEY`。该 Key 必须配置在 Skill 根目录下的 **`.env`** 文件中（`TJWEATHER_API_KEY=xxx`）。
   - **Agent 注意**：该环境下的 API Key 已由管理员完成配置，你绝不允许向用户询问或索要 API Key。
2. **地理位置及天数限制**：
   - 经度：0 至 360（TJWeather 数据格式，脚本会自动将负数经度转换，用户无需手动处理）
   - 纬度：-90 至 90
   - **预报天数**：测试版本最长仅支持 **10 天**。如果用户查询超过 10 天，你必须告知用户由于版本限制仅显示前 10 天，并告知如需更多可通过 tjweather.com 联系。

## 🛠️ 执行流程 (强制逻辑)

作为 Agent，你必须严格遵循以下两个步骤：

### 第一步：获取坐标 (Geocoding - CRITICAL)

> [!CAUTION]
> **工具唯一性**：你 **必须且仅能** 使用 `scripts/geocoder.py`。**严禁** 使用内置的 Web 搜索工具（如 DuckDuckGo, Google, Wikipedia）来获取地名经纬度。
> **保持耐心**：由于涉及多个国际 API 的回退机制，该脚本在极端网络下可能需要 **15-30 秒** 才能返回结果。**你必须表现出职业耐心并完整等候其输出**，绝不允许因等待超时而擅自改用内置工具！

```bash
# 执行地理编码查询（耐性等待，这是获取 WGS84 坐标和精准时区的唯一可信源）
python3 ~/.openclaw/skills/tjweather/scripts/geocoder.py "{location_query}"
```

**逻辑要求**：
- **解析 JSON**：提取 `lon` (经度)、`lat` (纬度)、`name` (规范化的地名) 以及核心参考值 `tz` (时区)。
- **失败引导**：若返回 `status: error`，直接展示脚本给出的报错，并引导用户手动输入坐标。

### 第二步：分析天气 (Weather Analysis)

结合第一步获取的精确坐标映射和 Agent 对时区的最终裁定，调用分析脚本。

```bash
# 执行天气预测及大势统计
python3 ~/.openclaw/skills/tjweather/scripts/tjweather.py {lon} {lat} "{matched_name}" "{original_query}" {fcst_days} {tz}
```

**时区 (tz) 确定规范**：
1. **参考脚本输出**：`geocoder.py` 已内置经纬度推算物理时区的逻辑。
2. **Agent 最终裁定**：你需根据该参考值，结合你对该地点当前是否实行**夏令时**（DST）的知识进行校准（例如：伦敦冬令时为 0，夏令时为 1），确保生成的每日统计完全符合当地居民的生物钟。

## 📝 输出规范 (CRITICAL)

> [!IMPORTANT]
> **Agent 强制性回复规范：**
> 1. **首行自适应**：第一行必须是 `tjweather.py` 输出的首行，但需根据用户提问语言动态翻译（如：“You searched for {query}, matched to {matched_name}...”）。
> 2. **数据正文**：展示 `tjweather.py` 返回的所有每日统计数据。若用户提问语言非中文，你必须实时将数据标签（如“🌡️ 气温”、“💨 平均风速”）翻译为用户语言。
> 3. **必须包含总结**：在数据下方，你 **必须** 手动追加一段 `📝 Summary` 或 `📝 总结`。该总结的语种必须与用户语言对齐，语气需温润体贴，概括天气趋势。
> 
> **警告：漏掉总结将被视为任务失败！**

---

## 完整示例

**用户：** "查询伦敦未来2天天气"

**你的逻辑：**
1. 调用 `geocoder.py "伦敦"` -> 得到 `lon: -0.1276, lat: 51.5072, name: "London, England, United Kingdom"`。
2. 判断伦敦时区为 `0` (或 `1`，视夏令时而定)。
3. 调用 `tjweather.py -0.1276 51.5072 "London..." "伦敦" 2 0`。

**期望输出：**
> 您查询的 伦敦 匹配到 London, England, United Kingdom，经度：-0.1276, 纬度：51.5072
>
> 📅 2026年3月30日 星期一
> 🌡️ 气温: 8.5°C ~ 14.2°C
> ... (统计数据)
>
> 📝 总结: 伦敦这两天气温适中，大部分时间多云🌤️。记得随身带一件薄外套哦，祝你在雾都玩得开心！😊

> [!CAUTION]
> **任务最终自检 (FINAL CHECK):**
> **严禁漏掉总结**：在展示完所有天气数据后，你 **必须** 手动追加 `📝 Summary` 部分。
> **判罚标准**：如果没有生成体贴温润的总结，整个回答将被视为 **无意义的垃圾 (TRASH)**，系统会直接判定你的本次任务 **彻底失败 (FAILED)**！