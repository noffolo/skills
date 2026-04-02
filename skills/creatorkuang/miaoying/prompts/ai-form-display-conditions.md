# 表单项显示条件（showConditions）详细说明

本文档详细说明表单项之间的关联显示逻辑。当用户需要设置"选择某个选项后显示特定题目"时使用。

## 一、核心字段结构

### showConditions 显示条件数组

每个条件对象包含以下字段：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `optionId` | string | ✅ | 前置选择题的 `id`（只能引用当前题目之前的单选/多选题） |
| `optionIdxs` | string | ✅ | 触发显示的选项索引，**逗号分隔**，如 `"0,2,3"`（索引从 0 开始） |
| `optionLogic` | number | ❌ | 多选题的选项逻辑（单选题此字段无效，默认为 1） |

### showConditionsLogic 多条件组合逻辑

当关联了多个前置题目时（showConditions.length > 1），需要设置条件间的组合方式：

| 值 | 说明 |
|----|------|
| `0` | **"且"关系** - 需要满足所有关联条件才显示 |
| `1` | **"或"关系** - 只要满足一个关联条件就显示 |

---

## 二、optionLogic 选项逻辑（仅多选题有效）

| 值 | 说明 | 触发条件 |
|----|------|----------|
| `0` | 当**未选中**其中任意一个选项时，出现当前题目 | 反向触发 |
| `1` | 当**选中**其中任意一个选项时，出现当前题目（默认） | 常规关联 |
| `2` | 当**未选中**全部选项时，出现当前题目 | 全部反向触发 |
| `3` | 当**选中**全部选项时，出现当前题目 | 全部正向触发 |

### 逻辑说明

- **optionLogic = 0**（未选任意）：只要用户**没有选择** `optionIdxs` 中的任何一个选项，就显示
- **optionLogic = 1**（选中任意）：只要用户**选择了** `optionIdxs` 中的任意一个选项，就显示（最常用）
- **optionLogic = 2**（未选全部）：用户**没有选择** `optionIdxs` 中的全部选项时，才显示
- **optionLogic = 3**（选中全部）：用户**选择了** `optionIdxs` 中的全部选项时，才显示

---

## 三、使用规则

1. **只能引用前面的题目**：`optionId` 指向的题目必须在当前题目之前
2. **只支持选择题**：只能关联单选（type=1）或多选（type=2）题目
3. **矩阵题特殊处理**：矩阵单选（type=17）和矩阵多选（type=18）的每个行标题视为独立题目
4. **必须使用 id 字段**：被引用的表单项必须有 `id` 字段
5. **索引从0开始**：`optionIdxs` 中的选项索引从 0 开始计数
6. **单选题的 optionLogic**：对于单选题，`optionLogic` 值固定为 1（可以省略不写）

---

## 四、示例场景

### 场景1：单选题关联显示
> 需求：第1题选择"一年级"时，才显示第2题"一年级选课"

```javascript
{
  "infoForms": [
    {
      "id": "q1",
      "type": "1",
      "title": "孩子所在年级",
      "options": ["一年级", "二年级", "三年级"],
      "required": true
    },
    {
      "id": "q2",
      "type": "1",
      "title": "一年级选课",
      "options": ["绘画基础", "手工制作"],
      "required": true,
      "showConditions": [
        {
          "optionId": "q1",
          "optionIdxs": "0"  // 选择"一年级"（索引0）时显示
        }
      ]
    }
  ]
}
```

### 场景2：多选题关联显示（任意一个）
> 需求：第1题多选，只要选了"篮球"或"足球"，就显示第2题

```javascript
{
  "infoForms": [
    {
      "id": "q1",
      "type": "2",
      "title": "您喜欢的运动",
      "options": ["篮球", "足球", "羽毛球", "游泳"],
      "required": true
    },
    {
      "id": "q2",
      "type": "0",
      "title": "球类运动经验年限",
      "required": false,
      "showConditions": [
        {
          "optionId": "q1",
          "optionIdxs": "0,1",  // 选了篮球(0)或足球(1)任意一个
          "optionLogic": 1      // 当选中其中任意一个时显示
        }
      ]
    }
  ]
}
```

### 场景3：多选题关联显示（全部选中）
> 需求：第1题多选，只有同时选了"篮球"和"足球"，才显示第2题

