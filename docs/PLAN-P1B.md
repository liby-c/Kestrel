# P1 改动方案（第二批）：方向深度清单

**状态**：已完成（2026-10-30）
**日期**：2026-10-30
**依据**：`demo-app.cn` 交战日志（2026-10-29）

## 0. 要解决的问题

- 日志里测了几个接口就写 `sqli: negative`；覆盖矩阵是"类"级，没有"这个类还有多少接口/参数/编码没测"的分母。
- AES 加密登录请求直到用户第 4 次推动后才补测；上传只测了少数扩展名；Shiro 时间盲测在 Windows 目标上用 `sleep`；这些都不是"挖穿"，是"试了一下"。
- `negative` 没有边界：没有清单，就无法证明"确实没东西"。

P1 第二批：把"挖穿"变成**每个方向的有限清单**。清单项全部有状态，才允许标 `negative` 或结束。

---

## 1. 设计

### 1.1 定义

方向 = 攻击面 × 漏洞类 × 手法。每个方向必须挂一张有限清单；清单来自专项技能，`pentest-flow` 负责门禁。

### 1.2 `plan.md` 的 `## 深度清单`

```markdown
## 深度清单

| 方向 | 清单项 | 状态 | 证据/说明 |
|---|---|---|---|
| 认证 | A1 登录编码 | done | evidence/src/login_enc.txt |
| 认证 | A2 用户名枚举 | done | 不存在/错误/锁定统一 |
| 上传 | U2 扩展名 | done | 白名单 png/txt |
| SQLi | S1 参数清单 | todo | 还有 12 个参数未测 |
```

状态：`todo / doing / done / n/a / blocked`。

- `done`：有证据或明确结论。
- `n/a`：不适用，必须写原因。
- `blocked`：必须写「已尝试」。
- `todo` / `doing`：**不得**把该方向标 `negative`，**不得**结束。

### 1.3 方向与清单来源

| 方向 | 清单 |
|---|---|
| 认证/会话 | `web-pentest` §7.1 |
| 文件上传 | `web-pentest` §7.2 |
| SQLi | `web-pentest` §7.3 |
| XSS / SSRF / XXE / SSTI | `web-pentest` §7.4–7.6 |
| 越权 / 业务逻辑 / 竞态 | `web-pentest` §7.7–7.8 |
| 信息泄露 / 默认口令 | `web-pentest` §7.9 |
| 反序列化 / RCE | `exploitation` §9 |
| 接口面（方法/参数/认证态） | `vuln-discovery` §5 |

### 1.4 门禁

- 一个方向标 `negative` 前：该方向清单所有适用项为 `done` 或 `n/a`；`blocked` 项有已尝试列表。
- 结束检查：`## 深度清单` 无 `todo` / `doing`；每个 `negative` 方向的清单无 `todo`。
- 没有清单的方向不得标 `negative`。
- 清单不替代攻击面账本：账本记"测了什么"，清单记"该类还差什么"。

---

## 2. 清单正文（插入各技能）

### 2.1 `web-pentest` §7

```markdown
## 7. 方向深度清单（挖穿标准）

一个方向标 `negative` 前，本节对应清单的所有适用项必须是 `done` 或 `n/a`；`blocked` 项必须写已尝试。清单项与 `plan.md` 的 `## 深度清单` 一一对应。

### 7.1 认证 / 会话

| # | 测试项 | 完成判据 |
|---|---|---|
| A1 | 每个登录入口 × 编码（明文 / form / json / AES / 其他前端加密） | 每种编码至少一次；能区分“格式错”和“凭据错” |
| A2 | 用户名枚举 | 不存在 / 密码错 / 锁定 三种响应；统一则记录 |
| A3 | 默认口令 | 产品默认 + 常见 20 组，锁定预算内 |
| A4 | 弱口令 | top100 小字典；记录尝试次数与锁定影响 |
| A5 | 验证码 | 无 / 固定 / 可重放 / 客户端校验 / 可爆破（限速） |
| A6 | 注册 / 找回 / 短信 | 每个入口 × 缺失 / 重放 / 枚举 / 越权 |
| A7 | 会话 | Cookie 属性、JWT alg/key、注销 / 固定 / 并发 |
| A8 | 认证绕过 | header / cookie / 路径 / 大小写 / 编码 / 双写 / 分号 |
| A9 | 锁定策略 | 触发一次并记录影响；不无限爆破 |

### 7.2 文件上传

| # | 测试项 | 完成判据 |
|---|---|---|
| U1 | 端点清单 | 每个上传端点一行 |
| U2 | 扩展名 | 白名单 / 黑名单 / 大小写 / 双扩展 / 尾随点 / 分号 / NULL |
| U3 | MIME / Content-Type | 允许 / 伪造 / 缺失 |
| U4 | magic bytes | 图片头 + 脚本尾 |
| U5 | 文件名 | 路径穿越 / 绝对路径 / 覆盖已有文件 / 超长 / 特殊字符 |
| U6 | 内容 | 脚本 / HTML / SVG / zip / 序列化 |
| U7 | 落点与可执行性 | 返回路径、目录、是否可访问、是否可解析 |
| U8 | 覆盖与清理 | 覆盖业务文件 = L4 ⛔，不测（P1C 细化，见 docs/PLAN-P1C.md）；测试文件记录并清理 |

