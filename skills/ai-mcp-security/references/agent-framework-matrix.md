# Agent 框架能力面矩阵

> 用途：先判断目标属于哪类宿主/框架，再决定读哪份检测清单。
> 本表是**能力面索引**，不是版本功能断言；标“按实际配置核对”的项，先用一次只读探针确认存在性。
> 来源：[S10] [S11] [S12] [S37] [S38] [S39] [S40] [S41]；具体字段/版本以目标实际配置为准。

## 矩阵

| 宿主/框架 | 指令/规则入口 | 工具/执行面 | 审批/权限 | 记忆/压缩 | MCP/协议 | 测试入口 |
|---|---|---|---|---|---|---|
| Claude Code | `CLAUDE.md`、skills、hooks | Bash/文件/网络/MCP 工具 | 权限模式、allow-rule、审批提示 | 上下文压缩/摘要 | MCP（按配置） | CLI/MCP |
| Cursor | `.cursor/rules`、`.cursorrules`、AGENTS.md（按版本） | 终端/文件/浏览器/MCP | Agent 模式确认 | 上下文管理 | MCP（按配置） | IDE Agent |
| GitHub Copilot | `.github/copilot-instructions.md`、仓库指令 | Agent 模式终端/工具 | 命令确认 | 上下文 | MCP（按版本/配置） | IDE/CLI |
| Dify | 应用 Prompt、知识库、工作流节点 | 工具/插件/HTTP/代码节点 | 应用/工作区权限、发布审批 | 会话记忆/知识检索 | MCP（按部署配置） | Web/API |
| LangChain / LangGraph | Prompt 模板、图节点/状态 | 工具/检索器/代码执行 | 自定义回调/审批 | checkpointer/记忆 | 适配器（按实现） | Python SDK |
| CrewAI | role/goal/backstory、task 描述 | 工具/委派/代码执行 | guardrails/人工确认（按实现） | memory（按配置） | 适配器（按实现） | Python SDK |
| AutoGen | agent system message、团队编排 | 工具/代码执行器 | 自定义审批/人工输入 | 会话状态 | 适配器（按实现） | Python SDK |
| n8n | 工作流节点、AI Agent 节点 | HTTP/工具节点/代码节点 | 凭据/审批节点 | memory 节点 | 按节点/版本 | 工作流 UI/API |

## 怎么用

1. **先定位宿主/框架**：从目标路径、配置文件名、进程/端点判断；不要仅凭 UI 猜。
2. **只测实际存在的面**：没有对应能力面就跳过，不硬套检测清单。
3. **规则/指令入口** → `instruction-file-injection-detection`；工具/执行面 → `tool-abuse` + `authorization-bypass`。
4. **审批/权限** → `agent-policy-bypass-detection` §B；记忆/压缩 → `context-compaction-poisoning-detection`。
5. **MCP** → `mcp-tool-poisoning-detection`；把多条面串起来时查 `agent-attack-chains.md`。

## 不能从本表直接得出的结论

- 不能推断某版本一定支持/不支持某能力；版本差异与插件配置必须实测。
- 不能把框架默认值当作目标配置；以目标实际文件、端点和权限设置为准。
- 不能因为表里有某面就跳过授权：所有动态测试仍受 RoE 与 L0–L4 分级约束。

## 注意

- 本表只给“去哪里找能力面”，不提供绕过方法；payload 仍走 `operators/`。
- 报告写清框架、版本、部署形态与配置来源，避免把通用结论套到具体目标。
- 参考：[S10] [S11] [S12] [S37] [S38] [S39] [S40] [S41]。
