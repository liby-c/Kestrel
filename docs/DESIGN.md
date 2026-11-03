# Kestrel 设计

**版本**：3.8（skill-first，无塔）
**状态**：设计定稿，P0 已落地，P1-1…P1-5、P2-A 已落地，L\* 3.0 授权分级、工具获取与镜像、发现播报、资产基线、消息格式已落地
**最后更新**：2026-11-04

## 0. 一句话

通用 agent + 24 个按需加载的技能 + Kali 工具；产物只写 `<cwd>/Work/OC-<target>/`。

## 1. 不可忘记的决策

| # | 决策 |
|---|---|
| 1 | 没有 `/opt/Kestrel`、没有固定塔根、没有 broker/state/lease/roe-load/审计链/报告模块 |
| 2 | 技能唯一运行时目录是 `~/.config/opencode/skills/`；本仓库只是源码，安装后可删 |
| 3 | 24 个技能全部保留，全部按需加载；启动只暴露 name/description，不加载正文 |
| 4 | 主技能 `pentest-flow` 的路由表是静态的，不随运行时状态变化 |
| 5 | 产物只在 `<cwd>/Work/OC-<target>/`；技能目录绝不放 RoE/state/evidence/findings |
| 6 | 同一目标复用目录；新目标由 agent 问四件事后自己写 `roe.yaml` |
| 7 | 默认风险上限 L3；L1/L2 直接做；L3 内 ✅ 直接做、⚠️ 逐次授权；L4-⚠️ 逐次授权后执行；L4-⛔ 默认禁止，明确授权后停下、回复确认才执行 |
| 8 | 默认口令、弱口令（≤top100）、目录爆破、WAF 绕过允许；大字典爆破、密码喷洒、账户锁定测试按 L3-⚠️ 逐次授权；下载、上传无害写、不中断服务、用户级持久化、同目标横移、数据导出允许 |
| 9 | 挖洞循环是策略循环；连续 3 轮复盘无新方向 + 结束检查全过才结束 |
| 10 | 没有原始证据不得标 confirmed；XSS/SSRF/RCE 必须有对应证据 |

## 2. 架构

```text
OpenCode 通用 agent
  ├─ 启动：扫描 24 个技能的 name + description
  ├─ 交战：加载 pentest-flow
  ├─ 按需：1 个主技能 + 1 个专项
  ├─ 执行：直接调用 Kali 工具
  └─ 落盘：<cwd>/Work/OC-<target>/
```

没有常驻进程、没有数据库、没有网关。

## 3. 目录

### 3.1 仓库（源码）

```text
Kestrel/
  README.md
  AGENTS.md
  docs/
    DESIGN.md
    RISK.md
  skills/
    pentest-flow/SKILL.md
    recon/SKILL.md
    ...
```

### 3.2 运行时（安装后）

```text
~/.config/opencode/skills/
  pentest-flow/SKILL.md
  ...
```

仓库不是运行时依赖。安装 = 复制 `skills/*` 到运行时目录，之后仓库可以删除。

### 3.3 交战产物

```text
<cwd>/Work/OC-<target>/
  roe.yaml
  plan.md
  approvals.md
  notes.md
  findings.md
  evidence/
```

`OC` = OpenCode 客户端标识。换客户端用对应前缀（如 `ZC-`）。
`<target>` 用主机名/IP，去掉 scheme、端口、路径。

## 4. 24 技能矩阵

| # | 技能 | 用途 | 触发条件 | 层级 |
|---|---|---|---|---|
| 1 | `pentest-flow` | 主流程、路由、产物约定、循环 | 任何交战/扫描/漏洞挖掘 | L0 |
| 2 | `recon` | 端口、子域、目录、指纹 | 需要主动侦察 | L1 |
| 3 | `osint-recon` | 公开信息、资产测绘 | 只有域名/公司名 | L1 |
| 4 | `rapid-checklist` | 快速覆盖清单 | 时间紧、怕漏项 | L1 |
| 5 | `web-pentest` | Web 常规漏洞 | 发现 HTTP 服务 | L2 |
| 6 | `web-security-advanced` | Web 高级漏洞/绕过 | 常规测试无果 | L2 |
| 7 | `vuln-discovery` | 漏洞发现方法论 | 不知道从哪下手 | L2 |
| 8 | `waf-bypass` | WAF/过滤绕过 | 请求被拦、payload 被过滤 | L3 |
| 9 | `intranet-pentest-advanced` | 内网、域、横向 | 进入内网或发现域 | L2 |
| 10 | `exploitation` | 利用开发、gadget 选链、payload 投递 | 要打 RCE/反序列化/上传 getshell | L2 |
| 11 | `post-exploitation` | 提权、持久化、横移、导出 | 已获得 shell/权限 | L3 |
| 12 | `redteam-playbooks` | 完整红队剧本 | 多阶段演练 | L3 |
| 13 | `cve-triage` | 版本匹配 CVE | 拿到组件/版本号 | L3 |
| 14 | `pentest-tools` | Kali 工具参数参考 | 不确定工具用法 | L3 |
| 15 | `ctf-web` | CTF Web | CTF 题目 | L2 |
| 16 | `ctf-crypto` | CTF Crypto | CTF 密码题 | L2 |
| 17 | `ctf-misc` | CTF Misc | CTF 杂项 | L2 |
| 18 | `android-pentest` | Android 渗透 | APK、Android 设备 | L2 |
| 19 | `client-reverse` | 客户端逆向 | APK/EXE/JS 逆向 | L2 |
| 20 | `crypto-toolkit` | 加解密、编码、证书 | 需要处理密文/编码 | L3 |
| 21 | `ai-mcp-security` | AI/MCP/Agent 安全 | 目标含 LLM、MCP、Agent | L2 |
| 22 | `hackerone` | 漏洞赏金流程 | HackerOne/平台提交 | L3 |
| 23 | `reporting` | 报告格式 | 用户明确要求生成报告 | L3 |
| 24 | `secknowledge-skill` | 方法论/经验检索 | 需要参考案例或流程 | L3 |

