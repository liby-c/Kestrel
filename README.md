# Kestrel

> 一个 AI 驱动的授权渗透测试工作流：先查清目标有哪些服务和入口，再按授权范围逐个测试，最后用原始证据下结论。

Kestrel 把通用 agent、24 个按需加载的技能和 Kali 工具组织成一套可审计的工作流。

它不替代扫描器，也不生成漂亮的报告；它负责把“测什么、为什么测、测到什么、证据在哪”串起来。

> **授权前提**：仅用于你拥有或已获得明确授权的目标。完整边界见 [安全声明](#安全声明)。

> **运行环境**：推荐在 Kali Linux（含 WSL Kali）部署和运行；Windows 原生环境未做测试，不推荐。

## 安装

### 环境要求

推荐在 Kali Linux（含 WSL Kali）部署和运行。技能依赖 Kali/Linux 工具链；Windows 原生环境未做测试，不推荐。

技能复制到客户端的全局技能目录：

| 客户端 | 技能目录 |
|---|---|
| OpenCode | `~/.config/opencode/skills/` |
| Claude Code | `~/.claude/skills/` |
| DSH | `~/.dsh/skills/` |

```bash
mkdir -p ~/.config/opencode/skills
cp -a skills/. ~/.config/opencode/skills/
```

技能不预装工具。缺少工具时，agent 会按 `apt → pipx → npm → go → gem → 二进制/JAR` 的顺序安装，优先使用国内镜像，并记录到 `notes.md`。

## 使用

以下命令在 Kali Linux shell 中执行。进入任意工作目录启动客户端：

```bash
cd /path/to/project
opencode        # 或 claude / dsh
```

直接说目标：

```text
打 <target>，目标 RCE
```

agent 会：

1. 在当前目录创建 `Work/OC-<target>/`；
2. 询问交战目标、风险上限、同 IP 范围、排除资产；
3. 写入 `roe.yaml`；
4. 画资产基线，然后按 L* 授权开始测试；
5. 实时写 `findings.md`、更新账本，结束前跑 lint。

## 工作机制

一次交战按下面的顺序推进：

```text
目标
  ↓
RoE：目标 / 范围 / 风险 / 时间
  ↓
资产基线：全端口 + 服务指纹 + HTTP/TLS + 证据
  ↓
攻击面账本：逐项验证，blocked 换下一个面
  ↓
findings + evidence：确认一条写一条
  ↓
复盘：3 轮无新方向 + untested=0 + lint PASS → 结束
```

### 1. 建立 RoE

新目标先在当前目录创建 `Work/OC-<target>/`，确认交战目标、风险上限、同 IP 范围和排除资产，然后写入 `roe.yaml`。

范围以 `scope` 为准：`same_ip: include` 时同 IP 的服务都在范围内；`same_ip: exclude` 时只测 target 对应的端口/路径；`exclude_assets` 命中才跳过。

### 2. 画资产基线

侦察资产：

- TCP 全端口 `-p-` 扫描；
- UDP 按需，不强制；不做写 `n/a` 并说明原因；
- 每个开放端口一行：服务、版本、HTTP title/技术栈、证据；
- 识别不出来的服务标 `unknown`，不能跳过；
- 原始探测输出写入 `evidence/src/`。

### 3. 选攻击面

资产基线完成后，按攻击面账本逐项验证。技能按阶段加载，不一次塞满上下文：

| 阶段 | 强制加载 |
|---|---|
| 交战开始 | `pentest-flow` |
| 主动侦察前 | `recon` |
| 发现 HTTP/Web 服务后 | `web-pentest` |
| 拿到组件/版本后 | `cve-triage` |
| 打命令执行类 payload 前 | `exploitation` |

每次加载都写入 `plan.md` 的 `## 技能加载` 表。某个方向 `blocked` 时，从资产基线挑下一个未测服务继续，不因单点阻塞结束。

### 4. 验证与记录

- 工具输出默认是线索，单一工具结果最多 `candidate`；
- `confirmed` 需要原始响应，加上第二种独立信号或可复现回显；
- 每确认一条 finding 立即写 `findings.md`，并给出端点、payload/命令、原始响应和证据路径；
- 命令、payload、原始响应使用代码块或反引号，不把多个字段挤成一段。

### 5. 复盘与结束

`plan.md` 维护攻击面账本、深度清单和下一步 3 个动作。连续 3 轮复盘无新方向、账本 `untested` 为 0、结束检查全过，才结束。

结束前运行：

```bash
python3 ~/.config/opencode/skills/pentest-flow/scripts/check_artifacts.py Work/OC-<target>
```

必须输出 `PASS`；FAIL 逐条修复后重跑。

## 核心理念

**技能是路由，不是提示词堆栈。**
启动时只暴露 24 个技能的 `name` 和 `description`；进入交战、侦察、Web、CVE、利用阶段时才加载对应正文。上下文留给目标，不留给目录。

**先资产，后利用。**
先把端口、服务、版本、HTTP/TLS 指纹画完整，再决定打哪里。单点 `blocked` 时，从资产基线挑下一个面，而不是从头重扫或直接收尾。

**工具输出是线索，不是结论。**
nmap 的服务名、whatweb 的指纹、版本 banner 都可能出错。单一工具结果最多算 `candidate`；`confirmed` 需要原始响应，加上第二种独立信号或可复现回显。

**授权边界写进文件。**
L0–L2 直接做，L3 逐项授权，L4 授权并回复确认；所有动作受 `roe.yaml` 约束。边界不是记忆，是文件。

**产物自包含。**
所有东西落在当前目录的 `Work/OC-<target>/`，不依赖固定根目录、常驻服务或状态机。

## 产物

```text
<cwd>/Work/OC-<target>/
  roe.yaml          # 本轮授权范围
  plan.md           # 方向、攻击面账本、深度清单、复盘、结束检查
  approvals.md      # ⚠️ 操作授权记录
  notes.md          # 范围变更、环境信息、工具记录
  findings.md       # 发现，最终交付
  challenges.md     # 目标提供挑战列表时
  evidence/
    scripts/        # agent 写的脚本
    src/            # 原始输出、源码、payload、下载工具
    tokens/         # token、cookie、凭据
```

不生成 `report.md`，`findings.md` 就是交付。

## 设计

- [docs/DESIGN.md](docs/DESIGN.md)：架构、24 技能矩阵、按需加载、资产基线、挖洞循环、验收
- [docs/RISK.md](docs/RISK.md)：L* 与授权表

## 安全声明

Kestrel 仅用于**你拥有或已获得明确授权**的目标。未授权扫描、入侵、数据获取或破坏均可能违法，本项目不为此提供任何支持。

使用前必须：

- 确认授权范围、时间窗和排除资产，并写入 `roe.yaml`；
- 遵守 L* 授权表：L0–L2 直接做，L3 逐项授权，L4 授权并回复确认；L4-⛔ 默认禁止；
- 不把工具输出当作授权依据，不越过 `scope`、`exclude_assets`、`time_window`、`max_rate`。

交战产物可能包含凭据、token、业务数据和个人信息。`evidence/tokens/` 与 `findings.md` 应按敏感数据处理，仅保存在授权环境，结束后按约定清理或移交。

本项目按“现状”提供，不附带任何担保；使用者对自身行为及后果负责。