<div align="center">

# Kestrel

**AI 驱动的授权渗透测试工作流**

24 个技能 · 按需加载 · 零依赖 · 产物自包含

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-24-brightgreen.svg)](skills)
[![Clients](https://img.shields.io/badge/clients-4-lightgrey.svg)](#客户端支持)

</div>

---

Kestrel 把通用 agent、24 个按需加载的技能和 Kali 工具组织成一套可审计的渗透测试工作流。

它不替代扫描器，也不生成漂亮的报告——它负责把「测什么、为什么测、测到什么、证据在哪」串起来。

> **授权前提**：仅用于你拥有或已获得明确授权的目标。完整边界见[安全声明](#安全声明)。
>
> **运行环境**：技能本身零依赖，但执行依赖工具环境——推荐 Kali Linux（全量工具集可用，技能列表不是白名单）。缺工具时按 `apt → pipx → npm → go → gem → 二进制/JAR` 安装，优先中国镜像，安装记录写入 `notes.md`。

## 核心优势

| 优势                | 说明                                                                                                 |
|---------------------|------------------------------------------------------------------------------------------------------|
| **证据驱动**        | 工具输出只算线索；标「已确认」必须附原始响应和第二种独立信号，每个结论都能追溯到证据                 |
| **可交接**          | 账本、清单、复盘、清理记录全部落在 `Work/OC-<target>/`——换人接手不用重来，压缩或重启都能续           |
| **授权可控**        | 分级写进 `roe.yaml`（L0–L3 自动上限 + `forbidden` 边界），L4 逐次授权——边界是文件，不是模型记忆      |
| **按需加载**        | 启动只加载 24 个技能的名称与用途；信号命中且当前动作需要时才读正文，用不到的技能不占上下文           |
| **零依赖**          | 24 个技能是纯 markdown，复制进技能目录即用——不装服务、不建库、不改环境                               |
| **离线/在线知识库** | AI 组件漏洞库、注入算子库、Agent 检测清单与攻击链全部内置，断网也能查；联网时接 NVD / OSV 补最新数据 |

## 快速开始

```bash
git clone https://github.com/liby-c/Kestrel.git
cd Kestrel
cp -a skills/. ~/.claude/skills/    # 换成你客户端的技能目录
```

在任意工作目录启动客户端，直接说目标：

```text
打 10.0.0.5，目标 RCE
```

agent 会建立 `Work/OC-10.0.0.5/`，写 RoE，画资产基线，然后按账本推进。

## 工作流

```text
目标 → RoE → 资产基线 → 攻击面账本
                              │
                              ▼
                    测试与取证（循环）
              每轮：选方向 → 测试 → 记录 → 复盘
                              │
              5 轮有效复盘无新方向 + untested = 0
                              ▼
              结束检查表 → 用户确认 → 交付 findings.md
```

## 技能矩阵

| 类别            | 技能                                                                                   |
|-----------------|----------------------------------------------------------------------------------------|
| 主流程          | `pentest-flow`                                                                         |
| 侦察            | `recon` · `osint-recon`                                                                |
| Web             | `web-pentest` · `web-security-advanced` · `waf-bypass`                                 |
| 漏洞与利用      | `vuln-discovery` · `cve-triage` · `exploitation`                                       |
| 后渗透          | `post-exploitation` · `intranet-pentest-advanced` · `redteam-playbooks`                |
| AI / Agent 安全 | `ai-mcp-security`                                                                      |
| CTF             | `ctf-web` · `ctf-crypto` · `ctf-misc`                                                  |
| 客户端          | `android-pentest` · `client-reverse` · `crypto-toolkit`                                |
| 支撑            | `pentest-tools` · `rapid-checklist` · `secknowledge-skill` · `hackerone` · `reporting` |

## 授权分级

| 等级  | 范围                                                           | 默认              |
|-------|----------------------------------------------------------------|-------------------|
| L0–L2 | 被动收集、端口 / 子域扫描、只读验证、默认口令、弱口令 ≤top100  | ✅ 直接做         |
| L3    | 只新增自己的对象或可回滚的改动                                 | ✅ 直接做         |
| L3-⚠️ | 大字典爆破、密码喷洒（不主动提出）、账户锁定测试、修改账号密码 | ⚠️ 逐次授权       |
| L4    | 改变目标原有状态或不可逆                                       | 🔴 明确授权后执行 |

**L3 覆盖**：目录爆破、WAF 绕过、可清理写入、测试上传、WebShell、用户级/系统级持久化、内存马、systemd、修改配置与回滚（有备份）、启停自己创建的服务、固定路径新建、同目标横移、数据导出、用户态提权、域控只读。

**L4 覆盖**：无法回滚的修改、停止/重启目标原有服务、为生效而重载其配置、重启主机、清防火墙、DoS、删除数据、覆盖文件/证书/密钥、同名覆盖、格式化、加密勒索、清日志、内核提权、域控写、横移 RoE 外。

**判据**：动自己新增的对象 → L3；动目标原有对象看能否回滚——配置类可回滚 → L3，业务文件 / 证书 / 密钥 → L4；让改动生效所需的重载 / 重启目标服务 → L4。

完整分级见 `skills/pentest-flow/references/constitution.md`——它是授权规则的唯一来源。

## 产物

```text
Work/OC-<target>/
  roe.yaml          # 授权范围
  plan.md           # 攻击面账本、深度清单、覆盖清单、复盘、结束检查
  findings.md       # 交付物
  approvals.md      # ⚠️ 操作授权记录
  cleanup.md        # 清理账本
  notes.md
  evidence/
    scripts/        # agent 写的脚本
    src/            # 原始输出、源码、payload
    tokens/         # 凭据
```

不生成 `report.md`——`findings.md` 就是交付。

## 客户端支持

| 客户端      | 技能目录                     |
|-------------|------------------------------|
| Claude Code | `~/.claude/skills/`          |
| Codex       | `~/.codex/skills/`           |
| OpenCode    | `~/.config/opencode/skills/` |
| DSH         | `~/.dsh/skills/`             |

24 个技能必须整体安装——存在跨技能的 `references/` 引用。

## 设计原则

1. **技能是参考，不是流程** —— 信号命中且当前动作需要时才加载，不预加载。
2. **先资产，后利用** —— 端口、服务、版本画完整，再决定打哪里。
3. **工具输出是线索，不是结论** —— 单一工具的结果只算线索，要第二种独立信号才能确认。
4. **授权边界写进文件** —— 不是记忆，是 `roe.yaml`。
5. **产物自包含** —— 不依赖固定根目录、常驻服务或状态机。
6. **打不下来如实交付** —— 卡住时不索要凭证、不把「需要爆破」当下一步；失败是正常结局。

## 安全声明

Kestrel 仅用于**你拥有或已获得明确授权**的目标。未授权扫描、入侵、数据获取或破坏均可能违法，本项目不为此提供任何支持。

使用前必须：

- 确认授权范围、时间窗和排除资产，并写入 `roe.yaml`；
- 遵守 L\* 授权表：L0–L3 直接做（其中 ⚠️ 项逐次授权），L4 经明确授权后执行（授权即执行，无二次确认）；
- 不把工具输出当作授权依据，不越过 `scope`、`exclude_assets`、`time_window`、`max_rate`。

交战产物可能包含凭据、token、业务数据和个人信息。`evidence/tokens/` 与 `findings.md` 应按敏感数据处理，仅保存在授权环境，结束后按约定清理或移交。

## 许可证

本项目采用 Apache License 2.0，全文见 [LICENSE](LICENSE)。

基于 [Tencent AI-Infra-Guard](https://github.com/Tencent/AI-Infra-Guard)（Apache-2.0）；内置第三方内容与数据集的来源和许可见 [NOTICE](NOTICE) 与 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

许可证不构成对任何未授权测试的授权。
