# AGENTS.md

## 先读

- `docs/DESIGN.md`：架构与不可忘记的决策
- `docs/RISK.md`：L\* 与授权表

## 硬约束

1. 没有固定塔根、broker、state、lease、`roe-load`、审计链、报告模块。
2. 技能唯一运行时目录是 `~/.config/opencode/skills/`；本仓库只是源码，安装后可删。
3. 产物只写 `<cwd>/Work/OC-<target>/`；技能目录不放 RoE、state、evidence、findings。
4. 24 个技能全部保留，全部按需加载；启动不预加载正文。
5. 主技能 `pentest-flow` 的路由表是静态的。
6. 默认风险上限 L3；L1/L2 直接做；L3 内 ✅ 直接做、⚠️ 逐次授权；L4-⚠️ 逐次授权后执行；L4-⛔ 默认禁止，明确授权后停下、回复确认才执行。
7. 挖洞循环：连续 3 轮复盘无新方向、且账本 `untested` 为 0、结束检查全过，才结束。
8. 没有原始证据不得标 `confirmed`；单一工具输出最多 `candidate`，`confirmed` 需要原始响应 + 第二种独立信号或可复现回显。
9. 强制加载：交战开始先加载 `pentest-flow`；侦察前 `recon`；发现 Web 后 `web-pentest`；拿到版本后 `cve-triage`；**打任何命令执行类 payload（RCE/反序列化/gadget/SSTI/表达式注入/上传 getshell/命令注入）前加载 `exploitation`**；并记入 `plan.md` 的 `## 技能加载` 表；缺行不得进入对应阶段。发 payload 前先看表，缺就先加载，不要打完补记。
10. 每确认一条 finding，立即写 `findings.md`。
11. 脚本/源码/token/上传测试文件/payload 只放 `Work/OC-<target>/evidence/{scripts,src,tokens}`；禁止 `/tmp`、`/var/tmp`、`/dev/shm`；任务结束不清理。
12. Web 覆盖矩阵每一类都有状态，才允许结束。
13. `plan.md` 每轮更新，必须有攻击面账本、深度清单、下一步 3 个动作（未完成时）、技能加载、交接块（如发生压缩）、不可逆写入判定（如发生）、回连申请记录（如发生）、覆盖清单、复盘、结束检查。
14. 不生成 `report.md`；`findings.md` 是交付。
15. 目标有挑战列表时，`challenges.md` 逐项状态。
16. RCE 线上被禁用时，起隔离复本验证或标 `blocked`，不得直接判 `negative`。
17. **不许闷头执行**：连续 15 次工具调用没有面向用户的文字，必须播报（方向 / 已得 / 卡点，三行内）。确认 finding 时改用「结论 + 端点/入口 + payload/命令 + 原始响应 + 证据路径」，先落盘再播报；只有结论、没有证据的 confirmed 播报视为没说完。消息必须换行分段，字段一行一个，不要用「；」串成一段；用空行或 `-` 列表分段，不能只靠单个换行；命令、payload、原始响应用代码块或反引号。
18. **现成工具优先**：写自制脚本前先确认没有现成的；同一方向自制脚本不超过 3 个。
19. **生成即投递**：payload 生成成功（`rc=0` 且非空）就直接打目标；本地回读失败不作为阻断理由。
20. **有公网回连就先用 OOB 打真实目标**，不要只用 `127.0.0.1` 回环。
21. **先确认目标 OS**：Windows 用 `cmd.exe /c` / ysoserial.net，不用 `/bin/sh`、`/tmp`。
22. **端口扫描两段式**：先全端口（`-p-`）拿开放端口清单，再只对开放端口 `-sV -sC` 详细识别；顺序不许反。默认限速：全端口 `-T3 --max-rate 3000`（RoE `scan_rate`），服务识别 `--max-rate 1000`（RoE `max_rate`）；敏感/WAF/云目标降到 100-300；被拉黑时继续降速；不要用 `--min-rate` 强制速率或 `-T4`。扫描前后用已知端口检测封禁，出现超时/拒绝立即停扫、降速、等待并记录，不连续重扫。UDP 按需（有 UDP 迹象且 RoE 允许时 top100），不做写 `n/a` + 原因，不阻塞结束。每个开放端口至少一行资产记录（服务/版本/HTTP/证据），未知写 `unknown`；进入 `exploitation`/投递 payload 前资产基线必须完成；`blocked` 时从基线挑下一面继续。
23. **范围由 RoE 的 `scope` 决定**：`same_ip: include` 时同 IP 全部端口/服务在范围内，不逐资产问授权；`same_ip: exclude` 时只测 target 域名对应的端口/路径，同 IP 其他不测；`scope.exclude_assets` 命中才停。
24. **`plan.md` 必须有攻击面账本**：资产×端口×服务×接口/参数×方法×类别×状态×证据×下一步；`untested` 未清零不得结束。
25. **上下文交接**：默认 1M；230k tokens（约 23%）是少见情况，不是满窗、不是接近上限。上下文接近实际上限（harness 提示或用量 >70%，默认约 700k）时，先写 `plan.md` 的 `## 交接块`，压缩/重开继续；**不得以「上下文有限/接近上限」为由结束**。
26. **技能加载门禁**：`plan.md` 必须有 `## 技能加载` 表；`pentest-flow`（交战开始）/ `recon` / `web-pentest` / `cve-triage` / `exploitation` 按阶段强制加载，缺行不得进入对应阶段，结束检查缺行即失败。
27. **方向深度清单门禁**：`plan.md` 必须有 `## 深度清单`，状态只用 `todo / doing / done / n/a / blocked`。清单来源：认证/会话、文件上传、SQLi、XSS / SSRF / XXE / SSTI、越权 / 业务逻辑 / 竞态、信息泄露 / 默认口令 → `web-pentest` §7；反序列化 / RCE → `exploitation` §9；接口面（方法 / 参数 / 认证态）→ `vuln-discovery` §5。方向标 `negative` 前，该方向清单所有适用项必须 `done` 或 `n/a`，`blocked` 项必须写「已尝试」；仍有 `todo` / `doing` 不得标 `negative`、不得结束；没有清单的方向不得标 `negative`。清单不替代攻击面账本：账本记「测了什么」，清单记「该类还差什么」。
28. **不可逆写入（W1–W6）**：任何上传/写入/导入/配置修改/数据库写之前，先做写入前判定。W1 端点行为（从源码/文档/响应确认写到哪里、文件名/目录是否可控）；W2 落点（新文件 / 随机名 / 测试目录 vs 固定路径 / 已有文件）；W3 覆盖风险（同名覆盖、业务文件、证书、密钥、配置）；W4 可清理（有删除接口 / 可回滚 / 有备份）；W5 探测方式（GET/HEAD/OPTIONS、无文件/空体、唯一临时名；**不向固定路径写内容**）；W6 授权（新文件 = L3 ✅ 或 L4-⚠️ 固定路径新建；修改已有配置 = L4-⚠️；覆盖业务文件/证书/密钥、同名覆盖、未知 = L4-⛔）。判定：新文件 + 随机名 + 测试目录 + 可清理 = L3 ✅，直接做并记账本；固定路径新建 + 可清理 = L4-⚠️，授权并记录清理；修改已有配置（备份+回滚）= L4-⚠️，授权并记录 diff；覆盖业务文件/证书/密钥、同名覆盖 = L4-⛔，授权 + 回复确认后执行；未知按 L4-⛔ 处理，只做非破坏探测，确认安全后再降级；数据库新增可清理的测试记录 = L3，更新/删除已有记录 = L4-⛔。
29. **疑似副作用当轮披露**：发现可能覆盖/破坏/产生副作用 → ①立即停止该端点，不再重试；②**当轮**向用户披露，不等最终报告；③记录时间、请求、响应、影响、回滚方式（`notes.md` / `findings.md` / `plan.md`）；④**不擅自恢复、不重试、不删除**，等用户指令；⑤账本状态标 `blocked`，备注 `incident`。
30. **账本驱动 next-3**：用户说「继续 / 接着 / 挖 / 下一步 / continue / go on」时，禁止从零重扫，禁止反问「接下来做什么」。固定动作：①读 `plan.md` 的 `## 攻击面账本`、`## 深度清单`、`## 交接块`（如有）；②生成候选：账本 `untested` 行、清单 `todo` / `doing` 项、`blocked` 但还有未尝试绕过的项；③按高→低排序：RCE / 反序列化 / gadget → 认证绕过 / 上传 getshell → SQLi / SSRF / XXE / SSTI → 越权 / 业务逻辑 → 信息泄露 / 默认口令；④取前 3 写入 `plan.md` 的 `## 下一步 3 个动作`；⑤**只执行第 1 个**，完成后立即更新账本/清单并三行播报；⑥第 1 个产生新方向则插到队首；没有候选则报告 `done` + `blocked` 清单。每次「继续」至少推进 1 个候选，没有推进就说明卡点；候选全是 `blocked` 时才对 top 1 请求授权，不得把「需要授权」当默认下一步。
31. **结束前 lint**：结束检查前运行 `python3 ~/.config/opencode/skills/pentest-flow/scripts/check_artifacts.py Work/OC-<target>`，**必须 PASS**；**FAIL 逐条修复后重跑，不得跳过**；`plan.md` / `findings.md` / `notes.md` / `approvals.md` 中 `/tmp`、`/var/tmp`、`/dev/shm` 零引用（否定句除外）。
32. **无公网回连**：本机没有公网入站/回连条件时，按下面处理；**不得跳过路径，不得判 negative/dead，不得用 127.0.0.1 冒充真实回连，不得先打再问**。
    - 反弹 shell / 入站监听：有公网 VPS / 端口转发 → 直接用；没有 → **必须先向用户提问申请**（VPS / 端口转发 / 回调地址）。
    - OOB DNS / HTTP（只需出站）：先试公共 dnslog / interactsh；不可达 → 向用户申请 OOB 服务。
    - 依赖回连的方向验证：反序列化 OOB、SSRF 回连、XXE OOB 等，按上面两个分支处理。
    - 用户提供 → 使用并记录；用户不提供/未回复 → 标 `blocked`（待回连），写清需要什么；任何需要回连的路径未申请/未提供不得判 negative。
    - 判定：能访问镜像/下载 ≠ 有公网回连；出站下载与入站回连是两件事。

    决策树：

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

    记录：`findings.md` / `plan.md` 记路径、为什么需要回连、已尝试、需要用户提供什么；账本状态 `blocked`，下一步写「向用户申请回连」；结束检查中凡需要回连的路径，必须有「已申请 / 已提供 / 待回连」记录，**未判 `negative`**。禁止：不得因为本机无公网就把路径标 `negative` / dead；不得跳过需要回连的 RCE / 反序列化 / SSRF / XXE 验证；不得用 `127.0.0.1` 回环冒充真实目标回连；不得「先打再说」，需要入站回连的利用先问用户再执行。
