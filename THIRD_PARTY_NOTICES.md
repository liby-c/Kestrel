# Third-Party Notices

本项目自身代码与文档采用 Apache License 2.0，全文见 [LICENSE](LICENSE)。

本文件记录项目内置的第三方内容及其许可证信息，不构成法律意见。
如上游许可证与本文件描述不一致，以上游仓库的原始许可证为准。

## Tencent AI-Infra-Guard

- 来源：https://github.com/Tencent/AI-Infra-Guard
- 许可证：Apache License 2.0（以上游仓库 `LICENSE` 为准）
- 版权：Copyright 2024-2026 Tencent Zhuque Lab
- 强制归属（上游 NOTICE，Apache-2.0 §4(d)）：
  - 必须明确标注 “Based on Tencent Zhuque Lab AI-Infra-Guard”
  - 必须包含原仓库链接：https://github.com/Tencent/AI-Infra-Guard

Based on Tencent Zhuque Lab AI-Infra-Guard
(https://github.com/Tencent/AI-Infra-Guard)。
本仓库基于其部分内容进行适配与修改，覆盖路径包括：

- `skills/cve-triage/data/aig-vuln/`：CVE 规则库（2440 条 / 142 个 AI 组件）
- `skills/recon/data/aig-fingerprints/`：AI 组件指纹库（168 个组件）
- `skills/ai-mcp-security/references/agent-detections/`：Agent 工作流检测清单
- `skills/ai-mcp-security/references/operators/`：变异算子库
- `skills/ai-mcp-security/data/eval-datasets/`：评估数据集
- `skills/ai-mcp-security/` 下与之对应的适配文档

上游 NOTICE 副本：

- `skills/cve-triage/data/aig-vuln/NOTICE`
- `skills/recon/data/aig-fingerprints/NOTICE`
- `skills/ai-mcp-security/data/eval-datasets/NOTICE`

## 评估数据集上游来源

本项目内置的评估数据集随 Tencent AI-Infra-Guard 的 `data/eval/` 分发。
各数据集的上游来源与许可证核实结果如下；这些许可证独立于项目自身的
Apache-2.0，不因项目整体许可而被重新许可。

| 文件 | 上游来源 | 许可证 | 再分发备注 |
|---|---|---|---|
| `CBRN-weapon.json` | 上游 `source` 为空；author = LouisHovaldt | 未声明 | 无法确认再分发权；建议移除或改为按需下载 |
| `ChatGPT-Jailbreak-Prompts.json` | https://huggingface.co/datasets/rubend18/ChatGPT-Jailbreak-Prompts | 未声明（dataset card 无 license） | 默认版权保留；建议移除或改为按需下载 |
| `HarmfulEvalBenchmark.json` | https://huggingface.co/datasets/JailbreakBench/JBB-Behaviors | MIT | 兼容；保留 MIT 声明 |
| `JADE-db-v3.0.json` | https://github.com/whitzard-ai/jade-db | MIT（Copyright 2023 whitzard-ai） | 兼容；保留 MIT 声明 |
| `copyright-violation.json` | https://huggingface.co/datasets/allenai/wildguardmix；https://github.com/STAIR-BUPT/JailBench | ODC-BY；MIT | 需署名；保留来源与许可声明 |
| `cyberattack.json` | https://huggingface.co/datasets/allenai/wildguardmix | ODC-BY | 需署名 |
| `misinformation.json` | https://huggingface.co/datasets/allenai/wildguardmix；https://github.com/STAIR-BUPT/JailBench | ODC-BY；MIT | 需署名 |
| `non-violent-illegal-activity.json` | https://huggingface.co/datasets/allenai/wildguardmix；https://github.com/STAIR-BUPT/JailBench；https://huggingface.co/datasets/PKU-Alignment/BeaverTails | ODC-BY；MIT；CC-BY-NC-4.0 | **含非商业限制**；商业分发前移除或替换 |
| `privacy-leakage.json` | https://huggingface.co/datasets/allenai/wildguardmix；https://github.com/STAIR-BUPT/JailBench | ODC-BY；MIT | 需署名 |
| `unethical-behavior.json` | https://huggingface.co/datasets/allenai/wildguardmix；https://github.com/STAIR-BUPT/JailBench；https://huggingface.co/datasets/PKU-Alignment/BeaverTails | ODC-BY；MIT；CC-BY-NC-4.0 | **含非商业限制**；商业分发前移除或替换 |
| `violent.json` | https://huggingface.co/datasets/allenai/wildguardmix；https://github.com/STAIR-BUPT/JailBench；https://huggingface.co/datasets/PKU-Alignment/BeaverTails | ODC-BY；MIT；CC-BY-NC-4.0 | **含非商业限制**；商业分发前移除或替换 |

**许可证汇总：**

- **MIT**：JBB-Behaviors（JailbreakBench）、JADE-db（Copyright 2023 whitzard-ai）、
  JailBench（Copyright 2024 gitkolento）— 与项目 Apache-2.0 兼容。
- **ODC-BY**：wildguardmix（Allen Institute for AI；HuggingFace `gated=auto`，
  使用前需接受上游条款）— 允许再分发与商业使用，但必须保留署名与许可声明。
- **CC-BY-NC-4.0**：BeaverTails（PKU-Alignment）— **禁止商业使用**；
  `non-violent-illegal-activity`、`unethical-behavior`、`violent` 含此来源。
- **未声明**：`CBRN-weapon`（author LouisHovaldt）、
  `ChatGPT-Jailbreak-Prompts`（author Rubén Darío Jaramillo，dataset card 无 license）
  — 无法确认再分发权。

**当前策略（2026-11-08）：保留全部数据集，按各自上游许可证分发。**

1. `CBRN-weapon.json`、`ChatGPT-Jailbreak-Prompts.json` 以及含 BeaverTails 的
   3 个数据集均保留在仓库中，不删除。
2. 使用或再分发时必须遵守对应上游许可证：CC-BY-NC-4.0 禁止商业使用；
   ODC-BY 需保留署名；MIT 需保留版权与许可声明；未声明数据集无法确认再分发权。
3. 项目自身的 Apache-2.0 不覆盖这些数据集；对外表述时不得声称整个仓库
   （含数据集）均为 Apache-2.0。
4. 如后续用于商业分发或对外交付，应重新评估并移除、替换或改为按需下载
   高风险数据集。

**备选处理（商业分发时）：** 移除含 BeaverTails 的 3 个数据集；
移除或按需下载 `CBRN-weapon.json` 与 `ChatGPT-Jailbreak-Prompts.json`。

**使用边界**：这些语料包含有害内容样本，唯一允许用途是评估被测模型/Agent
是否拒绝生成此类内容；禁止用于实际危害行为、传播或攻击真实系统。

## 其他参考内容

- `skills/secknowledge-skill/`：融合 WooYun 案例、先知方法论、GAARM 风险矩阵、
  OWASP Top 10（LLM/ASI/WSTG）等公开资料；具体来源与许可证需逐个核实，
  原始内容版权归各自作者。如权利人提出异议，应移除对应内容。
- `skills/redteam-playbooks/`：参考 Claude-Red 等公开红队资料；来源与许可证
  需逐个核实。
- 各技能 `references/` 中引用的公开文档、博客、工具说明，版权归原作者；
  本仓库仅保留方法论摘要与链接。

## NVD

`cve-triage` 在运行时通过 NVD 公开 API 查询 CVE，不内置 NVD 数据。
NVD 数据的使用受 NVD 使用条款约束：https://nvd.nist.gov/general/legal

## 许可证不构成测试授权

Apache-2.0 及任何第三方许可证都不构成对目标系统的测试授权。
授权边界见 README 的「安全声明」与 `docs/RISK.md`。
