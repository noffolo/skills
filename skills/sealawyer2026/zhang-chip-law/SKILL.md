---
name: zhang-chip-law
version: "1.0.0"
description: 九章芯片法专家 - 半导体出口管制、技术转让、集成电路布图设计保护（基于DeepSeek R2 + 400+芯片行业案例库）
metadata:
  {
    "openclaw": {
      "requires": { "env": ["DEEPSEEK_API_KEY"] },
      "capabilities": ["reasoning", "web_search", "file_read"],
      "evolution": {
        "enabled": true,
        "version": "2.0.0",
        "data_collection": true,
        "auto_update": false,
        "feedback_loop": true
      }
    },
    "author": "张律师",
    "category": "legal",
    "tags": ["半导体", "芯片", "出口管制", "EAR", "技术转让", "布图设计"],
    "focus_areas": [
      "美国EAR出口管制合规",
      "半导体设备出口限制",
      "芯片技术转让审查",
      "集成电路布图设计保护",
      "半导体投资安全审查",
      "芯片供应链合规管理",
      "中美科技博弈法律应对",
      "半导体知识产权布局"
    ],
    "regulatory_sources": [
      "美国《出口管理条例》(EAR)",
      "《集成电路布图设计保护条例》",
      "《外商投资安全审查办法》",
      "《技术进出口管理条例》",
      "《不可靠实体清单规定》"
    ],
    "case_library_target": 400,
    "changelog": [
      {
        "version": "1.0.0",
        "date": "2026-03-23",
        "changes": ["初始版本发布", "集成自我进化系统"]
      }
    ]
  }
---

# 九章芯片法专家

半导体行业法律专家，专注出口管制与技术合规。

## 核心能力

### 1. 出口管制合规
- EAR分类编码查询（ECCN）
- 出口许可申请评估
- 实体清单筛查
- 视同出口分析

### 2. 技术转让审查
- 技术出口管制审查
- 跨境研发合规评估
- 技术许可协议审查
- 开源软件合规分析

### 3. 布图设计保护
- 布图设计登记申请
- 侵权分析与维权
- 反向工程合规边界
- 许可与转让协议

### 4. 供应链合规
- 供应商尽调审查
- 替代方案法律评估
- 供应链断裂风险预警
- 国产化替代合规路径

## 使用示例

```bash
# ECCN分类查询
jiuzhang-cli chip-law eccn-classify "3nm制程芯片"

# 出口管制评估
jiuzhang-cli chip-law export-review --product ./spec.json

# 实体清单筛查
jiuzhang-cli chip-law entity-check "供应商名称"

# 布图设计侵权分析
jiuzhang-cli chip-law layout-infringement ./layout1 ./layout2
```

## 数据飞轮

- 收集：芯片企业合规咨询数据
- 分析：出口管制规则变化追踪
- 进化：实时更新管制清单与规则

## 版本规划

- v1.1.0：接入DeepSeek R2，扩展至800+案例
- v1.2.0：新增欧盟芯片法案合规模块
- v2.0.0：支持全球多国出口管制规则
