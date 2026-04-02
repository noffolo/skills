# 秒应 - 表单配置参考

本文档列出创建秒应活动时可用的所有配置项。根据用户描述的需求，选择对应的配置字段。

## 一、必填字段

所有表单都必须包含：

```javascript
{
  "title": "表单标题（必填，最多20字符）",
  "content": "表单描述（选填，最多2000字符）",
  "infoForms": [ /* 表单字段数组 */ ]
}
```

## 二、基础内容模块

### 封面与媒体
| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `cover` | string | 封面图URL | `xxxurl.jpg` |
| `pictures` | array | 图片数组（最多15张）,不需要uploads/的前缀 | `["url1", "xxxurl.jpg"]` |
| `bigPictures` | array | 大图数组（全屏展示） | - |
| `videoArr` | array | 视频数组 | - |
| `files` | array | 附件数组 | - |
| `sharePoster` | string | 分享海报图 | - |

### 引导链接
| 字段 | 类型 | 说明 |
|------|------|------|
| `intros` | array | 引导链接数组 |

### 位置信息
| 字段 | 类型 | 说明 |
|------|------|------|
| `locationInfos` | array | 地图位置信息数组 |

### 作者信息
| 字段 | 类型 | 说明 |
|------|------|------|
| `hideAuthorInfo` | boolean | 隐藏发布人信息 |
| `authorName` | string | 发布人名称 |
| `wxLogo` | string | 发布人头像 |

---

## 三、名单打卡模块

### 打卡模式
| 字段 | 类型 | 说明 | 触发关键词 |
|------|------|------|------------|
| `fixedNo` | boolean | 是否固定序号 | 名单、学号、工号 |
| `showNameList` | boolean | 是否导入名单 | 需要名单、名单导入 |
| `nameList` | array | 名单数组 | 提供名单内容 |

```javascript
// 名单列表结构
"nameList": [
  { "no": "001", "name": "张三", "groupName": "一班" },
  { "no": "002", "name": "李四", "groupName": "一班" }
]
```

### 名单字段自定义
| 字段 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `noName` | string | 序号标签名称 | `"学号"` |
| `nameLabel` | string | 姓名标签名称 | `"姓名"` |
| `groupLabelName` | string | 分组标签名称 | `"班级"` |

### 名单隐私
| 字段 | 类型 | 说明 | 触发关键词 |
|------|------|------|------------|
| `hideNameListNo` | boolean | 隐藏名单序号 | 隐藏学号、隐藏序号 |
| `isHideNameList` | boolean | 隐藏整个名单 | 隐私名单、保密名单 |
| `needNameListQRCode` | boolean | 生成名单专属二维码 | 专属码、个人码 |

### 人数限制
| 字段 | 类型 | 说明 |
|------|------|------|
| `count` | number | 打卡数量限制 |
| `totalAllow` | number | 总结果条数限制，0为不限 |
| `removeNos` | array | 需要剔除的序号数组 |

---

## 四、时间控制模块

### 填报时间
| 字段 | 类型 | 说明 | 触发关键词 |
|------|------|------|------------|
| `needTimeLimit` | boolean | 是否需要时间限制 | 开始时间、结束时间、截止时间 |
| `startTime` | number | 开始时间（时间戳，毫秒） | - |
| `endTime` | number | 结束时间（时间戳，毫秒） | - |

### 连续打卡
| 字段 | 类型 | 说明 | 触发关键词 |
|------|------|------|------------|
| `isRepeat` | boolean | 是否连续打卡 | 每天、每周、重复、连续 |
| `repeatDaysType` | number | 打卡频率 | - |
| `repeatDays` | array | 重复日期数组（0-6，0=周日） | - |
| `repeatDates` | array | 自定义日期数组（YYYY-MM-DD） | - |
| `repeatStartDate` | number | 打卡开始日期（时间戳） | - |
| `repeatEndDate` | number | 打卡结束日期（时间戳） | - |
| `dayRepeatCount` | number | 每天打卡次数，默认1 | 每天几次 |
| `allowSubmitTimeRules` | array | 允许提交时间段规则 | 特定时间段 |

```javascript
// 重复日期类型
// repeatDaysType: 0-每天，1-单号，2-双号，3-自定义，4-每周

// repeatDays 数组示例
"repeatDays": [0, 1, 2, 3, 4, 5, 6]  // 每天
"repeatDays": [1, 2, 3, 4, 5]         // 工作日

// 时间段规则
"allowSubmitTimeRules": [
  { "_id": 1, "startTime": "07:00", "endTime": "09:00" },
  { "_id": 2, "startTime": "12:00", "endTime": "14:00" }
]
```

