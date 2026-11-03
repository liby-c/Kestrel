# P2-A 改动方案：无公网回连 + GitHub 镜像

**状态**：已完成（2026-10-30）
**日期**：2026-10-30
**依据**：用户 2026-10-30 指令

## 0. 要解决的问题

1. **本机没有公网（无公网入站/回连监听）。** 需要反弹 shell、OOB 回连或依赖回连的方向验证时，代理可能直接跳过路径，或把它判成 `negative`/dead，导致本来可达的 RCE/反序列化/SSRF 方向被误杀。
2. **GitHub 网页搜索、raw、release 直连失败。** 代理可能据此判"工具/PoC 不存在"，而不是换镜像。

P2-A 只做两件事：**无公网回连的申请规则**、**GitHub 镜像回退**。

---

## 1. 无公网回连

### 1.1 判定

- **能访问镜像/下载 ≠ 有公网回连。** 出站下载与入站回连是两件事。
- 需要以下任一时，先检查回连条件：
  - 反弹 shell（bash/python/perl/nc 回连）；
  - 入站监听（nc -lvnp、msf handler、HTTP 回调）；
  - 依赖回连的方向验证（反序列化 OOB、SSRF 回连、XXE OOB 等）。

### 1.2 决策树

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

### 1.3 记录

- `findings.md` / `plan.md` 记：路径、为什么需要回连、已尝试、需要用户提供什么。
- 账本状态 `blocked`，下一步写「向用户申请回连」。
- 结束检查：凡需要回连的路径，必须有「已申请 / 已提供 / 待回连」记录，**未判 `negative`**。

### 1.4 禁止

- 不得因为本机无公网就把路径标 `negative` / dead。
- 不得跳过需要回连的 RCE / 反序列化 / SSRF / XXE 验证。
- 不得用 `127.0.0.1` 回环冒充真实目标回连。
- 不得"先打再说"：需要入站回连的利用，先问用户再执行。

---

## 2. GitHub 镜像

### 2.1 触发

GitHub 网页搜索、`raw.githubusercontent.com`、release、API 直连失败/超时。

### 2.2 回退顺序

1. `https://gh-proxy.com/https://github.com/...`
2. `https://ghproxy.net/https://github.com/...`
3. `https://raw.gitmirror.com/...`
4. `https://cdn.jsdelivr.net/gh/<user>/<repo>@<ref>/<path>`（仓库文件）
5. Gitee 镜像 / 用户提供的镜像

代码搜索：`grep.app`、`sourcegraph.com`、`searchcode.com`、Gitee 搜索。

### 2.3 纪律

- **一次直连失败 ≠ 工具/PoC 不存在**；至少试 2 个镜像再判断。
- 下载放 `evidence/src/tools/`；校验大小/类型（`file`、`jar tf`、`unzip -t`）；有 checksum 就校验。
- 记录哪个镜像成功（`notes.md`）。
- 不运行下载目录里的其他脚本，只运行确认过的工具。

---

## 3. 每文件改动

### 3.1 `AGENTS.md`

新增：

```text
32. **无公网回连**：本机没有公网入站/回连条件时，凡需要反弹 shell、入站监听、OOB 回连或依赖回连的方向验证，**必须向用户提问申请**（VPS / 端口转发 / 回调地址 / OOB 服务 / 替代验证授权）；用户提供就用，未提供就标 `blocked`（待回连）并写明需要什么；**不得跳过路径，不得判 negative/dead，不得用 127.0.0.1 冒充真实回连，不得先打再问**。公共 dnslog/interactsh 只需出站，可先试；不可达再申请。
33. **GitHub 镜像**：GitHub 网页搜索/raw/release/API 直连失败时，按 gh-proxy.com → ghproxy.net → raw.gitmirror.com → jsdelivr → Gitee/用户镜像回退；代码搜索用 grep.app/sourcegraph/searchcode；至少试 2 个镜像再判断；下载放 `evidence/src/tools/` 并校验；**一次直连失败不等于工具/PoC 不存在**。
```

「当前阶段」新增：`- [ ] P2-A：无公网回连 + GitHub 镜像（docs/PLAN-P2A.md）`

### 3.2 `skills/pentest-flow/SKILL.md`

- 在「不可逆写入」之后、「静态路由」之前新增 `## 无公网回连`（1.1–1.4）。
- 在「已有工具优先」之后新增 `## 网络与镜像`（2.1–2.3）。
- 「RCE 优先」第 3 条补：「若缺的是公网回连，先按「无公网回连」向用户申请；不得直接判死。」
- 结束检查追加：
  - 需要回连的路径已「已申请 / 已提供 / 待回连」，未判 `negative`；
  - GitHub 直连失败时已尝试镜像（至少 2 个）或记录原因。
