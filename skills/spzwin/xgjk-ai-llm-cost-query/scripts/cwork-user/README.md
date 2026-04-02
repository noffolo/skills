# 脚本清单 — cwork-user

## 共享依赖

无（标准库 + 环境变量 `appKey`）。

## 脚本列表

| 脚本 | 对应接口 | 用途 |
|---|---|---|
| `search-emp-by-name.py` | `GET /open-api/cwork-user/searchEmpByName` | 按姓名搜索员工，从返回中取 `personId` 供费用查询 |

## 使用方式

```bash
export XG_BIZ_API_KEY="your-app-key"
# 或 export XG_APP_KEY="your-app-key"

python3 scripts/cwork-user/search-emp-by-name.py --search-key "张三"
```

## 输出说明

所有脚本的输出均为 **JSON 格式**（`Result<T>`）。

## 规范

1. **必须使用 Python** 编写
2. **鉴权遵循** `cms-auth-skills/SKILL.md` 规范
3. **入参定义以** `openapi/cwork-user/` 文档为准
4. 出错时**间隔 1 秒、最多重试 3 次**（可重试错误）