`reporting` 默认不加载。产物 `findings.md` 不依赖它。

## 5. 按需加载

1. 启动只暴露 `name` + `description`，不加载正文。
2. 任何交战先加载 `pentest-flow`。
3. 根据目标类型加载 1 个主技能，例如 Web → `web-pentest`。
4. 遇到具体问题时再加载 1 个专项，例如被 WAF 拦 → `waf-bypass`。
5. 建议同时不超过 3 个技能正文；复杂任务可临时多加载。
6. 阶段切换后不再引用旧技能，上下文自然淘汰。
7. `references/`、`data/` 只在需要时读取。
8. 两条触发路径：主技能静态路由表 + 子技能 description 直接匹配。
9. 强制加载：侦察前 `recon`；发现 Web 后 `web-pentest`；拿到版本后 `cve-triage`；**打任何命令执行类 payload（RCE/反序列化/gadget/SSTI/表达式注入/上传 getshell/命令注入）前加载 `exploitation`**。每次加载在 `plan.md` 记一行「加载 `<skill>`：原因」，并写入 `## 技能加载` 表（技能/时间/触发阶段/原因）；缺行不得进入对应阶段；发 payload 前先看表，缺就先加载，不要打完补记。
10. **执行纪律**：不许闷头连续执行；连续 15 次工具调用无面向用户的文字必须播报；确认 finding 时改用「结论 + 端点/入口 + payload/命令 + 原始响应 + 证据路径」，先落盘再播报；消息必须换行分段，字段一行一个，不要用「；」串成一段；用空行或 `-` 列表分段，不能只靠单个换行；先完成资产基线再投递利用 payload；工具结果需复核；现成工具优先，同一方向自制脚本不超过 3 个；payload 生成成功即投递，本地回读失败不作为阻断理由；有公网回连条件优先用 OOB 打真实目标；先确认目标 OS 再选 payload 平台。

## 6. 主技能规范

`skills/pentest-flow/SKILL.md` 必须包含：

1. 产物目录与禁止写入位置。
2. 新目标初始化流程（问四件事、默认值、自己写 RoE）。
3. 已有目录复用流程（问沿用/修改、追加不删）。
4. L1/L2 直接做；L3 内 ✅ 直接做、⚠️ 逐次授权；L4-⚠️ 授权即执行；L4-⛔ 授权后停下、回复确认才执行；越界拒绝。
5. 24 技能静态路由表 + 强制加载规则（`recon` / `web-pentest` / `cve-triage` / `exploitation`；`plan.md` 技能加载表门禁）。
6. 挖洞循环：方向 → 挖穿 → 换方向 → 复盘 → 3 轮无新方向且账本 `untested` 为 0 → 结束检查。
7. Web 覆盖矩阵：每类必须有状态，缺一类不得结束。
8. 记录格式：每确认一条立即写 `findings.md`；无证据不得标 confirmed。
9. 产物纪律：脚本/源码/token 只放 `evidence/{scripts,src,tokens}`，任务结束不清理。
10. `plan.md` 每轮更新，至少包含攻击面账本、深度清单、下一步 3 个动作（未完成时）、技能加载、交接块（如发生压缩）、不可逆写入判定（如发生）、回连申请记录（如发生）、覆盖清单、复盘、结束检查。
11. 不生成 `report.md`；`findings.md` 是交付。
12. RCE 线上被 `safetyMode`/容器限制禁用时，起隔离复本验证或标 `blocked`，不得直接判 `negative`。
13. 目标提供挑战列表时，`challenges.md` 逐项状态。
14. 临时文件禁止 `/tmp`、`/var/tmp`、`/dev/shm`。
15. 方向深度清单门禁：每个方向挂有限清单；标 `negative` 前适用项必须 `done` / `n/a`；`todo` / `doing` 不得标 `negative`，也不得结束。
16. 不可逆写入判定：上传/写入/导入/配置修改前先做 W1–W6 落点判定；固定路径新建、修改已有配置 = L4-⚠️（备份+回滚+授权）；覆盖业务文件/证书/密钥、同名覆盖 = L4-⛔（授权+确认）；疑似副作用立即停止并当轮披露。
17. 账本驱动 next-3：用户说「继续/接着/挖/下一步/continue/go on」时，读 `plan.md` 的攻击面账本、深度清单、交接块生成候选，按 RCE 潜力排序取前 3，写入 `## 下一步 3 个动作`，只执行第 1 个并立即更新账本/清单；不许从零重扫，不许反问「接下来做什么」。
18. 结束前 lint：运行 `check_artifacts.py Work/OC-<target>`（运行时路径 `~/.config/opencode/skills/pentest-flow/scripts/check_artifacts.py`），必须 PASS；FAIL 逐条修复后重跑；不得跳过。
19. 工具获取：技能里的工具默认按需可用，不要求预装；缺失按 apt → pipx → npm → go → gem → 二进制/JAR 安装，优先中国镜像，校验并记录 `notes.md`。

主技能不复制子技能正文，不写编排契约，不写 broker/lease/approval/roe-load。

## 7. 产物职责

| 文件 | 内容 |
|---|---|
| `roe.yaml` | 目标、范围（`scope.same_ip` / `scope.exclude_assets`）、端口、时间窗、速率、风险上限、交战目标 |
| `plan.md` | 当前方向、攻击面账本、深度清单、下一步 3 个动作、技能加载、交接块（如发生压缩）、不可逆写入判定（如发生）、回连申请记录（如发生）、覆盖清单、复盘、结束检查 |
| `approvals.md` | ⚠️ 操作的时间、操作、目标、用户授权、结果 |
| `notes.md` | 范围变更、环境信息、未归类线索 |
| `findings.md` | 发现列表、请求响应摘要、证据路径、状态 |
| `challenges.md` | 目标提供挑战列表时的逐项状态 |
| `evidence/` | 原始命令输出、HTTP 请求响应 |
| `evidence/scripts/` | agent 写的脚本，任务结束不清理 |
| `evidence/src/` | 下载的源码、临时文件，不清理 |
| `evidence/tokens/` | token、cookie、凭据，不清理 |

