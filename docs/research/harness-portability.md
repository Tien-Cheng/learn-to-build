# Harness portability for the learn-to-build skill

Researched 2026-10-11 against official docs and source repos. Versions in view: Claude Code v2.1.29x (docs cite features up to v2.1.295), Codex CLI `rust-v0.162.1` (released 2026-10-09, [releases](https://github.com/openai/codex/releases)), Pi at commit [`ea448f4`](https://github.com/earendil-works/pi/tree/ea448f454af474f3e2fe9733b331e17b0662f5d6), OpenCode `dev` at [`e31136b`](https://github.com/anomalyco/opencode/tree/e31136bdbdb43e934d8bbd81e75a2065a2625699), and the current Cursor and Gemini CLI docs.

Two housekeeping notes:

- **Pi moved.** `badlogic/pi-mono` now redirects to [`earendil-works/pi`](https://github.com/earendil-works/pi), and the npm package is `@earendil-works/pi-coding-agent` ([Pi README](https://github.com/earendil-works/pi/blob/ea448f454af474f3e2fe9733b331e17b0662f5d6/packages/coding-agent/README.md)).
- **Codex docs moved.** `developers.openai.com/codex/*` now 308-redirects to `learn.chatgpt.com/docs/*`. The links below use the new URLs.
- **Gemini CLI is partly retired.** Google AI Pro/Ultra and free individual users lost Gemini CLI on 2026-06-18 and were moved to Antigravity CLI. Enterprise Code Assist licences and paid API keys keep Gemini CLI ([Google Developers Blog](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli)). Antigravity CLI is not covered in depth here.

## Comparison table

| | Claude Code | Codex CLI | Pi | OpenCode | Cursor (editor + CLI) | Gemini CLI |
|---|---|---|---|---|---|---|
| **Agent Skills (SKILL.md)** | Yes, plus extensions | Yes | Yes | Yes | Yes | Yes |
| **Project skill dir** | `.claude/skills/` only | `.agents/skills/` (cwd up to repo root) | `.pi/skills/`, `.agents/skills/` | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/` | `.agents/skills/`, `.cursor/skills/`, `.claude/skills/`, `.codex/skills/` | `.gemini/skills/`, `.agents/skills/` |
| **User skill dir** | `~/.claude/skills/` | `~/.agents/skills/` | `~/.pi/agent/skills/`, `~/.agents/skills/` | `~/.config/opencode/skills/`, `~/.claude/skills/`, `~/.agents/skills/` | `~/.agents/skills/`, `~/.cursor/skills/`, `~/.claude/skills/`, `~/.codex/skills/` | `~/.gemini/skills/`, `~/.agents/skills/` |
| **Bundled scripts/refs** | Yes (`${CLAUDE_SKILL_DIR}`) | Yes | Yes | Not documented | Yes | Yes (skill dir becomes readable) |
| **Explicit invocation** | `/name` | `$name` or `/skills` | `/skill:name` | `/name` only if `metadata.opencode/slash: "true"` | `/name` | None; model calls `activate_skill`, user consents |
| **Reads AGENTS.md by default** | Yes, but only if no `CLAUDE.md` exists | Yes | Yes (also `CLAUDE.md`) | Yes (`CLAUDE.md` fallback) | Yes | No; needs `context.fileName` setting |
| **Subagents (fresh context)** | Yes (Agent tool; skill `context: fork`) | Yes (on by default) | No (example extension only) | Yes (`task` tool, child session) | Yes (Task tool) | Yes (no nesting) |
| **Headless mode** | `claude -p` | `codex exec` | `pi -p` | `opencode run` | `-p` / `--print` | `gemini -p` |
| **Block edits to paths** | `Edit(...)` deny rules + PreToolUse hooks + sandbox `denyWrite` | PreToolUse hooks + permission profiles | Extension `tool_call` handler | `permission.edit` globs + plugin `tool.execute.before` | `preToolUse` hook; CLI `Write(...)` deny | `BeforeTool` hook (workspace policies disabled) |
| **Committable in repo** | `.claude/settings.json` | `.codex/hooks.json`, `.codex/config.toml` (trusted projects only) | `.pi/extensions/` (trusted projects only) | `opencode.json`, `.opencode/plugins/` | `.cursor/hooks.json`, `.cursor/cli.json` | `.gemini/settings.json` (fingerprinted trust) |
| **Structured questions** | `AskUserQuestion` | `request_user_input`, Plan mode only | No built-in; extension can add one | `question` tool | "Ask questions" tool (since 2.4) | `ask_user` tool |

## Notes per harness

### Claude Code

**Skills.**

- Claude Code skills "follow the [Agent Skills](https://agentskills.io) open standard" and add invocation control, subagent execution and dynamic context injection ([skills](https://code.claude.com/docs/en/skills)).
- Locations ([skills](https://code.claude.com/docs/en/skills)):
  - Personal: `~/.claude/skills/<name>/SKILL.md`.
  - Project: `.claude/skills/<name>/SKILL.md`.
  - Also nested `<subdir>/.claude/skills/`, `--add-dir` directories and plugins.
- The docs list no `.agents/skills/` location ([skills.md](https://code.claude.com/docs/en/skills.md), grep 2026-10-11). Claude Code is the only harness here that does not read `.agents/skills/`.
- Supporting files (`reference.md`, `scripts/`) are supported. `${CLAUDE_SKILL_DIR}` resolves to the skill's directory ([skills](https://code.claude.com/docs/en/skills)).
- Invocation is `/skill-name args`. `$ARGUMENTS` receives the arguments ([skills](https://code.claude.com/docs/en/skills)).
- `disable-model-invocation: true` means a skill can only be invoked by slash command ([skills](https://code.claude.com/docs/en/skills)).
- User-invoked skills also work in `-p` mode ([headless](https://code.claude.com/docs/en/headless)).
- Claude-only frontmatter includes `context: fork`, `agent`, `hooks`, `disallowed-tools` and `user-invocable`.
  - Outside Claude Code, only `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools` are supported.
  - Claude.ai uploads and the Skills API reject other keys with a hard error ([skills](https://code.claude.com/docs/en/skills)).

**AGENTS.md.**

- Claude Code reads `AGENTS.md` natively from v2.1.277 ([memory](https://code.claude.com/docs/en/memory#agents-md)). By default it reads `AGENTS.md` only when there is no `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` in the working directory or above it.
- A `CLAUDE.md` that imports `@AGENTS.md` makes both load.
- The `claude-md-and-agents-md` option also loads both, but it can only be set from user or managed settings, not project settings ([memory](https://code.claude.com/docs/en/memory#agents-md)).

**Subagents and headless runs.**

- "Each subagent starts with a fresh, isolated context window" ([sub-agents](https://code.claude.com/docs/en/sub-agents)).
- Definitions live in `.claude/agents/` (project, meant to be committed) or `~/.claude/agents/`.
- Subagents can nest up to 3 levels by default ([sub-agents](https://code.claude.com/docs/en/sub-agents)).
- A skill can run itself in a subagent with `context: fork`. The subagent "doesn't see your conversation history" ([skills](https://code.claude.com/docs/en/skills)).
- Headless: `claude -p "..."` with `--allowedTools`, `--permission-mode`, `--output-format json` and `--json-schema`. `--bare` skips hooks, skills, CLAUDE.md and so on ([headless](https://code.claude.com/docs/en/headless)).

**Blocking edits to paths.**

- **Permission rules.**
  - `Edit(path)` deny rules use gitignore syntax, e.g. `Edit(/tests/**)` anchored at the project ([permissions](https://code.claude.com/docs/en/permissions)).
  - Path rules on `Write` are accepted but never consulted. Use `Edit(...)` instead ([permissions](https://code.claude.com/docs/en/permissions)).
  - Deny rules also cover Bash file commands Claude Code recognises (`sed`, `tee`) and redirections like `> file`.
  - They do **not** cover "arbitrary subprocesses that read or write files indirectly, like a Python or Node script" ([permissions](https://code.claude.com/docs/en/permissions)).
- **PreToolUse hooks.**
  - A matcher such as `Edit|Write` and exit code 2, or `permissionDecision: "deny"`, blocks the call ([hooks](https://code.claude.com/docs/en/hooks)).
  - The file path is in `tool_input.file_path`.
  - Deny rules apply even if a hook returns `allow` ([permissions](https://code.claude.com/docs/en/permissions)).
- **Sandbox.** `sandbox.filesystem.denyWrite` is OS-enforced for shell commands and their child processes. The sandbox does not cover Claude's own file tools; those are governed by `Edit` rules ([sandboxing](https://code.claude.com/docs/en/sandboxing)).
- **Where it lives.**
  - All of this goes in `.claude/settings.json`, which "can be committed to the repo" ([hooks](https://code.claude.com/docs/en/hooks)).
  - A skill can also carry its own `hooks:` in frontmatter, registered when the skill is invoked ([skills](https://code.claude.com/docs/en/skills)).
  - Skill frontmatter also accepts `disallowed-tools` ([skills](https://code.claude.com/docs/en/skills)).

**Questions.**

- `AskUserQuestion` "asks multiple-choice questions to gather requirements or clarify ambiguity", with a free-text `Other` row ([tools reference](https://code.claude.com/docs/en/tools-reference#askuserquestion-tool-behavior)).
- It is removed under `--permission-prompts none` and denied under `dontAsk` ([headless](https://code.claude.com/docs/en/headless)).

### Codex CLI (OpenAI)

**Skills.**

- Skills follow the "open agent skills standard" ([build skills](https://learn.chatgpt.com/docs/build-skills)). A skill is a `SKILL.md` with `name`/`description` plus optional `scripts/`, `references/`, `assets/` and `agents/openai.yaml`.
- Locations: repo `$CWD/.agents/skills` and parent dirs up to `$REPO_ROOT/.agents/skills`; user `$HOME/.agents/skills`; admin `/etc/codex/skills` ([build skills](https://learn.chatgpt.com/docs/build-skills)).
- `.codex/skills` is not a documented Codex location, even though Cursor reads it for compatibility.
- Explicit invocation is `/skills` or a `$skill-name` mention. Implicit invocation can be turned off with `policy.allow_implicit_invocation: false` in `agents/openai.yaml` ([build skills](https://learn.chatgpt.com/docs/build-skills)).

**AGENTS.md.**

- Codex reads `~/.codex/AGENTS.md`, then one file per directory from the project root down to cwd: `AGENTS.override.md`, then `AGENTS.md`, then `project_doc_fallback_filenames` ([AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md)).
- The combined files are capped at `project_doc_max_bytes`, 32 KiB by default.

**Subagents.**

- "Current Codex releases enable subagent workflows by default" ([subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)). The source agrees: feature `multi_agent` is stable with `default_enabled: true` ([features/src/lib.rs@6c0c675](https://github.com/openai/codex/blob/6c0c6759d0617d7670826b61aca0a931bbb6db1f/codex-rs/features/src/lib.rs#L1457-L1462)).
- Codex spawns agents "after a direct request or applicable project or skill instruction", so a skill can ask for one ([subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)).
- Custom agents are TOML files in `.codex/agents/` or `~/.codex/agents/`. "Subagents inherit your current sandbox policy" ([subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents.md)).
- The docs don't say whether a child starts with a fresh or a forked context.

**Headless.**

- `codex exec "..."` writes the final message to stdout ([non-interactive](https://learn.chatgpt.com/docs/non-interactive-mode)).
- "By default, `codex exec` runs in a read-only sandbox." Use `--sandbox workspace-write` to allow edits.
- Other flags: `--json`, `-o/--output-last-message`, `--output-schema`, `--ephemeral`.

**Blocking edits to paths.**

- **Hooks.**
  - Hooks are stable and on by default ([hooks](https://learn.chatgpt.com/docs/hooks.md); [features/src/lib.rs](https://github.com/openai/codex/blob/6c0c6759d0617d7670826b61aca0a931bbb6db1f/codex-rs/features/src/lib.rs#L1333-L1338)).
  - `PreToolUse` fires for shell and for `apply_patch` file edits (matchable as `apply_patch`, `Edit` or `Write`).
  - It blocks with `permissionDecision: "deny"` or exit code 2.
  - **Unlike Claude Code, `apply_patch` gives only the patch text in `tool_input.command`.** A guard must parse file paths out of the patch ([hooks](https://learn.chatgpt.com/docs/hooks.md)).
  - Config goes in `<repo>/.codex/hooks.json` or `<repo>/.codex/config.toml`.
  - "Non-managed hooks must be reviewed and trusted before they run". They are tracked by hash and reviewed in `/hooks`. Project hooks load only when the project `.codex/` layer is trusted ([hooks](https://learn.chatgpt.com/docs/hooks.md)).
- **Permission profiles.**
  - `[permissions.<name>.filesystem]` maps paths to `read`/`write`/`deny`, e.g. `".devcontainer" = "read"` under `":workspace_roots"` ([permissions](https://learn.chatgpt.com/docs/permissions.md)).
  - `.git` and `.codex` stay read-only under `:workspace`.
  - The docs describe profiles as governing "sandboxed commands". They don't say whether `apply_patch` respects a per-path `read` entry, so test before relying on it.
- **Trust.** Project `.codex/config.toml` loads "only when you trust the project" ([config basics](https://learn.chatgpt.com/docs/config-file/config-basic)).

**Questions.**

- `request_user_input` asks "one to three short questions", and every question needs non-empty options ([request_user_input_spec.rs@e2c0837](https://github.com/openai/codex/blob/e2c0837923ca29b54facdb567326db42a0aefd1b/codex-rs/core/src/tools/handlers/request_user_input_spec.rs)).
- It is only available in Plan mode ([config_types.rs@883af10](https://github.com/openai/codex/blob/883af106b957d21cba92121f70ce68bf58ecea50/codex-rs/protocol/src/config_types.rs#L700-L702)).
- The flag that enables it in Default mode, `default_mode_request_user_input`, is `UnderDevelopment` and off by default ([features/src/lib.rs](https://github.com/openai/codex/blob/6c0c6759d0617d7670826b61aca0a931bbb6db1f/codex-rs/features/src/lib.rs#L1793-L1798); [tool_config.rs@cd85a26](https://github.com/openai/codex/blob/cd85a26cae00385a0dd9247381ef5d1d7ffe9ef3/codex-rs/tools/src/tool_config.rs#L6-L15)).
- In normal sessions a skill therefore has to ask questions in plain chat.

### Pi (earendil-works/pi, formerly badlogic/pi-mono)

Doc links are pinned to `ea448f4` under `packages/coding-agent/`.

**Skills.**

- "Pi implements the Agent Skills specification." Skills can bundle `scripts/`, `references/` and `assets/`, referenced by paths relative to the skill dir ([docs/skills.md](https://github.com/earendil-works/pi/blob/ea448f454af474f3e2fe9733b331e17b0662f5d6/packages/coding-agent/docs/skills.md)).
- Locations: `~/.pi/agent/skills/` and `.pi/skills/` ([docs/configuration.md](https://github.com/earendil-works/pi/blob/ea448f454af474f3e2fe9733b331e17b0662f5d6/packages/coding-agent/docs/configuration.md)). Pi also reads `~/.agents/skills/` and `.agents/skills/`, walking ancestors up to the repo root ([docs/skills.md](https://github.com/earendil-works/pi/blob/ea448f454af474f3e2fe9733b331e17b0662f5d6/packages/coding-agent/docs/skills.md)).
- Explicit invocation is `/skill:name args`. `disable-model-invocation: true` is honoured.
- Project skills (`.pi/skills`, `.agents/skills`) load only after the user grants project trust ([docs/security.md](https://github.com/earendil-works/pi/blob/ea448f454af474f3e2fe9733b331e17b0662f5d6/packages/coding-agent/docs/security.md)).
- Print/JSON modes can't show the trust prompt, so they skip project resources unless `--approve` or `defaultProjectTrust: "always"` is set ([docs/security.md](https://github.com/earendil-works/pi/blob/ea448f454af474f3e2fe9733b331e17b0662f5d6/packages/coding-agent/docs/security.md)).

**AGENTS.md.**

- Context files are `AGENTS.override.md`, `AGENTS.md` or `CLAUDE.md`. Pi loads them from the agent dir, the cwd and parent directories ([docs/configuration.md](https://github.com/earendil-works/pi/blob/ea448f454af474f3e2fe9733b331e17b0662f5d6/packages/coding-agent/docs/configuration.md)).
- Context files load "regardless of project trust" ([docs/security.md](https://github.com/earendil-works/pi/blob/ea448f454af474f3e2fe9733b331e17b0662f5d6/packages/coding-agent/docs/security.md)).

**Subagents.**

- "Pi ships with powerful defaults but skips features like sub-agents and plan mode" ([README](https://github.com/earendil-works/pi/blob/ea448f454af474f3e2fe9733b331e17b0662f5d6/packages/coding-agent/README.md)).
- A reference `subagent` extension runs "each subagent in a separate `pi` process" ([examples/extensions/subagent](https://github.com/earendil-works/pi/blob/ea448f454af474f3e2fe9733b331e17b0662f5d6/packages/coding-agent/examples/extensions/subagent/README.md)).
- Headless: `pi -p "..."` writes the final text and exits; `--mode json` streams JSONL events. `--tools read,grep,find,ls` restricts the toolset ([docs/cli.md](https://github.com/earendil-works/pi/blob/ea448f454af474f3e2fe9733b331e17b0662f5d6/packages/coding-agent/docs/cli.md)).

**Blocking edits to paths.**

- Pi has no permission system or sandbox. It "does not ask for approval before every tool call" ([docs/security.md](https://github.com/earendil-works/pi/blob/ea448f454af474f3e2fe9733b331e17b0662f5d6/packages/coding-agent/docs/security.md)).
- An extension's `tool_call` handler "can mutate input or block execution" ([docs/extensions.md](https://github.com/earendil-works/pi/blob/ea448f454af474f3e2fe9733b331e17b0662f5d6/packages/coding-agent/docs/extensions.md)).
- The shipped `protected-paths.ts` example returns `{ block: true, reason }` for `write`/`edit` calls whose `event.input.path` matches ([examples/extensions/protected-paths.ts](https://github.com/earendil-works/pi/blob/ea448f454af474f3e2fe9733b331e17b0662f5d6/packages/coding-agent/examples/extensions/protected-paths.ts)).
- Project extensions in `.pi/extensions/` can be committed but load only after trust.
- `bash` is not covered by that example, so shell writes bypass it.

**Questions.**

- Pi has no built-in question tool.
- Extensions get `ctx.ui` dialogs (`confirm`, `select`) in interactive and RPC modes, and print/JSON modes have no UI ([docs/extensions.md](https://github.com/earendil-works/pi/blob/ea448f454af474f3e2fe9733b331e17b0662f5d6/packages/coding-agent/docs/extensions.md)).
- The `question.ts` and `questionnaire.ts` examples register an option-picker tool ([examples/extensions/question.ts](https://github.com/earendil-works/pi/blob/ea448f454af474f3e2fe9733b331e17b0662f5d6/packages/coding-agent/examples/extensions/question.ts)).

### OpenCode (anomalyco/opencode, formerly sst/opencode)

**Skills.**

- Project locations: `.opencode/skills/`, `.claude/skills/` and `.agents/skills/`, walking up to the git worktree ([skills](https://opencode.ai/docs/skills/)).
- Global locations: `~/.config/opencode/skills/`, `~/.claude/skills/` and `~/.agents/skills/`.
- Recognised frontmatter: `name`, `description`, `license`, `compatibility` and `metadata`.
- The agent loads a skill via the `skill` tool. A skill becomes a TUI slash command only with `metadata: { opencode/slash: "true" }`.
- Skill access can be gated per pattern under `permission.skill` ([skills](https://opencode.ai/docs/skills/)).
- The docs don't explicitly cover bundled supporting files.

**AGENTS.md.**

- OpenCode reads `AGENTS.md`, searching upward from cwd, plus global `~/.config/opencode/AGENTS.md` ([rules](https://opencode.ai/docs/rules/)).
- It falls back to `CLAUDE.md` and `~/.claude/CLAUDE.md`.
- `OPENCODE_DISABLE_CLAUDE_CODE*` env vars turn the Claude fallbacks off.

**Subagents.**

- Primary agents invoke subagents automatically, or the user can `@mention` one ([agents](https://opencode.ai/docs/agents/)).
- Custom agents live in `.opencode/agents/` or `~/.config/opencode/agents/`.
- The tool "Spawns an agent in a child session… New child sessions start with fresh context" ([subagent.ts@e31136b](https://github.com/anomalyco/opencode/blob/e31136bdbdb43e934d8bbd81e75a2065a2625699/packages/core/src/tool/plugin/subagent.ts#L55-L58)).
- Headless: `opencode run "..."` with `--agent`, `--format json` and `--auto` ("auto-approve permissions that are not explicitly denied") ([cli](https://opencode.ai/docs/cli/)).

**Blocking edits to paths.**

- `permission.edit` covers `edit`, `write` and `patch`, and takes path globs, e.g. `"edit": { "*": "allow", "tests/**": "deny" }`. The last matching rule wins ([permissions](https://opencode.ai/docs/permissions/)).
- Permissions can be overridden per agent.
- Project `opencode.json` "is also safe to be checked into Git" ([config](https://opencode.ai/docs/config/)).
- Plugins in `.opencode/plugins/` can throw from `tool.execute.before` to block a call ([plugins](https://opencode.ai/docs/plugins/)).

**Questions.**

- The built-in `question` tool asks questions "during execution" ([tools](https://opencode.ai/docs/tools/)).
- Each question has a header, text and options, plus a custom answer. Multiple questions can be answered before submitting.
- It is gated by `permission.question`.

### Cursor (editor and Cursor CLI)

**Skills.**

- Agent Skills arrived in 2.4 for the editor and CLI ([changelog 2.4](https://cursor.com/changelog/2-4)).
- Project locations: `.agents/skills/` and `.cursor/skills/` ([skills](https://cursor.com/docs/context/skills)).
- User locations: `~/.agents/skills/` and `~/.cursor/skills/`.
- Compatibility locations: `.claude/skills/`, `.codex/skills/` and their `~` equivalents.
- `name` "must match the parent folder name".
- `scripts/`, `references/` and `assets/` are supported. Invoke with `/skill-name`. `disable-model-invocation` is honoured.

**AGENTS.md.** Cursor reads `AGENTS.md` at the root and in subdirectories, with nested files taking priority ([rules](https://cursor.com/docs/context/rules)). `CLAUDE.md` is not mentioned.

**Subagents.**

- "Each subagent has its own context window" and starts "with a clean context" ([subagents](https://cursor.com/docs/context/subagents)).
- Definitions live in `.cursor/agents/` or `~/.cursor/agents/`. `.claude/agents/` and `.codex/agents/` are also read.
- Subagents are available "in the editor, CLI, and Cloud Agents".
- Headless: `-p/--print`. File changes need `--force`/`--yolo`; without it the agent only proposes edits ([headless](https://cursor.com/docs/cli/headless)).

**Blocking edits to paths.**

- **Hooks.** `.cursor/hooks.json` (project) or `~/.cursor/hooks.json` ([hooks](https://cursor.com/docs/agent/hooks)).
  - `preToolUse` matchers include `Write`, `Shell`, `Delete` and `Task`.
  - Returning `"permission": "deny"` or exiting with code 2 blocks the call.
  - `afterFileEdit` fires too late to block.
- **CLI permissions.** `<project>/.cursor/cli.json` takes `deny` entries like `Write(**/.env*)`, and "Deny rules take precedence" ([CLI permissions](https://cursor.com/docs/cli/reference/permissions)).
- The hooks page doesn't say whether every agent hook fires in the CLI.

**Questions.** Since 2.4 the agent's "interactive Q&A tool now lets agents ask clarifying questions in any conversation", and the agent keeps working while it waits ([changelog 2.4](https://cursor.com/changelog/2-4)).

### Gemini CLI

**Skills.**

- User locations: `~/.gemini/skills/` or the `~/.agents/skills/` alias ([skills](https://geminicli.com/docs/cli/skills/)).
- Workspace locations: `.gemini/skills/` or the `.agents/skills/` alias. `.agents/` wins within a tier.
- Bundled files are supported, and the skill dir becomes an allowed path once the skill is active.
- Activation is model-driven via `activate_skill`, with a **user confirmation prompt** each time.
- `/skills` only manages skills (list, enable, disable, reload). There is no per-skill slash invocation.

**AGENTS.md.**

- The default context file is `GEMINI.md`. Gemini reads it from global, workspace and ancestor directories, and just-in-time when a tool touches a directory ([GEMINI.md](https://geminicli.com/docs/cli/gemini-md/)).
- To read `AGENTS.md`, set `"context": { "fileName": ["AGENTS.md", "GEMINI.md"] }` in `settings.json`. This can go in a committed `.gemini/settings.json`.

**Subagents.**

- "Subagents are enabled by default." Each "runs in its own isolated context loop" ([subagents](https://geminicli.com/docs/core/subagents/)).
- Definitions live in `.gemini/agents/*.md` or `~/.gemini/agents/*.md`.
- Subagents cannot call other subagents.
- Headless: `gemini -p` (or a non-TTY stdin) with `--output-format json|stream-json` ([headless](https://geminicli.com/docs/cli/headless/)).

**Blocking edits to paths.**

- **Hooks.**
  - `BeforeTool` hooks take a regex matcher such as `write_file|replace` ([hooks](https://geminicli.com/docs/hooks/)).
  - A hook blocks with `{"decision":"deny"}` or exit code 2.
  - They are configured in project `.gemini/settings.json`.
  - Project hooks are fingerprinted, and a changed hook is treated as "a new, untrusted hook".
- **Policy engine.**
  - TOML `[[rule]]` entries with `toolName`, `argsPattern`, `decision` and `priority` ([policy engine](https://geminicli.com/docs/reference/policy-engine/)).
  - Workspace policies are disabled: "Defining policies in a workspace's `.gemini/policies` directory will not have any effect."
- The argument key that carries the file path for `write_file`/`replace` was not verified for this doc.

**Questions.**

- The `ask_user` tool takes 1 to 4 questions, each typed `choice` (2 to 4 options, optional `multiSelect`), `text` or `yesno` ([ask_user](https://geminicli.com/docs/tools/ask-user/)).
- It pauses until the user answers.

## Lowest common denominator

### What a portable skill can rely on everywhere

1. **One spec-only `SKILL.md`.** Use only `name` (matching the directory) and `description`, optionally `license`, `compatibility` and `metadata` ([spec](https://agentskills.io/specification)).
   - Claude-only keys (`context`, `agent`, `hooks`, `disallowed-tools`) break claude.ai/API uploads ([Claude skills](https://code.claude.com/docs/en/skills)). Other harnesses ignore them or only warn.
   - Put harness-specific hints under `metadata` (e.g. OpenCode's `opencode/slash`).
2. **Supporting files by relative path.** Put them in `references/`, `scripts/` and `assets/`, and keep `SKILL.md` under 500 lines ([spec](https://agentskills.io/specification)). Every harness gives the model a shell, so scripts run everywhere. Write them in POSIX sh or Python and don't assume `${CLAUDE_SKILL_DIR}`.
3. **Model-driven activation from `description`.** This works everywhere. Explicit invocation syntax differs (`/name`, `$name`, `/skill:name`, opt-in slash in OpenCode, none in Gemini), so user docs should say "ask your agent to use learn-to-build" and list the per-harness shortcut.
4. **Install to two directories.** No single skill directory works everywhere.
   - `.agents/skills/` (or `~/.agents/skills/`) covers Codex, Pi, OpenCode, Cursor and Gemini.
   - `.claude/skills/` covers Claude Code, plus OpenCode and Cursor.
   - The installer should copy or symlink to both.
5. **Project instructions via `AGENTS.md`.** Codex, Pi, OpenCode and Cursor read it, and so does Claude Code when no `CLAUDE.md` exists. Two adapters fill the gaps:
   - If the learner's repo has a `CLAUDE.md`, add an `@AGENTS.md` import.
   - For Gemini, ship `.gemini/settings.json` with `context.fileName`.
6. **Plain-chat questions.** Present choices as a numbered list the learner can answer by number. This works in every harness and mode, including Codex Default mode, Pi and headless runs.
7. **A headless CLI exists everywhere:** `claude -p`, `codex exec`, `pi -p`, `opencode run`, Cursor `-p` and `gemini -p`. But default write permissions differ:
   - `codex exec` is read-only by default.
   - Cursor needs `--force` to write.
   - `claude -p` denies anything that would prompt.
   - Pi print mode skips untrusted project resources.

### What must be an optional per-harness adapter

- **Isolation (fresh context).** Five of six harnesses have built-in subagents, but each invokes them differently: Agent tool, `context: fork`, Codex spawn, OpenCode `task`, Cursor Task, Gemini `@agent`. Pi has none.
  - Portable wording: "If you can spawn a subagent with fresh context, do X there; otherwise run `scripts/isolated-run.sh`."
  - The script would detect the harness and shell out to that harness's own headless CLI. That needs the same CLI and auth, so treat it as best-effort.
- **Path protection** (e.g. stopping the agent from editing the black-box test suite, per ADR-0002). No config format is shared, and every mechanism has gaps:
  - Claude deny rules miss arbitrary subprocesses.
  - Codex hooks see only patch text.
  - Pi has no permission layer, and its example extension does not guard bash.
  - Codex, Pi and Gemini project config needs trust or fingerprint approval.
  - Plan per-harness adapters: Claude `.claude/settings.json` `Edit(...)` deny plus a PreToolUse hook; Codex `.codex/hooks.json`; Pi `.pi/extensions/protect.ts`; OpenCode `opencode.json` `permission.edit`; Cursor `.cursor/hooks.json` plus `.cursor/cli.json`; Gemini `.gemini/settings.json` BeforeTool.
  - Claude, Codex, Cursor and Gemini command hooks all read JSON on stdin and treat exit 2 as block, so one guard script with per-harness payload parsing could serve all four.
  - The **portable baseline** is detection, not prevention: record a checksum or git tree hash of protected paths and have the skill's verify script refuse to grade if they changed.
- **Structured questions.**
  - Native tools: Claude `AskUserQuestion`, OpenCode `question`, Gemini `ask_user` and Cursor Q&A. Codex has one in Plan mode only.
  - Pi needs an extension.
  - Write the skill's instructions as "ask the learner to choose one of these options (use your structured question tool if you have one)", with the plain-chat list as the fallback.
- **Skill-scoped hooks and tool restrictions.** Only Claude Code supports these in skill frontmatter (`hooks`, `disallowed-tools`). Elsewhere they belong in project config.
