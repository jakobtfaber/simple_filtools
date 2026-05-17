# AI coding vocabulary (bridge)

Plain-English definitions for **how we talk about AI-assisted work** (sessions, handoffs, skills, AFK agents). This project’s science lives in **`CONTEXT.md`** / **`README.md`**; this file connects **workflow language** to [Matt Pocock’s AI Coding Dictionary](https://github.com/mattpocock/dictionary-of-ai-coding).

- **Browse:** generated [README](https://github.com/mattpocock/dictionary-of-ai-coding/blob/main/README.md) on GitHub (full TOC).
- **Optional local clone (offline / grep):** `~/Developer/reference/ai-tools/dictionary-of-ai-coding/` — atomized entries under `dictionary/*.md`; regenerate aggregated README with `npm run generate` in that repo.

## Curated entries for this codebase

Use these terms in issues, handoffs, and agent prompts so humans and harnesses align:

| Term | Why it matters here |
|------|---------------------|
| [Handoff artifact](https://github.com/mattpocock/dictionary-of-ai-coding/blob/main/dictionary/Handoff%20artifact.md) | Structured brief between sessions (e.g. multibeam params, `.diag` paths, bottleneck diagnosis). |
| [Handoff](https://github.com/mattpocock/dictionary-of-ai-coding/blob/main/dictionary/Handoff.md) | Passing state across sessions/agents without re-explaining the repo. |
| [Spec](https://github.com/mattpocock/dictionary-of-ai-coding/blob/main/dictionary/Spec.md) / [Ticket](https://github.com/mattpocock/dictionary-of-ai-coding/blob/main/dictionary/Ticket.md) | Maps cleanly to GitHub issues (`docs/agents/issue-tracker.md`). |
| [Skill](https://github.com/mattpocock/dictionary-of-ai-coding/blob/main/dictionary/Skill.md) | Instructions loaded on demand — prefer over stuffing **`AGENTS.md`**. |
| [Progressive disclosure](https://github.com/mattpocock/dictionary-of-ai-coding/blob/main/dictionary/Progressive%20disclosure.md) | Keep **`AGENTS.md`** lean; link skills and deep docs instead. |
| [Context pointer](https://github.com/mattpocock/dictionary-of-ai-coding/blob/main/dictionary/Context%20pointer.md) | Explicit “open this path/skill next” in prompts and handoffs. |
| [AGENTS.md](https://github.com/mattpocock/dictionary-of-ai-coding/blob/main/dictionary/AGENTS.md.md) | Harness-loaded project brief — token cost every turn; don’t duplicate long guides here. |
| [Session](https://github.com/mattpocock/dictionary-of-ai-coding/blob/main/dictionary/Session.md) / [Turn](https://github.com/mattpocock/dictionary-of-ai-coding/blob/main/dictionary/Turn.md) | Framing long chats (e.g. full pipeline debugging). |
| [Context window](https://github.com/mattpocock/dictionary-of-ai-coding/blob/main/dictionary/Context%20window.md) | Large `.diag` / log paste discipline. |
| [Attention degradation](https://github.com/mattpocock/dictionary-of-ai-coding/blob/main/dictionary/Attention%20degradation.md) / [Attention budget](https://github.com/mattpocock/dictionary-of-ai-coding/blob/main/dictionary/Attention%20budget.md) | Prefer summaries + pointers over megabytes of raw output in chat. |
| [AFK](https://github.com/mattpocock/dictionary-of-ai-coding/blob/main/dictionary/AFK.md) | Unattended agent runs — pair with sandboxed permissions for long cleans/tests. |
| [Tool](https://github.com/mattpocock/dictionary-of-ai-coding/blob/main/dictionary/Tool.md) vs Skill | Tools are invoked calls; skills are instructions read — avoids conflating CLI with runbooks. |

## Contributing upstream

Improvements to definitions belong in **[dictionary-of-ai-coding](https://github.com/mattpocock/dictionary-of-ai-coding)** (see its `CLAUDE.md`). This repo only **curates** which entries matter for **`simple_filtools`**.
