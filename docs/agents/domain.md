# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root, or
- **`CONTEXT-MAP.md`** at the repo root if it exists — it points at one `CONTEXT.md` per context. Read each one relevant to the topic.
- **`docs/adr/`** — read ADRs that touch the area you're about to work in. In multi-context repos, also check `src/<context>/docs/adr/` for context-scoped decisions.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The producer skill (`/grill-with-docs`) creates them lazily when terms or decisions actually get resolved.

## File structure

Single-context repo (most repos):

```
/
├── CONTEXT.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

Multi-context repo (presence of `CONTEXT-MAP.md` at the root):

```
/
├── CONTEXT-MAP.md
├── docs/adr/                          ← system-wide decisions
└── src/
    ├── ordering/
    │   ├── CONTEXT.md
    │   └── docs/adr/                  ← context-specific decisions
    └── billing/
        ├── CONTEXT.md
        └── docs/adr/
```

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal — either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/grill-with-docs`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0007 (event-sourced orders) — but worth reopening because…_

## Graph caveats — `graphify-out/`

When using `graphify-out/graph.json` for navigation or refactor planning, know these about this repo's extractor behavior:

- **`src_diag_h` is permanently isolated** (no in/out edges). `src/diag.h` exposes only function *declarations* (`diag_open_write`, `diag_write_section`); their bodies live in `src/diag.c`, where they ARE represented as `src_diag_diag_open_write` / `src_diag_diag_write_section` contained by `src_diag_c`. `src/filhdr.h` and `src/unpack.h`, by contrast, expose `static inline` definitions (`fil_bytes_per_sample`, `unpack_2bit_byte`) — Graphify emits `contains` edges for those because there's an in-header body to extract. Not a bug; just the extractor's scope. Don't infer "diag.h is unused" — it's the canonical `.diag` format spec, `#include`d by `src/diag.c` and `src/rfidiag.c`, and mirrored in `python/diagio.py`.
- **Most cross-file C and Python call edges are `INFERRED`, not `EXTRACTED`.** The AST extractor under-resolves direct function calls across translation units (C) and module boundaries (Python). Examples that are real but tagged INFERRED at conf 0.8: every `test_dispatch_*()` → `unpack_to_uint8()` edge in `tests/test_unpack.c`, every `rfidiag_main()` → `fil_open` / `unpack_to_uint8` / `diag_open_write` edge, `analyse_beam()` → `read_diag()` in `python/compare_beam_rfi.py`. Trust these — they were spot-verified against source. Treat them as load-bearing structure, even though confidence-tagged INFERRED.
- **Watch for fabricated INFERRED targets** at conf 0.8. Specifically, `compare_beam_rfi.py::main → multibeam_clean.py::SigprocHeader::set` (sourced at L994) does not exist — the L994 line is `tstarts = [b.diag.tstart for b in beams if b.name in {z.name for z in zdms}]` (a set comprehension). The inferrer hallucinated a `SigprocHeader.set` target by confusing the set literal with the `SigprocHeader` class name in `multibeam_clean.py`. Verify INFERRED targets by line lookup before relying on them.
- **`uses` edges at conf 0.5 are unreliable.** The three `BeamStats / ZdmStats / SpatialStats → DiagFile` edges all anchored at L98 (the `from diagio import DiagFile, read_diag` line) are mixed: `BeamStats` really does have a `diag: DiagFile` field (L108), but `ZdmStats` (L361) and `SpatialStats` (L579) have no `DiagFile` field at all — the inferrer applied import context indiscriminately to every nearby `@dataclass`. Treat conf-0.5 `uses` edges as hypotheses, not facts.
- **`*_rationale_*` nodes in `GRAPH_REPORT.md`'s "Knowledge Gaps" are not gaps.** Graphify lifts every docstring into a `rationale_*` concept node and connects it to its parent function via one `rationale_for` edge. The report's "isolated node" count therefore includes every documented function (degree-1 leaves), not graph-theoretic isolates. Shortening or expanding a docstring does not remove the rationale node, only changes its label — confirmed by experiment on `find_coincident_bursts` (L417) and `analyse_spatial_feasibility` (L606). To eliminate a rationale node, the docstring would need to be removed entirely; per repo convention, docstrings stay.

## Graphify hygiene

- `.graphifyignore` lives at the repo root (gitignore syntax). It excludes `.cursor/`, `.claude/`, `.remember/`, `graphify-out/`, Makefile outputs, and Python caches from extraction.
- Rebuild: `graphify update <repo-root>`. If you've added new ignore patterns but the graph hasn't shrunk, the topology-equality short-circuit (`graphify/watch.py::487`) is suppressing the rewrite — remove `graphify-out/graph.json` and re-run `update` to force a clean regenerate.
- The Gemini ban (see `AGENTS.md` Learned User Preferences) is operationally enforced by `cost.json`: every rebuild must keep `runs[-1].input_tokens == 0` and `output_tokens == 0`. Any nonzero value means a key leaked into the env.
