---
name: redteam-playbooks
description: 红队实战方法论补充（Claude-Red 精选）— 竞态/请求走私/GraphQL/HPP/反序列化/JWT/OAuth/API/业务逻辑/云/容器/K8s/CI-CD 密钥/快速 triage；用于补齐现有 Web/API/内网技能的缺口
metadata:
  layer: "L2"
  risk: "L2"
  phase: "vuln-discovery,exploitation"
  target_types: "web,api,auth,cloud,container,cicd"
  task_types: "pentest"
  vulnerability_classes: "race_condition,request_smuggling,graphql,parameter_pollution,deserialization,jwt,oauth,api,cloud,container,k8s,cicd_secrets,business_logic"
---

# 红队实战方法论（Claude-Red 精选）

本技能把 [Claude-Red](https://github.com/SnailSploit/claude-red)（MIT）中**当前工程缺口最大**的
方法论并入本框架。它不是替代现有技能，而是补齐：

- 竞态条件 / 请求走私 / GraphQL / HTTP 参数污染；
- 反序列化 / JWT / OAuth / API 安全；
- 业务逻辑、云、容器/K8s、CI/CD 密钥；
- 快速 triage。

> 来源：Claude-Red，作者 SnailSploit / Kai Aizen，MIT License。
> 许可证原文见 `references/CLAUDE-RED-LICENSE.md`。
> 本技能只做格式与路由适配；技术内容的最终判定仍以 `findings.md` 的证据、`plan.md` 的账本与 `roe.yaml` 的 `scope` 为准。

## 场景路由

| 场景 | 先读 |
|---|---|
| 竞态 / TOCTOU / 并发兑换 / 限额绕过 | `references/claude-red-race-condition.md` |
| HTTP 请求走私 / CL.TE / TE.CL / H2 desync | `references/claude-red-request-smuggling.md` |
| GraphQL introspection / batching / alias IDOR | `references/claude-red-graphql.md` |
| HTTP 参数污染 / WAF 绕过 / 逻辑混淆 | `references/claude-red-parameter-pollution.md` |
| Java/PHP/.NET 反序列化链 | `references/claude-red-deserialization.md` |
| JWT alg:none / 密钥混淆 / kid/jku | `references/claude-red-jwt.md` |
| OAuth/OIDC redirect_uri / PKCE / token 泄露 | `references/claude-red-oauth.md` |
| REST/gRPC/WebSocket API、BOLA/BFLA/批量赋值 | `references/claude-red-api-security.md` |
| 价格/优惠券/流程/多步业务逻辑 | `references/claude-red-business-logic.md` |
| AWS/Azure/GCP / IMDS / 跨账号 | `references/claude-red-cloud.md` |
| 容器逃逸 | `references/claude-red-container-escape.md` |
| Kubernetes 集群攻击 | `references/claude-red-k8s-attacks.md` |
| CI/CD 密钥提取 / pipeline 滥用 | `references/claude-red-cicd-secrets.md` |
| 快速 triage / 检查顺序 | `references/claude-red-fast-checking.md` |

## 使用纪律

1. **只读相关单篇**，不要一次加载全部 references；
2. 先看对应 `references/claude-red-*.md` 的证据要求，再用本技能补充技术路径；
3. 任何主动操作仍受 `roe.yaml` 的 `scope` / `allowed_risk` 约束；⚠️ 操作逐次授权并记 `approvals.md`；L4-⚠️ 授权即执行；L4-⛔ 授权后停下、回复确认才执行；
4. 破坏性/不可逆步骤（覆盖文件、系统级持久化、批量导出）按 `pentest-flow` 的「不可逆写入」判定；覆盖业务文件/证书/密钥 L4-⛔；用户级持久化 L3 ✅；系统级持久化 L4-⚠️；
5. 发现必须立即写入 `findings.md`；`confirmed` 必须有证据；疑似副作用当轮披露；
6. 不与现有技能冲突：`web-security-advanced` / `intranet-pentest-advanced` / `ai-mcp-security`
   仍是主知识库，本技能只补缺口。

## 参考文档

- `references/claude-red-*.md` — 14 篇精选方法论；
- `references/CLAUDE-RED-LICENSE.md` — MIT 许可证与归属。