### 7.3 SQLi

| # | 测试项 | 完成判据 |
|---|---|---|
| S1 | 参数清单 | 每个参数 × GET / POST / JSON / form |
| S2 | 检测手法 | 报错 / 布尔 / 时间 / union，至少 3 种 |
| S3 | 认证态 | 未授权 / 低权 / 高权 |
| S4 | 工具 | 有 sqlmap 就跑；没有则记录原因 |
| S5 | 写文件 / 命令 | 仅授权时尝试；否则标 blocked |

### 7.4 XSS

| # | 测试项 | 完成判据 |
|---|---|---|
| X1 | 输入点清单 | 每个反射/存储/DOM 输入点 |
| X2 | 上下文 | HTML / 属性 / JS / URL / CSS |
| X3 | 证据 | 浏览器执行截图或 DOM 证据 |
| X4 | 防护 | CSP / HttpOnly / 编码绕过 |

### 7.5 SSRF

| # | 测试项 | 完成判据 |
|---|---|---|
| R1 | URL 参数清单 | 每个接受 URL/域名/IP 的参数 |
| R2 | 目标 | 内网 / 云元数据 / 本机 / 文件协议 |
| R3 | 证据 | 回连或响应差异；盲 SSRF 用 OOB |
| R4 | 绕过 | 跳转 / DNS rebinding / 编码 / 短地址 |

### 7.6 XXE / SSTI

| # | 测试项 | 完成判据 |
|---|---|---|
| T1 | XML 入口 | 每个解析 XML 的接口 × 外部实体 / 参数实体 / 盲 XXE |
| T2 | 模板入口 | 每个模板参数 × 引擎指纹 / 表达式 / 时间 |
| T3 | 证据 | 回连 / 回显 / 时间差 |

### 7.7 越权 / IDOR

| # | 测试项 | 完成判据 |
|---|---|---|
| I1 | 对象 ID | 每个 ID 参数 × 双身份 |
| I2 | 方向 | 水平 / 垂直 / 跨租户 |
| I3 | 方法 | GET / POST / PUT / DELETE |

### 7.8 业务逻辑 / 竞态

| # | 测试项 | 完成判据 |
|---|---|---|
| B1 | 状态变更接口 | 每个接口 × 跳过步骤 / 重放 / 负值 / 边界 |
| B2 | 竞态 | 并发请求；记录窗口与结果 |
| B3 | 支付 / 额度 | 仅授权时测；否则标 blocked |

### 7.9 信息泄露 / 默认口令

| # | 测试项 | 完成判据 |
|---|---|---|
| D1 | 文档 / 源码 | Swagger / Actuator / 源码包 / 备份 |
| D2 | 配置 / 日志 | 配置键枚举、错误页、日志 |
| D3 | 默认口令 | 产品默认 + 常见组合 |
```

### 2.2 `exploitation` §9

```markdown
## 9. 方向深度清单（反序列化 / RCE）

一个入口标 `negative` 前，下表适用项必须 `done` 或 `n/a`；`blocked` 必须写已尝试。

| # | 测试项 | 完成判据 |
|---|---|---|
| E1 | 入口清单 | cookie / header / body / 参数 / 协议，逐个 |
| E2 | 组件与链 | 每个组件 × 每条可用链 |
| E3 | 平台 | OS 确认；Windows / Linux 命令区分 |
| E4 | 回连 | OOB DNS/HTTP 优先；无回连用时间盲 |
| E5 | 投递 | 生成即投递；原始响应落盘 |
| E6 | 判定 | 回显 / 回连 / 时间差；negative 必须平台兼容 |
```

### 2.3 `vuln-discovery` §5

```markdown
## 5. 方向深度清单（接口面）

| # | 测试项 | 完成判据 |
|---|---|---|
| V1 | 资产/端口/服务 | 每个开放服务至少一行账本 |
| V2 | 接口 × 方法 | GET / POST / PUT / DELETE / OPTIONS |
| V3 | 参数 | 缺失 / 空 / 类型 / 边界 / 注入字符 |
| V4 | 认证态 | 未授权 / 低权 / 高权 |
| V5 | 响应差异 | 状态码 / 长度 / 时间 / 错误 |
| V6 | 文档 / 源码 | Swagger / Actuator / source / backup |
| V7 | 工具 | nuclei / sqlmap / ffuf 等调用记录 |
```

---

## 3. 每文件改动

### 3.1 `skills/pentest-flow/SKILL.md`

- 「产物」目录树 `plan.md` 注释加「深度清单」；正文加一句「账本记测了什么，深度清单记该类还差什么」。
- 在「技能加载门禁」之后、「挖掘循环」之前新增 `## 方向深度清单`：1.2 模板、1.3 方向/清单来源、1.4 门禁。
- 「挖掘循环」第 3 步改为「判断挖穿：该方向清单适用项全部 `done` / `n/a`，证据够」。
- 「结束检查」追加：`## 深度清单` 无 `todo` / `doing`；每个 `negative` 方向清单无 `todo`；`blocked` 项有已尝试。
- 「记录」：`plan.md` 必含项加「深度清单」。

