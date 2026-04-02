# 秒应 - 预约、考试、选课与统计创建指南

## 一、判断用户需求：预约 vs 考试 vs 选课 vs 统计

### 创建**预约**的场景：
- 用户需要"分时段预约"功能（如：上午场/下午场/晚场）
- 用户提到"预约"、"订号"、"限号"、"时间段"等关键词
- 用户需要控制每个时间段的人数（如：每时段限10人）
- 用户提到"开放预约时间"、"几点开始预约"等

### 创建**考试**的场景：
- 用户需要创建在线考试、测验、问卷考试
- 用户提到"考试"、"测验"、"在线考试"、"考试时长"等关键词
- 需要设置考试时长、自动阅卷、成绩排名功能

### 创建**选课/抢课**的场景：
- 用户需要创建课程选择、抢课活动
- 学校选课、培训机构课程报名、兴趣班抢课
- 需要展示课程列表、配额限制、时间安排等
- 用户提到"选课"、"抢课"、"课程选择"、"课程报名"等关键词

### 创建**统计**的场景：
- 用户需要收集信息、报名、打卡、问卷
- 用户提到"统计"、"报名"、"问卷"、"收集信息"等关键词
- 用户不需要分时段，只需总人数限制或不限制人数

---

## 二、预约必填字段清单

创建预约时，**必须包含**以下字段：

### 核心标识（必须）
```javascript
{
  "needBookMode": true,  // 必须：标识这是预约模式
  "title": "预约标题",    // 必须：活动标题
}
```

### 预约时段配置（二选一）

#### 选项1：使用 `preset` 快捷配置（推荐）
```javascript
{
  "preset": 1  // 1=全天开放, 2=上午下午, 3=三时段
}
```
- `preset: 1` → 全天 07:00-23:59
- `preset: 2` → 上午 07:00-09:00，下午 12:00-14:00
- `preset: 3` → 上午 07:00-09:00，下午 12:00-14:00，晚上 18:00-20:00

#### 选项2：自定义时段
```javascript
{
  "dayRepeatCount": 3,  // 每天时段数：1/2/3
  "allowSubmitTimeRules": [
    {
      "_id": 1,
      "startTime": "07:00",  // HH:mm 格式
      "endTime": "09:00",    // HH:mm 格式
      "notifyTime": "07:00"  // HH:mm 格式
    },
    {
      "_id": 2,
      "startTime": "12:00",
      "endTime": "14:00",
      "notifyTime": "12:00"
    },
    {
      "_id": 3,
      "startTime": "18:00",
      "endTime": "20:00",
      "notifyTime": "18:00"
    }
  ]
}
```

### 重复规则（推荐）
```javascript
{
  "repeatDays": [0, 1, 2, 3, 4, 5, 6],  // 0=周日, 1=周一, ..., 6=周六
  "repeatStartDate": 1774022400000,        // 开始日期时间戳
  "repeatEndDate": 1774627200000           // 结束日期时间戳
}
```

### 固定名单模式（可选）
```javascript
{
  "fixedNo": true,        // 使用固定名单
  "noName": "序号",       // 序号名称："序号"/"学号"/"工号"等
  "nameList": [           // 名单列表
    { "no": "1", "name": "张三", "groupName": "一班" },
    { "no": "2", "name": "李四", "groupName": "一班" }
  ]
}
```

### 其他常用配置
```javascript
{
  "allowBuka": true,      // 是否允许补卡
  "limitCount": false,    // 预约模式通常不限制总人数
  "count": 0,            // 0=不限制人数
  "content": "活动描述",  // 活动说明
  "notifyTime": 32400000  // 提前通知时间（毫秒）
}
```

---

## 三、考试必填字段清单

创建考试时，**必须包含**以下字段：

### 核心标识（必须）
```javascript
{
  "needExamMode": true,  // 必须：标识这是考试模式
  "title": "考试标题",   // 必须：考试标题
  "examDuration": 60,    // 考试时长（分钟），0 表示不限时
}
```

