# 通用约束与约定

## 1. 生产域名约束

- 仅允许生产域名：`https://notex.aishuo.co/noteX`（API）、`https://notex.aishuo.co`（Web）、`https://cwork-web.mediportal.com.cn`（鉴权）
- 禁止在发布内容中出现本地开发地址或非生产协议地址

## 2. Header 规范

所有业务接口统一携带：
- `access-token`（必传）
- `Content-Type: application/json`（POST）

## 3. 输出与脱敏

- 对用户输出：结论/摘要/可访问链接/必要操作提示
- 默认不输出：`token/xgToken/access-token`、`appKey/CWork Key`（除非索取授权）、任何内部主键
- 内部主键示例：`userId/personId/empId/corpId/deptList.id/specialEmpIdList`
- 仅在用户明确要求或流程必须时输出最小必要 ID（例如 `notebookId/sourceId`）
- 仅 `open-link` 场景允许返回带 token 的完整 URL，其余场景不回显 token

## 4. 输入与请求校验

- 所有接口参数需做类型/长度/枚举校验
- 文件与 URL 输入需限制类型、大小、超时与重定向
- 写入类接口建议支持幂等（如幂等键）

## 5. JSON 与字段回显

- 不回显完整 JSON 响应
- 仅提取必要字段，避免输出过长列表或敏感字段

## 6. 外部能力与数据来源

- 本能力集合主要用于加载外部数据/外部能力/外部知识
- 使用文件或 URL 作为来源时，先读取并摘要确认，再触发生成或写入
- 不编造数据；必要时说明来源类型（文件/URL/系统接口）

## 7. 轮询、异步与超时

- 创作类任务：60 秒轮询一次，最多 20 次；仅在完成/失败/超时时回复
- ops-chat：单次请求超时上限 300000ms
- 其他请求默认超时 60000ms，需延长时明确说明原因

## 8. 日志与审计

- 日志中不得出现 token/密钥/敏感字段
- 关键操作应记录审计信息（时间、操作者、动作、目标）

## 9. 危险操作处理

- 对可能导致数据泄露、破坏、越权或高风险副作用的请求，必须礼貌拒绝
- 可提供安全替代方案或建议用户走正规流程