没有 `report.md`。

## 8. RoE 生命周期

### 8.1 新目标

目录不存在：

1. `mkdir -p Work/OC-<target>/evidence`
2. 问四件事：交战目标、风险上限、同 IP 是否在范围内（默认 include）、排除资产
3. 默认：`scope.same_ip: include`、`scope.exclude_assets: []`、`allowed_ports: all`、`time_window: "00:00-23:59"`、`max_rate: 1000`、`scan_rate: 3000`、`allowed_risk: [L0, L1, L2, L3]`
4. 自己写 `roe.yaml`
5. 回读一句确认
6. 开始侦察

### 8.2 同一目标

目录已存在：

1. 读 `roe.yaml`
2. 范围语义以 `scope` 为准：`scope.same_ip: include` 时目标解析 IP 上全部端口/服务在范围内；`scope.exclude_assets` 命中才跳过
3. 问一句：沿用还是修改
4. 沿用直接开始；修改则更新 `roe.yaml`，修改 `scope` 时 `notes.md` 记一条
5. 旧 `findings` / `evidence` 不删，追加

### 8.3 模板

```yaml
engagement:
  target: "<target>"
  scope:
    same_ip: include          # include | exclude
    exclude_assets: []        # 明确排除的主机/域名/端口
  allowed_ports: all
  time_window: "00:00-23:59"
  max_rate: 1000
  scan_rate: 3000
  allowed_risk: [L0, L1, L2, L3]
  forbidden:
    - "mkfs"
    - "dd if=/dev/zero of=/dev/"
    - "shutdown"
    - "reboot"
    - "iptables -F"
    - "drop table"
    - "truncate table"
  goal: "RCE"
```

`scope.same_ip: include`：目标解析出的 IP 上全部端口/服务在范围内，直接枚举、指纹、测试，不逐资产询问授权。`scope.same_ip: exclude`：只测 target 域名对应的端口/路径。`scope.exclude_assets` 是唯一排除项，命中即跳过并在 `notes.md` 记一行。同 IP 内服务互相横移不算"横移到 RoE 外新主机"；不同 IP 的新主机仍按 ⚠️ 处理。

兼容：旧 `roe.yaml` 的顶层 `exclude` 视为 `scope.exclude_assets`，读到旧字段按新语义处理，不报错。

没有归档、没有版本化、没有 `roe-load`。

## 9. L\* 与授权

核心分级见 `docs/RISK.md`。摘要：

| 等级 | 范围 | 默认 |
|---|---|---|
| L0 | 被动收集、本地读 | ✅ 直接做 |
| L1 | 端口/目录（被动）/子域/漏洞扫描 | ✅ 直接做 |
| L2 | 只读验证、默认口令、弱口令（≤top100）、SQLi/XSS/IDOR | ✅ 直接做 |
| L3 | 目录爆破、WAF 绕过、写入（新文件/可清理）、上传（测试文件/随机名）、WebShell、用户级持久化、同目标横移、数据导出、用户态提权 | ✅ 直接做（⚠️ 项除外） |
| L3-⚠️ | 大字典爆破、密码喷洒、账户锁定测试、修改账号密码、上传影响服务的配置 | ⚠️ 逐次授权 |
| L4-⚠️ | 内核提权、systemd 服务、系统级后门、内存马、域控操作、修改关键配置、重启单个服务、修改防火墙、清除日志（仅本次交战产生的）、横移到 RoE 外新主机、固定路径新建文件 | ⚠️ 逐次授权 |
| L4-⛔ | 破坏/中断/不可逆（清单见 RISK §12） | ⛔ 默认禁止，授权 + 回复确认后执行 |

写入前判定见 §10 `### 不可逆写入`。固定路径新建、修改已有配置 = L4-⚠️；覆盖业务文件/证书/密钥、同名覆盖 = L4-⛔。

⚠️ 需授权（授权即执行）：大字典爆破、密码喷洒、账户锁定测试、修改目标账号密码、上传影响服务的配置、内核提权、systemd 服务、系统级后门、内存马、横移到 RoE 外新主机、域控操作、修改关键配置、重启单个服务、修改防火墙、清除日志（只删本次交战自己产生的日志）、固定路径新建文件。

⛔ 默认禁止（授权 + 回复确认后执行）：DoS/压力测试、删除业务数据、格式化/磁盘操作、加密勒索、kill -9 业务进程、修改业务数据、rootkit/内核模块、停止服务、重启主机、清空防火墙、覆盖业务文件/证书/密钥、同名覆盖、固定路径覆盖已有文件、删除目标业务文件。

⚠️ 授权流程：

1. 说明操作、目标、风险、回滚。
2. 等用户明确回复「授权」。
3. 记 `approvals.md`。
4. L4-⛔：动作停下，等用户回复确认（如「确认执行」）。
5. 执行。
6. 记录结果。

## 10. 挖洞循环

1. 选方向：攻击面 × 漏洞类 × 手法。
2. 执行、记录。
3. 判断挖穿：该测的类都测了、证据够。
4. 换方向。
5. 复盘遗漏：入口、参数、版本、漏洞类、`negative`、blocked。
6. 一轮 = 对攻击面账本的一次完整推进；有新方向继续；连续 3 轮无新方向且 `untested` 为 0，进入结束检查。
7. 结束检查全过才结束；否则回补。

### 攻击面账本

`plan.md` 的核心是一张账本，逐行记录资产 × 端口 × 服务 × 接口/参数 × 方法 × 类别 × 状态 × 证据 × 下一步：

