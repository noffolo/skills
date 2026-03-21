# Feishu Doc Template

Use this scaffold when writing the final Feishu cloud doc. Adapt the numbering to the real module count. Keep the headings stable and hierarchical.

## Document top section

```markdown
# 20260320-需求简称-测试用例

需求来源：
- 飞书需求文档：<粘贴在线链接>
- 补充材料：<如有则列出>

文档说明：
- 输出类型：测试用例设计稿
- 状态：待执行
- 生成原则：基于需求原文与标准 QA 覆盖维度生成，未执行部分不填写实际结果
```

## Module scaffold

```markdown
## 1. 模块名称

测试人：<仅在已知时填写>
路径：<菜单路径或入口路径>

### 1.1 列表页

#### 1.1.1 展示字段
- 编号：系统自动生成，只读
- 状态：默认展示最近状态，支持按状态筛选

#### 1.1.2 查询与筛选
- 关键字搜索：支持按编号模糊搜索
- 默认排序：按创建时间倒序

#### 1.1.3 按钮与操作
- 新建：有权限用户可见
- 导出：仅审核态允许导出

### 1.2 详情页

#### 1.2.1 表头

##### 1.2.1.1 组织
- 必填，可编辑
- 默认值：当前登录组织
- 权限：仅允许选择有权限的组织层级
- 边界/异常：
  - 无权限组织不可选
  - 切换组织后联动刷新下游数据

测试步骤：
1. 新建单据，观察“组织”默认值
2. 展开组织选择器，尝试选择有权限组织
3. 尝试选择无权限组织

预期结果：
1. 默认带出当前登录组织
2. 有权限组织可正常选择
3. 无权限组织不可见或不可选

测试结果：待执行
验证数据：待补充
相应SQL：待补充

##### 1.2.1.2 调整方式
- 必填，下拉选项：按加价前调整总金额、按价格明细
- 联动规则：
  - 选择“按加价前调整总金额”时，价格明细中的“调整单价”不可编辑
  - 选择“按价格明细”时，表头“加价前调整总金额”清 0 并隐藏

### 1.3 流程校验

#### 1.3.1 提交/确认
- 提交后状态变为“待审核”
- 审核前不允许再次编辑关键字段

### 1.4 逻辑校验

#### 1.4.1 保存时重复校验
> 根据“调整月份”“交货工厂”和明细中的“种猪场”判断是否重复创建。

测试步骤：
1. 使用已存在组合再次创建单据
2. 点击“保存”

预期结果：
1. 系统阻止保存
2. 页面提示具体重复对象

测试结果：待执行
验证数据：待补充
相应SQL：待补充
```

## Requirement confirmation section

Append this section only when needed:

```markdown
## 需求确认项

| 序号 | 疑问点 | 待确认内容 | 影响范围 |
| --- | --- | --- | --- |
| 1 | 调整方式切换后的历史数据处理 | 切换前已录入的明细是否全部清空重算 | 详情页联动与保存逻辑 |
```

## Writing rules

- Prefer headings plus short bullets over large paragraphs.
- Keep each leaf node executable.
- Write explicit field names, button names, and states.
- If the requirement has no formula, do not invent one.
- If the requirement has no actual screenshots, do not fabricate them.
