#!/usr/bin/env python3
"""检查技能新增资产的上下文预算（ai-mcp-security / post-exploitation）。

只检查本轮新增/扩展的参考文件，不要求技能运行时使用。
退出码：0 = PASS，1 = 超预算或文件缺失，2 = 参数错误。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "ai-mcp-security"
POST = ROOT / "skills" / "post-exploitation"

# 行数上限：检测清单按设计预算；算子按现有体例给 90 行余量。
CAPS = {
    "references/sources/INDEX.md": 40,
    "references/sources/mcp-and-tools.md": 60,
    "references/sources/agents-and-frameworks.md": 80,
    "references/sources/policy-approval.md": 60,
    "references/sources/context-memory.md": 60,
    "references/agent-attack-chains.md": 100,
    "references/agent-framework-matrix.md": 80,
    "references/agent-detections/mcp-tool-poisoning-detection.md": 105,
    "references/agent-detections/agent-policy-bypass-detection.md": 100,
    "references/agent-detections/instruction-file-injection-detection.md": 80,
    "references/agent-detections/context-compaction-poisoning-detection.md": 100,
    "references/operators/mcp_description_poison.md": 90,
    "references/operators/repo_instruction_injection.md": 90,
    "references/operators/tool_arg_smuggle.md": 90,
    "references/operators/approval_forgery.md": 90,
    "references/operators/approval_fatigue.md": 90,
    "references/operators/context_compaction_seed.md": 90,
    "references/operators/subagent_delegation_abuse.md": 90,
}

POST_CAPS = {
    "references/shell-stabilization.md": 150,
    "references/shell-stabilization-containers.md": 150,
    "references/shell-stabilization-linux.md": 150,
    "references/shell-stabilization-windows.md": 150,
    "references/shell-stabilization-file-transfer.md": 150,
    "references/shell-stabilization-c2.md": 150,
    "references/cleanup-ledger.md": 100,
}


def check_source_ids() -> list[str]:
    """校验技能内所有 [Sxx] 引用都能在 references/sources/ 找到。"""
    src_dir = SKILL / "references" / "sources"
    known: set[str] = set()
    for path in src_dir.glob("*.md"):
        known |= set(re.findall(r"\| (S\d{2}) \|", path.read_text(encoding="utf-8")))

    missing: list[str] = []
    targets = [SKILL / "SKILL.md", *(SKILL / "references").rglob("*.md")]
    for path in targets:
        if src_dir in path.parents:
            continue
        refs = set(re.findall(r"\[(S\d{2})\]", path.read_text(encoding="utf-8")))
        for ref in sorted(refs - known):
            missing.append(f"{path.relative_to(SKILL)}:{ref}")
    return missing


def main() -> None:
    failures = []
    total = 0
    for skill_dir, caps in ((SKILL, CAPS), (POST, POST_CAPS)):
        for rel, cap in caps.items():
            total += 1
            path = skill_dir / rel
            label = f"{skill_dir.name}/{rel}"
            if not path.exists():
                print(f"MISS {label}")
                failures.append(label)
                continue
            lines = len(path.read_text(encoding="utf-8").splitlines())
            status = "OK" if lines <= cap else "OVER"
            print(f"{status:4} {lines:4}/{cap:<4} {label}")
            if lines > cap:
                failures.append(label)
    broken = check_source_ids()
    if broken:
        print("BROKEN SOURCE IDS:")
        for item in broken:
            print(f"  {item}")
        failures.extend(broken)

    if failures:
        print(f"FAIL: {len(failures)} issue(s)")
        sys.exit(1)
    print(f"PASS: {total} files within budget; source IDs OK")
    sys.exit(0)


if __name__ == "__main__":
    main()
