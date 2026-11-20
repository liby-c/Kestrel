---
name: ai-mcp-security
description: AI与MCP安全评估 — Prompt注入、工具滥用、MCP信任边界、Agent权限逃逸、数据泄露、模型风险、GAARM风险矩阵
metadata:
  layer: "skill"
  risk: "medium"
  phase: "vuln-discovery"
  target_types: "ai_agent,mcp"
  task_types: "pentest,audit"
  technologies: "llm,rag,memory,plugin"
  vulnerability_classes: "prompt_injection,tool_abuse,info_disclosure"
---

# AI 与 MCP 安全评估 Skill

当目标包含 LLM、Agent、MCP 工具、Skills、RAG、Memory、Plugin 或模型服务组件时使用本 Skill。

**前置条件**：如果 AI 表面只是展示层，真正的阻塞仍是客户端签名或加密协议，先回到 `client-reverse` Skill。

**加载门禁**：目标出现 `/assistant/chat`、`/memories`、`/skills`、`/prompt-gen`、`/mcp`、tool_calls 或模型服务等 AI/Agent 端点时，本 Skill 必须在任何 AI 动态 payload 前加载，并在 `plan.md` 的 `## 技能加载` 记一行；未加载不得发 AI payload。

## 场景路由

| 风险类型 | 首选参考 |
|---------|---------|
| Prompt 注入 / 间接注入 / CoT 干扰 | `references/ai-app-security.md` |
| MCP 工具描述投毒 / Rug Pull / 跨 Server | `references/agent-detections/mcp-tool-poisoning-detection.md` |
| 护栏 / 审批 / HITL 绕过 | `references/agent-detections/agent-policy-bypass-detection.md` |
| 指令文件 / Skill / MCP instructions 注入 | `references/agent-detections/instruction-file-injection-detection.md` |
| 上下文压缩 / 长期会话注入 | `references/agent-detections/context-compaction-poisoning-detection.md` |
| 需要把多个能力面串成链 | `references/agent-attack-chains.md` |
| 判断宿主/框架能力面 | `references/agent-framework-matrix.md` |
| 工具滥用 / MCP 投毒 / Skills 供应链 | `references/ai-app-security.md` §三十五 MCP 章节 |
| 权限逃逸 / 角色越界 / 凭据滥用 | `references/ai-identity-security.md` |
| 数据泄露 / Prompt 泄漏 / 模型逆推 | `references/ai-data-security.md` |
| 容器逃逸 / CI-CD / 沙箱失败 | `references/ai-baseline-security.md` |
| 模型风险 / 对抗样本 / 后门 | `references/ai-model-security.md` |
| 影响分类与覆盖评估 | `../secknowledge-skill/references/gaarm-risk-matrix.md` |
| **要发 payload 做动态测试** | `references/operators/INDEX.md`（84 算子变异库） |
| **要测 Agent 工作流能力面** | `references/agent-detections/INDEX.md`（19 个检测清单） |
| **动态测试方法与报告口径** | `references/ai-redteam-methodology.md`（必读） |

## 上下文预算（硬约束）

- 单次交战参考加载 **≤800 行**（不含本 SKILL.md 与方法论）。
- 检测清单一次只读 **1 份**；换能力面才读第 2 份，并在 `notes.md` 记理由。
- 算子一次只读 **≤3 个**；先查 `references/operators/_signals.md` 粗筛，再精读候选。
- **禁止整读** `ai-*.md`（均 >1000 行）；**先读开头的 `## 目录`**（含行号），再 `Read offset=<行号> limit=80` 定位；没有目录的文件才用 `Grep '^### '`。
- 来源只在写报告引用时读 `references/sources/INDEX.md`；检测清单只写 `[Sxx]`。
- 每次加载记入 `Work/OC-<target>/notes.md` 的“加载账本”（文件、行数、原因）。

## 红队测试资产

