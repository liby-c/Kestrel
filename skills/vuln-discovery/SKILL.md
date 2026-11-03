---
name: vuln-discovery
description: 漏洞发现流程 — 基于信息收集结果扫描漏洞
metadata:
  layer: "L1"
  risk: "L1"
  phase: "vuln-discovery"
  task_types: "pentest"
---

# 漏洞发现 Skill

基于信息收集结果，系统性地发现目标存在的安全漏洞。

## 执行步骤

### 1. 已知 CVE 匹配
- 根据已识别的服务版本搜索对应 CVE
- 优先关注 Critical/High 级别
- 记录 CVE ID、影响版本、利用条件

### 2. Web 漏洞扫描
- SQL 注入检测
- XSS 检测（反射型/存储型/DOM型）
- SSRF 检测
- LFI/RFI 检测
- 命令注入检测
- 文件上传漏洞检测

### 3. 配置缺陷检测
- 默认凭据测试
- 信息泄露检测
- 未授权访问检测
- CORS 配置检测
- HTTPS 配置检测

### 4. 输出
- 漏洞列表（类型、严重等级、URL、参数、验证方法）

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
| V7 | 工具 | nuclei / sqlmap / ffuf 等调用记录 |