```markdown
## 攻击面账本

| # | 资产 | 端口 | 服务 | 接口/参数 | 方法 | 类别 | 状态 | 证据 | 下一步 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | <target> | 80 | demo-app | /manage/Login | POST | auth_bypass | untested | - | 加密体复测 |
| 2 | <target> | 28080 | demo-api | /upload/uploadCert | POST | file_upload | confirmed | evidence/src/... | 无 |
```

状态只允许：`untested / testing / confirmed / candidate / negative / blocked / n/a`。

- `untested`：未测；必须有「下一步」。
- `testing`：进行中。
- `confirmed`：已确认；必须有证据路径。
- `candidate`：疑似；必须有线索/证据。
- `negative`：已排除；必须有证据。
- `blocked`：被阻断；必须有「已尝试」列表。
- `n/a`：不适用；写原因。

规则：

- 发现一个资产/端口/服务，至少一行；发现一个接口（或一组同构接口），至少一行。
- 每次测试后更新状态与证据，不攒到最后。
- 覆盖矩阵保留为汇总，但**以账本为准**。
- 一轮 = 对账本的一次完整推进；连续 **3 轮**无新方向 **且** `untested` 为 0，才进入结束检查。

### 上下文交接

默认上下文窗口 **1M**。230k tokens（约 23%）**不是满窗，不是接近上限**，不得据此交接或收尾；这是极少见的低用量情形。

触发交接的条件（满足其一）：

- harness 明确提示上下文压缩/接近上限；
- agent 判断快满，**且能给出实际用量**（超过当前窗口的 **70%**，默认 1M 时约 **700k**）。

给不出实际用量 → 不得以「上下文有限/接近上限」为由交接或收尾，继续做。

交接动作（不是结束）：

1. 先更新攻击面账本；
2. 在 `plan.md` 写 `## 交接块`；
3. 压缩/重开上下文；
4. 重读 `plan.md` + 交接块，重新加载 `pentest-flow` 与当前阶段技能；
5. 从「下一步 3 个动作」继续。

交接块模板：

```markdown
## 交接块

- 时间：
- 当前方向：
- 已完成（账本行号 + 证据路径）：
- 未测清单（账本行号）：
- 下一步 3 个动作：
  1.
  2.
  3.
- 需要重新加载的技能：
```

硬禁令：

- 不得以「上下文有限/接近上限/需要收尾」为理由结束，除非账本 `untested` 为 0 且结束检查全过。
- 说「接近上限」必须给出实际用量/窗口；给不出数字就继续。
- 交接块不替代账本；账本仍是结束检查依据。

### 技能加载门禁

`plan.md` 必须有 `## 技能加载` 表：

```markdown
## 技能加载

| 技能 | 时间 | 触发阶段 | 原因 |
|---|---|---|---|
| pentest-flow | 18:27 | 交战开始 | 主流程 |
| recon | 18:28 | 主动侦察前 | 强制 |
| web-pentest | 18:40 | 首个 HTTP 服务确认后 | 强制 |
| cve-triage | 19:10 | 拿到首个组件/版本后 | 强制 |
| exploitation | 19:20 | 打 RCE/gadget 前 | 强制 |
```

门禁表：

| 阶段 | 必须已加载 | 缺行时 |
|---|---|---|
| 交战开始 | `pentest-flow` | 先加载，补行 |
| 主动侦察前 | `recon` | 先加载，补行 |
| 首个 HTTP/Web 服务确认后、Web 漏洞测试前 | `web-pentest` | 先加载，补行 |
| 拿到首个组件/版本后、CVE 匹配/利用前 | `cve-triage` | 先加载，补行 |
| 打命令执行类 payload（RCE/反序列化/gadget/SSTI/表达式注入/上传 getshell/命令注入）前 | `exploitation` | 先加载，补行 |

- 每次加载后立即在表里追加一行；不攒到最后。
- 适用性：没发现 HTTP → `web-pentest` 不适用；没拿到版本 → `cve-triage` 不适用；没打命令执行类 payload → `exploitation` 不适用。**适用但缺行 = 失败。**
- 结束检查：表里必须有所需行；缺行不得结束。

### 资产基线门禁

进入 `exploitation` 或投递任何利用 payload 前，`plan.md` 必须已有资产基线：

1. TCP `-p-` 完成，原始输出在 `evidence/src/`。
2. UDP top100 按需；做则记录，不做写 `n/a` + 原因，不阻塞结束。
3. 每个开放端口一行：服务/版本/HTTP title/技术栈/证据；未知写 `unknown`。
4. 每个 HTTP/HTTPS 端口有响应头 + title；TLS 端口有证书 subject/issuer/SAN。
5. 账本覆盖所有开放端口；`filtered` 单独一行。

基线未完成时可以并行做被动探测/版本识别，但**不得投递利用 payload**。某路径 `blocked` 时，从基线表挑下一个未测服务继续，不从零重扫、不因单点阻塞结束。

扫描默认：全端口 `-T3 --max-rate 3000`（RoE `scan_rate`），服务识别 `--max-rate 1000`（RoE `max_rate`）；敏感/WAF/云目标降到 100-300；扫描前后用已知端口检测封禁，出现超时/拒绝立即停扫、降速、等待并记录，不连续重扫。

工具输出默认是线索：单一工具结果最多 `candidate`，`confirmed` 需要原始响应 + 第二种独立信号或可复现回显。nmap `-sV` 的服务名是猜测，必须用 HTTP/TLS/应用版本复核。

### 方向深度清单

方向 = 攻击面 × 漏洞类 × 手法。每个方向必须挂一张有限清单；清单来自专项技能，`pentest-flow` 负责门禁。

`plan.md` 必须有 `## 深度清单` 表：

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

方向与清单来源：

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

门禁：

