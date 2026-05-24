## Learned User Preferences

- When explaining this codebase, move between abstraction levels (whole pipeline vs byte-level `.fil` layout and tagged `.diag` sections) using this repo’s vocabulary rather than generic radio-astronomy background unless asked.
- For long or large-data runs, default to pre-flight bottleneck and failure-mode review of both the C streaming tools and the Python multibeam/diagnostic path before committing wall time.
- **Graphify:** Do **not** use Gemini for Graphify in this workspace. Leave **`GEMINI_API_KEY`** and **`GOOGLE_API_KEY`** unset when running Graphify; do **not** enable Graphify’s Gemini / `backend="gemini"` semantic path. Prefer deterministic **AST** extraction (`graphify update`, `--watch`), **host‑ or subagent‑driven** semantic work (Cursor / Codex), or **local Ollama** (`graphify extract --backend ollama`) as the approved headless semantic option — see **`docs/agents/domain.md`**. Treat “Graphify semantic extraction defaults to Gemini when keys exist” upstream behavior as **out of scope** here—explicitly avoid that configuration.
- For broad orientation (e.g. zoom-out), prioritize module/caller maps and concrete data-flow edges in this tree over hand-wavy overview.
- **Supertool:** Use the **global** CLI on **`$PATH`** (`~/.local/bin/supertool` → dpt-plugins cache via **`my-skillset`** **`meta/sync-tools.sh`**). Do **not** add a repo-root **`supertool`** symlink or vendored copy; optional project presets belong in **`.supertool.json`** only if reused deliberately.
- Prefer the `~/Developer/research/simple_filtools` path for everyday edits and commands; use the canonical `~/Library/Mobile Documents/com~apple~CloudDocs/Developer-iCloud/research/simple_filtools` spelling only when a tool demands an explicit absolute root or when acting on iCloud retention (Finder “Always Keep on This Mac”), not as a second checkout.
- Git: create commits only when explicitly requested; default **`git push`** target is **`origin`** (fork), not **`upstream`**; **`git fetch upstream`** / merge or rebase before opening PRs unless told otherwise.
- **Claude Code & Codex auth:** Use subscription login only — **`claude`** via **claude.ai / Max** OAuth (keychain); **`codex`** via **`codex login`** / ChatGPT tokens (`auth mode: chatgpt` in **`codex doctor`**). Do **not** set **`ANTHROPIC_API_KEY`** or **`OPENAI_API_KEY`** for repo automation or agent shells. From Cursor agent **`Shell`**, omit **`--bare`** on **`claude -p`** (API-key-only) and append **`< /dev/null`** when the prompt is an argument; run **`codex exec "…" < /dev/null`** — an open stdin pipe makes Codex hang on `Reading additional input from stdin...`. Sanity check: **`claude auth status`** and **`codex doctor`**.

## Learned Workspace Facts

- Core flow: SIGPROC `.fil` → C tools (`rfidiag` writes `.diag` only; `header`, `chop_fil`; unpack helpers); Python reads `.diag` via `diagio` / `plot_diagnostics` / `compare_beam_rfi` (beam/RFI comparison from diagnostics); **`multibeam_clean.py`** rewrites multi-beam **`.fil`** inputs — README / `CLAUDE.md` command table for flags.
- This clone is normally wired **`origin`** → `jakobtfaber/simple_filtools` (fork) and **`upstream`** → `dsa110/simple_filtools`; confirm with `git remote -v`.
- Repo root is the same working copy via **`~/Developer/research/simple_filtools`** and **`~/Library/Mobile Documents/.../Developer-iCloud/research/simple_filtools`**: **`~/Developer/research`** symlinks into Developer‑iCloud **`research/`**, so there is only one checkout on disk.
- Agent-docs CI on the fork: **`.github/workflows/check-agent-sync.yml`** runs **`python3 scripts/sync_agent_skills.py --check`** on PRs and pushes to **`main`/`master`** (validates the mirrored **`## Agent skills`** block only).
- **`make install-hooks`** installs pre-commit → **`sync_agent_skills.py --stage`**, which rewrites **`CLAUDE.md`** when the mirror drifts; deliberate out-of-sync commits (e.g. negative CI tests) need **`git commit --no-verify`**.
- Graphify outputs for this repo live under `graphify-out/` (e.g. `graph.json`, `GRAPH_REPORT.md`, `graph.html`; usually untracked), with the pinned interpreter in `graphify-out/.graphify_python` and scan root in `graphify-out/.graphify_root`. **Never** enable Graphify’s Gemini path for builds here — see **Learned User Preferences**.
- **Graphify + Ollama (approved local semantic):** CLI **`/opt/homebrew/bin/ollama`** (Homebrew, chezmoi **`~/.Brewfile`**); models under **`~/.ollama/models/`** (default **`qwen2.5-coder:7b`**). Headless semantic: `graphify extract <repo-root> --backend ollama --max-concurrency 1`, then `graphify cluster-only <repo-root>`. Unset cloud API keys first; full recipe in **`docs/agents/domain.md`**.
- **Supertool (global only):** `command -v supertool` → `~/.local/bin/supertool` (wired by **`~/Developer/my-skillset/meta/sync-tools.sh`**). No repo-root symlink; `.graphifyignore` lists `supertool` so a stray link is not ingested. Stale `graphify-out/manifest.json` entries for a removed repo-root symlink clear on the next forced rebuild (see **Graphify hygiene** in `docs/agents/domain.md`).
- **Global harness (Claude/Codex):** Short form in **Learned User Preferences** above; long-form in **`~/CLAUDE.md`** / **`~/AGENTS.md`** and **`~/.cursor/rules/*-cursor-shell.mdc`**; full runbook **`~/Developer/reference/cursor-agent-shell-cli-insights.md`** (argv-vs-stdin, stream-json, diagnostics).
- **Machine-wide runner:** Lives in dotfiles repo (`agent-docs-sync`, registry `~/.config/agent-docs/repos.toml`); repo Makefile and CI remain canonical for portable fork execution.

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
