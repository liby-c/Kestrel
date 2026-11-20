#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kestrel 可选静态检查工具。

用法：
    python3 tools/check_artifacts.py <Work/OC-target>
    python3 tools/check_artifacts.py --check-tmp <Work/OC-target>
    Windows: python tools/check_artifacts.py <Work/OC-target>

退出码：0 = 结构 PASS，1 = FAIL，2 = 参数错误。

这不是结束门禁。结束条件以 plan.md 的结束检查表和用户确认为准；
本工具只检查结构，不检查证据真实性，也不能证明测试质量。
"""

import os
import re
import sys

REQUIRED_SECTIONS = [
    "## 攻击面账本",
    "## 技能加载",
    "## 深度清单",
    "## 覆盖清单",
    "## 复盘",
    "## 结束检查",
]
LEDGER_STATUSES = {"untested", "testing", "confirmed", "candidate", "negative", "blocked", "n/a"}
CHECK_STATUSES = {"todo", "doing", "done", "n/a", "blocked"}
WEB_STATUSES = {"confirmed", "candidate", "negative", "blocked", "not_applicable"}
WEB_CATEGORIES = [
    "sqli", "xss", "csrf", "idor", "auth_bypass", "file_upload",
    "path_traversal", "ssrf", "xxe", "ssti", "deserialization",
    "request_smuggling", "race_condition", "info_disclosure",
    "business_logic", "default_credential", "cve",
]

# 只匹配绝对临时路径；相对路径 evidence/src/tmp/ 不算。
TMP_PAT = re.compile(r"(?<![\w:/])/(?:var/)?tmp/|(?<![\w:/])/dev/shm/")
# 否定句豁免：只保留明确的否定词，避免“检查 /tmp”这类句子被误豁免。
NEGATION = re.compile(r"不写|禁止|不得|不要|避免|没有|无需|no\b|not\b", re.I)
SKIP_TMP_DIRS = (
    ".bun-",
    "hsperfdata",
    "node-compile-cache",
    "opencode",
    "systemd-private",
    ".X11-unix",
    "codeg-delegation",
    "codeg-acp",
)
TMP_MAX_FILES = 5000
TMP_MAX_DEPTH = 2


def read_text(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except FileNotFoundError:
        return None


def parse_section_table(text, heading):
    """返回 heading 之后第一张 Markdown 表的 (header, rows)。"""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start = i + 1
            break
    if start is None:
        return None, []

    header = None
    rows = []
    for line in lines[start:]:
        s = line.strip()
        if s.startswith("## ") or s.startswith("### "):
            break
        if not s.startswith("|"):
            # 表头之后出现非表格行，说明这张表已结束；
            # 不再继续扫描后续表格，避免把下一节表误当本节表。
            if header is not None:
                break
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if cells and all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        rows.append(cells)
    return header, rows


def section_lines(text, heading):
    """返回 heading 到下一个 ## / ### 之间的原始行。"""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start = i + 1
            break
    if start is None:
        return []
    out = []
    for line in lines[start:]:
        s = line.strip()
        if s.startswith("## ") or s.startswith("### "):
            break
        out.append(line)
    return out


def col(header, name):
    if not header:
        return None
    for i, h in enumerate(header):
        if name in h:
            return i
    return None


def cell(row, idx):
    if idx is None or idx >= len(row):
        return ""
    return row[idx].strip()


def is_empty(value):
    return value in ("", "-", "—", "n/a", "N/A", "无")