---

## 五、位置限制模块

### 地点限制
| 字段 | 类型 | 说明 | 触发关键词 |
|------|------|------|------------|
| `needLocation` | boolean | 是否限制地点范围打卡 | 指定地点、范围内打卡 |
| `locations` | array | 地点数组 | - |
| `locationInfos` | array | 地图位置信息数组 | - |

```javascript
// locations 结构
"locations": [
  {
    "latitude": 39.9,      // 纬度
    "longitude": 116.4,   // 经度
    "name": "会议室",      // 地点名称
    "distance": 100      // 允许范围（米）
  }
]
```

### 打卡位置收集
| 字段 | 类型 | 说明 | 触发关键词 |
|------|------|------|------------|
| `needSubmitLocation` | boolean | 是否收集打卡实时位置 | 需要位置、定位 |
| `openLocationInfo` | boolean | 是否公开位置信息 | - |

### WiFi 限制
| 字段 | 类型 | 说明 | 触发关键词 |
|------|------|------|------------|
| `needWifi` | boolean | 是否必须连接指定WiFi签到 | WiFi、连接WiFi |
| `wifiInfos` | array | WiFi数组 | - |

```javascript
// wifiInfos 结构
"wifiInfos": [
  { "ssid": "会议室WiFi", "bssid": "xx:xx:xx:xx:xx:xx" }
]
```

---

## 六、权限设置模块

### 填写次数限制
| 字段 | 类型 | 说明 | 触发关键词 |
|------|------|------|------------|
| `limitCount` | boolean | 是否限制可提交微信号个数 | 限制次数 |
| `allowBaomingCount` | number | 每个微信号允许报名次数，默认1，0为不限 | 限制每人几次 |
| `userAllowBaomingCount` | number | 有名单时每个微信号可打卡总数 | - |

### 修改权限
| 字段 | 类型 | 说明 | 触发关键词 |
|------|------|------|------------|
| `allowManagerChangeResult` | boolean | 允许管理员修改已提交信息 | 管理员修改 |
| `canUpdateDuration` | number | 打卡后多少分钟内可修改或删除 | 可以修改、提交后可改 |
| `banUpdate` | boolean | 禁止更新报名 | 不能修改、禁止修改 |

### 代填权限
| 字段 | 类型 | 说明 | 触发关键词 |
|------|------|------|------------|
| `fillInLicensee` | number | 代替填写权限：0-不允许，1-创建人，2-创建人和管理员 | 代填、帮填 |

### 结果可见性
| 字段 | 类型 | 说明 | 触发关键词 |
|------|------|------|------------|
| `publishResult` | boolean | 允许打卡结果所有人可见 | 公开结果、所有人可见 |
| `restrictGroupMember` | boolean | 禁止转发（更加私密） | 禁止转发、不能转发 |
| `isAnonymous` | boolean | 匿名填写 | 匿名、保密 |

---

## 七、通知配置模块

### 定时通知
| 字段 | 类型 | 说明 | 触发关键词 |
|------|------|------|------------|
| `needNotify` | boolean | 是否需要定时通知 | 定时通知、提醒打卡 |
| `notifyTime` | number | 定时通知的时间（时间戳，毫秒） | - |
| `notifyGroupId` | string | 通知群组ID | - |
| `notifyDays` | array | 通知包含周几（值为[0-6]） | 每周几通知 |
| `notifyDayTime` | string | 通知时间字符串，如'09:00' | 具体时间 |

### 实时通知
| 字段 | 类型 | 说明 | 触发关键词 |
|------|------|------|------------|
| `newBaomingNotify` | boolean | 有新填写时提醒通知 | 新提交提醒 |
| `closeBaomingProgressNotify` | boolean | 项目完成情况提醒 | 完成进度提醒 |

---

## 八、高级功能模块

| 字段 | 类型 | 说明 | 触发关键词 |
|------|------|------|------------|
| `needSignature` | boolean | 需要手写签名确认 | 签名、签字确认 |
| `isOpenRanking` | boolean | 是否开启打卡排行榜 | 排行榜、排名 |
| `needCorrectsMode` | boolean | 开启反馈内容的点评&点赞&批改 | 点评、批改 |
| `baomingCommentPermission` | number | 反馈内容权限：0-仅发起人，1-允许互相点评 | - |
| `isPreFill` | boolean | 允许成员在接龙开始前预填内容 | 提前填、预填 |

---

## 九、UI 自定义模块