### 3.2 `skills/web-pentest/SKILL.md`

- 在「## 6. 输出」之后新增 `## 7. 方向深度清单（挖穿标准）`，内容为 2.1 的矩阵。
- 在「## 6. 输出」里加一句「输出前先核对 §7 清单」。

### 3.3 `skills/exploitation/SKILL.md`

- 在「## 8. PoC 脚本要求」之后新增 `## 9. 方向深度清单（反序列化 / RCE）`，内容为 2.2。

### 3.4 `skills/vuln-discovery/SKILL.md`

- 在「### 4. 输出」之后新增 `## 5. 方向深度清单（接口面）`，内容为 2.3。

### 3.5 `docs/DESIGN.md`

- 头部 **2.5 → 2.6**；状态改「P0 已落地，P1-1/P1-2/P1-3 已落地」；最后更新 2026-10-30。
- §6 主技能规范新增第 15 条：方向深度清单门禁。
- §7 `plan.md` 职责加「深度清单」。
- §10 在「技能加载门禁」之后新增 `### 方向深度清单`（1.2/1.3/1.4）；结束检查追加清单门禁。
- §12 验收新增第 24、25 条。
- §14 变更记录加 `2026-10-30 | 2.6 | P1-3：方向深度清单（认证/上传/SQLi/反序列化/接口面）；negative 前清单适用项必须 done/n/a`。

### 3.6 `AGENTS.md`

- 新增硬约束 27：方向深度清单门禁。
- 「当前阶段」新增 `- [ ] P1-3：方向深度清单（docs/PLAN-P1B.md）`，完成后勾选。

---

## 4. 验收

```bash
# 1. 清单存在且状态集合一致
grep -nE "深度清单" skills/pentest-flow/SKILL.md skills/web-pentest/SKILL.md skills/exploitation/SKILL.md skills/vuln-discovery/SKILL.md docs/DESIGN.md AGENTS.md
grep -nE "todo|doing|done|n/a|blocked" skills/pentest-flow/SKILL.md

# 2. 四张核心矩阵
grep -nE "A1|A2|U1|U2|S1|S2|T1|T2|E1|E2|V1|V2" skills/web-pentest/SKILL.md skills/exploitation/SKILL.md skills/vuln-discovery/SKILL.md

# 3. negative 门禁
grep -nE "不得.*negative|negative.*不得|清单.*done|todo.*不得" skills/pentest-flow/SKILL.md docs/DESIGN.md AGENTS.md

# 4. 旧塔引用：SKILL/RISK 必须为空
grep -rnE "roe-load|state\.sh|workdir\.sh|broker|\blease\b" skills/pentest-flow/SKILL.md skills/web-pentest/SKILL.md skills/exploitation/SKILL.md skills/vuln-discovery/SKILL.md docs/RISK.md
```

### 4.1 验收结果（2026-10-30）

- 工作流 `p1b-depth-checklists`：7 个代理、`ok=true`、`issues=[]`。
- `web-pentest` §7.1–7.9 共 42 项；`exploitation` §9 E1–E6；`vuln-discovery` §5 V1–V7；`pentest-flow` 模板/来源/门禁；DESIGN 2.6、§12 第 24/25 条、§14 v2.6；AGENTS #27 与 P1-3 勾选。
- 冲突修正：XXE/SSTI 的清单项由 `E1–E3` 改为 `T1–T3`，避免与反序列化 `E1–E6` 混淆。
- 收尾：PLAN-P1B 状态改为已完成；AGENTS P1-3 勾选；`pentest-flow` 结束检查项格式修正。

---

## 5. P1 剩余 backlog

1. 用户说「继续」时的固定动作（账本驱动 next-3）。
2. 不可逆写入 ⚠️/L4 细化（覆盖已有文件/证书/密钥）。
3. `/tmp` 零写入 + 可选 lint。

---

## 6. 完成标准

- 四个技能 + DESIGN/AGENTS 改完，验收 grep 通过；
- 四张核心矩阵（认证/上传/SQLi/反序列化/接口面）存在且状态集合一致；
- `negative` 前清单适用项必须 `done`/`n/a` 的门禁在三处一致；
- 没有引入 broker/lease/state/roe-load/report 模块。