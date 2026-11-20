# 上下文、记忆与评测来源（S23–S34）

> 新增压缩 / 记忆 / RAG / 评测来源直接追加到本表末尾，使用下一个未占用的 S 编号。

| ID | 来源 | 链接 | 支撑 |
|---|---|---|---|
| S23 | Compaction Laundering（arXiv 2610.29869） | https://arxiv.org/abs/2610.29869 | `context_compaction_seed`、上下文压缩检测 |
| S24 | Governance Decay（arXiv 2606.22528） | https://arxiv.org/abs/2606.22528 | `context_compaction_seed`、上下文压缩检测 |
| S25 | OpenAI Alignment：压缩摘要自生成注入 | https://alignment.openai.com/misalignment-reports/self-generated-prompt-injections-in-compaction-summaries | `context_compaction_seed`、上下文压缩检测 |
| S26 | AgentPoison（arXiv 2407.12784） | https://arxiv.org/abs/2407.12784 | 记忆/RAG 投毒 |
| S27 | PoisonedRAG（arXiv 2402.07867） | https://arxiv.org/abs/2402.07867 | 知识库投毒 |
| S28 | Memory Injection Attacks（arXiv 2503.03704） | https://arxiv.org/abs/2503.03704 | 记忆注入 |
| S29 | AgentDojo（arXiv 2406.13352） | https://arxiv.org/abs/2406.13352 | 评测设计 |
| S30 | InjecAgent（arXiv 2403.02691） | https://arxiv.org/abs/2403.02691 | 间接注入用例 |
| S31 | Agent Security Bench（arXiv 2410.02644） | https://arxiv.org/abs/2410.02644 | 攻击/防御基准 |
| S32 | CaMeL（arXiv 2503.18813） | https://arxiv.org/abs/2503.18813 | 架构性防御 |
| S33 | Instruction Hierarchy（arXiv 2404.13208） | https://arxiv.org/abs/2404.13208 | `instruction-file-injection`、优先级基线 |
| S34 | Spotlighting（arXiv 2403.14720） | https://arxiv.org/abs/2403.14720 | A2-A、数据/指令分离 |

## 新增区

（暂无；新条目追加到上表后，在 `INDEX.md` 更新区间。）
