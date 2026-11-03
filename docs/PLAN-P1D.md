# P1 改动方案（第五批）：账本驱动 next-3 + /tmp lint

**状态**：已完成（2026-10-30）
**日期**：2026-10-30
**依据**：`demo-app.cn` 交战日志（2026-10-29）

## 0. 要解决的问题

1. **用户每次说"继续"，代理都从零重析。** 日志里用户推了 5 次（`8107`、`14684`、`15353`、`15800`、`15975`），每次代理都重新梳理一遍，先前列出的方向被否定后才补测。没有"读账本 → 取下一步 → 做 1 个"的固定动作。
2. **`/tmp` 没有机械检查。** 日志里写了 **69 次** `/tmp`，最后清理时把探测文件删了，既违反"不写 `/tmp`"，也可能丢证据。只靠模型自觉不够。

P1 第五批：**账本驱动 next-3**、**静态 lint 脚本**。

---

## 1. 账本驱动 next-3

### 1.1 触发词

`继续` / `接着` / `挖` / `下一步` / `continue` / `go on`。

### 1.2 固定动作

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

### 1.3 规则

- 不许从零重扫；不许反问"接下来做什么"。
- 每次"继续"至少推进 1 个候选；没有推进就说明卡点。
- 候选全是 `blocked` 时，才对 top 1 请求授权；不得把"需要授权"当默认下一步。

### 1.4 `plan.md` 模板

```markdown
## 下一步 3 个动作
1. <账本行号/清单项> — <动作>
2. ...
3. ...
```

---

## 2. /tmp lint

### 2.1 脚本

`skills/pentest-flow/scripts/check_artifacts.py <Work/OC-target>`

无第三方依赖，退出码：`0` = PASS，`1` = FAIL。

检查项：

1. `roe.yaml`、`plan.md`、`findings.md` 存在。
2. `plan.md` 必含：`## 攻击面账本`、`## 技能加载`、`## 深度清单`、`## 覆盖清单`、`## 复盘`、`## 结束检查`。
3. 攻击面账本：
   - 无 `untested` 行；
   - `untested` 行必须有「下一步」；
   - `confirmed` / `negative` / `candidate` 必须有证据；
   - `blocked` 必须有「已尝试」。
4. 深度清单：
   - 无 `todo` / `doing`；
   - `blocked` 必须有「已尝试」。
5. 技能加载表：必须有 `pentest-flow` / `recon`；出现 HTTP 则必须有 `web-pentest`；账本含 `cve` 则必须有 `cve-triage`；含 `deserialization` / `rce` 则必须有 `exploitation`。
6. `/tmp` lint：
   - `plan.md` / `findings.md` / `notes.md` / `approvals.md` 中出现 `/tmp/`、`/var/tmp/`、`/dev/shm/` 且不是"不写/禁止/没有/清理"等否定句 → FAIL；
   - 本地 `/tmp`、`/var/tmp`、`/dev/shm` 中存在比 `roe.yaml` 更新的文件 → WARN（列出，不自动判失败，系统运行时文件可能混入）。
7. 不得存在 `report.md`。
8. `findings.md` 中 `confirmed` 的条目必须含「证据」或 `evidence/`。

### 2.2 调用

结束检查前运行：

```bash
python3 ~/.config/opencode/skills/pentest-flow/scripts/check_artifacts.py Work/OC-<target>
```

必须输出 `PASS`；FAIL 时逐条修复后重跑，不得跳过。

---

## 3. 每文件改动

### 3.1 `skills/pentest-flow/SKILL.md`

- 「产物」目录树 `plan.md` 注释加「下一步 3 个动作」；正文加一句「lint 通过才允许结束」。
- 在「方向深度清单」之后、「挖掘循环」之前新增 `## 用户说「继续」时的固定动作（账本驱动 next-3）`（1.1/1.2/1.3/1.4）。
- 「结束检查」追加：
  - 运行 `check_artifacts.py` 输出 PASS；
  - `plan.md` / `findings.md` / `notes.md` / `approvals.md` 无 `/tmp` 引用；
  - `## 下一步 3 个动作` 在未完成时为最新。
