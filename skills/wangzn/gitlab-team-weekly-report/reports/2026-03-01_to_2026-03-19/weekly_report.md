# GitLab Weekly Report

时间范围：`2026-03-01` 至 `2026-03-19`

## 参与成员

- [张辉](https://dev.msh.team/zhanghui) (`zhanghui`)
- [李华儒](https://dev.msh.team/lihuaru) (`lihuaru`)
- [许京爽](https://dev.msh.team/xujingshuang) (`xujingshuang`)
- [曹现峰](https://dev.msh.team/caoxianfeng) (`caoxianfeng`)
- [张惠施](https://dev.msh.team/zhanghuishi) (`zhanghuishi`)

## 一、产品功能

### 基础体验和基建

#### CDN 管理（2 个 MR）

- [!1 Add new directory](https://dev.msh.team/zhanghuishi/cdn/-/merge_requests/1)
  - 仓库：`zhanghuishi/cdn` ｜ 作者：[张惠施](https://dev.msh.team/zhanghuishi) ｜ 状态：**已合并**
- [!2 Feat: onboarding preset](https://dev.msh.team/zhanghuishi/cdn/-/merge_requests/2)
  - 仓库：`zhanghuishi/cdn` ｜ 作者：[许京爽](https://dev.msh.team/xujingshuang) ｜ 状态：**进行中**

#### 客户端/交互体验（3 个 MR）

- [!5 Develop](https://dev.msh.team/zhanghuishi/multi-exec/-/merge_requests/5)
  - 仓库：`zhanghuishi/multi-exec` ｜ 作者：[张惠施](https://dev.msh.team/zhanghuishi) ｜ 状态：**已合并**
- [!4 Develop](https://dev.msh.team/zhanghuishi/multi-exec/-/merge_requests/4)
  - 仓库：`zhanghuishi/multi-exec` ｜ 作者：[张惠施](https://dev.msh.team/zhanghuishi) ｜ 状态：**已合并**
- [!3 Develop](https://dev.msh.team/zhanghuishi/multi-exec/-/merge_requests/3)
  - 仓库：`zhanghuishi/multi-exec` ｜ 作者：[张惠施](https://dev.msh.team/zhanghuishi) ｜ 状态：**已合并**

#### 性能与稳定性（16 个 MR）

- [!2023 feat(apps/kimiapi): 实现Claw workspace备份与恢复功能，支持会员到期前自动备份至TOS](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2023)
  - 仓库：`engineering/kimi-darkmatter` ｜ 作者：[张辉](https://dev.msh.team/zhanghui) ｜ 状态：**已合并**
- [!1279 feat(apps/kimiapi): ws ingress need HTTP backend](https://dev.msh.team/delivery/canary/-/merge_requests/1279)
  - 仓库：`delivery/canary` ｜ 作者：[李华儒](https://dev.msh.team/lihuaru) ｜ 状态：**已合并**
- [!1943 feat(apps/kimiapi): claw operation 通过 ssh 替代小助手操作](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/1943)
  - 仓库：`engineering/kimi-darkmatter` ｜ 作者：[张辉](https://dev.msh.team/zhanghui) ｜ 状态：**已合并**
- [!1227 feat(kimi.claw.v1): 增加 claw bot 备份能力](https://dev.msh.team/protos/kimi/-/merge_requests/1227)
  - 仓库：`protos/kimi` ｜ 作者：[张辉](https://dev.msh.team/zhanghui) ｜ 状态：**已合并**
- [!2026 feat：kimi claw 舆情补偿](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2026)
  - 仓库：`engineering/kimi-darkmatter` ｜ 作者：[曹现峰](https://dev.msh.team/caoxianfeng) ｜ 状态：**已合并**
- 其余 11 个 MR（6 merged / 2 opened / 3 closed），主要涉及 kimi-darkmatter / kimi / canary。

#### 数据与监控（8 个 MR）

- [!2013 feat(apps/kimiapi): claw 补充腾讯云供应商](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2013)
  - 仓库：`engineering/kimi-darkmatter` ｜ 作者：[张辉](https://dev.msh.team/zhanghui) ｜ 状态：**已合并**
- [!540 feat(apps/kimiapi): claw 切换腾讯云国内](https://dev.msh.team/engineering/secrets/kimi-secret-prod/-/merge_requests/540)
  - 仓库：`engineering/secrets/kimi-secret-prod` ｜ 作者：[张辉](https://dev.msh.team/zhanghui) ｜ 状态：**已合并**
- [!530 feat:  kimiclaw 更新火山、阿里镜像](https://dev.msh.team/engineering/secrets/kimi-secret-prod/-/merge_requests/530)
  - 仓库：`engineering/secrets/kimi-secret-prod` ｜ 作者：[张辉](https://dev.msh.team/zhanghui) ｜ 状态：**已合并**
- [!543 feat(apps/kimiapi): claw 国内供应商切换到腾讯](https://dev.msh.team/engineering/secrets/kimi-secret-prod/-/merge_requests/543)
  - 仓库：`engineering/secrets/kimi-secret-prod` ｜ 作者：[张辉](https://dev.msh.team/zhanghui) ｜ 状态：**已合并**
- [!541 feat(apps/kimiapi): claw 创建机器切换回火山](https://dev.msh.team/engineering/secrets/kimi-secret-prod/-/merge_requests/541)
  - 仓库：`engineering/secrets/kimi-secret-prod` ｜ 作者：[张辉](https://dev.msh.team/zhanghui) ｜ 状态：**已合并**
- 其余 3 个 MR（1 merged / 1 opened / 1 closed），主要涉及 kimi-secret / kimi-darkmatter / kimi-secret-prod。

#### 权限/安全/配置（4 个 MR）

- [!2050 feat(kimiapi/internal): add download file function](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2050)
  - 仓库：`engineering/kimi-darkmatter` ｜ 作者：[许京爽](https://dev.msh.team/xujingshuang) ｜ 状态：**已合并**
- [!544 feat(kimiapi/internal): add pattern for download data](https://dev.msh.team/engineering/secrets/kimi-secret-prod/-/merge_requests/544)
  - 仓库：`engineering/secrets/kimi-secret-prod` ｜ 作者：[许京爽](https://dev.msh.team/xujingshuang) ｜ 状态：**已合并**
- [!2049 feat(apps/kimiapi): support proxy path rewrite](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2049)
  - 仓库：`engineering/kimi-darkmatter` ｜ 作者：[李华儒](https://dev.msh.team/lihuaru) ｜ 状态：**已合并**
- [!522 feat(apps/kimiapi): update claw ecs image id](https://dev.msh.team/engineering/secrets/kimi-secret-prod/-/merge_requests/522)
  - 仓库：`engineering/secrets/kimi-secret-prod` ｜ 作者：[张辉](https://dev.msh.team/zhanghui) ｜ 状态：**已合并**

### 用户和商业化

#### 登录注册/账号体系（6 个 MR）

- [!177 feat(account): 读取V2用户缓存的会员信息](https://dev.msh.team/engineering/user-center/-/merge_requests/177)
  - 仓库：`engineering/user-center` ｜ 作者：[曹现峰](https://dev.msh.team/caoxianfeng) ｜ 状态：**已合并**
- [!1220 feat(admin): add vest account management APIs for outsight (protos/kimi!1062)](https://dev.msh.team/protos/kimi/-/merge_requests/1220)
  - 仓库：`protos/kimi` ｜ 作者：[许京爽](https://dev.msh.team/xujingshuang) ｜ 状态：**已合并**
- [!1062 feat(admin): add vest account management APIs for outsight](https://dev.msh.team/protos/kimi/-/merge_requests/1062)
  - 仓库：`protos/kimi` ｜ 作者：[曹现峰](https://dev.msh.team/caoxianfeng) ｜ 状态：**已合并**
- [!1078 feat(account): 新增邮箱验证与绑定接口](https://dev.msh.team/protos/kimi/-/merge_requests/1078)
  - 仓库：`protos/kimi` ｜ 作者：[曹现峰](https://dev.msh.team/caoxianfeng) ｜ 状态：**进行中**
- [!178 feat: 更新go.mod](https://dev.msh.team/engineering/user-center/-/merge_requests/178)
  - 仓库：`engineering/user-center` ｜ 作者：[曹现峰](https://dev.msh.team/caoxianfeng) ｜ 状态：**已合并**
- 其余 1 个 MR（0 merged / 1 opened / 0 closed），主要涉及 kimi-darkmatter。

#### 订阅/支付/套餐（5 个 MR）

- [!2056 feat(kimiapi): kc支持切换订阅独立计费](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2056)
  - 仓库：`engineering/kimi-darkmatter` ｜ 作者：[曹现峰](https://dev.msh.team/caoxianfeng) ｜ 状态：**已合并**
- [!1237 feat(kimiapi): 新增billing rate limit log meta](https://dev.msh.team/protos/kimi/-/merge_requests/1237)
  - 仓库：`protos/kimi` ｜ 作者：[曹现峰](https://dev.msh.team/caoxianfeng) ｜ 状态：**已合并**
- [!1236 feat(kimiapi): 新增billing rate limit log meta](https://dev.msh.team/protos/kimi/-/merge_requests/1236)
  - 仓库：`protos/kimi` ｜ 作者：[曹现峰](https://dev.msh.team/caoxianfeng) ｜ 状态：**已合并**
- [!2066 feat(apps/kimiapi): v2 版本按量计费](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2066)
  - 仓库：`engineering/kimi-darkmatter` ｜ 作者：[张辉](https://dev.msh.team/zhanghui) ｜ 状态：**进行中**
- [!1948 feat(apps/kimiapi): kimiclaw 商业化](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/1948)
  - 仓库：`engineering/kimi-darkmatter` ｜ 作者：[张辉](https://dev.msh.team/zhanghui) ｜ 状态：**已合并**

#### 用户运营/留存/增长转化（0 个 MR）

- 本周暂无归入该分类的 MR

#### 管理后台/配置运营（12 个 MR）

- [!1235 feat(kimi.claw.admin.v1): add RecreateBotWithImage RPC for admin to rebuild bot with custom image](https://dev.msh.team/protos/kimi/-/merge_requests/1235)
  - 仓库：`protos/kimi` ｜ 作者：[张辉](https://dev.msh.team/zhanghui) ｜ 状态：**已合并**
- [!1225 feat(apps/kimiapi): claw admin add restartInstance](https://dev.msh.team/protos/kimi/-/merge_requests/1225)
  - 仓库：`protos/kimi` ｜ 作者：[张惠施](https://dev.msh.team/zhanghuishi) ｜ 状态：**已合并**
- [!2057 feat(apps/kimiapi): modify  admin RestartInstanceByBotID](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2057)
  - 仓库：`engineering/kimi-darkmatter` ｜ 作者：[张惠施](https://dev.msh.team/zhanghuishi) ｜ 状态：**已合并**
- [!2055 feat(apps/kimiapi): impl claw admin svc RestartInstance](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2055)
  - 仓库：`engineering/kimi-darkmatter` ｜ 作者：[张惠施](https://dev.msh.team/zhanghuishi) ｜ 状态：**已合并**
- [!1239 Feat admin instance](https://dev.msh.team/protos/kimi/-/merge_requests/1239)
  - 仓库：`protos/kimi` ｜ 作者：[张惠施](https://dev.msh.team/zhanghuishi) ｜ 状态：**已合并**
- 其余 7 个 MR（6 merged / 0 opened / 1 closed），主要涉及 kimi / kimi-darkmatter / kimi-bigbang。

### Chat 核心链路

#### 会话入口与创建（1 个 MR）

- [!1281 feat(apps/kimiapi): http ingress](https://dev.msh.team/delivery/canary/-/merge_requests/1281)
  - 仓库：`delivery/canary` ｜ 作者：[李华儒](https://dev.msh.team/lihuaru) ｜ 状态：**已合并**

#### 消息收发与渲染（37 个 MR）

- [!503 feat: 优化会员等级文案](https://dev.msh.team/engineering/kimi/kimi-bigbang/-/merge_requests/503)
  - 仓库：`engineering/kimi/kimi-bigbang` ｜ 作者：[曹现峰](https://dev.msh.team/caoxianfeng) ｜ 状态：**已合并**
- [!2006 feat(apps/outsight): redis debug zcard](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2006)
  - 仓库：`engineering/kimi-darkmatter` ｜ 作者：[李华儒](https://dev.msh.team/lihuaru) ｜ 状态：**已合并**
- [!1976 feat(apps/kimiapi): run script b64 decode](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/1976)
  - 仓库：`engineering/kimi-darkmatter` ｜ 作者：[张惠施](https://dev.msh.team/zhanghuishi) ｜ 状态：**已合并**
- [!456 feat(apps/kimiapi): 修改镜像信息](https://dev.msh.team/engineering/devops/kimi-secret/-/merge_requests/456)
  - 仓库：`engineering/devops/kimi-secret` ｜ 作者：[张辉](https://dev.msh.team/zhanghui) ｜ 状态：**已合并**
- [!1961 feat(apps/kimiapi): claw phase3 sendMsgStream](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/1961)
  - 仓库：`engineering/kimi-darkmatter` ｜ 作者：[李华儒](https://dev.msh.team/lihuaru) ｜ 状态：**已合并**
- 其余 32 个 MR（24 merged / 6 opened / 2 closed），主要涉及 kimi-darkmatter / kimi-secret-prod / kimi。

#### 上下文/记忆（0 个 MR）

- 本周暂无归入该分类的 MR

#### Agent/工具调用（60 个 MR）

- [!1955 feat(apps/kimiapi): claw phase3 - support IM protocol](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/1955)
  - 仓库：`engineering/kimi-darkmatter` ｜ 作者：[许京爽](https://dev.msh.team/xujingshuang) ｜ 状态：**已合并**
- [!2031 feat(apps/kimiapi): 更换新的快捷指令](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2031)
  - 仓库：`engineering/kimi-darkmatter` ｜ 作者：[张辉](https://dev.msh.team/zhanghui) ｜ 状态：**已合并**
- [!2034 feat(kimiapi/claw): support wecom plugins](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2034)
  - 仓库：`engineering/kimi-darkmatter` ｜ 作者：[许京爽](https://dev.msh.team/xujingshuang) ｜ 状态：**已合并**
- [!2036 refactor(apps/kimiapi): extract plugin config setup and replace gjson with typed manifest parsing](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2036)
  - 仓库：`engineering/kimi-darkmatter` ｜ 作者：[许京爽](https://dev.msh.team/xujingshuang) ｜ 状态：**已合并**
- [!1200 feat(proto): add user membership service, membership change event and bot membership expiration](https://dev.msh.team/protos/kimi/-/merge_requests/1200)
  - 仓库：`protos/kimi` ｜ 作者：[曹现峰](https://dev.msh.team/caoxianfeng) ｜ 状态：**已合并**
- 其余 55 个 MR（43 merged / 10 opened / 2 closed），主要涉及 kimi-darkmatter / kimi / kimi-secret。

#### 模型路由与推理（0 个 MR）

- 本周暂无归入该分类的 MR

## 二、人员统计

### [张辉](https://dev.msh.team/zhanghui)

- 主要贡献仓库数：**6**
- MR 总数：**42**（已合并 37 / 进行中 2 / 已关闭 3）
- Commit 总数：**1189**

#### Repo: `engineering/kimi-darkmatter`

- MR：25（merged 20 / opened 2 / closed 3）
- Commit：995
- 主要 MR：
  - [!2031 feat(apps/kimiapi): 更换新的快捷指令](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2031)（已合并）
  - [!2013 feat(apps/kimiapi): claw 补充腾讯云供应商](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2013)（已合并）
  - [!2023 feat(apps/kimiapi): 实现Claw workspace备份与恢复功能，支持会员到期前自动备份至TOS](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2023)（已合并）
- 贡献总结：本周在 `engineering/kimi-darkmatter` 主要推进了 25 个 MR、995 次提交，重点集中在 Agent/工具调用、数据与监控、性能与稳定性

#### Repo: `protos/kimi`

- MR：6（merged 6 / opened 0 / closed 0）
- Commit：78
- 主要 MR：
  - [!1235 feat(kimi.claw.admin.v1): add RecreateBotWithImage RPC for admin to rebuild bot with custom image](https://dev.msh.team/protos/kimi/-/merge_requests/1235)（已合并）
  - [!1216 feat(kimi.claw.admin.v1): 预检和删除七天前过期的用户 BOT](https://dev.msh.team/protos/kimi/-/merge_requests/1216)（已合并）
  - [!1227 feat(kimi.claw.v1): 增加 claw bot 备份能力](https://dev.msh.team/protos/kimi/-/merge_requests/1227)（已合并）
- 贡献总结：本周在 `protos/kimi` 主要推进了 6 个 MR、78 次提交，重点集中在 管理后台/配置运营、性能与稳定性

#### Repo: `engineering/secrets/kimi-secret-prod`

- MR：9（merged 9 / opened 0 / closed 0）
- Commit：35
- 主要 MR：
  - [!540 feat(apps/kimiapi): claw 切换腾讯云国内](https://dev.msh.team/engineering/secrets/kimi-secret-prod/-/merge_requests/540)（已合并）
  - [!542 feat(apps/kimiapi): 更新适配企微版本 claw 镜像](https://dev.msh.team/engineering/secrets/kimi-secret-prod/-/merge_requests/542)（已合并）
  - [!522 feat(apps/kimiapi): update claw ecs image id](https://dev.msh.team/engineering/secrets/kimi-secret-prod/-/merge_requests/522)（已合并）
- 贡献总结：本周在 `engineering/secrets/kimi-secret-prod` 主要推进了 9 个 MR、35 次提交，重点集中在 数据与监控、Agent/工具调用、权限/安全/配置

#### Repo: `engineering/devops/kimi-secret`

- MR：1（merged 1 / opened 0 / closed 0）
- Commit：73
- 主要 MR：
  - [!456 feat(apps/kimiapi): 修改镜像信息](https://dev.msh.team/engineering/devops/kimi-secret/-/merge_requests/456)（已合并）
- 贡献总结：本周在 `engineering/devops/kimi-secret` 主要推进了 1 个 MR、73 次提交，重点集中在 消息收发与渲染

#### Repo: `engineering/kimi/kimi-bigbang`

- MR：1（merged 1 / opened 0 / closed 0）
- Commit：3
- 主要 MR：
  - [!501 fix(apps/outsight): 修复后台筛选](https://dev.msh.team/engineering/kimi/kimi-bigbang/-/merge_requests/501)（已合并）
- 贡献总结：本周在 `engineering/kimi/kimi-bigbang` 主要推进了 1 个 MR、3 次提交，重点集中在 管理后台/配置运营

#### Repo: `zhanghuishi/cdn`

- MR：0（merged 0 / opened 0 / closed 0）
- Commit：5
- 贡献总结：本周在 `zhanghuishi/cdn` 主要推进了 0 个 MR、5 次提交，重点集中在 日常迭代与问题修复

### [李华儒](https://dev.msh.team/lihuaru)

- 主要贡献仓库数：**8**
- MR 总数：**34**（已合并 26 / 进行中 6 / 已关闭 2）
- Commit 总数：**1570**

#### Repo: `engineering/kimi-darkmatter`

- MR：21（merged 15 / opened 4 / closed 2）
- Commit：1179
- 主要 MR：
  - [!2006 feat(apps/outsight): redis debug zcard](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2006)（已合并）
  - [!1966 feat(apps/chatty): repair json for nanobanana](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/1966)（已合并）
  - [!1961 feat(apps/kimiapi): claw phase3 sendMsgStream](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/1961)（已合并）
- 贡献总结：本周在 `engineering/kimi-darkmatter` 主要推进了 21 个 MR、1179 次提交，重点集中在 消息收发与渲染

#### Repo: `protos/kimi`

- MR：4（merged 3 / opened 1 / closed 0）
- Commit：272
- 主要 MR：
  - [!1202 feat(claw): im protocal phase 3](https://dev.msh.team/protos/kimi/-/merge_requests/1202)（已合并）
  - [!1199 feat(claw): im protocal phase 2](https://dev.msh.team/protos/kimi/-/merge_requests/1199)（已合并）
  - [!1188 feat(apps/kimiapi): claw chat](https://dev.msh.team/protos/kimi/-/merge_requests/1188)（已合并）
- 贡献总结：本周在 `protos/kimi` 主要推进了 4 个 MR、272 次提交，重点集中在 Agent/工具调用、消息收发与渲染

#### Repo: `delivery/canary`

- MR：3（merged 3 / opened 0 / closed 0）
- Commit：15
- 主要 MR：
  - [!1279 feat(apps/kimiapi): ws ingress need HTTP backend](https://dev.msh.team/delivery/canary/-/merge_requests/1279)（已合并）
  - [!1284 Revert "feat(apps/kimiapi): http ingress"](https://dev.msh.team/delivery/canary/-/merge_requests/1284)（已合并）
  - [!1281 feat(apps/kimiapi): http ingress](https://dev.msh.team/delivery/canary/-/merge_requests/1281)（已合并）
- 贡献总结：本周在 `delivery/canary` 主要推进了 3 个 MR、15 次提交，重点集中在 性能与稳定性、会话入口与创建

#### Repo: `engineering/secrets/kimi-secret-prod`

- MR：3（merged 3 / opened 0 / closed 0）
- Commit：14
- 主要 MR：
  - [!531 feat(apps/kimiapi): chatty pre](https://dev.msh.team/engineering/secrets/kimi-secret-prod/-/merge_requests/531)（已合并）
  - [!520 feat(kimiapi): claw chat](https://dev.msh.team/engineering/secrets/kimi-secret-prod/-/merge_requests/520)（已合并）
  - [!524 feat(apps/chatty): nanobanana2 for ppt](https://dev.msh.team/engineering/secrets/kimi-secret-prod/-/merge_requests/524)（已合并）
- 贡献总结：本周在 `engineering/secrets/kimi-secret-prod` 主要推进了 3 个 MR、14 次提交，重点集中在 消息收发与渲染

#### Repo: `engineering/devops/kimi-secret`

- MR：1（merged 1 / opened 0 / closed 0）
- Commit：55
- 主要 MR：
  - [!462 feat(apps/hooker): feishu proxy](https://dev.msh.team/engineering/devops/kimi-secret/-/merge_requests/462)（已合并）
- 贡献总结：本周在 `engineering/devops/kimi-secret` 主要推进了 1 个 MR、55 次提交，重点集中在 消息收发与渲染

#### Repo: `engineering/kimi/kimi-bigbang`

- MR：1（merged 0 / opened 1 / closed 0）
- Commit：20
- 主要 MR：
  - [!508 feat: claw chat](https://dev.msh.team/engineering/kimi/kimi-bigbang/-/merge_requests/508)（进行中）
- 贡献总结：本周在 `engineering/kimi/kimi-bigbang` 主要推进了 1 个 MR、20 次提交，重点集中在 消息收发与渲染

#### Repo: `search-engine/bridge_kimi_openclaw`

- MR：1（merged 1 / opened 0 / closed 0）
- Commit：6
- 主要 MR：
  - [!56 feat: send msg stream websocket](https://dev.msh.team/search-engine/bridge_kimi_openclaw/-/merge_requests/56)（已合并）
- 贡献总结：本周在 `search-engine/bridge_kimi_openclaw` 主要推进了 1 个 MR、6 次提交，重点集中在 消息收发与渲染

#### Repo: `lihuaru/kimiim-py`

- MR：0（merged 0 / opened 0 / closed 0）
- Commit：9
- 贡献总结：本周在 `lihuaru/kimiim-py` 主要推进了 0 个 MR、9 次提交，重点集中在 日常迭代与问题修复

### [许京爽](https://dev.msh.team/xujingshuang)

- 主要贡献仓库数：**7**
- MR 总数：**31**（已合并 22 / 进行中 7 / 已关闭 2）
- Commit 总数：**580**

#### Repo: `engineering/kimi-darkmatter`

- MR：18（merged 13 / opened 4 / closed 1）
- Commit：432
- 主要 MR：
  - [!1955 feat(apps/kimiapi): claw phase3 - support IM protocol](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/1955)（已合并）
  - [!2050 feat(kimiapi/internal): add download file function](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2050)（已合并）
  - [!2036 refactor(apps/kimiapi): extract plugin config setup and replace gjson with typed manifest parsing](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2036)（已合并）
- 贡献总结：本周在 `engineering/kimi-darkmatter` 主要推进了 18 个 MR、432 次提交，重点集中在 Agent/工具调用、权限/安全/配置

#### Repo: `protos/kimi`

- MR：8（merged 6 / opened 1 / closed 1）
- Commit：108
- 主要 MR：
  - [!1241 feat(kimiapi): support lark](https://dev.msh.team/protos/kimi/-/merge_requests/1241)（已合并）
  - [!1220 feat(admin): add vest account management APIs for outsight (protos/kimi!1062)](https://dev.msh.team/protos/kimi/-/merge_requests/1220)（已合并）
  - [!1206 feat(claw): workspace file](https://dev.msh.team/protos/kimi/-/merge_requests/1206)（已合并）
- 贡献总结：本周在 `protos/kimi` 主要推进了 8 个 MR、108 次提交，重点集中在 Agent/工具调用、登录注册/账号体系

#### Repo: `engineering/devops/kimi-secret`

- MR：2（merged 1 / opened 1 / closed 0）
- Commit：32
- 主要 MR：
  - [!452 feat(app/claw): support file system for kimi claw](https://dev.msh.team/engineering/devops/kimi-secret/-/merge_requests/452)（已合并）
  - [!457 Draft: feat(kimiapi/claw): for rl](https://dev.msh.team/engineering/devops/kimi-secret/-/merge_requests/457)（进行中）
- 贡献总结：本周在 `engineering/devops/kimi-secret` 主要推进了 2 个 MR、32 次提交，重点集中在 Agent/工具调用

#### Repo: `engineering/secrets/kimi-secret-prod`

- MR：2（merged 2 / opened 0 / closed 0）
- Commit：6
- 主要 MR：
  - [!544 feat(kimiapi/internal): add pattern for download data](https://dev.msh.team/engineering/secrets/kimi-secret-prod/-/merge_requests/544)（已合并）
  - [!538 feat(claw): add claw endpoint](https://dev.msh.team/engineering/secrets/kimi-secret-prod/-/merge_requests/538)（已合并）
- 贡献总结：本周在 `engineering/secrets/kimi-secret-prod` 主要推进了 2 个 MR、6 次提交，重点集中在 权限/安全/配置、Agent/工具调用

#### Repo: `zhanghuishi/cdn`

- MR：1（merged 0 / opened 1 / closed 0）
- Commit：0
- 主要 MR：
  - [!2 Feat: onboarding preset](https://dev.msh.team/zhanghuishi/cdn/-/merge_requests/2)（进行中）
- 贡献总结：本周在 `zhanghuishi/cdn` 主要推进了 1 个 MR、0 次提交，重点集中在 CDN 管理

#### Repo: `lihuaru/gizmo`

- MR：0（merged 0 / opened 0 / closed 0）
- Commit：1
- 贡献总结：本周在 `lihuaru/gizmo` 主要推进了 0 个 MR、1 次提交，重点集中在 日常迭代与问题修复

#### Repo: `search-engine/bridge_kimi_openclaw`

- MR：0（merged 0 / opened 0 / closed 0）
- Commit：1
- 贡献总结：本周在 `search-engine/bridge_kimi_openclaw` 主要推进了 0 个 MR、1 次提交，重点集中在 日常迭代与问题修复

### [曹现峰](https://dev.msh.team/caoxianfeng)

- 主要贡献仓库数：**6**
- MR 总数：**25**（已合并 20 / 进行中 5 / 已关闭 0）
- Commit 总数：**621**

#### Repo: `engineering/kimi-darkmatter`

- MR：12（merged 9 / opened 3 / closed 0）
- Commit：442
- 主要 MR：
  - [!2056 feat(kimiapi): kc支持切换订阅独立计费](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2056)（已合并）
  - [!1960 fix(outsight): 优化waitlist bot 长链接](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/1960)（已合并）
  - [!2011 feat(kimiapi-internal): 修改kimi code 并发兜底时间为10min](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2011)（已合并）
- 贡献总结：本周在 `engineering/kimi-darkmatter` 主要推进了 12 个 MR、442 次提交，重点集中在 订阅/支付/套餐、Agent/工具调用、消息收发与渲染

#### Repo: `protos/kimi`

- MR：7（merged 6 / opened 1 / closed 0）
- Commit：102
- 主要 MR：
  - [!1200 feat(proto): add user membership service, membership change event and bot membership expiration](https://dev.msh.team/protos/kimi/-/merge_requests/1200)（已合并）
  - [!1237 feat(kimiapi): 新增billing rate limit log meta](https://dev.msh.team/protos/kimi/-/merge_requests/1237)（已合并）
  - [!1236 feat(kimiapi): 新增billing rate limit log meta](https://dev.msh.team/protos/kimi/-/merge_requests/1236)（已合并）
- 贡献总结：本周在 `protos/kimi` 主要推进了 7 个 MR、102 次提交，重点集中在 Agent/工具调用、订阅/支付/套餐

#### Repo: `engineering/kimi/kimi-bigbang`

- MR：2（merged 1 / opened 1 / closed 0）
- Commit：29
- 主要 MR：
  - [!503 feat: 优化会员等级文案](https://dev.msh.team/engineering/kimi/kimi-bigbang/-/merge_requests/503)（已合并）
  - [!506 feat（outsight）: 支持创建马甲号](https://dev.msh.team/engineering/kimi/kimi-bigbang/-/merge_requests/506)（进行中）
- 贡献总结：本周在 `engineering/kimi/kimi-bigbang` 主要推进了 2 个 MR、29 次提交，重点集中在 消息收发与渲染

#### Repo: `engineering/user-center`

- MR：2（merged 2 / opened 0 / closed 0）
- Commit：30
- 主要 MR：
  - [!177 feat(account): 读取V2用户缓存的会员信息](https://dev.msh.team/engineering/user-center/-/merge_requests/177)（已合并）
  - [!178 feat: 更新go.mod](https://dev.msh.team/engineering/user-center/-/merge_requests/178)（已合并）
- 贡献总结：本周在 `engineering/user-center` 主要推进了 2 个 MR、30 次提交，重点集中在 登录注册/账号体系

#### Repo: `engineering/secrets/kimi-secret-prod`

- MR：2（merged 2 / opened 0 / closed 0）
- Commit：10
- 主要 MR：
  - [!529 Revert "Merge branch 'feat_cron' into 'main'"](https://dev.msh.team/engineering/secrets/kimi-secret-prod/-/merge_requests/529)（已合并）
  - [!528 Update file overrides.yaml](https://dev.msh.team/engineering/secrets/kimi-secret-prod/-/merge_requests/528)（已合并）
- 贡献总结：本周在 `engineering/secrets/kimi-secret-prod` 主要推进了 2 个 MR、10 次提交，重点集中在 消息收发与渲染

#### Repo: `engineering/devops/kimi-secret`

- MR：0（merged 0 / opened 0 / closed 0）
- Commit：8
- 贡献总结：本周在 `engineering/devops/kimi-secret` 主要推进了 0 个 MR、8 次提交，重点集中在 日常迭代与问题修复

### [张惠施](https://dev.msh.team/zhanghuishi)

- 主要贡献仓库数：**10**
- MR 总数：**22**（已合并 17 / 进行中 3 / 已关闭 2）
- Commit 总数：**371**

#### Repo: `engineering/kimi-darkmatter`

- MR：8（merged 5 / opened 1 / closed 2）
- Commit：109
- 主要 MR：
  - [!1976 feat(apps/kimiapi): run script b64 decode](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/1976)（已合并）
  - [!2057 feat(apps/kimiapi): modify  admin RestartInstanceByBotID](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2057)（已合并）
  - [!2055 feat(apps/kimiapi): impl claw admin svc RestartInstance](https://dev.msh.team/engineering/kimi-darkmatter/-/merge_requests/2055)（已合并）
- 贡献总结：本周在 `engineering/kimi-darkmatter` 主要推进了 8 个 MR、109 次提交，重点集中在 消息收发与渲染、管理后台/配置运营

#### Repo: `zhanghuishi/multi-exec`

- MR：3（merged 3 / opened 0 / closed 0）
- Commit：113
- 主要 MR：
  - [!5 Develop](https://dev.msh.team/zhanghuishi/multi-exec/-/merge_requests/5)（已合并）
  - [!4 Develop](https://dev.msh.team/zhanghuishi/multi-exec/-/merge_requests/4)（已合并）
  - [!3 Develop](https://dev.msh.team/zhanghuishi/multi-exec/-/merge_requests/3)（已合并）
- 贡献总结：本周在 `zhanghuishi/multi-exec` 主要推进了 3 个 MR、113 次提交，重点集中在 客户端/交互体验

#### Repo: `protos/kimi`

- MR：5（merged 5 / opened 0 / closed 0）
- Commit：27
- 主要 MR：
  - [!1225 feat(apps/kimiapi): claw admin add restartInstance](https://dev.msh.team/protos/kimi/-/merge_requests/1225)（已合并）
  - [!1209 Feat claw key](https://dev.msh.team/protos/kimi/-/merge_requests/1209)（已合并）
  - [!1239 Feat admin instance](https://dev.msh.team/protos/kimi/-/merge_requests/1239)（已合并）
- 贡献总结：本周在 `protos/kimi` 主要推进了 5 个 MR、27 次提交，重点集中在 管理后台/配置运营、Agent/工具调用

#### Repo: `zhanghuishi/cdn`

- MR：1（merged 1 / opened 0 / closed 0）
- Commit：86
- 主要 MR：
  - [!1 Add new directory](https://dev.msh.team/zhanghuishi/cdn/-/merge_requests/1)（已合并）
- 贡献总结：本周在 `zhanghuishi/cdn` 主要推进了 1 个 MR、86 次提交，重点集中在 CDN 管理

#### Repo: `agentic/kimiclaw-image`

- MR：2（merged 2 / opened 0 / closed 0）
- Commit：0
- 主要 MR：
  - [!2 feat: set heartbeat every 60m](https://dev.msh.team/agentic/kimiclaw-image/-/merge_requests/2)（已合并）
  - [!1 Feat bootstrap](https://dev.msh.team/agentic/kimiclaw-image/-/merge_requests/1)（已合并）
- 贡献总结：本周在 `agentic/kimiclaw-image` 主要推进了 2 个 MR、0 次提交，重点集中在 Agent/工具调用

#### Repo: `engineering/devops/kimi-secret`

- MR：2（merged 0 / opened 2 / closed 0）
- Commit：17
- 主要 MR：
  - [!448 Feat/tencent cloud](https://dev.msh.team/engineering/devops/kimi-secret/-/merge_requests/448)（进行中）
  - [!455 feat(apps/kimiapi): claw image](https://dev.msh.team/engineering/devops/kimi-secret/-/merge_requests/455)（进行中）
- 贡献总结：本周在 `engineering/devops/kimi-secret` 主要推进了 2 个 MR、17 次提交，重点集中在 数据与监控、Agent/工具调用

#### Repo: `zhanghuishi/openclaw-gwcheck`

- MR：1（merged 1 / opened 0 / closed 0）
- Commit：6
- 主要 MR：
  - [!1 feat: add all](https://dev.msh.team/zhanghuishi/openclaw-gwcheck/-/merge_requests/1)（已合并）
- 贡献总结：本周在 `zhanghuishi/openclaw-gwcheck` 主要推进了 1 个 MR、6 次提交，重点集中在 Agent/工具调用

#### Repo: `engineering/secrets/kimi-secret-prod`

- MR：0（merged 0 / opened 0 / closed 0）
- Commit：6
- 贡献总结：本周在 `engineering/secrets/kimi-secret-prod` 主要推进了 0 个 MR、6 次提交，重点集中在 日常迭代与问题修复

#### Repo: `zhanghuishi/bot-cli`

- MR：0（merged 0 / opened 0 / closed 0）
- Commit：5
- 贡献总结：本周在 `zhanghuishi/bot-cli` 主要推进了 0 个 MR、5 次提交，重点集中在 日常迭代与问题修复

#### Repo: `zhanghuishi/bot`

- MR：0（merged 0 / opened 0 / closed 0）
- Commit：2
- 贡献总结：本周在 `zhanghuishi/bot` 主要推进了 0 个 MR、2 次提交，重点集中在 日常迭代与问题修复

## 三、团队整体产出统计

- 总 MR：**154**
- 总 Commit：**4331**
- 活跃仓库数：**16**
- 活跃成员数：**5**

### 统计摘要

| 指标 | 数值 |
|---|---:|
| 提交数 | 4331 |
| MR 状态分布（Merged/Opened/Closed） | 122/23/9 |
| 每日最高活动 | 2026-03-05 |
| 最高产出仓库 | engineering/kimi-darkmatter |

_报告生成时间：2026-03-19 22:25:04_
