# 策略、审批与护栏来源（S13–S22）

> 新增策略 / 审批 / 护栏来源直接追加到本表末尾，使用下一个未占用的 S 编号。

| ID | 来源 | 链接 | 支撑 |
|---|---|---|---|
| S13 | OWASP Agentic Top 10（ASI01–ASI10） | https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ | A2、ASI 映射、`subagent_delegation_abuse` |
| S14 | OWASP LLM01:2025 Prompt Injection | https://genai.owasp.org/llmrisk/llm01-prompt-injection/ | A2-A |
| S15 | OWASP LLM06:2025 Excessive Agency | https://genai.owasp.org/llmrisk/llm062025-excessive-agency/ | A2-B、`tool_arg_smuggle`、`subagent_delegation_abuse` |
| S16 | From Approval to Abuse（arXiv 2610.22987） | https://arxiv.org/abs/2610.22987 | A2-B、`approval_forgery`/`approval_fatigue` |
| S17 | Approve What, Exactly?（arXiv 2610.21063） | https://arxiv.org/abs/2610.21063 | A2-B、审批绑定 |
| S18 | Oversight Has a Capacity（arXiv 2606.08919） | https://arxiv.org/abs/2606.08919 | A2-B、审批疲劳 |
| S19 | Reframing LLM Agent Security（arXiv 2605.24309） | https://arxiv.org/abs/2605.24309 | A2-B、运行时审批现状 |
| S20 | Constitutional Classifiers（arXiv 2501.18837） | https://arxiv.org/abs/2501.18837 | A2-A、护栏设计 |
| S21 | Azure AI Content Safety：Prompt Shields | https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection | A2-A、商业护栏边界 |
| S22 | NCSC：Prompt injection is not SQL injection | https://www.ncsc.gov.uk/blog-post/prompt-injection-is-not-sql-injection | A2-A、输入清洗不成立 |

## 新增区

（暂无；新条目追加到上表后，在 `INDEX.md` 更新区间。）