| 字段 | 类型 | 说明 |
|------|------|------|
| `infoFormsDisplayPosition` | string | 表单填写页位置：'在底部按钮后'或'在第一页显示' |
| `dakaBtnText` | string | 参与接龙按钮文字，默认'立即打卡' |
| `multiSubmitBtnText` | string | 再次打卡按钮文字 |
| `submitSuccessText` | string | 提交成功提示文字，默认'您已提交成功' |

---

## 十、表单字段类型（infoForms）

| type 值 | 名称 | 说明 |
|---------|------|------|
| `0` | 单行文本填空题 | 简短文本输入 |
| `1` | 单选 | 非性别及民族等特殊字段 |
| `2` | 多选 | 若选项只有两个且互斥需使用单选 |
| `3` | 文件（只图片除外）收集 | - |
| `4` | 图片收集 | 图片类的信息收集 |
| `5` | 录音收集 | 跟读作业等 |
| `6` | 视频收集 | - |
| `7` | 多行文本填空题 | 内容较多时 |
| `8` | 日期选择题 | 时间选择 |
| `9` | 数字填空题 | 非身份证/手机号 |
| `10` | 省市区三级联动选择 | 地址/籍贯 |
| `11` | 手机号码 | - |
| `12` | 身份证 | 身份证相关字段 |
| `13` | 出生日期 | - |
| `14` | 知情确认 | 法律效力、责任归属等 |
| `15` | 拼图 | 上传多张图拼在一起 |
| `16` | 评分 | 星级评分 |
| `17` | 矩阵单选 | 评估多个主题的统一维度 |
| `18` | 矩阵多选 | 类似矩阵单选，列量表可选多个 |
| `19` | 自增表格 | 可动态增减条目的表格题 |
| `20` | 多项填空 | 一题多空，常用于考试 |
| `21` | 手写签名 | 法律效力、责任归属等 |
| `22` | 地图地点选择 | 收集用户自己的地点 |
| `23` | 扫码录入 | 商品入库、设备巡检 |
| `31` | 性别 | - |
| `32` | 民族 | - |
| `33` | 政治面貌 | - |
| `34` | 学历 | - |
| `35` | 水印拍照 | 上传照片自带定位信息 |

---

## 十一、表单项关联设置（显示条件）

> 📖 **详细文档**：当用户需要设置"选择某个选项后显示对应题目"等联动逻辑时，请先阅读 `ai-form-display-conditions.md` 了解完整配置和示例。

---

## 十二、表单项跳题设置

通过跳题设置，可以让用户在做完当前题目后，直接跳过中间题目到达指定题目。

### 跳题字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `skipToFormId` | string | 跳转目标题目的 `id`，空表示不需要跳题 |

### 跳题示例

```javascript
{
  "infoForms": [
    {
      "id": "q1",
      "type": "1",
      "title": "您是否已参加工作",
      "options": ["是", "否"],
      "required": true,
      "skipToFormId": "q3"  // 做完此题直接跳到 q3，跳过 q2
    },
    {
      "id": "q2",
      "type": "0",
      "title": "学生相关信息（被跳过）",
      "required": false
    },
    {
      "id": "q3",
      "type": "0",
      "title": "继续填写",
      "required": true
    }
  ]
}
```

### 跳题设置规则

1. **只能向后跳**：跳转目标必须在当前题目之后
2. **跳转目标是 id**：`skipToFormId` 的值是目标题目的 `id` 字段
3. **留空不跳**：如果不设置或为空字符串，则正常进入下一题

---

## 十三、场景示例

### 场景1：每日健康打卡
> 用户描述："创建一个每日健康打卡，需要上传照片和位置，每天早上8点提醒"

```javascript
{
  "title": "每日健康打卡",
  "content": "请每日完成健康打卡，上传照片并记录位置信息",
  "isRepeat": true,
  "repeatDaysType": 0,
  "infoForms": [
    { "type": 4, "title": "上传照片", "required": true },
    { "type": 22, "title": "定位地点", "required": true }
  ],
  "needSubmitLocation": true,
  "needNotify": true,
  "notifyDayTime": "08:00"
}
```

### 场景2：班级活动报名
> 用户描述："班级活动报名，限制20人，需要填写姓名和联系方式，截止到本周五"

```javascript
{
  "title": "班级活动报名",
  "content": "请填写信息完成活动报名",
  "count": 20,
  "totalAllow": 20,
  "needTimeLimit": true,
  "endTime": 1760000000000,
  "infoForms": [
    { "type": 0, "title": "姓名", "required": true },
    { "type": 11, "title": "手机号码", "required": true }
  ]
}
```

### 场景3：会议签到
> 用户描述："会议签到，需要连接指定WiFi，限制地点范围100米"