- 一个方向标 `negative` 前：该方向清单所有适用项为 `done` 或 `n/a`；`blocked` 项有已尝试列表。
- 结束检查：`## 深度清单` 无 `todo` / `doing`；每个 `negative` 方向的清单无 `todo`。
- 没有清单的方向不得标 `negative`。
- 清单不替代攻击面账本：账本记「测了什么」，清单记「该类还差什么」。

### 不可逆写入

任何上传、写入、导入、配置修改、数据库写之前，先做写入前判定（W1–W6）：

| # | 判定项 | 判据 |
|---|---|---|
| W1 | 端点行为 | 从源码/文档/响应确认写到哪里、文件名/目录是否可控 |
| W2 | 落点 | 新文件 / 随机名 / 测试目录 vs 固定路径 / 已有文件 |
| W3 | 覆盖风险 | 同名覆盖、业务文件、证书、密钥、配置 |
| W4 | 可清理 | 有删除接口 / 可回滚 / 有备份 |
| W5 | 探测方式 | GET/HEAD/OPTIONS、无文件/空体、唯一临时名；**不向固定路径写内容** |
| W6 | 授权 | 新文件 = L3 ✅（随机名/测试目录）或 L4-⚠️（固定路径新建）；修改已有配置 = L4-⚠️（备份+回滚）；覆盖业务文件/证书/密钥、同名覆盖、未知 = L4-⛔ |

判定结果：

- **新文件 + 随机名 + 测试目录 + 可清理** → L3 ✅，直接做，记账本。
- **固定路径新建 + 可清理** → L4-⚠️，需授权，记录路径并清理。
- **修改已有配置（先备份、可回滚）** → L4-⚠️，需授权，记录 diff 与回滚命令。
- **固定路径覆盖已有文件 / 同名覆盖 / 业务文件 / 证书 / 密钥** → L4-⛔，默认禁止；用户明确授权后停下、回复确认才执行。
- **未知** → 按 L4-⛔ 处理，只做非破坏探测；确认安全后再降级。
- **数据库**：新增可清理的测试记录 = L3；更新/删除已有记录 = L4-⛔。

疑似副作用处置：

1. **立即停止**该端点，不再重试；
2. **当轮**向用户披露（不等最终报告）；
3. 记录时间、请求、响应、影响、回滚方式（`notes.md` / `findings.md` / `plan.md`）；
4. **不擅自恢复、不重试、不删除**；等用户指令；
5. 账本状态标 `blocked`，备注 `incident`。

### 账本驱动 next-3

触发词：`继续` / `接着` / `挖` / `下一步` / `continue` / `go on`。

固定动作：

1. 读 `plan.md`：`## 攻击面账本`、`## 深度清单`、`## 交接块`（如有）。
2. 生成候选：
   - 账本 `untested` 行；
   - 清单 `todo` / `doing` 项；
   - `blocked` 但还有未尝试绕过的项。
3. 排序（高→低）：
   - RCE / 反序列化 / gadget；
   - 认证绕过 / 上传 getshell；
   - SQLi / SSRF / XXE / SSTI；
   - 越权 / 业务逻辑；
   - 信息泄露 / 默认口令。
4. 取前 3，写入 `plan.md` 的 `## 下一步 3 个动作`。
5. **只执行第 1 个**；完成后立即更新账本/清单，三行播报。
6. 第 1 个产生新方向 → 插到队首；没有候选 → 报告 `done` + `blocked` 清单。

规则：

- 不许从零重扫；不许反问「接下来做什么」。
- 每次「继续」至少推进 1 个候选；没有推进就说明卡点。
- 候选全是 `blocked` 时，才对 top 1 请求授权；不得把「需要授权」当默认下一步。

```markdown
## 下一步 3 个动作
1. <账本行号/清单项> — <动作>
2. ...
3. ...
```

### 结束前 lint

结束检查前运行：

```bash
python3 ~/.config/opencode/skills/pentest-flow/scripts/check_artifacts.py Work/OC-<target>
```

必须 PASS；FAIL 逐条修复后重跑；不得跳过。

脚本 `skills/pentest-flow/scripts/check_artifacts.py` 无第三方依赖，退出码：`0` = PASS，`1` = FAIL。检查项：

1. `roe.yaml`、`plan.md`、`findings.md` 存在。
2. `plan.md` 必含：`## 攻击面账本`、`## 技能加载`、`## 深度清单`、`## 覆盖清单`、`## 复盘`、`## 结束检查`。
3. 攻击面账本：无 `untested` 行；`untested` 行必须有「下一步」；`confirmed` / `negative` / `candidate` 必须有证据；`blocked` 必须有「已尝试」。
4. 深度清单：无 `todo` / `doing`；`blocked` 必须有「已尝试」。
5. 技能加载表：必须有 `pentest-flow` / `recon`；出现 HTTP 则必须有 `web-pentest`；账本含 `cve` 则必须有 `cve-triage`；含 `deserialization` / `rce` 则必须有 `exploitation`。
6. `/tmp` lint：`plan.md` / `findings.md` / `notes.md` / `approvals.md` 中出现 `/tmp/`、`/var/tmp/`、`/dev/shm/` 且不是「不写/禁止/没有/清理」等否定句 → FAIL；本地 `/tmp`、`/var/tmp`、`/dev/shm` 中存在比 `roe.yaml` 更新的文件 → WARN（列出，不自动判失败）。
7. 不得存在 `report.md`。
8. `findings.md` 中 `confirmed` 的条目必须含「证据」或 `evidence/`。

### 无公网回连

**判定**：能访问镜像/下载 ≠ 有公网回连；出站下载与入站回连是两件事。需要以下任一时，先检查回连条件：

- 反弹 shell（bash/python/perl/nc 回连）；
- 入站监听（nc -lvnp、msf handler、HTTP 回调）；
- 依赖回连的方向验证（反序列化 OOB、SSRF 回连、XXE OOB 等）。

**决策树**：