33. **GitHub 镜像**：GitHub 网页搜索/raw/release/API 直连失败时，按 gh-proxy.com → ghproxy.net → raw.gitmirror.com → jsdelivr → Gitee/用户镜像回退；代码搜索用 grep.app/sourcegraph/searchcode；至少试 2 个镜像再判断；下载放 `evidence/src/tools/` 并校验；**一次直连失败不等于工具/PoC 不存在**。

    触发：GitHub 网页搜索、`raw.githubusercontent.com`、release、API 直连失败/超时。

    回退顺序：

    1. `https://gh-proxy.com/https://github.com/...`
    2. `https://ghproxy.net/https://github.com/...`
    3. `https://raw.gitmirror.com/...`
    4. `https://cdn.jsdelivr.net/gh/<user>/<repo>@<ref>/<path>`（仓库文件）
    5. Gitee 镜像 / 用户提供的镜像

    代码搜索：`grep.app`、`sourcegraph.com`、`searchcode.com`、Gitee 搜索。

    纪律：**一次直连失败 ≠ 工具/PoC 不存在**，至少试 2 个镜像再判断；下载放 `evidence/src/tools/`，校验大小/类型（`file`、`jar tf`、`unzip -t`），有 checksum 就校验；记录哪个镜像成功（`notes.md`）；不运行下载目录里的其他脚本，只运行确认过的工具。

