# Learning-tools landscape: AI learning modes, test-driven platforms, autograders

Researched 2026-10-11. The question: what exists to keep programmers building real skill while they work alongside AI, and how a Claude Code skill could mechanically ensure that the learner writes the code. Primary sources (docs, changelogs, source, first-party posts) are preferred throughout. Claims resting on secondary or unofficial sources are marked as such.

## 1. Claude Code "Explanatory" and "Learning" output styles

### History

- Shipped in v1.0.81: "Released output styles, including new built-in educational output styles 'Explanatory' and 'Learning'" ([CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).
- v2.0.30 deprecated output styles, and v2.0.32 reversed that "based on community feedback" ([CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).
- While styles were deprecated, Anthropic published two SessionStart-hook plugins as stand-ins: `explanatory-output-style` and `learning-output-style` ([plugins dir](https://github.com/anthropics/claude-code/tree/main/plugins)).
- v2.1.73 deprecated `/output-style` in favour of `/config`, and fixed the style at session start for prompt caching. v2.1.269 re-added `/output-style [name]` ([CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).
- The built-in styles today are Proactive, Concise, Explanatory and Learning ([docs](https://code.claude.com/docs/en/output-styles)).

### How Learning works, per the docs

- Learning adds Explanatory's `★ Insight` blocks "and also asks you to write some of the code. Claude handles routine implementation itself. When it reaches a piece with a real design decision ... it leaves a few lines for you" ([docs](https://code.claude.com/docs/en/output-styles#learning)).
- Claude writes a `TODO(human)` comment into the file and sends a "● Learn by Doing" block with three parts: **Context**, **Your Task** and **Guidance**. It then "stops and waits". After you finish, it gives one Insight about your code and continues ([docs](https://code.claude.com/docs/en/output-styles#learning)).
- A style is a system-prompt instruction: "nothing enforces it". The docs say to use a hook for anything that must happen "without fail" ([docs](https://code.claude.com/docs/en/output-styles#choose-between-an-output-style-and-other-features)).
- Styles don't apply to subagents, except a fork ([docs](https://code.claude.com/docs/en/output-styles#how-output-styles-work)).

### The prompt itself

Anthropic doesn't publish the built-in prompt. A community extraction (unofficial, from ccVersion 2.0.14) is at [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts/blob/main/system-prompts/system-prompt-learning-mode.md). The key lines:

- "ask the human to contribute **2-10 line** code pieces when generating **20+ lines**"
- "requesting user input for meaningful design decisions while **handling routine implementation yourself**"
- "Make sure there is **one and only one** TODO(human) section in the code"

Anthropic's own `learning-output-style` plugin does publish its prompt ([session-start.sh](https://github.com/anthropics/claude-code/blob/main/plugins/learning-output-style/hooks-handlers/session-start.sh)). It asks for "5-10 lines of meaningful code". It says not to request "Boilerplate", "Obvious implementations", "Configuration or setup code" or "Simple CRUD operations". It also says "Frame it as valuable input ... not busy work."

### Why it feels thin (our analysis of the above)

The design caps the learner's share at one 2-10 line hole per 20+ generated lines, and only one hole open at a time. The agent writes the scaffolding, the function signature, the surrounding context and the integration. The learner never designs structure, never writes tests, never debugs from a blank page, and never meets the boilerplate that builds fluency. There's no difficulty progression, no learner model, and no verification step, since no test is written for the hole. The model decides what counts as "meaningful", and nothing measures it.

### Documented criticism

- **Nothing found matching the motivating complaint (Learning-mode TODOs are too small to teach much)**, in either the issue tracker or first-party sources. Searches of `anthropics/claude-code` issues ("learning output style", "learning mode", "TODO human", "learn by doing") return only plumbing bugs:
  - plugin hook scripts losing the execute bit, e.g. [#39931](https://github.com/anthropics/claude-code/issues/39931) and [#38705](https://github.com/anthropics/claude-code/issues/38705)
  - Windows hook failures, e.g. [#15013](https://github.com/anthropics/claude-code/issues/15013)
  - a duplicate menu option, [#18874](https://github.com/anthropics/claude-code/issues/18874)
  - a docs-wording question, [#87538](https://github.com/anthropics/claude-code/issues/87538)
- Adjacent issue: [#77949](https://github.com/anthropics/claude-code/issues/77949) reports that Desktop's suggested-reply chip leaks answers in active-recall workflows.
- Public commentary is mostly positive. Anthropic's Lydia Hallie: "keeps me so much sharper" ([X](https://x.com/lydiahallie/status/2056420694087594283)). A Hacker News mention is neutral ([HN](https://news.ycombinator.com/item?id=47123858)). That critique appears to be undocumented rather than refuted.

### Evidence base

Anthropic ran an RCT with 52 mostly junior engineers learning the Trio library ([Anthropic research, 2026-01-29](https://www.anthropic.com/research/AI-assistance-coding-skills); [arXiv:2601.20245](https://arxiv.org/abs/2601.20245)).

- The AI group scored 50% on the quiz against 67% for the hand-coding group (d=0.738, p=0.01). The speed gain was not significant. The largest gap was on debugging.
- The low-scoring patterns were "AI delegation", "progressive AI reliance" and "iterative AI debugging". The high scorers asked conceptual questions and "resolved errors independently".
- The authors write: "getting painfully stuck—is likely important for fostering mastery." The post cites Claude Code's Learning/Explanatory styles and ChatGPT Study Mode as modes "designed to foster understanding".

## 2. Chat-assistant learning modes

| Product | What it does | How it withholds answers | Source |
|---|---|---|---|
| Claude learning mode (Claude for Education) | Launched 2025-04-02 inside Projects. "guides students' reasoning process rather than providing answers". Asks e.g. "How would you approach this problem?" | Socratic questioning, prompt-level only | [Anthropic](https://www.anthropic.com/news/introducing-claude-for-education) |
| Claude learning mode (all users) | Opened to everyone 2025-08-14 as a style in the dropdown; can be turned off any time | Same | [Engadget](https://engadget.com/ai/anthropic-brings-claudes-learning-mode-to-regular-users-and-devs-170018471.html) (secondary; no Anthropic post found) |
| ChatGPT Study Mode | Launched July 2025. "powered by custom system instructions" written with teachers and pedagogy experts | Leaked prompt's top rule: "DO NOT DO THE USER'S WORK FOR THEM". Guides with questions, hints, small steps and comprehension checks | [Simon Willison](https://simonwillison.net/2025/Jul/29/openai-introducing-study-mode/), quoting OpenAI (openai.com returned 403) |
| Gemini Guided Learning | Launched 2025-08-06. "probing, open-ended questions", step-by-step breakdowns, quizzes, diagrams. Built on LearnLM | Pedagogy-tuned model plus mode | [Google blog](https://blog.google/outreach-initiatives/education/guided-learning/) |

All three are opt-in conversational modes that the learner can switch off. None owns an artifact, a test suite or a progression. They withhold answers in chat, but they don't make anyone build anything.

## 3. CodeCrafters

**Format** ([how challenges work](https://docs.codecrafters.io/challenges/how-challenges-work)):

- Challenges are broken into stages, and the web UI shows one stage's instructions at a time, "tailored to the language you're using".
- You can switch language freely. CodeCrafters creates the git repo.
- "For each stage we'll run tests on your code", and you submit with `git push`, with results streamed to that terminal.
- Stage 1 is "uncomment the code ... and then run a git push".
- Hints arrive "at the right time".
- The CLI's `codecrafters test` runs the tests without a commit, and `--previous` re-runs earlier stages ([CLI usage](https://docs.codecrafters.io/cli/usage)).

**Pause**:

- On 2026-05-22, co-founders Sarup Banskota and Paul Kuruvilla announced they are pausing new challenges ([blog](https://codecrafters.io/blog/pausing-new-challenges); [forum](https://forum.codecrafters.io/t/were-pausing-new-challenges/16129)).
- Stated reason: "we were unsuccessful at turning CodeCrafters into a business that justifies the time, energy, and capital we've put in". They could not close the gap between user enthusiasm and paying customers at startup scale.
- The post doesn't cite AI.
- Existing challenges and infrastructure stay up, maintained by Andy Li. The founders say they're open to "a new home" for CodeCrafters.

## 4. Exercism, boot.dev, JetBrains

- **Exercism**:
  - Learning Mode means "Requiring Learning Exercises to be completed to unlock more exercises". In Practice Mode, "all exercises are unlocked from the start" ([unlocking](https://exercism.org/docs/building/product/unlocking-exercises)).
  - Concept exercises are "very tightly focused" and form a dependency tree ([syllabus](https://exercism.org/docs/building/tracks/syllabus)).
  - Per-language test runners let students "iterate on a solution seeing whether the tests pass or fail" ([test runners](https://exercism.org/docs/building/tooling/test-runners)). Analyzers give automated feedback in a mentor's style ([automated mentoring](https://exercism.org/blog/automated-mentoring-support-project)).
  - Human mentoring is free and done by volunteers ([private feedback](https://exercism.org/docs/using/feedback/private); [mentoring FAQ](https://exercism.org/docs/mentoring/faqs)).
- **boot.dev**:
  - Lessons are graded by tests in the browser or by a local CLI. `bootdev run` debugs, and `-s` submits and records pass/fail ([CLI](https://pkg.go.dev/github.com/bootdotdev/bootdev@v1.16.1)).
  - The AI tutor "Boots" can see "The official solution" but has "been trained to not give you the answer" and is Socratic ([lesson help page](https://www.boot.dev/lessons/e4fac74c-9d67-41ad-a85c-c579cb3ad76f); [2023 announcement](https://blog.boot.dev/news/bootdev-beat-2023-10)).
  - Asking Boots before you pass a lesson costs a "baked salmon" or 50% of the lesson's XP. After you pass, it's free. This is a rare example of putting a price on help.
- **JetBrains Academy AI hints**: in-IDE next-step hints, shown as a text banner first and an optional code diff second. In a study of 1,050 sessions, students often adapted only part of a hint ([JetBrains Research, Feb 2026](https://blog.jetbrains.com/research/2026/02/how-ai-powered-hints-used/)).

## 5. University autograded problem sets

- **Berkeley CS61A**:
  - "What Would Python Display" (WWPD) questions are *locked* tests. The expected outputs are stored as hashes, and the student must type the correct output to unlock them (`_verify: locking.lock(hash_key, guess) == locked`). The client also shows misconception-targeted guidance ([okpy/ok-client unlock.py](https://github.com/okpy/ok-client/blob/master/client/protocols/unlock.py)).
  - Fall 2026 moved to pytest (`python3 -m pytest -k return_and_print --unlock`). WWPD answers "are not submitted". Credit comes from the coding questions, submitted via a provenance bundle to Gradescope ([fa26 lab01](https://cs61a.org/fa26/labs/lab01/)).
- **NUS CS2109S / Coursemology**:
  - Weekly problem sets run on Coursemology. Students praise the worked example before each new library ([CS2109S AY23/24 S1 course report](https://comp.nus.edu.sg/~bleong/teaching/feedback/module_assessment-2023-2024S1-cs2109s.pdf)).
  - The same report also has complaints that "private test cases are not clear", about fixed model templates, and about multi-hour grading queues.
  - Coursemology uses three kinds of test case ([NUS CS1010S Coursemology guide](https://www.comp.nus.edu.sg/~cs1010s/notes/Guides/Coursemology/)):
    - **public**: you see the inputs and outputs and which test failed
    - **private**: you only learn that one failed, "to penalize ... hardcoding"
    - **evaluation**: fully silent, possibly used for plagiarism checks
  - No official CS2109S pset spec was found publicly.
- **MIT 6.031**:
  - Reading exercises are embedded after each subsection, with check/explain buttons. They are "graded solely on completion, never on correctness" and due the night before class ([reading 02](https://web.mit.edu/6.031/www/sp20/classes/02-basic-java/)).
  - Each class opens with a 3-minute closed-book nanoquiz.
  - Problem sets go through alpha, then classmate and staff code review, then a beta that must "address all the code reviews". Grades combine "automated tests and ... graders reading the code" ([general info sp21](https://web.mit.edu/6.031/www/sp21/general/)).

**Structural features that make these effective** (synthesis of the above):

1. **Predict before you run.** Locked WWPD tests force a prediction, and hashing means nobody can peek at the answer.
2. **Visible tests to iterate on, plus hidden ones** that defeat hardcoding and test-gaming.
3. **Small, frequent, low-stakes checks** graded on effort, separate from the graded build work.
4. **Scaffolding that fades.** Worked examples and starter code come first, then a blank function.
5. **Human review of the code**, not just its test results, with a mandatory revision pass.
6. **Separation of roles.** Staff own the spec and the tests; the student owns the solution.

## 6. Agent-native learning tools (2025-2026)

- **Anthropic `learning-output-style` / `explanatory-output-style` plugins**: SessionStart hooks that inject prompt text. They're advisory only ([plugins](https://github.com/anthropics/claude-code/tree/main/plugins)).
- **kirilxd/claude-tutor** (136★): a learning plan, adaptive quizzes, SM-2 spaced repetition and a web dashboard, for any topic. It's quiz-centred, not build-centred ([repo](https://github.com/kirilxd/claude-tutor)).
- **kubilaiswf/claude-tutor** (0★, Aug 2026): `/teach`, `/quiz`, `/exam`, `/review`, mastery-gated objectives, and a mistakes log under `~/.claude/tutor/` ([repo](https://github.com/kubilaiswf/claude-tutor)).
- **EveryInc `coding-tutor`**: tutorials built from the learner's own code, with `/quiz-me` spaced repetition. It was **removed as deprecated** in June 2026 ([#951](https://github.com/EveryInc/compound-engineering-plugin/issues/951)).
- **Marketplace "Socratic mentor" skills**, such as [Socratic Mentor Sensei](https://mcpmarket.com/tools/skills/socratic-mentor-sensei) and [AI Learning Mentor](https://mcpmarket.com/tools/skills/ai-learning-mentor), are prompt-only. They're listed on directories, and their implementations weren't verified.
- **Waldek Mastykarz, "What if coding agents had a learning mode?"** (2026-09-04) is a concept piece, not a product ([blog](https://blog.mastykarz.nl/coding-agents-learning-mode/)). It proposes:
  - a side conversation triggered by the work, with its own isolated context
  - Socratic questioning rather than lectures
  - memory of what the learner has already shown they know
  - letting the learner challenge the agent's decisions
- **Not found**: an "Intuition IDE", and any learning or tutor mode in Cursor, Windsurf or Copilot. Searches turned up nothing first-party. The nearest are Code.org's [AI Tutor](https://code.org/en-US/tools/ai-tutor) and JetBrains Academy hints.

## Gaps nobody fills well

1. **Enforced authorship inside the agent.** Every agent-side learning mode is a prompt (output style, SessionStart hook, Socratic skill). None stops the agent from writing the solution, and the Learning style deliberately has the agent write most of it.
2. **Test-driven progression on the learner's own machine and stack, with an agent as the course author.** CodeCrafters has the best format (stages, a test runner, any language, git) but a fixed catalogue that is now frozen. Exercism and boot.dev also have fixed catalogues. No tool generates a staged spec and hidden tests for an arbitrary "build your own X".
3. **Hidden and locked tests in an agent setting.** University courses use private, evaluation and locked tests. No agent tool keeps tests the learner can't read, or that the agent can't leak.
4. **Fading scaffolding and difficulty calibration.** The Learning style's hole size is fixed at 2-10 lines. Nothing grows the learner's share over time, or tracks what they have demonstrated (Mastykarz's proposal, unbuilt).
5. **Predict-then-verify and debugging practice.** WWPD-style prediction and "resolve errors independently" (the RCT's high-scoring pattern) aren't designed into any agent tool.
6. **Review of the learner's code as code**, in the style of 6.031's alpha → review → beta. Tutors quiz knowledge; none run a structured review-and-revise loop on the learner's solution.
7. **Pricing help.** Boot.dev's salmon/XP cost for asking before passing is the only friction mechanism found. Agent tools answer for free and instantly.

## Enforcement mechanisms available in Claude Code

| Mechanism | What it can enforce | Limits | Source |
|---|---|---|---|
| **PreToolUse hook** (`matcher: "Edit\|Write\|NotebookEdit"`, read `tool_input.file_path`) | Return `permissionDecision: "deny"` with a `permissionDecisionReason` that Claude sees, or exit 2, to block edits to learner-owned paths. A per-handler `if: "Edit(src/**)"` can narrow it | A timed-out command hook does *not* block unless `"onFailure": "block"` is set. Bash can still write files, so also match `Bash` and inspect `tool_input.command` | [hooks](https://code.claude.com/docs/en/hooks) |
| **Hooks in skill frontmatter** | Hooks "registered when the skill is invoked and ... keep running for the rest of the session", so the skill carries its own guard | Active only after the skill has been invoked | [hooks](https://code.claude.com/docs/en/hooks), [skills](https://code.claude.com/docs/en/skills) |
| **Plugin `hooks/hooks.json`** | Ships the guard with the plugin; merged with user and project hooks while the plugin is enabled | Users can disable the plugin. Script exec-bit bugs on install were common in 2026 ([#38705](https://github.com/anthropics/claude-code/issues/38705)) | [plugins ref](https://code.claude.com/docs/en/plugins-reference) |
| **Permission deny rules** (`"deny": ["Edit(/src/**)"]`) | Deny always wins over allow, and hooks can't override it. `Edit` rules cover all built-in edit tools, file commands Claude Code recognises in Bash (`sed`, `tee`), and redirect targets (`> file`) | They "don't apply to ... arbitrary subprocesses that read or write files indirectly, like a Python or Node script". Rules for `Write(...)` are never consulted, so use `Edit(...)`. **Plugins can't ship permission rules**: plugin `settings` honours only `agent` and `subagentStatusLine`, so the user or project `.claude/settings.json` must hold them | [permissions](https://code.claude.com/docs/en/permissions), [plugins ref](https://code.claude.com/docs/en/plugins-reference) |
| **Sandbox** (`sandbox.filesystem.denyWrite`, with `Edit` deny rules merged in) | OS-level: blocks writes by Bash commands *and their child processes*, which closes the script loophole | Covers shell commands only, not the file tools (permissions cover those). macOS, Linux and WSL2 only | [sandboxing](https://code.claude.com/docs/en/sandboxing) |
| **Main thread as a restricted agent** (`claude --agent tutor`, or `"agent": "tutor"` in settings or plugin `settings.json`) | The agent's `disallowedTools: Edit, Write, NotebookEdit` then applies to the main conversation: "the main thread itself takes on that subagent's tool restrictions" | Plugin agents ignore their own `hooks`, `mcpServers` and `permissionMode`. Bash remains unless also disallowed | [sub-agents](https://code.claude.com/docs/en/sub-agents), [plugins ref](https://code.claude.com/docs/en/plugins-reference) |
| **Skill `disallowed-tools`** | "Tools removed from Claude's available pool while this skill is active" | How long "active" lasts is unspecified. `allowed-tools` only pre-approves and "does not restrict" | [skills](https://code.claude.com/docs/en/skills) |
| **Output style** (plugin `force-for-plugin: true`) | Sets the tutor persona for the whole session | Advisory: "nothing enforces it". Doesn't reach non-fork subagents | [output styles](https://code.claude.com/docs/en/output-styles) |
| **Separate tutor/harness subagent** (`tools`/`disallowedTools`, `isolation: worktree`) | Splits roles: a harness author writes specs and tests, and a reviewer reads the learner's code read-only | Its system prompt replaces the main style, so the instructions must be self-contained | [sub-agents](https://code.claude.com/docs/en/sub-agents) |
| **Stop / PostToolUse hooks** | A Stop hook with `decision: "block"` keeps the turn going, e.g. to require a test run before Claude ends it. PostToolUse can flag an edit after the fact | They react rather than prevent | [hooks](https://code.claude.com/docs/en/hooks) |
| **Read deny rules on hidden tests** (`Read(./.harness/hidden/**)`) | Stops Claude's file tools from reading or leaking hidden tests | The same Bash-subprocess caveat applies; pair with the sandbox's `denyRead`. The learner can still read them, so hashing (as in ok-client) or a remote grader is needed to hide tests from the learner | [permissions](https://code.claude.com/docs/en/permissions), [ok-client](https://github.com/okpy/ok-client/blob/master/client/protocols/unlock.py) |

**Strongest combination available today:**

- A plugin that ships a PreToolUse hook denying Edit/Write/NotebookEdit and file-writing Bash on learner-owned paths.
- A project `.claude/settings.json`, written by the skill at setup, with `Edit(...)` deny rules and the sandbox enabled. That closes the subprocess loophole.
- Optionally, a main-thread `agent` with `disallowedTools`.

The user can always turn these off; the point is to make cheating a deliberate act rather than a default.
