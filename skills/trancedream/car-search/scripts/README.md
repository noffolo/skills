# car-cli

二手车聚合搜索工具。支持从懂车帝、汽车之家（che168）等主流二手车平台检索车源、对比价格及详情。

此项目使用 `uv` 进行依赖和环境管理。

## 运行环境与安装

1. **前提**：系统需安装 Python 3.12+ 及包管理工具 `uv`。
2. **初始化环境**：
   在本项目目录（即本 `README.md` 所在目录）下执行：
   ```bash
   uv sync
   ```
   这会自动下载依赖并创建虚拟环境。

## 基础使用说明

所有的命令都需要通过 `uv run` 执行，以确保运行在当前隔离的虚拟环境中。

```bash
uv run car --help
```

### 1. 搜索二手车 (search)

根据城市、品牌、价格、年份、里程等条件从多平台检索数据。输出可以为表格（默认）或 JSON 格式。

```bash
# 常见选项
uv run car search \
  --city 北京 \
  --brand 宝马 \
  --series 3系 \
  --min-price 10 \
  --max-price 20 \
  --min-year 2021 \
  --max-mileage 5 \
  --transmission auto \
  --platform dongchedi \
  --output json
```

**参数说明**：
- `--city`：城市建议使用全称中文，如`上海`。默认`全国`。
- `--brand`：品牌必须使用中文，如`丰田`。
- `--min-price` / `--max-price`：单位为**万元**。
- `--max-mileage`：单位为**万公里**。
- `--output`：支持 `table`、`json`、`yaml`。建议程序调用时始终使用 `--output json`。

### 2. 查看车辆详情 (detail)

获取单辆车的更多明细（排量、首牌日期、过户次数、图片等）。需要从 `search` 的结果中获取 ID。

```bash
# ID 格式为 "平台:车辆ID"
uv run car detail dongchedi:22805067 --output json
```

### 3. 多车对比 (compare)

支持跨平台将多辆车的参数并排对比（如排量、环保标准、保值情况）。

```bash
uv run car compare dongchedi:22805067 che168:478339_57621125 --output json
```

### 4. 查品牌车系字典 (series)

因为必须输入标准车系名才能准确过滤，提供 `series` 命令用于查询指定平台某品牌下的正规车系名称。

```bash
uv run car series 宝马 --platform dongchedi
```

### 5. 车贷计算 (loan)

基于预设价格、首付比例和利率计算月供。

```bash
# 价格 15 万，首付 3 成，分期 3 年计算月供（默认等额本息：equal_principal_interest）
uv run car loan --total 15 --down-payment 0.3 --years 3

# 修改为等额本金（equal_principal）
uv run car loan --total 15 --method equal_principal
```

### 6. 导出历史搜索结果 (export)

每次执行 `search` 后结果会暂存在 `~/.config/car-cli/last_search.json`。可用此命令一键导出到 CSV。

```bash
uv run car export --format csv -o out.csv
```

---

## 开发者与调试

调试请求或解析流程时，可以在主命令前加 `--debug`：

```bash
uv run car --debug search --brand 理想 --max-price 20
```

更详细的网络请求日志可以使用 `--trace-http`。

关于具体的底层抓取、特殊平台反爬与限流处理，以及具体的数据字典对照，请参阅外层目录的 `references/adapters.md`。