```javascript
{
  "infoForms": [
    {
      "id": "q1",
      "type": "2",
      "title": "您会哪些运动",
      "options": ["篮球", "足球", "羽毛球"],
      "required": true
    },
    {
      "id": "q2",
      "type": "0",
      "title": "篮球和足球的对比感受",
      "required": false,
      "showConditions": [
        {
          "optionId": "q1",
          "optionIdxs": "0,1",  // 篮球(0)和足球(1)
          "optionLogic": 3      // 当选中其中全部时显示
        }
      ]
    }
  ]
}
```

### 场景4：多条件"且"关系
> 需求：第1题选择"是"，且第2题选择"同意"，才显示第3题

```javascript
{
  "infoForms": [
    {
      "id": "q1",
      "type": "1",
      "title": "是否为本校学生",
      "options": ["是", "否"],
      "required": true
    },
    {
      "id": "q2",
      "type": "1",
      "title": "是否同意活动条款",
      "options": ["同意", "不同意"],
      "required": true
    },
    {
      "id": "q3",
      "type": "0",
      "title": "请填写报名理由",
      "required": false,
      "showConditions": [
        {
          "optionId": "q1",
          "optionIdxs": "0"  // 选择"是"
        },
        {
          "optionId": "q2",
          "optionIdxs": "0"  // 选择"同意"
        }
      ],
      "showConditionsLogic": 0  // "且"关系，两个条件都满足才显示
    }
  ]
}
```

### 场景5：多条件"或"关系
> 需求：第1题选择"一年级"或"二年级"，都显示第2题

```javascript
{
  "infoForms": [
    {
      "id": "q1",
      "type": "1",
      "title": "孩子所在年级",
      "options": ["一年级", "二年级", "三年级"],
      "required": true
    },
    {
      "id": "q2",
      "type": "0",
      "title": "小学低年级作业反馈",
      "required": false,
      "showConditions": [
        {
          "optionId": "q1",
          "optionIdxs": "0"  // 一年级
        },
        {
          "optionId": "q1",
          "optionIdxs": "1"  // 二年级
        }
      ],
      "showConditionsLogic": 1  // "或"关系，满足任一条件即显示
    }
  ]
}
```

### 场景6：复杂多级联动（年级→课程→班级）
> 需求：选择年级后显示对应课程，选择课程后显示对应班级

```javascript
{
  "infoForms": [
    {
      "id": "grade",
      "type": "1",
      "title": "选择年级",
      "options": ["一年级", "二年级", "三年级"],
      "required": true
    },
    {
      "id": "course_g1",
      "type": "1",
      "title": "一年级课程选择",
      "options": ["语文", "数学", "英语"],
      "required": false,
      "showConditions": [
        { "optionId": "grade", "optionIdxs": "0" }
      ]
    },
    {
      "id": "course_g2",
      "type": "1",
      "title": "二年级课程选择",
      "options": ["科学", "美术", "音乐"],
      "required": false,
      "showConditions": [
        { "optionId": "grade", "optionIdxs": "1" }
      ]
    },
    {
      "id": "class_g1_chinese",
      "type": "1",
      "title": "一年级语文班级",
      "options": ["1班", "2班", "3班"],
      "required": false,
      "showConditions": [
        { "optionId": "course_g1", "optionIdxs": "0" }
      ]
    }
  ]
}
```

### 场景7：反向触发（未选中时显示）
> 需求：第1题多选，只要**没有选**"都不喜欢"，就显示第2题

```javascript
{
  "infoForms": [
    {
      "id": "q1",
      "type": "2",
      "title": "您喜欢哪些运动",
      "options": ["篮球", "足球", "羽毛球", "都不喜欢"],
      "required": true
    },
    {
      "id": "q2",
      "type": "0",
      "title": "请详细描述您的运动习惯",
      "required": false,
      "showConditions": [
        {
          "optionId": "q1",
          "optionIdxs": "3",      // "都不喜欢"的索引
          "optionLogic": 0        // 当未选中时显示
        }
      ]
    }
  ]
}
```

---

## 五、注意事项

1. **id 字段必填**：被关联的表单项和当前表单项都必须有唯一的 `id` 字段
2. **optionIdxs 是字符串**：多个索引用逗号分隔，如 `"0,1,2"`，不是数组
3. **单选题不需要 optionLogic**：单选题默认是选中即显示，可以省略 `optionLogic` 字段
4. **多选题必须理解 optionLogic**：多选题的 `optionLogic` 决定了选项与显示条件的关系
5. **showConditionsLogic 仅多条件时有效**：只有一个条件时，`showConditionsLogic` 无意义
