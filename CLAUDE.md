# CLAUDE.md

Standalone C + Python utilities for **SIGPROC filterbank** (`.fil`) data: streaming diagnostics to `.diag`, time slicing, header inspection, multi-beam RFI cleaning, and diagnostic plots — **no C deps beyond libc + libm**.

## Project map

- `src/` — SIGPROC reader (`filhdr`), n-bit unpack (`unpack`), FILDIAG writer (`diag`), CLI entrypoints (`rfidiag.c`, `chop_fil.c`, `header.c`)
- `python/` — `.diag` I/O (`diagio.py`), plotting (`plot_diagnostics.py`), multi-beam compare (`compare_beam_rfi.py`), eigen cleaner (`multibeam_clean.py`), `requirements.txt`
- `python/tools/` — synthetic `.fil` generator (`make_test_fil.py`), multibeam smoke test (`test_multibeam_clean.py`)
- `tests/` — unpack C tests (`test_unpack.c`), numpy parity vs `rfidiag` (`check_against_numpy.py`)
- `docs/agents/` — issue tracker, triage, domain rules, AI coding vocabulary bridge (`AGENTS.md` mirrors **`## Agent skills`** here — keep in sync)
- **`graphify-out/`** — project graph artifacts; **do not** configure Graphify with Gemini (**leave `GEMINI_API_KEY` / `GOOGLE_API_KEY` unset**; no `backend="gemini"`). AST default: `graphify update .`. Approved local semantic: **Ollama** (`graphify extract . --backend ollama --max-concurrency 1`) — see **`docs/agents/domain.md`** and **`AGENTS.md`** Learned Workspace Facts.
- Upstream semantics: canonical org repo is **`dsa110/simple_filtools`**; personal work often uses a **fork** (`origin` → your fork, `upstream` → `dsa110`) — confirm with `git remote -v`.

<important if="you need to run commands to build, test, lint, or generate code">

From repo root (`PYTHON` defaults to `python3` in the Makefile).

| Command | What it does |
|--------|----------------|
| `make` | Build `rfidiag`, `chop_fil`, `header` |
| `make test` | Build and run `tests/test_unpack`, then `tests/check_against_numpy.py` (needs `rfidiag` binary + numpy) |
| `make test-unpack` | Build `tests/test_unpack` if needed and run it |
| `make test-numpy` | Run `tests/check_against_numpy.py` (needs built `rfidiag`) |
| `make clean` | Remove built objects, binaries, `tests/test_unpack`, `tests/_tmp` |
| `./rfidiag <input.fil> -o <out.diag>` | Stream `.fil` → `.diag`; see `./rfidiag --help` for `-s`, `-d`, `-c`, `-Z`, `-q` |
| `./chop_fil <input.fil> -s <start_sec> -d <dur_sec> [-o out.fil]` | Time-slice to new `.fil` (default `<input>.cut.fil`) |
| `./header <input.fil>` | Print header; field flags per `./header --help` |
| `python3 python/plot_diagnostics.py <out.diag> [--outdir …]` | PNG suite from `.diag`; see `--help` for decimation/spectra options |
| `python3 python/compare_beam_rfi.py beam0.diag beam1.diag … [options]` | Multi-beam `.diag` comparison; see `--help` |
| `python3 python/multibeam_clean.py beam00.fil … --outdir … [options]` | Multi-beam `.fil` cleaner; `--dry-run`, `--diag`, `--cores` etc. — see `--help` |
| `python3 python/tools/make_test_fil.py …` | Generate synthetic `.fil` for tests (see script docstring / `--help`) |
| `python3 python/tools/test_multibeam_clean.py` | Smoke test for `multibeam_clean.py` |
| `python3 scripts/sync_agent_skills.py` | Copy **`AGENTS.md`** **`## Agent skills`** into **`CLAUDE.md`** agent-skills block (canonical → mirror) |
| `python3 scripts/sync_agent_skills.py --check` | Exit non-zero if **`CLAUDE.md`** drifts (for CI) |
| `make install-hooks` | Install **`pre-commit`** hook that runs **`sync_agent_skills.py --stage`** |
| `graphify update .` | AST-only graph rebuild (no LLM; default for code changes) |
| `graphify extract . --backend ollama --max-concurrency 1` | Local semantic extract via Homebrew Ollama; then `graphify cluster-only .` — see domain docs |

