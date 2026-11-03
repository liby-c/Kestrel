---
name: recon
description: 信息收集流程 — 被动+主动侦察
metadata:
  layer: "L1"
  risk: "L1"
  phase: "recon"
  task_types: "recon"
---

# 信息收集 Skill

执行被动和主动信息收集，构建目标画像和攻击面地图。

## 执行步骤

### 1. 被动侦察
- 通过 Bash + curl 访问目标，收集 HTTP 响应头
- 识别服务器类型、版本、WAF
- 分析 HTML 源码中的技术栈标识

### 2. 端口扫描（两段式，强制）

先用限速全端口扫描拿开放端口清单，再只对开放端口做详细识别。不要一上来就 `-sV -sC -A` 全端口——那是几小时级的等待。

**第一段：限速全端口**（TCP，3000 pps 约 20-40 秒）

```bash
# 全端口用 RoE 的 scan_rate（默认 3000）；root 用 -sS，非 root 用 -sT。
nmap -n -Pn -sS -T3 --max-rate 3000 --max-retries 1 -p- <target> -oN evidence/src/nmap_allports.txt
# 开放端口提取
grep -E '^[0-9]+/tcp' evidence/src/nmap_allports.txt | awk '{print $1,$2,$3}'
```

**第二段：只对开放端口详细识别**（-sV 版本 / -sC 脚本 / -O 系统指纹）

```bash
# 服务识别用 RoE 的 max_rate（默认 1000），不跟随全端口提速。
nmap -n -Pn -sV -sC --version-intensity 5 --max-rate 1000 -p <逗号分隔的开放端口> <target> -oN evidence/src/nmap_services.txt
```

硬性要求：

1. **先 `-p-` 后 `-sV`，顺序不许反**；第二段的 `-p` 列表必须来自第一段的结果，不得凭常见端口表猜。
2. **两段输出都落盘** `evidence/src/`，第二段不做完不算侦察结束。
3. **UDP 按需，不是强制**：目标有 UDP 迹象（DNS/SNMP/NTP/VPN 等）且 RoE 允许时，做 `nmap -n -Pn -sU --top-ports 100 --max-rate 100 <target>`；不做写 `n/a` + 原因。UDP 无响应/被限速时标 `blocked`，不阻塞结束。
4. `filtered` 端口单独记一行进 `plan.md`——它们是防火墙策略的情报，不是「没扫到」。
5. **限速**：全端口默认 `-T3 --max-rate 3000`（RoE `scan_rate`），服务识别 `--max-rate 1000`（RoE `max_rate`）；敏感/WAF/云目标降到 100-300；被拉黑时继续降速。不要用 `--min-rate 3000` 或 `-T4` 做资产绘制。
6. 每个开放端口必须有资产记录（服务/版本/HTTP title/证据）；没识别出来写 `unknown`，不能跳过。
7. **封禁检测**：扫描前用已知开放端口做基线（`curl -m 5`），扫描中每 1-2 分钟复测；出现超时/连接拒绝立即停扫，等待 5-15 分钟，降速重试；仍不通标 `blocked`，记 `notes.md`，不得连续重扫。

### 3. 服务与技术栈识别
- 前端框架（React/Vue/Angular/jQuery）
- 后端框架（Express/Django/Flask/Spring）
- CMS 系统（WordPress/Joomla/自定义）
- 数据库类型

### 4. Web 层枚举
- 被动发现优先：页面链接、robots.txt、sitemap、敏感文件（.env, .git）
- 目录爆破（ffuf/gobuster/dirsearch）按 L3 ✅ 直接做；控制速率，不中断服务
- 发现 API 端点

### 4.5 AI 组件识别（本地指纹库）

目标涉及 LLM、AI 平台、Agent 框架、MCP Server、向量库或推理服务时，用本地指纹库加速识别：

`data/aig-fingerprints/` — 168 个 AI 组件指纹规则（来源：腾讯朱雀实验室 AI-Infra-Guard，MIT）

1. 读 `data/aig-fingerprints/INDEX.md`，按类别定位候选组件；
2. 读 `<组件>.yaml`，按其中 `http[].method` + `path` 用 `curl` 探测，按 `matchers` 判定命中，
   按 `version[].extractor.regex` 提取版本；
3. 命中后把 `组件 + 版本` 交给 `cve-triage`（其 `cve-triage/data/aig-vuln/` 为同源 CVE 库，覆盖 142 个 AI 组件）。

注意：**指纹命中只证明组件暴露，不等于存在漏洞**；版本提取失败时不得推断 CVE 适用性。

### 5. 资产基线

侦察的输出不是“端口清单”，是“每个开放端口一行”的资产基线。未完成不得进入利用。

```text
| 端口/协议 | 服务 | 版本 | HTTP title/技术栈 | 证据 | 状态 |
|---|---|---|---|---|---|
| 22/tcp   | ssh  | OpenSSH 8.9p1 | - | evidence/src/nmap_services.txt | confirmed |
| 6006/tcp | http | TensorBoard 2.21.0 | TensorBoard | evidence/src/tensorboard_env.txt | confirmed |
| 30921/tcp| https| unknown | - | evidence/src/tls_30921.txt | unknown |
```

- 每个开放端口一行；未知服务写 `unknown`，并在「下一步」写探测方法。
- 每个 HTTP/HTTPS 端口至少有一次响应头 + title；TLS 端口记录证书 subject/issuer/SAN。
- 每个端口的探测原始输出（nmap/curl/TLS）落盘 `evidence/src/`，不只写摘要。
- `plan.md` 攻击面账本每个开放端口至少一行；不能只写“发现多个服务”。
- 基线完成 = TCP `-p-` + 每个开放端口已做服务识别/HTTP 探测 + 原始输出落盘；UDP 按需（`n/a` 有原因）。
- 进入 `exploitation` / 投递利用 payload 前基线必须完成；可以并行做被动探测。
- 某路径 `blocked` 时，从基线表挑下一个未测服务继续，不得因单点阻塞结束。

### 6. 输出
- 资产基线表（上面）
- 目标画像（IP/域名/端口/服务/技术栈）
- 攻击面地图（可访问路径、API、管理入口）
- 开放端口清单（含 `filtered` 项）+ nmap 原始输出路径（全端口、服务识别、UDP）

### 7. 工具结果复核

工具输出是线索，不是结论。**单一工具结果最多 `candidate`；`confirmed` 需要原始响应 + 第二种独立信号或可复现回显。**

| 工具 | 常见不可靠点 | 二次确认 |
|---|---|---|
| nmap `-sV` | 服务名可能是猜测（X11 / iwg1 / Ajenti） | HTTP title/API、TLS 证书、应用版本 |
| whatweb / httpx | Header、title 可伪造或被 CDN/WAF 改写 | 响应体、JS、API |
| 版本 banner / JS bundle | 代理、回代补丁、依赖版本（如 AntD） | 应用 `/version`、静态文件、包信息 |
| nuclei / nikto / wpscan | 模板误报 | 手工请求复现 |
| ffuf / gobuster | soft 404、通配符 | 与基线响应对比 |
| DNS / 子域 | 泛解析 | 解析 + HTTP 验证 |
| UDP / filtered | 无响应 ≠ 关闭 | 标 `blocked / inconclusive`，写原因 |
| TLS 证书 | issuer 可能通用或伪造 | 结合 HTTP 指纹 |
| HTTP 状态码 | 200 可能是通用响应；GET/POST 语义不同 | 看响应体、认证逻辑、实际方法 |

高影响结论（RCE / 认证绕过 / 版本-CVE / 数据导出）必须二次确认；低危信息可以保留 `candidate`。