```text
需要回连验证？
├─ 反弹 shell / 入站监听
│  ├─ 有公网 VPS / 端口转发 → 直接用
│  └─ 没有 → 向用户提问申请（VPS / 端口转发 / 回调地址）；不得跳过、不得判死
├─ OOB DNS / HTTP（只需出站）
│  ├─ 公共 dnslog / interactsh 可达 → 先用 OOB 打真实目标
│  └─ 不可达 → 向用户申请 OOB 服务；不得跳过、不得判死
└─ 用户提供 → 使用并记录；用户不提供/未回复 → 标 blocked（待回连），写清需要什么
```

**记录**：

- `findings.md` / `plan.md` 记：路径、为什么需要回连、已尝试、需要用户提供什么。
- 账本状态 `blocked`，下一步写「向用户申请回连」。
- 结束检查：凡需要回连的路径，必须有「已申请 / 已提供 / 待回连」记录，**未判 `negative`**。

**禁止**：

- 不得因为本机无公网就把路径标 `negative` / dead。
- 不得跳过需要回连的 RCE / 反序列化 / SSRF / XXE 验证。
- 不得用 `127.0.0.1` 回环冒充真实目标回连。
- 不得「先打再说」：需要入站回连的利用，先问用户再执行。

### 工具获取与镜像

技能里出现的工具默认**按需可用**，不要求预装；本仓库不 vendor 工具。缺失时先 `command -v` 检测，再按顺序安装：

1. 系统包：`apt-get install -y --no-install-recommends <pkg>`
2. Python：`pipx install <pkg>`
3. Node：`npm install -g <pkg>`
4. Go：`go install <module>@latest`
5. Ruby：`gem install <pkg>`
6. Java/JAR 或单文件二进制

中国镜像：

| 类型 | 主源 | 备选 |
|---|---|---|
| Kali apt | 清华 `https://mirrors.tuna.tsinghua.edu.cn/kali/` | 中科大 `https://mirrors.ustc.edu.cn/kali/`、阿里云 `https://mirrors.aliyun.com/kali/` |
| PyPI | 清华 `https://pypi.tuna.tsinghua.edu.cn/simple` | 阿里云、中科大 |
| npm | `https://registry.npmmirror.com` | 腾讯云 npm |
| Go | `https://goproxy.cn,direct` | `https://goproxy.io,direct` |
| RubyGems | `https://gems.ruby-china.com/` | 清华 Ruby 镜像 |
| Maven | `https://maven.aliyun.com/repository/public` | 华为云 |
| Docker | 用户阿里云加速器 | daocloud 等可用镜像 |

GitHub 网页搜索、`raw.githubusercontent.com`、release、API 直连失败/超时：

1. `https://gh-proxy.com/https://github.com/...`
2. `https://ghproxy.net/https://github.com/...`
3. `https://raw.gitmirror.com/...`
4. `https://cdn.jsdelivr.net/gh/<user>/<repo>@<ref>/<path>`（仓库文件）
5. Gitee 镜像 / 用户提供的镜像

代码搜索：`grep.app`、`sourcegraph.com`、`searchcode.com`、Gitee 搜索。

**纪律**：

- **一次直连失败 ≠ 工具/PoC 不存在**；至少试 2 个镜像/源再判断。
- 系统安装到 PATH；单文件二进制/JAR 放 `evidence/src/tools/`；不写技能目录、不写 `/tmp`、`/var/tmp`、`/dev/shm`。
- 校验大小/类型（`file`、`jar tf`、`unzip -t`）；有 SHA256/签名就校验。
- 不运行来源不明的安装脚本；`curl | bash` 先下载审阅或校验。
- 记录工具、版本、来源、镜像、校验结果到 `notes.md`。
- 本地工具安装只影响工作机，不改变对目标操作的 L\*；Windows-only 工具用替代或标 `blocked`。

### Web 覆盖矩阵

Web/HTTP 目标至少覆盖以下类，每类在 `findings.md` 必须有状态：

```text
sqli, xss, csrf, idor, auth_bypass, file_upload, path_traversal,
ssrf, xxe, ssti, deserialization, request_smuggling, race_condition,
info_disclosure, business_logic, default_credential, cve
```

状态：`confirmed / candidate / negative / blocked / not_applicable`。

任何一类没有状态，不得结束。

如果目标提供挑战列表（如 Juice Shop `/api/Challenges`），落盘 `challenges.md`，每项标状态。不得只写“以挑战列表为清单”而没有文件。

### RCE 优先

1. 线上 RCE 被 `safetyMode` / `isDocker` / 容器限制禁用时，不得直接判 `negative`。
2. 有同镜像或本地复本条件：起隔离复本（`127.0.0.1:<verify-port>`），记录 `approvals.md`，在复本上验证，结束删除容器。
3. 没有复本条件：标 `blocked`，写清阻断原因和已尝试的路径。
4. 线上 `negative` 与复本 confirmed 必须分开写。

结束检查：

- 资产基线：TCP 全端口 + 每个开放端口有服务/版本/证据；UDP 按需（`n/a` 有原因）
- 目录/备份/源码
- API/参数/方法
- 认证/越权/默认口令
- 上传/SSRF/RCE/反序列化
- 版本 CVE
- 方向深度清单无 `todo` / `doing`，每个 `negative` 方向清单适用项齐全
- Web 覆盖矩阵每一类都有状态
- `challenges.md` 每项有状态（如果目标有挑战列表）
- `findings.md` 每条 confirmed 有真实证据路径
- `plan.md` 有攻击面账本、技能加载、交接块（如发生压缩）、覆盖清单、复盘、结束检查
- 没有 `report.md`
- `/tmp`、`/var/tmp`、`/dev/shm` 没有任务期间新增文件
- `negative` 有证据
- blocked 已尝试绕过
- 需要回连的路径已「已申请 / 已提供 / 待回连」，未判 `negative`
- GitHub 直连失败时已尝试镜像（至少 2 个）或记录原因
- 写入前判定（W1–W6）已记录；固定路径新建/修改配置已授权并备份；覆盖业务文件/证书/密钥未测，或已授权 + 确认后执行（L4-⛔）
- 无未披露的疑似覆盖/副作用；`incident` 已记录
- `check_artifacts.py` 输出 PASS；FAIL 逐条修复后重跑；不得跳过

