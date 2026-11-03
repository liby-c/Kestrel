# Agent 工作流检测清单索引（16 个）

> 来源：[tencent/AI-Infra-Guard](https://github.com/Tencent/AI-Infra-Guard) `agent-scan/prompt/skills/`（MIT，腾讯朱雀实验室）
> 用途：对 AI Agent / AI 应用做**工作流层**的授权安全检测（区别于 `operators/` 的 payload 变异视角）

## 与 operators/ 的分工

| 视角 | 目录 | 回答的问题 |
|---|---|---|
| **payload 视角** | `operators/` | 怎么构造能绕过防御的输入（变异、编码、多轮） |
| **工作流视角** | 本目录 | 目标有哪些可被滥用的能力面（工具、记忆、RAG、多 Agent、人机接口） |

两者配合：本目录定位"测什么边界"，`operators/` 提供"用什么样的输入去测"。

## 使用前提

同 `operators/INDEX.md`：先确定 target 的 `send` / `observe` 接口与 RoE 授权；
再把原文的 `dialogue(...)` 理解为"向目标发一次请求并记录完整响应 + 工具 trace"。
**若目标不具备该清单对应的能力面，跳过该清单**（不硬测）。

## 清单一览（16 个）

| 清单 | 检测目标 | 主要 ASI |
|---|---|---|
| `direct-injection-detection.md` | 直接提示词注入 | ASI01 |
| `indirect-injection-detection.md` | 间接注入（外部内容/RAG/文件成为指令） | ASI01、ASI06 |
| `tool-abuse-detection.md` | 工具滥用、命令注入、路径遍历、SSRF | ASI02、ASI05、ASI07 |
| `unexpected-code-execution-detection.md` | 意外代码执行（RCE/命令注入/代码求值） | ASI05、ASI04 |
| `data-leakage-detection.md` | 数据泄露（系统提示词、凭据、跨边界数据） | ASI06、ASI07 |
| `hardcoded-secret-detection.md` | 硬编码密钥（代码/配置/Skill 包） | ASI06、ASI04 |
| `authorization-bypass-detection.md` | 越权与鉴权绕过 | ASI03、ASI09 |
| `file-path-traversal-detection.md` | 文件路径穿越 | ASI05、ASI02 |
| `web-exfiltration-detection.md` | Web 外传（外连/外泄通道） | ASI07、ASI02 |
| `memory-poisoning-detection.md` | 记忆投毒 | ASI06 |
| `memory-rag-poisoning-detection.md` | 记忆与 RAG 语料投毒 | ASI06、ASI01、ASI04 |
| `inter-agent-comm-security-detection.md` | Agent 间通信安全 | ASI07、ASI06 |
| `human-agent-trust-exploit-detection.md` | 人机信任利用（社工/欺骗性响应） | ASI09、ASI01 |
| `cascading-failure-detection.md` | 级联失败（错误传播/链式反应） | ASI08、ASI10 |
| `agentic-supply-chain-detection.md` | Agent 供应链（恶意依赖/工具投毒） | ASI04、ASI10 |
| `owasp-asi.md` | **OWASP ASI 2026 分类框架**（发现归类用，非检测清单） | — |

## 推荐选用顺序（按目标能力面）

1. **先摸能力面**：目标暴露哪些工具、是否有文件/代码/网络权限、有无记忆与 RAG、是否多 Agent。
2. **注入类优先**：`direct-injection` → `indirect-injection`（后者风险通常更高，因绕过用户交互）。
3. **按能力面展开**：有工具 → `tool-abuse` + `unexpected-code-execution` + `file-path-traversal`；
   有记忆/RAG → `memory-poisoning` + `memory-rag-poisoning`；
   有外连 → `web-exfiltration`；多 Agent → `inter-agent-comm-security`。
4. **收尾归类**：用 `owasp-asi.md` 把发现映射到 ASI01–ASI10，写进报告。

## 输出与记录

原文的 `<vuln>` XML 块可保留作为结构化记录，但**最终报告按本工程 `reporting` 技能规范输出**：

- 记录：标题、位置、证据（完整 prompt + 完整响应 + 工具 trace）、影响、修复建议
- 分类：映射到 `ASI0x`（见 `owasp-asi.md`）
- 严重级别：与 `reporting` 口径取更严者
- 多轮对话必须逐轮完整展示，不得合并成摘要

## 注意事项

- SSRF / 外连验证必须用**操作员提供的可控端点**（`<VERIFY_ENDPOINT>`）与自建 canary token，
  不得依赖外部第三方 URL——遵守 RoE 的外连与限速约束。
- 涉及真实数据外传、持久化写入、修改目标状态的测试属 **L4**，需人工审批（见 RoE 分级）。
- 报告引用来源：`[tencent/AI-Infra-Guard](https://github.com/Tencent/AI-Infra-Guard) agent-scan`。