def lint(work, check_tmp=False):
    issues = []
    warnings = []

    if not os.path.isdir(work):
        return ["工作目录不存在: " + work], warnings

    roe_path = os.path.join(work, "roe.yaml")
    plan_path = os.path.join(work, "plan.md")
    findings_path = os.path.join(work, "findings.md")

    if not os.path.isfile(roe_path):
        issues.append("roe.yaml 缺失")
    plan = read_text(plan_path)
    findings = read_text(findings_path)
    if plan is None:
        issues.append("plan.md 缺失")
        plan = ""
    if findings is None:
        issues.append("findings.md 缺失")
        findings = ""

    for section in REQUIRED_SECTIONS:
        if section not in plan:
            issues.append("plan.md 缺少章节: " + section)

    # 攻击面账本
    ledger_header, ledger_rows = parse_section_table(plan, "## 攻击面账本")
    if ledger_header is None:
        issues.append("plan.md 无 ## 攻击面账本 表")
        ledger_rows = []
    else:
        status_idx = col(ledger_header, "状态")
        evidence_idx = col(ledger_header, "证据")
        next_idx = col(ledger_header, "下一步")
        if status_idx is None:
            issues.append("攻击面账本缺少「状态」列")
        for n, row in enumerate(ledger_rows, 1):
            status = cell(row, status_idx).lower()
            if not status:
                issues.append("账本第 %d 行状态为空" % n)
                continue
            if status not in LEDGER_STATUSES:
                issues.append("账本第 %d 行状态非法: %s" % (n, status))
            if status == "untested":
                issues.append("账本第 %d 行仍为 untested: %s" % (n, " | ".join(row)[:160]))
                if is_empty(cell(row, next_idx)):
                    issues.append("账本第 %d 行 untested 但无下一步" % n)
            if status in ("confirmed", "negative", "candidate"):
                if is_empty(cell(row, evidence_idx)):
                    issues.append("账本第 %d 行 %s 但无证据" % (n, status))
            if status == "blocked":
                blob = cell(row, evidence_idx) + " " + cell(row, next_idx)
                if "已尝试" not in blob and "尝试" not in blob:
                    issues.append("账本第 %d 行 blocked 但无已尝试说明" % n)

    # 深度清单
    header, rows = parse_section_table(plan, "## 深度清单")
    if header is None:
        issues.append("plan.md 无 ## 深度清单 表")
    else:
        status_idx = col(header, "状态")
        if status_idx is None:
            issues.append("深度清单缺少「状态」列")
        for n, row in enumerate(rows, 1):
            status = cell(row, status_idx).lower()
            if not status:
                issues.append("深度清单第 %d 行状态为空" % n)
                continue
            if status not in CHECK_STATUSES:
                issues.append("深度清单第 %d 行状态非法: %s" % (n, status))
            if status in ("todo", "doing"):
                issues.append("深度清单第 %d 行仍为 %s" % (n, status))
            if status == "blocked":
                blob = " ".join(row)
                if "已尝试" not in blob and "尝试" not in blob:
                    issues.append("深度清单第 %d 行 blocked 但无已尝试说明" % n)

    # 是否为 Web 目标：账本/发现中出现 HTTP 或 Web 类服务
    text_all = (plan + "\n" + findings).lower()
    service_text = ""
    if ledger_header:
        svc_idx = col(ledger_header, "服务")
        service_text = " ".join(cell(r, svc_idx) for r in ledger_rows).lower()
    web_like = (
        "http://" in text_all
        or "https://" in text_all
        or any(k in service_text for k in ("http", "web", "nginx", "tomcat", "apache", "iis", "spring"))
    )

    # 覆盖清单：Web 目标必须覆盖 17 类，每类有状态
    header, rows = parse_section_table(plan, "## 覆盖清单")
    if header is None:
        issues.append("plan.md 无 ## 覆盖清单 表")
    else:
        cat_idx = col(header, "类别")
        status_idx = col(header, "状态")
        if cat_idx is None or status_idx is None:
            issues.append("覆盖清单缺少「类别」或「状态」列")
        else:
            seen = {}
            for n, row in enumerate(rows, 1):
                cat = cell(row, cat_idx).lower()
                status = cell(row, status_idx).lower()
                if not cat:
                    issues.append("覆盖清单第 %d 行类别为空" % n)
                    continue
                seen[cat] = status
                if status not in WEB_STATUSES:
                    issues.append("覆盖清单第 %d 行状态非法: %s" % (n, status))
            if web_like:
                missing = [c for c in WEB_CATEGORIES if c not in seen]
                if missing:
                    issues.append("覆盖清单缺少 Web 类别: " + ", ".join(missing))

    # 技能加载表：只查存在与非空。
    # 具体该加载哪些技能由 skills/pentest-flow/SKILL.md 的「技能路由」信号表定义，
    # 属于规则内容，不在检查器里复制。
    header, rows = parse_section_table(plan, "## 技能加载")
    if header is None:
        issues.append("plan.md 无 ## 技能加载 表")
    elif not rows:
        issues.append("## 技能加载 表为空")

    # 5 轮有效复盘：至少 5 条列表项，每条要有账本/清单/证据/理由等记录
    review_lines = section_lines(plan, "## 复盘")
    review_items = [
        l.strip() for l in review_lines
        if re.match(r"^([-*]|\d+[.、])\s*", l.strip())
    ]
    if len(review_items) < 5:
        issues.append("复盘记录不足 5 条: %d" % len(review_items))
    else:
        weak = []
        for i, item in enumerate(review_items, 1):
            if not re.search(r"账本|清单|证据|negative|blocked|理由|轮", item, re.I):
                weak.append(str(i))
        if weak:
            issues.append("复盘第 %s 条缺少账本/清单/证据/理由记录" % ", ".join(weak))

    # 结束检查：至少 12 条记录，且不得有 FAIL
    end_items = [l.strip() for l in section_lines(plan, "## 结束检查") if l.strip()]
    if len(end_items) < 12:
        issues.append("结束检查记录不足 12 条: %d" % len(end_items))
    if any("FAIL" in l.upper() for l in end_items):
        issues.append("结束检查存在 FAIL 项")

    # /tmp 引用：只检查 agent 产物四文件
    for name in ("plan.md", "findings.md", "notes.md", "approvals.md"):
        text = read_text(os.path.join(work, name)) or ""
        for lineno, line in enumerate(text.splitlines(), 1):
            if TMP_PAT.search(line) and not NEGATION.search(line):
                issues.append("%s:%d 引用临时目录: %s" % (name, lineno, line.strip()[:160]))

    # 禁止 report.md
    if os.path.exists(os.path.join(work, "report.md")):
        issues.append("存在 report.md（禁止）")

    # confirmed 必须有证据，且证据文件真实存在
    for block in re.split(r"(?m)^##\s+F-", findings)[1:]:
        lines = block.splitlines()
        title = lines[0].strip() if lines else ""
        is_confirmed = bool(
            re.search(r"(?m)^##\s+F-.*\bconfirmed\b", block)
            or re.search(r"(?m)^\s*-\s*状态[：:]\s*confirmed\b", block)
        )
        has_evidence = re.search(r"证据(?:路径)?[：:]|evidence/|\|\s*证据(?:路径)?\s*\|", block) is not None
        if is_confirmed and not has_evidence:
            issues.append("findings 中 confirmed 无证据: F-" + title[:60])
        if is_confirmed:
            for rel in re.findall(r"evidence/[A-Za-z0-9._/\-]+", block):
                rel = rel.rstrip(".,;:)")
                if "*" in rel or "?" in rel:
                    continue
                if not os.path.exists(os.path.join(work, rel)):
                    issues.append("findings 证据文件不存在: " + rel)

    # 本地临时目录较新文件（WARN，默认关闭；--check-tmp 开启）
    if check_tmp and os.path.isfile(roe_path):
        try:
            roe_mtime = os.path.getmtime(roe_path)
        except OSError:
            roe_mtime = None
        if roe_mtime:
            for base in ("/tmp", "/var/tmp", "/dev/shm"):
                if not os.path.isdir(base):
                    continue
                count = 0
                stop = False
                for root, dirs, files in os.walk(base):
                    # 限制深度，避免在共享机/容器上遍历整棵临时目录树
                    if root[len(base):].count(os.sep) >= TMP_MAX_DEPTH:
                        dirs[:] = []
                    dirs[:] = [d for d in dirs if not any(x in d for x in SKIP_TMP_DIRS)]
                    for filename in files:
                        count += 1
                        if count > TMP_MAX_FILES:
                            warnings.append("临时目录扫描超过 %d 个文件，已停止: %s" % (TMP_MAX_FILES, base))
                            stop = True
                            break
                        path = os.path.join(root, filename)
                        try:
                            if os.path.getmtime(path) > roe_mtime:
                                warnings.append("临时目录有较新文件: " + path)
                        except OSError:
                            pass
                    if stop:
                        break

    return issues, warnings


def main():
    # Windows 控制台默认 GBK，统一按 UTF-8 输出，避免中文乱码
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check_tmp = "--check-tmp" in sys.argv[1:]
    if len(args) != 1:
        print("usage: check_artifacts.py [--check-tmp] <Work/OC-target>")
        return 2
    work = args[0]
    issues, warnings = lint(work, check_tmp=check_tmp)
    for warning in warnings[:20]:
        print("WARN: " + warning)
    if len(warnings) > 20:
        print("WARN: ... 另有 %d 条" % (len(warnings) - 20))
    if issues:
        print("FAIL: %d issue(s)" % len(issues))
        for issue in issues:
            print("- " + issue)
        return 1
    print("STRUCTURE PASS (not an end-of-engagement gate): " + work)
    return 0


if __name__ == "__main__":
    sys.exit(main())