结束检查的机械条件（缺一即失败）：

- 攻击面账本 `untested` 行数为 0。
- 每条 `negative` / `candidate` 有证据路径。
- 每条 `blocked` 有「已尝试」列表。
- 每条 `confirmed` 有证据路径。
- 资产基线完成：TCP 全端口 + 每个开放端口有服务/版本/证据；UDP 按需（`n/a` 有原因）。
- `plan.md` 含 `## 攻击面账本`、`## 技能加载`、`## 深度清单`、`## 覆盖清单`、`## 复盘`、`## 结束检查`；未完成时有最新的 `## 下一步 3 个动作`；如发生压缩/不可逆写入/回连申请，含对应记录。
- `## 技能加载` 表适用行齐全（`pentest-flow` / `recon` / `web-pentest` / `cve-triage` / `exploitation`）。
- `## 深度清单` 无 `todo` / `doing`；每个 `negative` 方向清单无 `todo`；`blocked` 清单项有「已尝试」。
- 发生压缩/重开时有 `## 交接块`。
- 未以「上下文有限/接近上限」为由提前结束（默认窗口 1M，230k 不是满窗）。
- `plan.md` / `notes.md` 有写入前判定记录（固定路径新建/修改配置已授权；覆盖业务文件/证书/密钥未测，或已授权 + 确认后执行）。
- L4-⚠️ 操作有 `approvals.md` 记录；L4-⛔ 操作有授权 + 回复确认记录。
- 无未披露的疑似覆盖/副作用；`incident` 已记录。

## 11. 质量规则

1. 没有原始证据不得标 `confirmed`；单一工具输出最多 `candidate`，`confirmed` 需要原始响应 + 第二种独立信号或可复现回显。
2. XSS 必须有浏览器执行证据。
3. SSRF 必须有回连或响应差异证据。
4. RCE 必须有命令回显或回连证据。
5. 证据不足标 `candidate`。
6. 每确认一条 finding，立即写 `findings.md`，不得攒到最后。
7. 目标上创建的文件、账号、计划任务，战后清理并记录；`evidence/` 下的本地脚本、源码、token 不清理。
8. `plan.md` 每轮更新，不得只写开头。
9. 不生成 `report.md`；`findings.md` 是交付。
10. 临时文件禁止 `/tmp`、`/var/tmp`、`/dev/shm`。
11. 写入/上传前先做不可逆判定；固定路径新建、修改已有配置按 L4-⚠️ 授权；覆盖业务文件/证书/密钥按 L4-⛔ 授权 + 确认；疑似副作用当轮披露并记录。
12. 需要公网回连但本机无公网：区分反弹 shell / 入站监听与 OOB。反弹 shell / 入站监听没有公网 VPS / 端口转发时，先向用户申请回连资源/授权；OOB（DNS / HTTP，只需出站）先试公共 dnslog / interactsh 打真实目标，不可达再向用户申请 OOB 服务。不得跳过或判死；不得用 `127.0.0.1` 回环冒充真实目标回连；不得「先打再说/先打再问」，需要入站回连的利用先问用户再执行。
13. GitHub 网页搜索/raw/release/API 直连失败：按镜像顺序回退，至少试 2 个镜像再判断；一次直连失败不等于工具/PoC 不存在。

## 12. 验收

1. 任意目录启动，产物只在 `cwd/Work/OC-<target>/`。
2. 新目标 4 个问题内写 RoE，5 个工具调用内开始侦察。
3. 同目标复用目录，旧产物不丢。
4. 24 个技能逐个可被 `skill` 加载。
5. 同时加载正文不超过 3 个。
6. ⚠️ 操作有 `approvals.md`；L4-⚠️ 逐次授权；L4-⛔ 授权后停下、回复确认再执行。
7. 连续 3 轮无新方向且账本 `untested` 为 0 才结束。
8. 技能目录无运行时产物。
9. 侦察前加载 `recon`；Web 前加载 `web-pentest`；拿到版本后加载 `cve-triage`；打 RCE 前加载 `exploitation`。
10. Web 覆盖矩阵每类都有状态。
11. 脚本/源码/token 只在 `evidence/{scripts,src,tokens}`。
12. `plan.md` 有攻击面账本、深度清单、下一步 3 个动作（未完成时）、技能加载、交接块（如发生压缩）、不可逆写入判定（如发生）、回连申请记录（如发生）、覆盖清单、复盘、结束检查。
13. 目标有挑战列表时 `challenges.md` 每项有状态。
14. 没有 `report.md`；`/tmp`、`/var/tmp`、`/dev/shm` 无任务期间新文件。
15. RCE 线上禁用时，复本验证或 `blocked` 有记录。
16. 每条 `confirmed` 有真实证据路径。
17. 任意连续 15 次工具调用内至少有一次面向用户的播报；confirmed finding 的播报含端点/入口、payload/命令、原始响应和证据路径；播报必须换行分段，字段一行一个；用空行或 `-` 列表分段，不能只靠单个换行。
18. 同一方向自制脚本不超过 3 个；有现成工具时 `findings.md` 有工具调用记录。
19. payload 生成成功后 3 次工具调用内出现投递到目标的记录。
20. `roe.yaml` 有 `scope.same_ip` / `scope.exclude_assets`。
21. `plan.md` 有 `## 攻击面账本`，结束前 `untested` 为 0。
22. `plan.md` 有 `## 技能加载` 表，适用技能在对应阶段前已加载，缺行不得进入阶段。
23. 发生压缩/重开时有 `## 交接块`；未以「上下文有限/接近上限」为由提前结束（默认窗口 1M，230k 不是满窗）。
24. `plan.md` 有 `## 深度清单`；状态集合统一为 `todo / doing / done / n/a / blocked`。
25. 标 `negative` 前该方向清单适用项均为 `done` / `n/a`；结束前 `## 深度清单` 无 `todo` / `doing`，`blocked` 项有「已尝试」。
26. `plan.md` / `notes.md` 有写入前判定记录；无未披露的疑似覆盖；`incident` 已记录。
27. 用户说「继续/接着/挖/下一步/continue/go on」时，`plan.md` 有最新 `## 下一步 3 个动作`；只执行第 1 个并立即更新账本/清单；未从零重扫、未反问。
28. 结束前运行 `check_artifacts.py Work/OC-<target>` 输出 PASS；`/tmp`、`/var/tmp`、`/dev/shm` 零引用。
29. 需要回连的路径有「已申请 / 已提供 / 待回连」记录，未判 `negative` / dead。
30. GitHub 直连失败时至少试 2 个镜像，或有记录说明。
31. 资产基线完成：TCP 全端口 + 每个开放端口有服务/版本/证据；UDP 按需（`n/a` 有原因）；未知写 `unknown`。
32. 单一工具结果复核：`confirmed` 有原始响应 + 第二独立信号或可复现回显。