34. **爆破分级**：默认口令、弱口令（≤top100 小字典）、目录爆破直接做；大字典爆破、密码喷洒、账户锁定测试按 L3-⚠️ 逐次授权；授权前说明字典规模、速率、锁定/WAF 风险。

35. **L4 执行**：L4-⚠️ 用户授权即执行；L4-⛔ 用户明确授权后必须停下，等用户回复确认才执行。清除日志只删本次交战自己产生的日志，非自己产生的不删；无法区分则不删。

36. **工具获取与镜像**：技能里的工具默认按需可用，不要求预装；缺失先 `command -v` 检测，按 apt → pipx → npm → go → gem → 二进制/JAR 顺序安装。安装/下载走镜像或中国源：apt 用清华/中科大/阿里云 Kali 源；PyPI 用清华 TUNA/阿里云；npm 用 npmmirror；Go 用 goproxy.cn；Ruby 用 gems.ruby-china.com；Maven 用阿里云；GitHub 按 #33。装到系统 PATH 或 `evidence/src/tools/`，不写技能目录、不写 `/tmp`；校验大小/类型/SHA256；记录 `notes.md`；一次源失败不等于工具不存在，至少试 2 个源。工具安装只影响工作机，不改变对目标操作的 L\* 授权；Windows-only 工具用替代或标 `blocked`。

## 禁止恢复

```text
broker
capability
lease / lease check
approval 链 / pending-approval
roe_versions / roe-load
state 七件套 / SQLite / views / archive
workdir.sh / init-state.sh / state.sh
report 模块 / report-unlock
orchestrator agent / 580 行编排契约
```

## 当前阶段

- [x] 新仓库骨架
- [x] 设计文档 `docs/DESIGN.md`
- [x] L\* 表 `docs/RISK.md`
- [x] 主技能 `skills/pentest-flow/SKILL.md`
- [x] 清理其余 23 个技能里的旧塔段落
- [ ] 安装到 `~/.config/opencode/skills/`
- [ ] 空目录验收
- [x] P0：RoE 范围语义 + 攻击面账本（docs/PLAN-P0.md）
- [x] P1-1/P1-2：上下文交接 + 技能加载门禁（docs/PLAN-P1.md）
- [x] P1-3：方向深度清单（docs/PLAN-P1B.md）
- [x] P1-4：不可逆写入（docs/PLAN-P1C.md）
- [x] P1-5：账本驱动 next-3 + /tmp lint（docs/PLAN-P1D.md）
- [x] P2-A：无公网回连 + GitHub 镜像（docs/PLAN-P2A.md）
- [x] L\* 3.0：L4 拆分、爆破分级、清除日志范围
