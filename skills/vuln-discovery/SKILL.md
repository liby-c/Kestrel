---
name: vuln-discovery
description: 按攻击面列出深度测试清单。触发：资产基线完成、所有端口已入账、需要决定下一步测什么时加载。
metadata:
  layer: "skill"
  risk: "low"
  phase: "vuln-discovery"
  task_types: "pentest"
---

# 漏洞发现 Skill

漏洞发现不靠“全量扫描”，靠“资产基线 → 攻击面 → 漏洞类 → 深度清单”。本技能只做路由，不复制各技能正文。

## 路由

| 攻击面 | 去哪里 |
|---|---|
| 认证 / 上传 / SQLi / XSS / SSRF / XXE / SSTI / 越权 / 业务逻辑 | `../web-pentest/SKILL.md` §7 方向深度清单 |
| 反序列化 / RCE / gadget / 表达式注入 | `../exploitation/SKILL.md` §9 方向深度清单 |
| 接口/API 面 | 本技能 §5 + `../web-pentest/references/web-modern-protocols.md` |
| 版本/CVE | `../cve-triage/SKILL.md` |
| 内网/域/横移 | `../intranet-pentest-advanced/SKILL.md` |
| WAF 拦截 | `../waf-bypass/SKILL.md` |
| 不确定从哪下手 | `../rapid-checklist/SKILL.md` |

## 1. 前置条件

- 资产基线完成：TCP 全端口、每个开放端口有服务/版本/证据（`../recon/SKILL.md`）。
- 账本已建：`plan.md` 的 `## 攻击面账本` 每个资产/端口/服务至少一行。
- 未完成基线不进入漏洞发现；先回 `recon`。

## 2. 接口面发现

- 从页面链接、JS bundle、Swagger/OpenAPI、GraphQL introspection、robots.txt、sitemap 提取接口。
- 按参数类型分类：认证、文件、查询、模板、反序列化、URL 回调。
- 每个接口写入账本一行，状态 `untested`，下一步写测试方法。

## 3. 选择漏洞类

- 按参数语义选类，不按扫描器模板选类。
- 每类挂 `web-pentest` §7 或 `exploitation` §9 的深度清单；清单项 `todo/doing` 不得标 `negative`。
- 扫描器输出只作线索，单一工具结果最多 `candidate`。

## 4. 输出

- 更新账本：接口/参数/类别/状态/证据/下一步。
- 新方向写入 `plan.md` 的 `## 下一步 3 个动作`。
- 确认漏洞立即写 `findings.md`，不攒到最后。

## 5. 方向深度清单（接口面）

一个方向标 `negative` 前，下表适用项必须 `done` 或 `n/a`；`blocked` 必须写已尝试。

状态集合：`todo / doing / done / n/a / blocked`。`todo` / `doing` 不得标 `negative`，不得结束。

| # | 测试项 | 完成判据 |
|---|---|---|
| V1 | 资产/端口/服务 | 每个开放服务至少一行账本 |
| V2 | 接口 × 方法 | GET / POST / PUT / DELETE / OPTIONS |
| V3 | 参数 | 缺失 / 空 / 类型 / 边界 / 注入字符 |
| V4 | 认证态 | 未授权 / 低权 / 高权 |
| V5 | 响应差异 | 状态码 / 长度 / 时间 / 错误 |
| V6 | 文档 / 源码 | Swagger / Actuator / source / backup |
| V7 | 工具 | sqlmap / ffuf 等调用记录；nuclei 用前必须 `nuclei -tl` 确认模板数 > 0，命中记 `candidate` |
