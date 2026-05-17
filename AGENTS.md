## Learned User Preferences

- When explaining this codebase, move between abstraction levels (whole pipeline vs byte-level `.fil` layout and tagged `.diag` sections) using this repo’s vocabulary rather than generic radio-astronomy background unless asked.
- For long or large-data runs, default to pre-flight bottleneck and failure-mode review of both the C streaming tools and the Python multibeam/diagnostic path before committing wall time.
- **Graphify:** Do **not** use Gemini for Graphify in this workspace. Leave **`GEMINI_API_KEY`** and **`GOOGLE_API_KEY`** unset when running Graphify; do **not** enable Graphify’s Gemini / `backend="gemini"` semantic path. Prefer deterministic **AST** extraction, code-only / incremental flows, **`--watch`** on code, and **host‑ or subagent‑driven** semantic extraction (Cursor / Codex) instead of Gemini-backed Graphify APIs. Treat “Graphify semantic extraction defaults to Gemini when keys exist” upstream behavior as **out of scope** here—explicitly avoid that configuration.
- For broad orientation (e.g. zoom-out), prioritize module/caller maps and concrete data-flow edges in this tree over hand-wavy overview.
- Prefer the `~/Developer/research/simple_filtools` path for everyday edits and commands; use the canonical `~/Library/Mobile Documents/com~apple~CloudDocs/Developer-iCloud/research/simple_filtools` spelling only when a tool demands an explicit absolute root or when acting on iCloud retention (Finder “Always Keep on This Mac”), not as a second checkout.

## Learned Workspace Facts

- Core flow: SIGPROC `.fil` → C tools (`rfidiag` writes `.diag` only; `header`, `chop_fil`; unpack helpers); Python reads `.diag` via `diagio` / `plot_diagnostics` / `compare_beam_rfi` (beam/RFI comparison from diagnostics); **`multibeam_clean.py`** rewrites multi-beam **`.fil`** inputs — README / `CLAUDE.md` command table for flags.
- This clone is normally wired **`origin`** → `jakobtfaber/simple_filtools` (fork) and **`upstream`** → `dsa110/simple_filtools`; confirm with `git remote -v`.
- Repo root is the same working copy via **`~/Developer/research/simple_filtools`** and **`~/Library/Mobile Documents/.../Developer-iCloud/research/simple_filtools`**: **`~/Developer/research`** symlinks into Developer‑iCloud **`research/`**, so there is only one checkout on disk.
- Graphify outputs for this repo live under `graphify-out/` (e.g. `graph.json`, `GRAPH_REPORT.md`, `graph.html`), with the pinned interpreter in `graphify-out/.graphify_python` and scan root in `graphify-out/.graphify_root`. **Never** enable Graphify’s Gemini path for builds here — see **Learned User Preferences**.

## Agent skills

### Issue tracker

Issues use GitHub (`dsa110/simple_filtools`); use `gh` per `docs/agents/issue-tracker.md`.

### Triage labels

Default Matt Pocock five-role strings; see `docs/agents/triage-labels.md`.

### Domain docs

Single-context: root `CONTEXT.md` and `docs/adr/` when present; see `docs/agents/domain.md`.

### AI coding vocabulary

Shared jargon for AI-assisted development (handoffs, skills, AFK, attention budget): see `docs/agents/ai-coding-vocabulary.md`.

---

**Maintainer sync (`AGENTS.md` ↔ `CLAUDE.md`):** **`AGENTS.md`** is canonical for **`## Agent skills`** (Issue tracker through this paragraph). The same block must appear **verbatim** in **`CLAUDE.md`** inside `<important if="you are configuring agent harness, skills, GitHub workflow, domain docs pointers, or AI coding vocabulary">`. Edit **`AGENTS.md`** first; run **`python3 scripts/sync_agent_skills.py`** to rewrite **`CLAUDE.md`**, or install **`make install-hooks`** so **`pre-commit`** runs that sync (**`--stage`**) every commit.