Python deps for tests/plotting: see `python/requirements.txt` (numpy; matplotlib for plots).

</important>

<important if="you are configuring agent harness, skills, GitHub workflow, domain docs pointers, or AI coding vocabulary">
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

</important>

<important if="you are rebuilding graphify-out or running semantic graph extraction">

- **No Gemini:** leave **`GEMINI_API_KEY`** / **`GOOGLE_API_KEY`** unset; never `backend="gemini"`.
- **Ollama (approved local semantic):** Homebrew **`/opt/homebrew/bin/ollama`** (chezmoi **`~/.Brewfile`**); models **`~/.ollama/models/`**; default **`qwen2.5-coder:7b`**. Unset cloud API keys, then:

```bash
env -u GEMINI_API_KEY -u GOOGLE_API_KEY -u ANTHROPIC_API_KEY -u OPENAI_API_KEY -u MOONSHOT_API_KEY \
  OLLAMA_BASE_URL=http://localhost:11434/v1 OLLAMA_MODEL=qwen2.5-coder:7b \
  graphify extract . --backend ollama --max-concurrency 1 --api-timeout 900
graphify cluster-only .
```

- **AST-only (no semantic):** `graphify update .` — use for routine code edits; keeps cloud tokens at zero in **`cost.json`**.
- Caveats and graph navigation: **`docs/agents/domain.md`** (Graphify hygiene + graph caveats).

</important>

<important if="you are editing, building, or debugging the C tools">

- `CC`, `CFLAGS`, `CPPFLAGS`, `LDLIBS` are overridable via Makefile; `CPPFLAGS` always appends POSIX and `_FILE_OFFSET_BITS=64` (see Makefile header).
- Header format and `.diag` section tags are documented in `src/filhdr.h` and `src/diag.h`; Python reader mirrors the header layout in `python/diagio.py`.
- Treat filterbank samples as **raw unsigned integer levels** per `nbits`; statistics in `rfidiag` use mean and **direct RMS**, not median/MAD (see README “Notes on conventions”).

</important>

<important if="you are running rfidiag, producing or consuming .diag files, or plotting diagnostics">

- `.diag` layout: fixed `FILDIAG` header + tagged sections (`SUMC`, `SUMQ`, `HIST`, `CMEA`, `CRMS`, optional `Z0DM`) — details in `src/diag.h` and README “Diagnostics produced”.
- `Z0DM` is **`4 × nsamples` bytes**; omit with `rfidiag -Z` when full-rate zero-DM is unnecessary (saves RAM and disk). Some plots skip if `Z0DM` is absent.
- Default throughput is usually **sequential disk I/O bound**; chunk size `-c` trades chunk stat resolution vs buffer size (README “Memory and throughput”).

</important>

<important if="you are running, tuning, or testing multibeam_clean.py">

- Algorithm and flag table: README section `multibeam_clean.py`. Per-chunk JSON diagnostics: `--diag <file.jsonl>`. Validate plan only: `--dry-run`.
- **`--cores` is parsed before NumPy import** and sets BLAS thread env vars — watch for thread-pool × BLAS oversubscription on large `B`; compare `--cores 1` vs higher on a short clip if CPU is chaotic.
- Edge bands: tiles smaller than `(tile_freq_chans × tile_time)` at array edges are **left uncleaned** (passed through); see code comments in `python/multibeam_clean.py`.

</important>

<important if="you are writing or modifying tests">

- **C:** `tests/test_unpack.c` vs `src/unpack.c` (2-bit exhaustive + random + nbits dispatch).
- **E2E:** `tests/check_against_numpy.py` runs `rfidiag` on synthetic `.fil` from `python/tools/make_test_fil.py`; integer sections must match **bit-exact**; floats **~1e-5** relative — see README “Testing strategy”.
- **Multibeam:** `python/tools/test_multibeam_clean.py` after changes to the cleaner.

</important>

<important if="you are pushing branches, syncing with upstream, or opening pull requests">

- Prefer **`git fetch upstream`** / merge or rebase from **`dsa110/simple_filtools`** for canonical changes; push personal work to **`origin`** (fork) unless the project’s convention says otherwise — confirm remotes with `git remote -v`.

</important>