### 考试题目（examForms）
```javascript
{
  "examForms": [
    {
      "id": "q1",                    // 题目 ID
      "type": "1",                   // 题目类型：1=单选, 2=多选, 7=简答, 0=单项填空, 20=多项填空, 5=录音
      "title": "题目内容",            // 题目标题
      "options": ["选项A", "选项B"],  // 选项（选择题必需）
      "answer": "0",                 // 正确答案（索引或文本）
      "fullScore": 10,               // 题目分值
      "order": 1                     // 题目顺序
    }
  ]
}
```

### 其他常用配置
```javascript
{
  "fixedNo": true,          // 通常使用固定名单
  "noName": "学号",          // 固定名单标签名
  "nameLabel": "姓名",       // 姓名标签名
  "dakaBtnText": "开始答卷", // 按钮文本
  "isOpenRanking": true,     // 是否显示排名
  "banViewExamResult": false // 是否禁止提交后查看试卷详情
}
```

---

## 四、统计必填字段清单

创建统计时，通常需要：

```javascript
{
  "title": "统计标题",    // 必须
  "content": "统计说明",  // 可选
  "count": 100,          // 人数限制
  "limitCount": true,    // 是否限制人数
  "infoForms": [         // 表单字段
    {
      "title": "姓名",
      "type": "0",       // 0=单行文本
      "required": true
    }
  ]
}
```

---

## 六、对话引导话术

### 场景1：用户需求不明确
> "请告诉我您的具体需求：
> 1. 是否需要分时段预约（如：上午场/下午场）？
> 2. 是否需要创建在线考试？
> 3. 是否需要固定名单？"

### 场景2：用户提到"考试"
> "好的，我将为您创建一个考试。请告诉我：
> 1. 考试时长是多少分钟？
> 2. 需要哪些类型的题目（单选、多选、简答等）？
> 3. 是否需要固定名单（如：只允许特定学生参加）？"

### 场景3：用户提到"选课/抢课"
> "好的，我将为您创建一个选课活动。请告诉我：
> 1. 有哪些课程可选？请提供课程名称、配额、上课时间等信息
> 2. 每人可以选择几门课程？
> 3. 是否需要限制单课程的人数（配额）？"

### 场景4：用户提到"预约"
> "好的，我将为您创建一个预约活动。请选择：
> 1. 全天开放（早上7点到晚上11点）
> 2. 分上午和下午两个时段
> 3. 分三个时段（上午、下午、晚上）"

### 场景5：用户需要固定名单
> "您提到需要固定名单，请提供：
> 1. 序号名称（如：学号、工号、座位号）
> 2. 名单列表（包括序号和姓名）"

---

## 五、字段验证规则

### 预约时段验证
- `dayRepeatCount` 必须是 1、2 或 3
- `allowSubmitTimeRules` 数组长度必须等于 `dayRepeatCount`
- 时间格式必须是 "HH:mm"（24小时制）
- 每个时段必须有 `_id`、`startTime`、`endTime`

### 固定名单验证
- 如果 `fixedNo: true`，则必须提供 `nameList`
- `nameList` 中每个项目必须有 `no`（序号）

---

## 六、示例配置

### 示例1：简单全天预约
```javascript
{
  "title": "图书馆座位预约",
  "content": "每天开放图书馆座位预约",
  "needBookMode": true,
  "preset": 1,
  "count": 50,
  "repeatDays": [0, 1, 2, 3, 4, 5, 6],
  "limitCount": false
}
```

### 示例2：分时段预约（固定名单）
```javascript
{
  "title": "实验室机位预约",
  "content": "分上午下午时段，限特定学生",
  "needBookMode": true,
  "preset": 2,
  "count": 0,
  "fixedNo": true,
  "noName": "学号",
  "nameList": [
    { "no": "2021001", "name": "张三" },
    { "no": "2021002", "name": "李四" }
  ]
}
```