```javascript
{
  "title": "会议签到",
  "content": "请在会场范围内完成签到",
  "needWifi": true,
  "wifiInfos": [{"ssid": "会议室WiFi", "bssid": "xx:xx:xx:xx:xx:xx"}],
  "needLocation": true,
  "locations": [{"latitude": 39.9, "longitude": 116.4, "name": "会议室", "distance": 100}],
  "needSubmitLocation": true
}
```

### 场景4：作业提交
> 用户描述："语文作业提交，需要上传录音（必填）和图片，开启批改点评"

```javascript
{
  "title": "语文作业提交",
  "content": "请完成语文作业并提交",
  "infoForms": [
    { "type": 5, "title": "上传录音", "required": true },
    { "type": 4, "title": "上传图片", "required": false }
  ],
  "needCorrectsMode": true,
  "baomingCommentPermission": 1
}
```

### 场景5：问卷调查
> 用户描述："客户满意度调查，匿名填写，包含矩阵评分题"

```javascript
{
  "title": "客户满意度调查",
  "content": "请根据您的真实体验填写",
  "isAnonymous": true,
  "publishResult": false,
  "infoForms": [
    {
      "type": 17,
      "title": "服务满意度评分",
      "required": true,
      "infoOptions": [{"title": "非常满意"}, {"title": "满意"}, {"title": "一般"}, {"title": "不满意"}],
      "questionOptions": [{"title": "服务态度"}, {"title": "专业水平"}, {"title": "响应速度"}]
    }
  ]
}
```

### 场景6：固定名单打卡
> 用户描述："班级打卡，需要按学号顺序，隐藏其他同学信息"

```javascript
{
  "title": "班级每日打卡",
  "content": "请按学号顺序完成每日打卡",
  "fixedNo": true,
  "showNameList": true,
  "noName": "学号",
  "nameLabel": "姓名",
  "hideNameListNo": true,
  "isHideNameList": false,
  "isRepeat": true,
  "repeatDaysType": 0,
  "infoForms": [
    { "type": 0, "title": "今日感悟", "required": false }
  ]
}
```

### 场景7：位置限制打卡
> 用户描述："要求在公司100米范围内打卡"

```javascript
{
  "title": "公司签到",
  "content": "请在公司范围内完成签到",
  "needLocation": true,
  "locations": [
    { "latitude": 39.9042, "longitude": 116.4074, "name": "公司总部", "distance": 100 }
  ],
  "needSubmitLocation": true,
  "openLocationInfo": true
}
```

---

## 十四、注意事项

1. **只输出用户明确提到的字段**，不要添加未提到的配置
2. **时间戳使用毫秒级**（JavaScript Date.now() 格式）
3. **数组格式**：locations, wifiInfos 等必须输出为 JSON 数组
4. **布尔值**：true/false 不要用引号包裹
5. **必填字段**：title, content, infoForms 必须有
6. **信息类型处理**：当用户提到"需要上传照片/录音/视频/文件/签名"等功能时，应将其转为对应的 infoForms 表单项类型：
   - 照片/图片 → type=4
   - 录音 → type=5
   - 视频 → type=6
   - 文件 → type=3
   - 手写签名 → type=21
7. **单选/多选字段选项格式**（⚠️ 非常重要）：
   - 当 `type` 为 `"1"`（单选）或 `"2"`（多选）时，**必须使用 `options` 字段**
   - **`options` 必须是字符串数组（arrayOfString），不是对象数组！**
   - ✅ 正确格式：`{"type": "1", "title": "选择题", "options": ["选项 A", "选项 B", "选项 C"]}`
   - ❌ 错误格式 1：`{"type": "1", "title": "选择题", "options": [{"title": "选项 A"}, {"title": "选项 B"}]}`（对象数组，选项会丢失）
   - ❌ 错误格式 2：`{"type": "1", "title": "选择题", "infoOptions": [...]}`（字段名错误，会报错"选项不能少于 2 个"）
   - 其他类型（如矩阵题 type=17/18）使用 `infoOptions` 或 `questionOptions` 字段
8. **显示条件设置**（⚠️ 重要）：
   - 需要设置表单项关联时，必须给相关表单项添加 `id` 字段
   - `showConditions` 只能引用当前题目**之前**的单选/多选题
   - `optionIdxs` 中的索引从 0 开始
   - 单选题的 `optionLogic` 固定为 1，可以省略
   - 多条件关联时，需要设置 `showConditionsLogic`（0=且关系，1=或关系）
9. **跳题设置**：
   - `skipToFormId` 只能跳转到当前题目**之后**的题目
   - 按选项跳题（`needOptionSkip`）仅对单选题有效
