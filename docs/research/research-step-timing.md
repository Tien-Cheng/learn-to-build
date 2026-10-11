# Research step timing (`new`, step 6)

Why `new` felt slow, measured from the researcher subagent transcripts of three complete runs (Claude Code, Opus), before the changes below. Time is split into model time (thinking and writing before each tool call) and tool time (the call running).

| | CPU scheduler | SQLite | Redis |
|---|---|---|---|
| Total | 28.7 min | 12.4 min | 10.2 min |
| Fetching sources (curl, WebFetch) | ~4 min | ~3 min | ~5 min |
| Writing and running its own simulator of X | ~15 min | none | none |
| Generating the four files | 6.4 min | 4.3 min | 3.8 min |
| Size of the four files | 84k chars | 66k chars | 60k chars |

## Findings

1. **Self-built oracles dominated the slow run.** A CPU scheduler has no canonical program to run. The researcher invented an output format, wrote a ~10k-char simulator, cross-checked it against the OSTEP course simulators (0 mismatches), debugged its CFS rules, and generated exact examples from it. The brief never asked for this; `spec.md`'s demand for exact examples with no oracle invited it. The per-Stage Reference solution ([ADR 0003](../adr/0003-reference-solutions-validate-tests.md)) already checks expected values, so the work was duplicated up front for every Stage at once. Finding the OSTEP simulators was the valuable part, and `overview.md` recorded them as the oracle.
2. **The Learner sat idle for the whole run.** Research started 2 minutes into the session and returned at minute 31, with no questions in between; the language Diagnostic, which needs no research, ran only afterwards.
3. **The files ran long.** `overview.md`, specified as three sentences plus four short sections, came out at 10–19k chars. Every Stage author rereads these files.
4. **`architecture.md` was on the critical path** (about 1–1.5 min of writing plus its source reading), though nothing reads it before the first `review`.
5. **Network was not the bottleneck** (3–5 min, largely parallel), which makes caching research per X a smaller win than first thought.

## Changes

- The brief asks researchers to name an oracle (the real X or an existing independent implementation) and to take exact examples only from sources, the oracle, or rules followed by hand.
- Three researchers (spec, history, architecture) run in parallel in the background. The Diagnostic and Harness setup proceed meanwhile; the domain questions wait for `overview.md`, the plan for `spec.md` and `history.md`, the final commit for `architecture.md`.
- Per-file length limits.

Expected: about 8–10 minutes for an X like the CPU scheduler and 5–7 for Redis or SQLite, much of it overlapped with the Learner answering questions. To be confirmed by timing the next runs.
