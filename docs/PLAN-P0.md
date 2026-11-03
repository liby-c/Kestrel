# P0 改动方案：范围语义 + 攻击面账本

**状态**：已完成（2026-10-30）
**日期**：2026-10-30
**依据**：`demo-app.cn` 交战日志（2026-10-29）

## 0. 要解决的问题

日志暴露两个结构性问题：

1. **范围每次都要重新判断。** 代理先判"同 IP 其他系统是 RoE 外"，用户说"全端口深度测试"后又自行改判，中途停下来问授权。用户口径：**同一 IP = 同一范围**。范围必须写进 RoE，不能靠每轮临场解释。
2. **`plan.md` 是自由文本，没有"未做完"的客观信号。** 覆盖矩阵是"类"级，测几个接口就能标 `negative`；代理在上下文接近上限时把"装不下"当成"做完了"（日志 `14317`、`15275`）。

P0 只做两件事：**把范围写进 RoE**、**把 `plan.md` 变成可检查的攻击面账本**。

---

## 1. P0-1：范围语义

### 1.1 RoE 模板

```yaml
engagement:
  target: "<target>"
  scope:
    same_ip: include          # include | exclude
    exclude_assets: []        # 明确排除的主机/域名/端口
  allowed_ports: all
  time_window: "00:00-23:59"
  max_rate: 1000
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

兼容：旧 `roe.yaml` 里的顶层 `exclude` 视为 `scope.exclude_assets`；读到旧字段时按新语义处理，不报错。

### 1.2 语义

- `same_ip: include`：目标解析出的 IP 上**全部端口/服务**在范围内；直接枚举、指纹、测试，**不逐资产询问授权**。
- `same_ip: exclude`：只测 target 域名对应的端口/路径，同 IP 其他服务不测。
- `exclude_assets`：唯一排除项；命中即跳过，并在 `notes.md` 记一行。
- 范围变更：只由用户指令触发；更新 `roe.yaml` + `notes.md` 各记一条，不删旧记录。
- 同 IP 内的服务互相横移不算"横移到 RoE 外新主机"；不同 IP 的新主机仍按 ⚠️ 处理。

### 1.3 落点

| 文件 | 改动 |
|---|---|
| `docs/DESIGN.md` | §8.1 新目标问题加"同 IP 是否在范围内（默认 include）"；§8.2 读 RoE 时以 `scope` 为准；§8.3 模板加 `scope.same_ip` / `scope.exclude_assets`；§14 变更记录加 v2.4 |
| `docs/RISK.md` | 开头范围声明改为以 `scope` 为准，明确 `same_ip: include` 时同 IP 全端口/服务在范围内 |
| `skills/pentest-flow/SKILL.md` | 「新目标」问题与模板加 `scope`；「已有目录」以 `scope` 为准；「风险与授权」加一句范围语义 |
| `AGENTS.md` | 硬约束新增一条"范围由 RoE 的 `scope` 决定" |

---

## 2. P0-2：攻击面账本

### 2.1 模板

```markdown
## 攻击面账本

| # | 资产 | 端口 | 服务 | 接口/参数 | 方法 | 类别 | 状态 | 证据 | 下一步 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | <target> | 80 | demo-app | /manage/Login | POST | auth_bypass | untested | - | 加密体复测 |
| 2 | <target> | 28080 | demo-api | /upload/uploadCert | POST | file_upload | confirmed | evidence/src/... | 无 |
```

### 2.2 状态

`untested / testing / confirmed / candidate / negative / blocked / n/a`

- `untested`：未测；必须有「下一步」。
- `testing`：进行中。
- `confirmed`：已确认；必须有证据路径。
- `candidate`：疑似；必须有线索/证据。
- `negative`：已排除；必须有证据。
- `blocked`：被阻断；必须有「已尝试」列表。
- `n/a`：不适用；写原因。

### 2.3 规则

- 发现一个资产/端口/服务，至少一行；发现一个接口（或一组同构接口），至少一行。
- 每次测试后更新状态与证据；不攒到最后。
- 覆盖矩阵保留为汇总，但**以账本为准**。
- 一轮 = 对账本的一次完整推进；连续 **3 轮**无新方向 **且** `untested` 为 0，才进入结束检查。

### 2.4 结束检查（机械条件）

- 攻击面账本 `untested` 行数为 **0**。
- 每条 `negative` / `candidate` 有证据路径。
- 每条 `blocked` 有「已尝试」列表。
- 每条 `confirmed` 有证据路径。
- `plan.md` 含 `## 攻击面账本`、`## 复盘`、`## 结束检查`。

### 2.5 落点

| 文件 | 改动 |
|---|---|
| `docs/DESIGN.md` | §7 `plan.md` 职责加账本；§10 挖洞循环定义"一轮"并加「攻击面账本」小节；结束检查加机械条件；§12 验收加账本项；§14 变更记录 |
| `skills/pentest-flow/SKILL.md` | 「产物」加账本；「挖掘循环」加「攻击面账本」小节；结束检查加机械条件；「记录」强调逐条更新 |
| `AGENTS.md` | 硬约束新增一条"`plan.md` 必须有攻击面账本"；「当前阶段」加一条 P0 待办 |

---

## 3. 每文件精确改动

### 3.1 `docs/DESIGN.md`

