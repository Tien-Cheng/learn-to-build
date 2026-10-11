# The Learner authors all Solution code

The agent writes only the Harness (specs, Test suites, starter repo); every line of Solution code is written by the Learner. Claude Code's Learning output style lets the agent write most of the code and leaves trivial TODOs, which trains nothing; the skill we want to rebuild is Unassisted authorship.

The rule is carried by the Project repo's `AGENTS.md` (portable across agent harnesses), which marks Solution code paths as Learner-owned and limits the agent to the Hint ladder and Design review. Mechanical enforcement (hooks, deny rules, sandbox) is an optional per-harness adapter offered at setup, not a requirement: the main threat is the agent's default of fixing code when asked about it, which instructions address; a Learner who chooses to bypass the rule is outside what a practice tool should police. Boilerplate not worth learning ships in the starter repo before Stage 1, never mid-session.