### 示例3：普通统计（非预约）
```javascript
{
  "title": "班级报名统计",
  "content": "统计班级学生报名情况",
  "count": 50,
  "limitCount": true,
  "infoForms": [
    { "title": "姓名", "type": "0", "required": true },
    { "title": "手机号", "type": "11", "required": true }
  ]
}
```

### 示例4：在线考试
```javascript
{
  "title": "数学期中考试",
  "content": "90分钟，共10道题",
  "needExamMode": true,
  "examDuration": 90,
  "fixedNo": true,
  "noName": "学号",
  "isOpenRanking": true,
  "examForms": [
    {
      "id": "q1",
      "type": "1",
      "title": "1 + 1 = ?",
      "options": ["1", "2", "3", "4"],
      "answer": "1",
      "fullScore": 10,
      "order": 1
    },
    {
      "id": "q2",
      "type": "7",
      "title": "请简述勾股定理",
      "fullScore": 20,
      "order": 2
    }
  ]
}
```

### 示例5：选课/抢课
```javascript
{
  "title": "选修课选课",
  "content": "请选择您的选修课程，每门课程人数有限",
  "isSelectCourse": true,  // 系统会自动设置
  "infoForms": [
    {
      "id": "course_1",
      "type": "24",  // 课程选择类型
      "title": "请选择课程",
      "required": true,
      "courseSetting": [
        {
          "id": "course_001",
          "title": "Python编程入门",
          "quota": 30,
          "schedule": [
            { "dayOfWeek": 1, "startTime": "14:00", "endTime": "16:00" },
            { "dayOfWeek": 3, "startTime": "14:00", "endTime": "16:00" }
          ],
          "description": "零基础Python编程课程",
          "teacher": "张老师",
          "location": "A101",
          "price": 0,
          "order": 1
        },
        {
          "id": "course_002",
          "title": "数据分析基础",
          "quota": 25,
          "schedule": [
            { "dayOfWeek": 2, "startTime": "10:00", "endTime": "12:00" }
          ],
          "description": "数据分析基础理论与实践",
          "teacher": "李老师",
          "location": "B203",
          "price": 0,
          "order": 2
        },
        {
          "id": "course_003",
          "title": "Web前端开发",
          "quota": 20,
          "schedule": [
            { "dayOfWeek": 4, "startTime": "18:30", "endTime": "20:30" }
          ],
          "description": "HTML/CSS/JavaScript基础",
          "teacher": "王老师",
          "location": "C305",
          "price": 0,
          "order": 3
        }
      ]
    }
  ]
}
```

---

## 六、选课必填字段清单

创建选课时，需要在 `infoForms` 中包含 **type=24** 的课程选择字段：

### 课程选择字段（type=24）
```javascript
{
  "type": "24",           // 必须：课程选择类型
  "title": "请选择课程",   // 课程选择标题
  "required": true,       // 是否必选
  "courseSetting": [      // 课程列表
    {
      "id": "course_xxx",          // 课程ID（唯一标识）
      "title": "课程名称",         // 课程标题
      "quota": 30,                 // 课程配额（最多选课人数）
      "schedule": [                // 上课时间安排
        {
          "dayOfWeek": 1,           // 星期几（1=周一, 2=周二, ..., 7=周日）
          "startTime": "14:00",     // 开始时间
          "endTime": "16:00"        // 结束时间
        }
      ],
      "description": "课程介绍",    // 课程描述
      "teacher": "授课人",         // 授课老师
      "location": "上课地点",       // 上课地点
      "price": 0,                 // 收费价格
      "order": 1                  // 排序
    }
  ]
}
```

### 其他配置
```javascript
{
  "isSelectCourse": true,   // 系统会自动设置（当包含 type=24 字段时）
  "count": 0,               // 选课通常不限制总人数（单课程有限制）
  "limitCount": false,      // 不限制总人数
  "multiSubmit": false,     // 每人只能提交一次
  "publishResult": false    // 不公开结果（保护学生选择）
}
```

---

## 七、对话引导话术
      "title": "请简述勾股定理",
      "fullScore": 20,
      "order": 2
    }
  ]
}
```
