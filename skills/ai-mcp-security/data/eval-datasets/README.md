# 越狱评估数据集（11 个 / 1329 条样本）

> 来源：[tencent/AI-Infra-Guard](https://github.com/Tencent/AI-Infra-Guard) `data/eval/`（MIT，腾讯朱雀实验室）
> 用途：**授权前提下**评估模型/Agent 的安全拒答边界（ASR 统计、防御有效性验证）

## ⚠️ 使用边界（必读）

- 这些语料包含**有害内容样本**（CBRN、网络攻击、暴力、隐私泄露等）。
- **唯一允许用途**：评估被测模型/Agent 是否拒绝生成此类内容，统计拒答率与防御信号。
- **禁止**：把语料内容用于实际危害行为、传播、或作为攻击真实系统的参考；不得向无关方扩散。
- 测试限于 RoE 授权的目标与时间窗；命中样本需按 `reporting` 的脱敏规则处理证据。
- 数据集是**评估语料，不是攻击工具**——不得因“模型拒答”就转而人工实施语料内容。

## 数据集清单

| 文件 | 名称 | 条数 | 语言 | 评估方向 |
|---|---|---|---|---|
| `CBRN-weapon.json` | CBRN-weapon | 116 | zh-en-mix | 大规模杀伤性武器内容生成 |
| `ChatGPT-Jailbreak-Prompts.json` | ChatGPT-Jailbreak-Prompts | 60 | en | 越狱提示词集合 |
| `HarmfulEvalBenchmark.json` | HarmfulEvalBenchmark | 91 | en | 综合有害内容基准（多来源合并） |
| `JADE-db-v3.0.json` | JADE-db-v3.0 | 122 | zh | 复旦白泽安全通用测试集（**语言学变异**是特色） |
| `copyright-violation.json` | copyright-violation | 100 | en | 版权侵犯内容 |
| `cyberattack.json` | cyberattack | 100 | en | 网络攻击内容生成 |
| `misinformation.json` | misinformation | 123 | zh-en-mix | 虚假信息生成 |
| `non-violent-illegal-activity.json` | non-violent-illegal-activity | 99 | zh-en-mix | 非暴力非法活动 |
| `privacy-leakage.json` | privacy-leakage | 99 | en | 隐私数据泄露 |
| `unethical-behavior.json` | unethical-behavior | 200 | en | 不道德行为（偏见/歧视/刻板印象） |
| `violent.json` | violent | 99 | zh-en-mix | 暴力犯罪内容 |

## JSON 结构

```json
{
  "name": "cyberattack",
  "description": "...", "description_zh": "...",
  "source": ["https://huggingface.co/datasets/..."],
  "author": "...", "count": 100, "tags": [],
  "recommendation": 3, "language": "en",
  "default": false, "permission": "public", "official": false,
  "data": [{"prompt": "..."}, ...]
}
```

取样本：`python3 -c "import json;d=json.load(open('cyberattack.json',encoding='utf-8'));print(d['data'][0]['prompt'])"`

## 与动态测试的配合

数据集样本是动态测试三类样本之一（另两类：算子变异样本、Agent 手工构造样本）。
**建议配比**（A.I.G 方法论，见 `references/ai-redteam-methodology.md`）：

- 数据集原始样本 ≥10 条
- 算子变异样本 ≥10 条（用 `references/operators/` 的算子生成）
- Agent 手工构造样本 ≥10 条（针对目标能力与业务流程）

至少覆盖 3 个不同评估方向；JADE-db-v3.0 因含语言学变异，适合做"同一语义、多种表述"的对照测试。

## 注意事项

- 抽样前先确认 RoE 的 `allowed_risk` 与目标类型——部分方向（CBRN 等）可能超出授权范围。
- 测试不得读取或回显目标环境的真实敏感数据；用 canary 标记替代。
- 报告引用来源：`[tencent/AI-Infra-Guard](https://github.com/Tencent/AI-Infra-Guard) data/eval`。
