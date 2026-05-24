#!/usr/bin/env python3
"""Keep CLAUDE.md's agent-skills <important> block identical to AGENTS.md ## Agent skills.

Canonical source: AGENTS.md from the heading ## Agent skills through end of file.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

IMPORTANT_OPEN = (
    '<important if="you are configuring agent harness, skills, GitHub workflow, '
    'domain docs pointers, or AI coding vocabulary">'
)
IMPORTANT_CLOSE = "</important>"


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def extract_agent_skills(agents_md: str) -> str:
    marker = "## Agent skills\n"
    i = agents_md.find(marker)
    if i == -1:
        alt = "## Agent skills"
        i = agents_md.find(alt)
        if i == -1:
            raise ValueError("AGENTS.md: missing '## Agent skills' section")
        nl = agents_md.find("\n", i)
        if nl == -1:
            raise ValueError("AGENTS.md: malformed '## Agent skills' heading")
        block = agents_md[i : nl + 1] + agents_md[nl + 1 :]
    else:
        block = agents_md[i:]
    return block.rstrip() + "\n"


def inject_into_claude(claude_md: str, agent_skills_block: str) -> str:
    start = claude_md.find(IMPORTANT_OPEN)
    if start == -1:
        raise ValueError(
            "CLAUDE.md: missing agent-skills <important if=\"you are configuring..."
        )
    inner_start = start + len(IMPORTANT_OPEN)
    end = claude_md.find(IMPORTANT_CLOSE, inner_start)
    if end == -1:
        raise ValueError(
            "CLAUDE.md: missing closing </important> for agent-skills block"
        )

    inner = "\n" + agent_skills_block.rstrip("\n") + "\n\n"
    return claude_md[:inner_start] + inner + claude_md[end:]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if CLAUDE.md would change; never write",
    )
    parser.add_argument(
        "--stage",
        action="store_true",
        help="After updating CLAUDE.md, run git add CLAUDE.md",
    )
    args = parser.parse_args()

    root = repo_root()

    # Look for global agent-docs-sync tool
    import os
    import shutil
    global_bin = None
    if shutil.which("agent-docs-sync"):
        global_bin = "agent-docs-sync"
    else:
        fallback = Path.home() / ".local" / "bin" / "agent-docs-sync"
        if fallback.is_file() and os.access(fallback, os.X_OK):
            global_bin = str(fallback)

    if global_bin:
        cmd = [global_bin, "check" if args.check else "sync", "--repo", str(root)]
        if not args.check and args.stage:
            cmd.append("--stage")
        try:
            res = subprocess.run(cmd)
            return res.returncode
        except Exception as e:
            print(f"sync_agent_skills: delegation failed ({e}), falling back to local logic", file=sys.stderr)

    agents_path = root / "AGENTS.md"
    claude_path = root / "CLAUDE.md"

    if not agents_path.is_file():
        print("sync_agent_skills: AGENTS.md not found", file=sys.stderr)
        return 1
    if not claude_path.is_file():
        print("sync_agent_skills: CLAUDE.md not found", file=sys.stderr)
        return 1

    agents_text = agents_path.read_text(encoding="utf-8")
    claude_text = claude_path.read_text(encoding="utf-8")

    try:
        block = extract_agent_skills(agents_text)
        merged = inject_into_claude(claude_text, block)
    except ValueError as e:
        print(f"sync_agent_skills: {e}", file=sys.stderr)
        return 1

    if merged == claude_text:
        return 0

    if args.check:
        print(
            "sync_agent_skills: CLAUDE.md is out of sync with AGENTS.md "
            "## Agent skills — run: python3 scripts/sync_agent_skills.py",
            file=sys.stderr,
        )
        return 1

    claude_path.write_text(merged, encoding="utf-8")
    print("sync_agent_skills: updated CLAUDE.md from AGENTS.md ## Agent skills")
    if args.stage:
        subprocess.run(
            ["git", "-C", str(root), "add", "CLAUDE.md"],
            check=True,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