- 记录：`plan.md` 必含项加「回连申请记录（如发生）」。

### 3.3 `skills/exploitation/SKILL.md`

- §0 铁律第 4 条补：「没有公网回连条件时，按 `pentest-flow` 的「无公网回连」向用户申请；不得跳过或判死。」
- §4「有公网回连时优先 OOB」补「无回连分支」：反弹 shell/入站监听先申请 VPS/端口转发；OOB 先试公共 dnslog/interactsh，不可达再申请；未提供标 blocked（待回连），不得用 `127.0.0.1` 冒充。
- §1/§8 工具下载处补：「GitHub 直连失败 → 按 `pentest-flow`「网络与镜像」回退；一次失败不等于工具不可用。」

### 3.4 `docs/RISK.md`

- §11 ⚠️ 汇总新增第 12 条：
  `需要回连但本机无公网：反弹 shell / 入站监听 → 先向用户申请 VPS/端口转发/回调地址；OOB（DNS/HTTP）→ 先试公共 dnslog/interactsh，不可达再申请。用户不提供/未回复 → blocked（待回连）。不得跳过、不得判 negative/dead、不得用 127.0.0.1 冒充、不得先打再问`
- 表后加一句：「回连资源不是风险等级：用户提供 VPS/回调后按对应 L\* 执行；未提供标 `blocked`（待回连），不判 negative。」

### 3.5 `docs/DESIGN.md`

- 头部 **2.8 → 2.9**；状态改「P0 已落地，P1-1…P1-5、P2-A 已落地」；最后更新 2026-10-30。
- §10 在「结束前 lint」之后新增 `### 无公网回连` 与 `### 网络与镜像`；结束检查追加回连申请与镜像记录。
- §11 质量规则新增第 12、13 条：无公网回连申请；GitHub 镜像回退。
- §12 验收新增第 29、30 条：回连路径有「已申请/已提供/待回连」记录且未判 negative；GitHub 直连失败至少试 2 个镜像或有记录。
- §14 变更记录加 `2026-10-30 | 2.9 | P2-A：无公网回连向用户申请（不跳过/不判死）；GitHub 直连失败用镜像回退`。

---

## 4. 验收

```bash
# 1. 无公网回连
grep -nE "无公网回连|反弹 shell|向用户.*申请|待回连|不得.*判" AGENTS.md skills/pentest-flow/SKILL.md skills/exploitation/SKILL.md docs/DESIGN.md docs/RISK.md

# 2. GitHub 镜像
grep -nE "gh-proxy|ghproxy|gitmirror|jsdelivr|grep\.app|sourcegraph|镜像" AGENTS.md skills/pentest-flow/SKILL.md skills/exploitation/SKILL.md docs/DESIGN.md

# 3. 结束检查项
grep -nE "已申请|待回连|至少 2 个镜像" skills/pentest-flow/SKILL.md docs/DESIGN.md

# 4. 旧塔引用：SKILL/RISK 必须为空
grep -rnE "roe-load|state\.sh|workdir\.sh|broker|\blease\b" skills/pentest-flow/SKILL.md skills/exploitation/SKILL.md docs/RISK.md
```

### 4.1 验收结果（2026-10-30）

- 工作流 `p2a-callback-mirrors`：10 个代理、`ok=true`、`issues=[]`。
- 无公网回连决策树在 AGENTS #32、pentest-flow「## 无公网回连」、exploitation §0/§4.1、DESIGN §10/§11#12/§12#29、RISK §11#12 一致；不得跳过/不得判 negative/dead/不得 127.0.0.1 冒充/不得先打再问均在位。
- GitHub 镜像顺序在 AGENTS #33、pentest-flow「## 网络与镜像」、exploitation §1.1/§8、DESIGN §10 四处一致；至少试 2 个镜像、下载放 `evidence/src/tools/` 并校验。
- 收尾：AGENTS #32 改为决策树形式（消除“OOB 也必须先申请”与“dnslog 可先试”的表述冲突）；P2-A 勾选；PLAN-P2A 标完成；验收 grep 4 用 `\blease\b`，避免 `release` 误命中。

---

## 5. P2 剩余

- 安装到 `~/.config/opencode/skills/`；
- 空目录验收；
- 运行时同步。

---

## 6. 完成标准

- 五个文件改完，验收 grep 通过；
- 无公网回连决策树在 AGENTS/pentest-flow/exploitation/DESIGN/RISK 一致；
- GitHub 镜像回退顺序在 AGENTS/pentest-flow/exploitation/DESIGN 一致；
- 没有引入 broker/lease/state/roe-load/report 模块。