## 13. 迁移

1. 从旧仓库只复制 24 个技能目录到本仓库 `skills/`。
2. 重写 `pentest-flow/SKILL.md`。
3. 清理其余技能里的旧塔段落，`SKILL.md` 和 `references/`、`data/` 都要扫：broker、lease、approval、roe-load、KSA_ROOT、state、workdir、report 模块。
4. 全目录 grep 确认旧引用为 0。
5. 安装到 `~/.config/opencode/skills/`。
6. 删除 `/opt/Kestrel`。

## 14. 变更记录

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-10-24 | 2.0 | 从塔式 KSA 改为 skill-first；删除固定根目录、状态机、租约、审计链、报告模块；保留 L* 与授权；24 技能按需加载 |
| 2026-10-24 | 2.1 | 强制加载 recon/web-pentest/cve-triage；findings 实时落盘；Web 覆盖矩阵；脚本/源码/token 集中 evidence 且不清理 |
| 2026-10-24 | 2.2 | plan.md 每轮更新；禁止 report.md；RCE 复本验证规则；challenges.md 逐项状态；延长临时文件禁止清单 |
| 2026-10-27 | 2.3 | 依某授权目标实战日志修正：新增「节奏与播报」（连续 15 次无文字必须播报）、「已有工具优先」（同方向自制脚本 ≤3、生成即投递、本地回读失败不算阻断）；`exploitation` 改为 RCE 前强制加载并重写（33 行 → 完整 gadget 决策树 + JDK9+ add-opens 全集 + Dubbo 协议封包 + Windows payload + OOB 优先）；验收加 3 条可观测项 |
| 2026-10-30 | 2.4 | P0：RoE 增加 scope 范围语义（`same_ip` / `exclude_assets`，同 IP 默认 include）；`plan.md` 增加攻击面账本（状态集合与逐行更新）；挖洞循环定义「一轮」；结束检查增加机械条件 |
| 2026-10-30 | 2.5 | P1-1/P1-2：上下文交接（默认 1M，230k 不是满窗；交接块；不以上下文为由结束）；技能加载门禁（`plan.md` 技能加载表） |
| 2026-10-30 | 2.6 | P1-3：方向深度清单（认证/上传/SQLi/反序列化/接口面）；negative 前清单适用项必须 done/n/a |
| 2026-10-30 | 2.7 | P1-4：不可逆写入（W1–W6 判定；覆盖类 L4 ⛔；疑似副作用当轮披露） |
| 2026-10-30 | 2.8 | P1-5：账本驱动 next-3；结束前 lint（check_artifacts.py，含 /tmp 零引用） |
| 2026-10-30 | 2.9 | P2-A：无公网回连向用户申请（不跳过/不判死）；GitHub 直连失败用镜像回退 |
| 2026-11-01 | 3.0 | L\* 3.0：L4 拆 L4-⚠️ / L4-⛔；L4-⛔ 授权 + 回复确认后执行；爆破类归 L3-⚠️；目录爆破、WAF 绕过 L3 ✅；清除日志限定为只删本次交战自己产生的日志 |
| 2026-11-01 | 3.1 | 工具获取：工具默认按需可用；缺失按 apt/pipx/npm/go/gem/二进制安装；中国镜像（apt/PyPI/npm/Go/Ruby/Maven）；校验与记录 |
| 2026-11-03 | 3.2 | 发现播报：confirmed finding 用「结论 + 端点/入口 + payload/命令 + 原始响应 + 证据路径」；先落盘再播报；命令执行类 payload 门禁补 SSTI/表达式注入/上传 getshell/命令注入 |
| 2026-11-03 | 3.3 | 资产基线：TCP 全端口 + UDP top100 + 每个开放端口一行；进入 exploitation 前基线完成；blocked 从基线挑下一面；单一工具结果最多 candidate |
| 2026-11-03 | 3.4 | 扫描限速：默认 `-T3 --max-rate 300`（不超过 RoE max_rate），敏感目标 100；封禁即停扫降速；UDP 改为按需（`n/a` 有原因），不阻塞结束 |
| 2026-11-03 | 3.5 | 默认扫描速率调整为 `-T3 --max-rate 1000`（不超过 RoE max_rate），敏感目标 100，被拉黑时 100-300 |
| 2026-11-04 | 3.6 | 消息格式：面向用户的消息必须换行分段，字段一行一个；禁止用「；」串成一段 |
| 2026-11-04 | 3.7 | 项目更名 Kestrel；README、设计文档、技能注释与治理报告路径统一替换 |
| 2026-11-04 | 3.8 | 扫描速率拆分：全端口使用 `scan_rate` 默认 3000，服务识别使用 `max_rate` 默认 1000 |
