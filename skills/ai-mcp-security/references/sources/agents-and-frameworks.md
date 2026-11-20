# 指令文件、Agent 与框架来源（S08–S12、S35–S41）

> 新增规则文件 / A2A / 框架来源追加到本表末尾，使用下一个未占用的 S 编号。

## 指令文件与编码 Agent

| ID | 来源 | 链接 | 支撑 |
|---|---|---|---|
| S08 | Pillar Security：Rules File Backdoor | https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents | `instruction-file-injection`、`repo_instruction_injection` |
| S09 | AGENTS.md 规范 | https://agents.md/ | `instruction-file-injection` |
| S10 | GitHub Copilot 仓库指令文档 | https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions | `instruction-file-injection`、`agent-framework-matrix` |
| S11 | Claude Code 记忆文档（CLAUDE.md） | https://code.claude.com/docs/en/memory | `instruction-file-injection`、`agent-framework-matrix` |
| S12 | Cursor Rules 文档 | https://cursor.com/docs/context/rules | `instruction-file-injection`、`agent-framework-matrix` |

## A2A / 多 Agent

| ID | 来源 | 链接 | 支撑 |
|---|---|---|---|
| S35 | LevelBlue：Agent in the Middle | https://www.levelblue.com/blogs/spiderlabs-blog/agent-in-the-middle-abusing-agent-cards-in-the-agent-2-agent-protocol-to-win-all-the-tasks | `subagent_delegation_abuse`、攻击链 C5 |
| S36 | A2A 协议规范 | https://a2a-protocol.org/latest/specification/ | `subagent_delegation_abuse`、攻击链 C5 |

## 框架与宿主

| ID | 来源 | 链接 | 支撑 |
|---|---|---|---|
| S37 | Dify 文档 | https://docs.dify.ai/ | `agent-framework-matrix` |
| S38 | LangChain / LangGraph 文档 | https://docs.langchain.com/ | `agent-framework-matrix` |
| S39 | CrewAI 文档 | https://docs.crewai.com/introduction | `agent-framework-matrix` |
| S40 | AutoGen 文档 | https://microsoft.github.io/autogen/stable/ | `agent-framework-matrix` |
| S41 | n8n 文档 | https://docs.n8n.io/ | `agent-framework-matrix` |

## 新增区

（暂无；新条目追加到对应小节后，在 `INDEX.md` 更新区间。）
