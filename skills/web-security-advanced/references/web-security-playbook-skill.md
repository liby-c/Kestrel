---
name: web-security-playbook
description: Authorized web security reference for selecting attack categories, payload families, bypass notes, workflow summaries, and mitigations across web, API, JWT, cloud, AI, framework, and WebSocket testing. Use for pentest planning, report drafting, or converting the extracted wiki into narrower web-focused skills.
---

# Web Security Playbook

Use this skill for authorized security testing, defense validation, training, or documentation work.

## When To Use

- The user needs a category-level web testing playbook rather than a single exploit recipe.
- The task involves choosing among multiple web attack families, payload styles, or bypass approaches.
- The user wants to turn the extracted wiki into narrower skills, checklists, notes, or reports.

## When Not To Use

- A narrower existing skill already covers the request better.
- The task is primarily internal network, AD, Windows, Exchange, or SharePoint work.
- The user only needs a tool cheat sheet rather than attack-family guidance.

## Workflow

1. Start with `web-playbook-index.md`, then narrow to 1-3 relevant category files.
2. If the request still spans multiple attack families, keep the answer grouped by category instead of by individual payload.
3. If a specific payload entry is needed, use the packaged reference entries in `references/`; any extracted source path still shown in entries should be treated as provenance only.
4. Return only the payload families, variants, prerequisites, bypass notes, OPSEC notes, and mitigations that match the authorized scope.
5. When writing a new skill, checklist, or report, rewrite the selected material into the target format instead of copying whole reference files.

## Category Map

- 点击劫持: `web-playbook-01-clickjacking.md`
- 供应链攻击: `web-playbook-02-supply-chain-attacks.md`
- 缓存与CDN安全: `web-playbook-03-cache-and-cdn-security.md`
- 开放重定向: `web-playbook-04-open-redirect.md`
- 框架漏洞: `web-playbook-05-framework-vulnerabilities.md`
- 请求走私: `web-playbook-06-request-smuggling.md`
- 认证漏洞: `web-playbook-07-authentication-vulnerabilities.md`
- 文件漏洞: `web-playbook-08-file-vulnerabilities.md`
- 业务逻辑漏洞: `web-playbook-09-business-logic-vulnerabilities.md`
- 原型链污染: `web-playbook-10-prototype-pollution.md`
- 云安全漏洞: `web-playbook-11-cloud-security-vulnerabilities.md`
- AI安全: `web-playbook-12-ai-security.md`
- API安全: `web-playbook-13-api-security.md`
- CSRF跨站请求伪造: `web-playbook-14-csrf-cross-site-request-forgery.md`
- JWT安全: `web-playbook-15-jwt-security.md`
- LFI/RFI文件包含: `web-playbook-16-lfi-rfi-file-inclusion.md`
- RCE远程代码执行: `web-playbook-17-rce-remote-code-execution.md`
- SQL/NoSQL注入: `web-playbook-18-sql-nosql-injection.md`
- SSRF服务端请求伪造: `web-playbook-19-ssrf-server-side-request-forgery.md`
- SSTI模板注入: `web-playbook-20-ssti-template-injection.md`
- WebSocket安全: `web-playbook-21-websocket-security.md`
- XSS跨站脚本: `web-playbook-22-xss-cross-site-scripting.md`
- XXE实体注入: `web-playbook-23-xxe-entity-injection.md`

## Notes

- Prefer 1-3 categories per request, not the whole corpus.
- Use `web-playbook-index.md` as the first stop for category selection.
- Use source markdown files for detailed commands and tutorial text.
- Keep outputs scoped to the user's target stack and authorization.