- §7 产物职责表：`plan.md` 一行改为「当前方向、攻击面账本、复盘、结束检查」。
- §8.1 新目标：第 2 步改为问四件事（交战目标、风险上限、同 IP 是否在范围内（默认 include）、排除资产）；默认值加 `scope.same_ip: include`、`scope.exclude_assets: []`。
- §8.2 同一目标：读 `roe.yaml` 后，范围语义以 `scope` 为准；修改 scope 记 `notes.md`。
- §8.3 模板：按 1.1 加 `scope` 块；加兼容说明。
- §10 挖洞循环：第 6 步改为「一轮 = 账本全量推进一次；连续 3 轮无新方向且 `untested` 为 0」；新增 `### 攻击面账本` 小节（模板、状态、规则）；结束检查加 2.4 的机械条件。
- §12 验收：新增「`roe.yaml` 有 `scope.same_ip`/`scope.exclude_assets`」「`plan.md` 有 `## 攻击面账本`，结束前 `untested` 为 0」。
- §14 变更记录：加 `2026-10-30 | 2.4 | P0：RoE 增加 scope 范围语义；plan.md 增加攻击面账本；结束检查增加机械条件`。

### 3.2 `docs/RISK.md`

开头第 5 行替换为：

> 所有动作仅限 `roe.yaml` 的 `target` 与 `scope` 范围。`scope.same_ip: include` 时，目标解析 IP 上的全部端口/服务在范围内，不逐资产询问；`scope.exclude_assets` 命中才停。横移到不同 IP 的新主机，先问用户加入 RoE。

### 3.3 `skills/pentest-flow/SKILL.md`

- 「产物」目录树 `plan.md` 注释改为「方向、攻击面账本、复盘、结束检查」；正文加一句「账本是结束检查的依据」。
- 「新目标」：问四件事（加同 IP 范围，默认 include）；RoE 模板按 1.1 加 `scope`；加兼容说明。
- 「已有目录」：第 1 步读 `roe.yaml` 后，范围以 `scope` 为准；改 scope 记 `notes.md`。
- 「风险与授权」：在 L 表前加一句「范围由 RoE 的 `scope` 决定；`same_ip: include` 时同 IP 全部端口/服务在范围内，不逐资产询问」。
- 「挖掘循环」：第 6 步改为「一轮 = 账本全量推进一次；连续 3 轮无新方向且 `untested` 为 0」；新增 `### 攻击面账本` 小节（2.1/2.2/2.3）。
- 「结束检查」：加 2.4 的机械条件。
- 「记录」：加一句「每条测试后立即更新账本行，不得攒到最后」。

### 3.4 `AGENTS.md`

硬约束新增：

```text
23. **范围由 RoE 的 `scope` 决定**：`same_ip: include` 时同 IP 全部端口/服务在范围内，不逐资产问授权；`scope.exclude_assets` 命中才停。
24. **`plan.md` 必须有攻击面账本**：资产×端口×服务×接口/参数×方法×类别×状态×证据×下一步；`untested` 未清零不得结束。
```

「当前阶段」新增：

```text
- [ ] P0：RoE 范围语义 + 攻击面账本（docs/PLAN-P0.md）
```

---

## 4. 验收

```bash
# 1. 范围语义三处一致
grep -n "same_ip" docs/DESIGN.md docs/RISK.md skills/pentest-flow/SKILL.md AGENTS.md

# 2. 账本模板与状态
grep -n "攻击面账本" docs/DESIGN.md skills/pentest-flow/SKILL.md AGENTS.md
grep -n "untested" docs/DESIGN.md skills/pentest-flow/SKILL.md

# 3. 结束检查机械条件
grep -n "untested.*0\|untested 行数\|untested.*为 0" docs/DESIGN.md skills/pentest-flow/SKILL.md

# 4. 旧塔引用：SKILL/RISK 必须为空；
#    DESIGN/AGENTS 的命中只允许是“禁止恢复/没有/迁移清理”说明（逐条人工确认）。
grep -rn "roe-load\|state\.sh\|workdir\.sh\|broker\|\blease\b" skills/pentest-flow/SKILL.md docs/RISK.md
grep -n "roe-load\|state\.sh\|workdir\.sh\|broker\|\blease\b" docs/DESIGN.md AGENTS.md
```

### 4.1 验收结果（2026-10-30）

- 四个文件已改；范围语义、账本模板/状态、结束检查机械条件在 DESIGN/SKILL/AGENTS/RISK 一致。
- 工作流 `p0-scope-ledger` 独立验收 `ok=true`；3 条非阻断问题（DESIGN 版本头、示例行状态、grep 门禁）已收尾修复。
- `AGENTS.md`「当前阶段」P0 项已勾选。

---

## 5. P1 backlog（本次不做）

1. 方向深度清单（认证/上传/反序列化/SQLi 最低测试矩阵）。
2. 上下文交接块 + 禁止“装不下所以结束”。
3. 强制加载门禁（技能加载表）。
4. 用户说“继续”时的固定动作（账本驱动 next-3）。
5. 不可逆写入 ⚠️/L4 细化（覆盖已有文件/证书/密钥）。
6. `/tmp` 零写入 + 可选 lint。

---

## 6. P0 完成标准

- 四个文件改完且验收 grep 通过；
- `plan.md` 账本模板、状态集合、结束检查在 DESIGN 与 SKILL 中一致；
- 范围语义在 DESIGN/RISK/SKILL/AGENTS 中一致；
- 没有把 broker/lease/state/roe-load/report 模块写回来。