# Existing learn-by-building skills: what's out there

Researched 2026-10-11. Primary subject: [0sakura721/build-your-own-x-skill](https://github.com/0sakura721/build-your-own-x-skill) at commit `42b1b8e` (HEAD). Short form `BYOX-SKILL:Lnn` means `SKILL.md` line nn at that commit, e.g. <https://github.com/0sakura721/build-your-own-x-skill/blob/42b1b8e/SKILL.md#L28-L47>.

## 1. 0sakura721/build-your-own-x-skill

### What it is

- The repo holds two files: `README.md` (92 bytes, one line: "Operit Skill - Build Your Own X: 从零构建一切的教程索引", i.e. "a tutorial index for building everything from scratch") and `SKILL.md` (329 lines, ~20 KB). It has no scripts, templates, tests or reference files (`git ls-files` at `42b1b8e`).
- It was written for Operit, an Android AI-agent app ([AAswordman/Operit](https://github.com/AAswordman/Operit)). The first version declared `http_request`, `web_access` and `command_line` compatibility and a `visit_web` tool. Commit `973c426` removed those to make it "generic" (`git diff 0443fa3 973c426`).
- All 6 commits landed in about 11 minutes on 2026-07-21 (`1f75f46`..`42b1b8e`). Activity since then: 0 stars, 0 forks, issues disabled, no PRs, no license (GitHub API, 2026-10-11).
- In substance the file is a curated copy of [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) (README at `aa17439`). The skill claims "200+ tutorials across 30+ tech domains" (BYOX-SKILL:L3, L10). It actually links 128 tutorials: 104 in 20 domain tables plus 24 in an "Uncategorized" table (BYOX-SKILL:L53-L284). Upstream lists 359 tutorial entries in 30 "Build your own" categories.
- Link rot (curl, 2026-10-11):
  - Real 404s: `github.com/roiaimiel1/Build-Deep-Learning-From-Scratch` (BYOX-SKILL:L144, a typo of upstream's `roiamiel1`, which returns 200) and `sj14.gitlab.io/...go-unix-shell` (BYOX-SKILL:L203).
  - Unreachable: `jamesmolloy.co.uk` (BYOX-SKILL:L156).
  - The 4 Medium links returned 403. That looks like bot blocking, so it doesn't prove they're dead.

### End-to-end flow when invoked (BYOX-SKILL:L28-L47)

The whole procedure is 3 steps:

1. **Clarify.** Ask 4 questions: what technology, what language, time budget ("one afternoon vs. multi-week"), and minimal (<500 lines) vs. full-featured (L30-L36).
2. **Match a tutorial** from the embedded index, ranked on "language + difficulty + domain" (L38-L40).
3. **Guide through the tutorial** (L42-L47), quoted in full:
   - "Open the tutorial link, extract key steps and code snippets"
   - "Plan the coding flow, guide the user step by step"
   - "If there's a companion code repo, point them to clone it"
   - "Verify compilation/execution at each step"

**Artifacts generated: none.** The skill specifies no repo, no files, no plan document and no progress file. Its only "persistence" advice is a tip to "create a Git repo per project" (L327, in Chinese).

### How it decomposes a project

- **It doesn't.** It delegates decomposition to whichever third-party tutorial it picks. There's no dependency graph, no step schema and no granularity rule; "Plan the coding flow" (L45) is the entire instruction.
- The only structure beyond single projects is three fixed **learning pathways**: Beginner, Intermediate and Expert lists of whole projects with time estimates, e.g. "Shell (C) — 一个下午" ("one afternoon"), "Database (Go/C) — 2-3 天" ("2–3 days") (L288-L320). It's a linear ordering of projects, not of concepts within a project.

### Who writes the code, tests, verification

- **Unspecified, and it leans toward the agent.** "extract key steps and code snippets" (L44) and "point them to clone" the companion repo (L46) mean the agent relays the tutorial's own code to the learner. Nothing says the learner must write it, and nothing forbids the agent from writing it.
- **No tests.** Verification is "Verify compilation/execution at each step" (L47): it compiles and runs, but behaviour is never checked against a spec. Nobody writes tests.
- **No scaffolding or stub policy** of any kind.

### Hints, stuck, review, reflection, design rationale

- **Stuck:** the only guidance is the tip "when stuck, go straight to the tutorial's comment section/Issues" (L328, in Chinese). There's no hint ladder.
- **Review, reflection, retrieval, explaining design choices:** absent.

### Adaptation and research

- **Language:** it asks for one and filters the index by it (L34, L40). It doesn't port a tutorial written for another language.
- **Proficiency:** only indirectly, through time budget, minimal vs. full scope (L35-L36) and the fixed Beginner/Intermediate/Expert lists. It never assesses the learner.
- **Research before planning:** only "open the tutorial link" (L44). It doesn't compare sources, look at the real-world X (e.g. the Redis protocol spec), or check whether a link is alive.

### Weaknesses

Judged against learning science:

- **Generation effect.** Nothing guarantees the learner generates code. "Extract code snippets" turns the agent into a copy-paste relay, which is the "AI delegation" pattern. In Anthropic's 2026 RCT that pattern scored <40% on the post-task quiz, against 65%+ for "conceptual inquiry" and 67% average for hand-coders vs. 50% for the AI group ([anthropic.com/research/AI-assistance-coding-skills](https://www.anthropic.com/research/AI-assistance-coding-skills); preprint [arXiv:2601.20245](https://www.arxiv.org/pdf/2601.20245)).
- **Desirable difficulty.** There's no calibration loop. Difficulty is fixed by whichever tutorial gets picked.
- **Retrieval practice and spacing.** None. No quizzes, no revisiting earlier steps, no persistence across sessions.
- **Fading scaffolds.** None. Support stays at the tutorial's level throughout.
- **Feedback.** "It compiles and runs" isn't a correctness oracle, and there are no tests.
- **The "agent writes most, leaves trivial TODOs" failure mode.** This skill doesn't even reach that bar: it sets no rule for code ownership. Worst case, the agent relays the tutorial code and the learner pastes it.
- **Quality.** The tutorial count is inflated (128 vs. "200+"). At least 2 links are broken, one of them by a transcription typo. The index is a stale snapshot, a subset of an upstream list the agent could fetch live.

## 2. codecrafters-io/build-your-own-x (the source list)

- A "compilation of well-written, step-by-step guides for re-creating our favorite technologies from scratch". It has 359 entries in 30 categories, each tagged with a language, and some marked `[video]` ([README @ aa17439](https://github.com/codecrafters-io/build-your-own-x/blob/aa17439/README.md); 552k stars).
- It's a pure link list. It has no structure, tests, difficulty ratings or progress tracking.
- The maintainer, CodeCrafters, sells the missing structure. Each challenge is split into **stages**, and stages follow a "TDD-like approach": "The tests will initially fail, and then you'll submit code to make those tests pass". The learner writes all the code, a `git push` runs the tests, and a passing stage unlocks the next. The starter repo's first stage is mostly "uncomment the provided code". Instructions are per-language ([docs.codecrafters.io/challenges/how-challenges-work](https://docs.codecrafters.io/challenges/how-challenges-work)).
- CodeCrafters is the closest existing model to our design. Its challenges are hand-authored, though, so the catalog is fixed.

## 3. Other agent skills and prompts aimed at learning by doing

GitHub repo and code search, 2026-10-11.

| Skill | What it does | How it differs |
|---|---|---|
| **Anthropic `learning-output-style` plugin** ([anthropics/claude-code @ 2301018, plugins/learning-output-style](https://github.com/anthropics/claude-code/tree/2301018/plugins/learning-output-style)) | A SessionStart hook injects instructions to "identify opportunities where the user can write **5-10 lines** of meaningful code". The agent first creates the file, the function signature and comments, and marks the spot with a TODO. Its listed "Don't request contributions for" cases are boilerplate, obvious code, config and CRUD. It also adds `★ Insight` blocks before and after code (`hooks-handlers/session-start.sh` L10). | This is the motivating complaint, built into the design. Contributions are capped at 5–10 lines per request, and the agent writes everything else. There are no tests, progress tracking or fading. |
| **ktaletsk/learn-codebase** (80 stars, [`SKILL.md` @ cbc0304](https://github.com/ktaletsk/learn-codebase/blob/cbc0304/SKILL.md)) | A Socratic tutor for understanding an existing codebase. Questions run predict → trace → design-reasoning → compare → error-prediction (L150-L170). A 3-level hint ladder (conceptual hint → narrowed options → fill-in-the-blank, then explain plus a follow-up prediction) is at L207-L225. It targets 60-80% success for zone of proximal development (ZPD) calibration (L230-L253). A `.claude/learning-journal.md` holds mastery as 🔴/🟡/🟢 with a 1/3/7/14-day spaced-review schedule (L255-L289). It also tells the learner to disable Prompt Suggestions so the CLI doesn't pre-fill answers (L74-L80). | It's read-only and "never modify files" (L314), so it trains comprehension, not authorship. It has the strongest hint and calibration design found, but it never builds anything. |
| **nagisanzenin/engram** (1,446 stars, [`skills/learn/SKILL.md` @ 0590eb8](https://github.com/nagisanzenin/engram/blob/0590eb8/skills/learn/SKILL.md)) | A general learning engine backed by a Python state store. A curriculum-architect subagent builds a **concept DAG** of 8-20 nodes. It decomposes "by necessity, not by textbook", backward-chaining from the goal. Each node carries a `requires`/`derives_from`/`contrasts_with` edge, a probe and a rubric ([`agents/engram-curriculum-architect.md` L9-L50](https://github.com/nagisanzenin/engram/blob/0590eb8/agents/engram-curriculum-architect.md)). Before teaching it pretests the frontier (learn L77-L96). For `procedure` nodes it uses a **fading ladder**: worked example → completion → faded "principle-bearing interior step" → cold solve, with fresh instances checked by execution ([`skills/_shared/problem-grammar.md` L10-L26, L33-L48](https://github.com/nagisanzenin/engram/blob/0590eb8/skills/_shared/problem-grammar.md)). Grading goes to a blind assessor subagent and leaves an FSRS-scheduled receipt (learn L149-L166). The capstone is a forced DAG node, not prose, because prose capstones "silently did not happen, every single time" (learn L188-L192). | It's the most rigorous on learning science, but it teaches concepts, not code projects. Code shows up only in the capstone ("a feature in their actual repo with `TODO(human)` on the load-bearing parts", learn L211). There's no runnable test suite per step. Grading is an LLM judging free-text recall. |
| **CHplus0/dsh-learning-mode** (8 stars, [`learning-mode/skills/learning-mode/SKILL.md` @ 960afb6](https://github.com/CHplus0/dsh-learning-mode/blob/960afb6/learning-mode/skills/learning-mode/SKILL.md)) | A port of Claude Code's Learning style to DeepSeek Harness. It uses `TODO(你)` blanks ("TODO(you)"), each with a "how to self-check" line (L92) and an L1-L3 hint ladder. On "just do it" it switches to a direct mode with no blanks (L21). | Its rules make the trivial-TODO failure explicit: "Dose: 1–2 per meaningful task" (L93), and "auth, payments, irreversible operations, correctness-critical steps are NEVER left blank" (L90). The hardest, most correctness-critical code is exactly what goes to the agent. |
| **mec07/claude_skills "Sensei"** (1 star, [`stow/Sensei/SKILL.md` @ 8360c04](https://github.com/mec07/claude_skills/blob/8360c04/stow/Sensei/SKILL.md)) | A toggle mode with these rules: "Never write code the developer didn't attempt first" (L55), lightest touch first ("hint > question > explanation > example > code", L61), and one `TODO(human)` at a time (L66-L75). It has 5 scaffolding levels (L80-L85) and a protégé effect step, "Teach me what this function is doing" (L89-L93). "Help abuse detection" refuses to give in after 3 low-effort asks (L102-L106). Stale knowledge gaps come back as retrieval questions (L95-L100). | It's a stance, not a curriculum. There's no project, decomposition or tests. |

## Implications for our design

These map to our glossary terms (`GLOSSARY.md`) and to ADR 0001 (Learner authors all Solution code).

1. **Own the whole loop, not just the index.** BYOX-SKILL stops at "here's a link". We should generate a real Project: a starter repo, a Stage DAG and a Test suite per Stage. That's CodeCrafters' structure, made on demand for any X, any language and the learner's level, so we aren't limited to a hand-authored catalog.
2. **Make ownership mechanical, not a dosage rule.** Every surveyed agent skill rations learner code: "5-10 lines" (Anthropic), "1–2 per task" and "never blank correctness-critical steps" (dsh). Ours inverts that. The agent writes only the Harness, and the most correctness-critical code belongs to the Learner. A test-first Stage is a clean place to enforce this: the agent can only touch `tests/`, `specs/` and the starter repo. (ADR 0001 already commits to this; no competitor does.)
3. **Tests are the verification oracle, not "it compiles".** Pass or fail decides whether a Stage is done (the CodeCrafters model). An LLM rubric (engram) and "verify compilation" (BYOX-SKILL) are both weaker. Generated tests need an execution check of their own: build a hidden reference solution, confirm every test passes against it, then delete it. That applies engram's "compute the answer key by execution" rule to tests (problem-grammar L39-L45).
4. **Use a real DAG with necessity edges, and research X first.** Borrow engram's architect discipline: backward-chain from the goal, one claim per node, `requires` edges, 8–20 nodes, a threshold flag. Ground it in research on the real X (protocol specs, reference implementations, curated tutorials pulled live from the upstream list, not a stale copy). BYOX-SKILL does no research and no decomposition.
5. **Fade scaffolds across Stages, not within a function.** Following engram's worked → completion → faded → cold ladder, early Stages can ship richer specs and more granular tests. Later Stages get only a behavioural spec and an empty file, which is Unassisted authorship. No competitor fades over a whole build.
6. **Hints without authorship leakage.** Use a graduated hint ladder (learn-codebase L207-L225, Sensei L80-L85) whose top rung is still not code, e.g. failing-test explanations or design questions. Count hints per Stage and feed the counts into difficulty calibration (learn-codebase's 60-80% ZPD target).
7. **Retrieval, reflection and design rationale after each Stage.** Ask the Learner to explain why their design works, predict the behaviour of an edge case, or rebuild an earlier piece from memory. Keep a progress journal in the repo with spaced revisits (learn-codebase journal; engram FSRS). BYOX-SKILL has none of this.
8. **Close known leaks.** Tell the Learner to disable Claude Code prompt suggestions (learn-codebase L74-L80). Make the capstone a forced DAG node, not prose, so it can't be silently dropped (engram learn L188-L192).
