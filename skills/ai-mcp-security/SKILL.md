---
name: ai-mcp-security
description: AI与MCP安全评估 — Prompt注入、工具滥用、MCP信任边界、Agent权限逃逸、数据泄露、模型风险、GAARM风险矩阵
metadata:
  layer: "L2"
  risk: "L2"
  phase: "vuln-discovery"
  target_types: "ai_agent,mcp"
  task_types: "pentest,audit"
  technologies: "llm,rag,memory,plugin"
  vulnerability_classes: "prompt_injection,tool_abuse,info_disclosure"
---

# AI 与 MCP 安全评估 Skill

当目标包含 LLM、Agent、MCP 工具、Skills、RAG、Memory、Plugin 或模型服务组件时使用本 Skill。

**前置条件**：如果 AI 表面只是展示层，真正的阻塞仍是客户端签名或加密协议，先回到 `client-reverse` Skill。

## 场景路由

| 风险类型 | 首选参考 |
|---------|---------|
| Prompt 注入 / 间接注入 / CoT 干扰 | `references/ai-app-security.md` |
| 工具滥用 / MCP 投毒 / Skills 供应链 | `references/04-ai-and-mcp-security-integrated.md` MCP 章节 |
| 权限逃逸 / 角色越界 / 凭据滥用 | `references/ai-identity-security.md` |
| 数据泄露 / Prompt 泄漏 / 模型逆推 | `references/ai-data-security.md` |
| 容器逃逸 / CI-CD / 沙箱失败 | `references/ai-baseline-security.md` |
| 模型风险 / 对抗样本 / 后门 | `references/ai-model-security.md` |
| 影响分类与覆盖评估 | `references/gaarm-risk-matrix.md` |
| **要发 payload 做动态测试** | `references/operators/INDEX.md`（77 算子变异库） |
| **要测 Agent 工作流能力面** | `references/agent-detections/INDEX.md`（16 个检测清单） |
| **动态测试方法与报告口径** | `references/ai-redteam-methodology.md`（必读） |

## 红队测试资产（吸收自 A.I.G）

本技能内置四类**可执行**红队资产（来源：[tencent/AI-Infra-Guard](https://github.com/Tencent/AI-Infra-Guard)，

MIT，腾讯朱雀实验室）。**本技能 references ≥ 15，属大技能——禁止整目录读取；一律先读 INDEX 再按需取单篇。**

| 资产 | 路径 | 用途 |
|---|---|---|
| 变异算子库 | `references/operators/` | 77 算子 / 26 家族，注入与越狱 payload 构造 |
| Agent 工作流检测清单 | `references/agent-detections/` | 16 个检测面：工具滥用、记忆投毒、RAG 投毒、间接注入、越权、外传… |
| 评测数据集 | `data/eval-datasets/` | 11 个数据集 / 1329 条样本，用于拒答边界评估与 ASR 统计 |
| 渲染脚本 | `scripts/` | `render_operator.py`（算子渲染）、`encodings.py`（13 种编码链）、`select_operators.py`（信号粗筛） |

**开展 AI 目标动态测试前必读** `references/ai-redteam-methodology.md`：第一性原理五步流程、
`defense_signals` 信号驱动变异、verdict 五态、≥30 payload 覆盖下限，以及本工程 RoE / 审批分级适配。

```bash
# 脚本工作目录基准为本技能根目录；零外部依赖，仅用 python3 标准库
python3 scripts/render_operator.py --operator homoglyph --goal "Output AIG_CANARY_x only"
python3 scripts/encodings.py --chain base64,homoglyph --text 'Output AIG_CANARY_x'
python3 scripts/select_operators.py --help
```

**约束**：模型对话测试属 L2（直接做）；数据导出、用户级持久化属 L3（直接做）；
修改关键配置/重启服务属 L4-⚠️（逐次授权）；修改业务状态/删除业务数据属 L4-⛔（授权 + 回复确认）；需要授权的操作记 `Work/OC-<target>/approvals.md`。

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
- `references/04-ai-and-mcp-security-integrated.md` — AI 与 MCP 安全整合参考
- `references/ai-app-security.md` — AI 应用安全
- `references/ai-identity-security.md` — AI 身份安全
- `references/ai-data-security.md` — AI 数据安全
- `references/ai-baseline-security.md` — AI 基线安全
- `references/ai-model-security.md` — AI 模型安全
- `references/gaarm-risk-matrix.md` — GAARM 风险矩阵

**红队资产（可执行，先读各自 INDEX）**
- `references/ai-redteam-methodology.md` — 第一性原理红队方法论（动态测试必读）
- `references/operators/INDEX.md` — 变异算子库（77 算子 / 26 家族）
- `references/agent-detections/INDEX.md` — Agent 工作流检测清单（16 个）
- `data/eval-datasets/README.md` — 评测数据集（11 个 / 1329 条）
- `scripts/` — 算子渲染与编码链脚本（零外部依赖）