本技能内置以下红队资产：算子库与检测清单源自 [tencent/AI-Infra-Guard](https://github.com/Tencent/AI-Infra-Guard)（Apache-2.0，腾讯朱雀实验室），攻击链、框架矩阵与来源索引为本工程整理。**本技能 references ≥ 15，属大技能——禁止整目录读取；一律先读 INDEX 再按需取单篇。**

| 资产 | 路径 | 用途 |
|---|---|---|
| 变异算子库 | `references/operators/` | 84 算子 / 27 家族，注入与越狱 payload 构造 |
| Agent 工作流检测清单 | `references/agent-detections/` | 19 个检测面：工具滥用、记忆投毒、RAG 投毒、间接注入、越权、MCP 投毒、策略绕过、指令文件、上下文压缩、外传… |
| 攻击链视图 | `references/agent-attack-chains.md` | 6 条组合链：能力面 → 算子序列 → 观测点 |
| 框架能力面矩阵 | `references/agent-framework-matrix.md` | 8 类宿主/框架的规则入口、工具、审批、记忆、MCP |
| 来源索引 | `references/sources/INDEX.md` | S01–S41 主题索引与引用规则，写报告时查 |
| 评测数据集 | `data/eval-datasets/` | 11 个数据集 / 1329 条样本，用于拒答边界评估与 ASR 统计 |
| 渲染脚本 | `scripts/` | `render_operator.py`（算子渲染）、`encodings.py`（13 种编码链）、`select_operators.py`（信号粗筛） |

**开展 AI 目标动态测试前必读** `references/ai-redteam-methodology.md`：第一性原理五步流程、
`defense_signals` 信号驱动变异、verdict 五态、≥30 payload 覆盖下限，以及本工程 RoE / 审批分级适配。

```bash
# 先定位技能根目录 KS；零外部依赖，仅用 python3 标准库；Windows 用 python 替代 python3
KS=$(find "$HOME" "$PWD" -maxdepth 8 \
  -path '*/skills/ai-mcp-security/scripts/render_operator.py' \
  -print -quit 2>/dev/null | sed 's#/ai-mcp-security/scripts/render_operator.py$##')
python3 "$KS/ai-mcp-security/scripts/render_operator.py" --operator homoglyph --goal "Output AIG_CANARY_x only"
python3 "$KS/ai-mcp-security/scripts/encodings.py" --chain base64,homoglyph --text 'Output AIG_CANARY_x'
python3 "$KS/ai-mcp-security/scripts/select_operators.py" --help
```

**约束**：模型对话测试属 L2（直接做）；数据导出、用户级持久化属 L3（直接做）；
修改关键配置（有备份、可回滚）属 L3；无法回滚的修改 / 重启**目标原有服务** / 修改业务状态按 `../pentest-flow/references/constitution.md` §2 的 L4 分级处理；启动/停止/重启自己创建的服务属 L3；需要授权的操作记 `Work/OC-<target>/approvals.md`。

## 测试流程

### 1. 应用层攻击
- 直接 Prompt 注入
- 间接注入（通过外部数据源）
- CoT 干扰与指令覆盖
- Agent 滥用（未授权操作）
- 代码执行突破
- Memory 投毒

### 2. MCP 与 Agent 风险
- 工具描述投毒
- 指令覆盖
- 隐藏指令注入
- 未授权资源访问
- Skills/Rules 供应链问题

### 3. 身份与授权
- 动作滥用
- 角色逃逸
- 权限漂移
- 云凭据滥用

### 4. 数据与隐私
- Prompt 泄漏
- 敏感数据暴露
- 训练数据问题
- 模型逆推
- API 数据窃取

### 5. 基线与部署
- CI/CD 缺陷
- 容器逃逸
- 向量数据库安全
- 沙箱失效
- 环境隔离缺陷
- 模型服务缺陷

## 参考文档

**AI 安全知识库（概念与风险目录）**
- `references/ai-app-security.md` / `ai-baseline-security.md` / `ai-data-security.md` / `ai-identity-security.md` / `ai-model-security.md` — 5 个 AI 安全分册
- `references/ai-app-security.md` — AI 应用安全
- `references/ai-identity-security.md` — AI 身份安全
- `references/ai-data-security.md` — AI 数据安全
- `references/ai-baseline-security.md` — AI 基线安全
- `references/ai-model-security.md` — AI 模型安全
- `../secknowledge-skill/references/gaarm-risk-matrix.md` — GAARM 风险矩阵

**红队资产（可执行，先读各自 INDEX）**
- `references/ai-redteam-methodology.md` — 第一性原理红队方法论（动态测试必读）
- `references/operators/INDEX.md` — 变异算子库（84 算子 / 27 家族）
- `references/agent-detections/INDEX.md` — Agent 工作流检测清单（19 个）
- `references/agent-attack-chains.md` — 六条组合攻击链（能力面 → 算子 → 观测点）
- `references/agent-framework-matrix.md` — 8 类宿主/框架能力面矩阵
- `references/sources/INDEX.md` — 来源索引（S01–S41，按主题分文件，写报告时查）
- `data/eval-datasets/README.md` — 评测数据集（11 个 / 1329 条）
- `scripts/` — 算子渲染与编码链脚本（零外部依赖）