- 「记录」：`plan.md` 必含项加「下一步 3 个动作（未完成时）」。
- 新增脚本 `skills/pentest-flow/scripts/check_artifacts.py`。

### 3.2 `docs/DESIGN.md`

- 头部 **2.7 → 2.8**；状态改「P0 已落地，P1-1…P1-5 已落地」；最后更新 2026-10-30。
- §6 主技能规范新增第 17 条（账本驱动 next-3）与第 18 条（结束前 lint）。
- §7 `plan.md` 职责加「下一步 3 个动作」。
- §10 在「不可逆写入」之后新增 `### 账本驱动 next-3` 与 `### 结束前 lint`；结束检查追加 lint PASS。
- §12 验收新增第 27、28 条。
- §14 变更记录加 `2026-10-30 | 2.8 | P1-5：账本驱动 next-3；结束前 lint（check_artifacts.py，含 /tmp 零引用）`。

### 3.3 `AGENTS.md`

- 新增：
  ```text
  30. **账本驱动 next-3**：用户说「继续/接着/挖/下一步」时，读 `plan.md` 账本与深度清单，按 RCE 潜力排序取前 3，写入 `## 下一步 3 个动作`，只做第 1 个并立即更新；不许从零重扫，不许反问。
  31. **结束前 lint**：运行 `check_artifacts.py Work/OC-<target>`，必须 PASS；FAIL 逐条修复后重跑；`/tmp`、`/var/tmp`、`/dev/shm` 零引用。
  ```
- 「当前阶段」新增 `- [ ] P1-5：账本驱动 next-3 + /tmp lint（docs/PLAN-P1D.md）`。

---

## 4. 验收

```bash
# 1. next-3
grep -nE "next-3|下一步 3 个动作|账本驱动" skills/pentest-flow/SKILL.md docs/DESIGN.md AGENTS.md

# 2. lint
grep -nE "check_artifacts|PASS|/tmp" skills/pentest-flow/SKILL.md docs/DESIGN.md AGENTS.md

# 3. 脚本可运行（用自测目录）
python3 skills/pentest-flow/scripts/check_artifacts.py Work/OC-lint-selftest

# 4. 旧塔引用：SKILL/RISK 必须为空
grep -rnE "roe-load|state\.sh|workdir\.sh|broker|\blease\b" skills/pentest-flow/SKILL.md docs/RISK.md
```

### 4.1 验收结果（2026-10-30）

- 工作流 `p1d-next3-lint`：4 个代理、`ok=true`、`issues=[]`。
- next-3 在 `pentest-flow` / DESIGN / AGENTS 三处一致：触发词、候选来源、RCE 优先级、取前 3、只做第 1 个、不许从零重扫/反问。
- lint 在 `pentest-flow` / DESIGN / AGENTS 三处一致：`check_artifacts.py`、必须 PASS、FAIL 修复后重跑、`/tmp` 零引用。
- 脚本自测：`Work/OC-lint-selftest` → `PASS` / exit 0；`Work/OC-lint-bad` → `FAIL: 9 issue(s)` / exit 1；无参数 → exit 2。
- Windows 自测用 `python`（本机 `python3` 是商店别名）；Kali 运行时用 `python3`。
- 收尾：PLAN-P1D 标完成；AGENTS P1-5 勾选；DESIGN 2.8 状态含 P1-5。

---

## 5. P1 完成后剩余

- 安装到 `~/.config/opencode/skills/`；
- 空目录验收（用本次 P0/P1 规则跑一遍）；
- 运行时同步后才在下次交战生效。

---

## 6. 完成标准

- `pentest-flow` / DESIGN / AGENTS 改完，验收 grep 通过；
- next-3 固定动作在三处一致；
- `check_artifacts.py` 在自测目录输出 PASS，在故意违规目录输出 FAIL；
- 没有引入 broker/lease/state/roe-load/report 模块。