# Agent Dev 团队周报 2026-03-14 ~ 2026-03-20

时间范围：`2026-03-14` 至 `2026-03-20`

## 参与成员

- [张辉](https://dev.msh.team/zhanghui) (`zhanghui`)
- [李华儒](https://dev.msh.team/lihuaru) (`lihuaru`)
- [许京爽](https://dev.msh.team/xujingshuang) (`xujingshuang`)
- [曹现峰](https://dev.msh.team/caoxianfeng) (`caoxianfeng`)
- [张惠施](https://dev.msh.team/zhanghuishi) (`zhanghuishi`)

## 一、产品功能

### KimiClaw 主营业务

#### 资源供应商与实例编排（8 个 MR）

- [!2013 feat(apps/kimiapi): claw 补充腾讯云供应商](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2013) ｜ 提交人：[张辉](https://dev.msh.team/zhanghui) ｜ 仓库：`engineering/kimi-darkmatter` ｜ 状态：**已合并**
- [!2052 feat(apps/kimiapi): claw 增加通过镜像 ID 创建 Bot](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2052) ｜ 提交人：[张辉](https://dev.msh.team/zhanghui) ｜ 仓库：`engineering/kimi-darkmatter` ｜ 状态：**已合并**
- [!544 feat(kimiapi/internal): add pattern for download data](https://dev.msh.team/engineering/secrets/kimi-secret-prod/-/merge_requests/544) ｜ 提交人：[许京爽](https://dev.msh.team/xujingshuang) ｜ 仓库：`engineering/secrets/kimi-secret-prod` ｜ 状态：**已合并**
- [!542 feat(apps/kimiapi): 更新适配企微版本 claw 镜像](https://dev.msh.team/engineering/secrets/kimi-secret-prod/-/merge_requests/542) ｜ 提交人：[张辉](https://dev.msh.team/zhanghui) ｜ 仓库：`engineering/secrets/kimi-secret-prod` ｜ 状态：**已合并**
- [!462 feat(apps/hooker): feishu proxy](https://dev.msh.team/engineering/devops/kimi-secret/-/merge_requests/462) ｜ 提交人：[李华儒](https://dev.msh.team/lihuaru) ｜ 仓库：`engineering/devops/kimi-secret` ｜ 状态：**已合并**
- 其余 3 个 MR（2 merged / 1 opened / 0 closed），主要涉及 kimi-secret-prod / kimi-secret。

#### 工作空间与数据生命周期（1 个 MR）

- [!2023 feat(apps/kimiapi): 实现Claw workspace备份与恢复功能，支持会员到期前自动备份至TOS](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2023) ｜ 提交人：[张辉](https://dev.msh.team/zhanghui) ｜ 仓库：`engineering/kimi-darkmatter` ｜ 状态：**已合并**

#### 稳定性、容灾与观测（7 个 MR）

- [!2062 feat(apps/kimiapi): 补充 claw bot 各操作运行指标](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2062) ｜ 提交人：[张辉](https://dev.msh.team/zhanghui) ｜ 仓库：`engineering/kimi-darkmatter` ｜ 状态：**已合并**
- [!2060 fix(apps/kimiapi): 修复 claw SSH 探活 偶现卡死的情况](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2060) ｜ 提交人：[张辉](https://dev.msh.team/zhanghui) ｜ 仓库：`engineering/kimi-darkmatter` ｜ 状态：**已合并**
- [!2063 feat(x/sshkit): new pkg](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2063) ｜ 提交人：[李华儒](https://dev.msh.team/lihuaru) ｜ 仓库：`engineering/kimi-darkmatter` ｜ 状态：**已合并**
- [!2059 fix(apps/kimiapi): 修复 SSH 链接偶现卡死的情况](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2059) ｜ 提交人：[张辉](https://dev.msh.team/zhanghui) ｜ 仓库：`engineering/kimi-darkmatter` ｜ 状态：**已关闭**
- [!2075 chore(apps/kimiapi): remove legacy sync claw chat logic](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2075) ｜ 提交人：[李华儒](https://dev.msh.team/lihuaru) ｜ 仓库：`engineering/kimi-darkmatter` ｜ 状态：**进行中**
- 其余 2 个 MR（0 merged / 0 opened / 2 closed），主要涉及 kimi-darkmatter。

#### 权限代理与环境配置（2 个 MR）

- [!2036 refactor(apps/kimiapi): extract plugin config setup and replace gjson with typed manifest parsing](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2036) ｜ 提交人：[许京爽](https://dev.msh.team/xujingshuang) ｜ 仓库：`engineering/kimi-darkmatter` ｜ 状态：**已合并**
- [!2049 feat(apps/kimiapi): support proxy path rewrite](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2049) ｜ 提交人：[李华儒](https://dev.msh.team/lihuaru) ｜ 仓库：`engineering/kimi-darkmatter` ｜ 状态：**已合并**

#### CDN 与边缘网络（2 个 MR）

- [!1 Add new directory](https://dev.msh.team/zhanghuishi/cdn/-/merge_requests/1) ｜ 提交人：[张惠施](https://dev.msh.team/zhanghuishi) ｜ 仓库：`zhanghuishi/cdn` ｜ 状态：**已合并**
- [!2 Feat: onboarding preset](https://dev.msh.team/zhanghuishi/cdn/-/merge_requests/2) ｜ 提交人：[许京爽](https://dev.msh.team/xujingshuang) ｜ 仓库：`zhanghuishi/cdn` ｜ 状态：**进行中**

### 用户体系与商业化

#### 账号、身份与登录（1 个 MR）

- [!1479 feat(apps/account): 实现邮箱验证码登录注册及易盾风控验证](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/1479) ｜ 提交人：[曹现峰](https://dev.msh.team/caoxianfeng) ｜ 仓库：`engineering/kimi-darkmatter` ｜ 状态：**进行中**

#### 会员权益与生命周期（0 个 MR）

- 本周暂无归入该分类的 MR

#### 订阅、计费与配额（2 个 MR）

- [!2056 feat(kimiapi): kc支持切换订阅独立计费](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2056) ｜ 提交人：[曹现峰](https://dev.msh.team/caoxianfeng) ｜ 仓库：`engineering/kimi-darkmatter` ｜ 状态：**已合并**
- [!2066 feat(apps/kimiapi): v2 版本按量计费](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2066) ｜ 提交人：[张辉](https://dev.msh.team/zhanghui) ｜ 仓库：`engineering/kimi-darkmatter` ｜ 状态：**进行中**

#### 增长活动与内容运营（0 个 MR）

- 本周暂无归入该分类的 MR

### 对话与交互体验

#### 会话连接与恢复（0 个 MR）

- 本周暂无归入该分类的 MR

#### 消息收发与状态同步（14 个 MR）

- [!2031 feat(apps/kimiapi): 更换新的快捷指令](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2031) ｜ 提交人：[张辉](https://dev.msh.team/zhanghui) ｜ 仓库：`engineering/kimi-darkmatter` ｜ 状态：**已合并**
- [!2034 feat(kimiapi/claw): support wecom plugins](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2034) ｜ 提交人：[许京爽](https://dev.msh.team/xujingshuang) ｜ 仓库：`engineering/kimi-darkmatter` ｜ 状态：**已合并**
- [!2050 feat(kimiapi/internal): add download file function](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2050) ｜ 提交人：[许京爽](https://dev.msh.team/xujingshuang) ｜ 仓库：`engineering/kimi-darkmatter` ｜ 状态：**已合并**
- [!2067 feat(kimiapi:claw): support lark](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2067) ｜ 提交人：[许京爽](https://dev.msh.team/xujingshuang) ｜ 仓库：`engineering/kimi-darkmatter` ｜ 状态：**已合并**
- [!2026 feat：kimi claw 舆情补偿](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2026) ｜ 提交人：[曹现峰](https://dev.msh.team/caoxianfeng) ｜ 仓库：`engineering/kimi-darkmatter` ｜ 状态：**已合并**
- 其余 9 个 MR（1 merged / 6 opened / 2 closed），主要涉及 kimi-darkmatter。

#### 多端体验与交互改版（1 个 MR）

- [!508 feat: claw chat](https://dev.msh.team/engineering/kimi/kimi-bigbang/-/merge_requests/508) ｜ 提交人：[李华儒](https://dev.msh.team/lihuaru) ｜ 仓库：`engineering/kimi/kimi-bigbang` ｜ 状态：**进行中**

#### 文件、媒体与附件能力（0 个 MR）

- 本周暂无归入该分类的 MR

#### 模板与内容生产（0 个 MR）

- 本周暂无归入该分类的 MR

### Agent 与渠道生态

#### 插件、工具与 Skill 框架（0 个 MR）

- 本周暂无归入该分类的 MR

#### 渠道接入与消息投递（0 个 MR）

- 本周暂无归入该分类的 MR

#### Bot 配置、人设与快捷指令（0 个 MR）

- 本周暂无归入该分类的 MR

#### OpenClaw Runtime 与 Workflow（1 个 MR）

- [!2 feat: set heartbeat every 60m](https://dev.msh.team/agentic/kimiclaw-image/-/merge_requests/2) ｜ 提交人：[张惠施](https://dev.msh.team/zhanghuishi) ｜ 仓库：`agentic/kimiclaw-image` ｜ 状态：**已合并**

#### 外部数据源与集成能力（0 个 MR）

- 本周暂无归入该分类的 MR

## 二、人员统计

### [张辉](https://dev.msh.team/zhanghui)

- 主要贡献仓库数：**4**
- MR 总数：**17**（已合并 13 / 进行中 2 / 已关闭 2）
- Commit 总数：**604**
- 重点仓库：
  - `engineering/kimi-darkmatter`：MR 10（merged 6 / opened 2 / closed 2），Commit 547；本周在 `engineering/kimi-darkmatter` 主要推进了 10 个 MR、547 次提交，重点集中在 消息收发与状态同步、资源供应商与实例编排、工作空间与数据生命周期
  - `protos/kimi`：MR 4（merged 4 / opened 0 / closed 0），Commit 28；本周在 `protos/kimi` 主要推进了 4 个 MR、28 次提交，重点集中在 运营后台与管理工具
  - `engineering/secrets/kimi-secret-prod`：MR 3（merged 3 / opened 0 / closed 0），Commit 14；本周在 `engineering/secrets/kimi-secret-prod` 主要推进了 3 个 MR、14 次提交，重点集中在 资源供应商与实例编排
  - `engineering/devops/kimi-secret`：MR 0（merged 0 / opened 0 / closed 0），Commit 15；本周在 `engineering/devops/kimi-secret` 主要推进了 0 个 MR、15 次提交，重点集中在 日常迭代与问题修复

### [李华儒](https://dev.msh.team/lihuaru)

- 主要贡献仓库数：**7**
- MR 总数：**9**（已合并 4 / 进行中 5 / 已关闭 0）
- Commit 总数：**275**
- 重点仓库：
  - `engineering/kimi-darkmatter`：MR 6（merged 3 / opened 3 / closed 0），Commit 133；本周在 `engineering/kimi-darkmatter` 主要推进了 6 个 MR、133 次提交，重点集中在 权限代理与环境配置、消息收发与状态同步、稳定性、容灾与观测
  - `protos/kimi`：MR 1（merged 0 / opened 1 / closed 0），Commit 87；本周在 `protos/kimi` 主要推进了 1 个 MR、87 次提交，重点集中在 运营后台与管理工具
  - `engineering/devops/kimi-secret`：MR 1（merged 1 / opened 0 / closed 0），Commit 36；本周在 `engineering/devops/kimi-secret` 主要推进了 1 个 MR、36 次提交，重点集中在 资源供应商与实例编排
  - `engineering/kimi/kimi-bigbang`：MR 1（merged 0 / opened 1 / closed 0），Commit 8；本周在 `engineering/kimi/kimi-bigbang` 主要推进了 1 个 MR、8 次提交，重点集中在 多端体验与交互改版

### [许京爽](https://dev.msh.team/xujingshuang)

- 主要贡献仓库数：**6**
- MR 总数：**16**（已合并 10 / 进行中 5 / 已关闭 1）
- Commit 总数：**108**
- 重点仓库：
  - `engineering/kimi-darkmatter`：MR 8（merged 5 / opened 2 / closed 1），Commit 64；本周在 `engineering/kimi-darkmatter` 主要推进了 8 个 MR、64 次提交，重点集中在 消息收发与状态同步、权限代理与环境配置
  - `protos/kimi`：MR 5（merged 4 / opened 1 / closed 0），Commit 33；本周在 `protos/kimi` 主要推进了 5 个 MR、33 次提交，重点集中在 运营后台与管理工具
  - `engineering/secrets/kimi-secret-prod`：MR 1（merged 1 / opened 0 / closed 0），Commit 4；本周在 `engineering/secrets/kimi-secret-prod` 主要推进了 1 个 MR、4 次提交，重点集中在 资源供应商与实例编排
  - `zhanghuishi/cdn`：MR 1（merged 0 / opened 1 / closed 0），Commit 2；本周在 `zhanghuishi/cdn` 主要推进了 1 个 MR、2 次提交，重点集中在 CDN 与边缘网络

### [曹现峰](https://dev.msh.team/caoxianfeng)

- 主要贡献仓库数：**3**
- MR 总数：**8**（已合并 6 / 进行中 2 / 已关闭 0）
- Commit 总数：**102**
- 重点仓库：
  - `engineering/kimi-darkmatter`：MR 4（merged 3 / opened 1 / closed 0），Commit 76；本周在 `engineering/kimi-darkmatter` 主要推进了 4 个 MR、76 次提交，重点集中在 订阅、计费与配额、消息收发与状态同步、运营后台与管理工具
  - `protos/kimi`：MR 4（merged 3 / opened 1 / closed 0），Commit 24；本周在 `protos/kimi` 主要推进了 4 个 MR、24 次提交，重点集中在 运营后台与管理工具
  - `engineering/user-center`：MR 0（merged 0 / opened 0 / closed 0），Commit 2；本周在 `engineering/user-center` 主要推进了 0 个 MR、2 次提交，重点集中在 日常迭代与问题修复

### [张惠施](https://dev.msh.team/zhanghuishi)

- 主要贡献仓库数：**5**
- MR 总数：**10**（已合并 7 / 进行中 1 / 已关闭 2）
- Commit 总数：**142**
- 重点仓库：
  - `engineering/kimi-darkmatter`：MR 5（merged 2 / opened 1 / closed 2），Commit 39；本周在 `engineering/kimi-darkmatter` 主要推进了 5 个 MR、39 次提交，重点集中在 运营后台与管理工具、消息收发与状态同步
  - `protos/kimi`：MR 2（merged 2 / opened 0 / closed 0），Commit 9；本周在 `protos/kimi` 主要推进了 2 个 MR、9 次提交，重点集中在 运营后台与管理工具
  - `zhanghuishi/cdn`：MR 1（merged 1 / opened 0 / closed 0），Commit 66；本周在 `zhanghuishi/cdn` 主要推进了 1 个 MR、66 次提交，重点集中在 CDN 与边缘网络
  - `agentic/kimiclaw-image`：MR 2（merged 2 / opened 0 / closed 0），Commit 12；本周在 `agentic/kimiclaw-image` 主要推进了 2 个 MR、12 次提交，重点集中在 OpenClaw Runtime 与 Workflow、Agent 与插件

## 三、团队整体产出统计

- 总 MR：**60**
- 总 Commit：**1231**
- 活跃仓库数：**11**
- 活跃成员数：**5**

### 统计摘要

- MR 状态分布：**Merged 40 / Opened 15 / Closed 5**
- 每日最高活动：**2026-03-17**
- 最高产出仓库：`engineering/kimi-darkmatter`
- 成员产出排行：
  - 张辉：MR 17，Commit 604
  - 许京爽：MR 16，Commit 108
  - 张惠施：MR 10，Commit 142
  - 李华儒：MR 9，Commit 275
  - 曹现峰：MR 8，Commit 102
- 产品方向分布：
  - KimiClaw 主营业务：20 个 MR
  - 对话与交互体验：15 个 MR
  - 用户体系与商业化：3 个 MR
  - Agent 与渠道生态：1 个 MR

_报告生成时间：2026-03-20 00:55:33_
