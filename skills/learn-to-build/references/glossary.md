# learn-to-build

A self-directed practice system that rebuilds and grows a programmer's ability to write code themselves when day-to-day work is done mostly by AI.

## Learners and their problem

**Learner**:
The person doing the practice; the only author of Solution code.
_Avoid_: User, student

**Atrophy**:
Decay of a coding skill the Learner once had, through disuse while AI does the work.
_Avoid_: Brainrot (fine in chat, too vague in docs)

**Acquisition**:
Forming a skill the Learner never had, e.g. one their AI-heavy job should have taught them but didn't.
_Avoid_: Onboarding, learning from scratch

**Goal**:
What a Learner wants a Project to teach: the language, the domain, or design. Decides which Dial gets the extra difficulty.
_Avoid_: Focus, track, mode

**Dial**:
One of three calibrated levels per Learner per Project: language fluency, domain familiarity, design skill. Set by the Diagnostic, adjusted at each `next`.
_Avoid_: Proficiency, level, skill rating

**Diagnostic**:
The skippable setup check that sets initial Dials: an adaptive "what does this print" quiz for language, a few concept questions for domain; design skill is read from Stage 1's Design review instead.
_Avoid_: Placement test, assessment

**Unassisted authorship**:
The core skill being trained: turning a spec into working code yourself, from a blank page, without AI.
_Avoid_: Coding ability, fluency (too loose)

## Practice structure

**Project**:
A build-your-own-X journey: an ordered set of Stages that together produce a working X.
_Avoid_: Course, challenge, curriculum

**Project repo**:
The repo (or subdirectory of a Learner's learning monorepo) where one Project's Solution code, Harness and progress live; never this skill's repo.
_Avoid_: Workspace, sandbox

**Stage**:
One self-contained rep of 20–45 minutes, done when its Test suite passes.
_Avoid_: Lesson, step, task, TODO

**Core path**:
The fixed, linear sequence of Stages every Learner of a Project completes.
_Avoid_: Main quest, spine

**Branch**:
An optional run of Stages leaving the Core path (e.g. persistence, replication), chosen by the Learner.
_Avoid_: Extension, side quest, DAG node

**Drill**:
A short, timed, from-memory rewrite of an earlier Stage's core against its Test suite, scheduled days later to fight Atrophy.
_Avoid_: Review, revision, flashcard

**Pressure Stage**:
A Stage whose requirement change is chosen to be cheap for well-structured Solution code and painful for poorly structured code.
_Avoid_: Refactor stage, twist

**Replay** (v2):
A Project generated from a concept the Learner saw AI implement at work, rebuilt from scratch outside the work codebase.
_Avoid_: Shadowing, re-implementation

## Checks and help

**Primer**:
The agent-written explanation of a Stage's concept and spec (the "what", never the code structure), citing primary sources; read before the Stage.
_Avoid_: Lesson, tutorial, docs

**Concept check**:
One to three quick prediction questions at the end of a Primer that unlock the Stage's Test suite; a wrong answer points back to the Primer rather than blocking.
_Avoid_: Quiz, MCQ, gate

**Skeleton**:
A suggested module structure given when the design-skill Dial is low, withdrawn progressively over later Stages; its one or two pure boundaries come with unit tests in the Learner's language.
_Avoid_: Template, starter code

**Reference solution**:
A throwaway solution written by an isolated subagent only to prove a Test suite is correct, then deleted; never seen by the Learner or the tutoring agent.
_Avoid_: Answer key, model solution

**Test suite**:
The pass/fail checks that decide whether a Stage's behaviour is correct, exercising the X only through its external interface (protocol, CLI, file format).
_Avoid_: Grader, autograder

**Hidden test**:
A Test suite check kept in `.ltb/hidden/` behind a spoiler banner and out of search results, so it is not read by accident; on failure the Learner sees its description, never its input.
_Avoid_: Private test, secret test

**Design review**:
The agent's critique of Solution code structure after a Stage's Test suite passes; the Stage is done only once each point is fixed or defended. Calibrated to the current Stage, so it flags over-engineering as readily as under-engineering; closes with how the real X solves the same problem.
_Avoid_: Code review (too generic), feedback

**Defence**:
The Learner's short written justification for keeping a design choice a Design review questioned. The agent may answer with one rebuttal; the Learner's reply is final.
_Avoid_: Override, dismissal

**Retrospective**:
The required whole-codebase review that closes a Project's Core path: compares the Learner's architecture with the real X, revisits Defences against later Pressure Stages, and seeds Drills.
_Avoid_: Final review, capstone, post-mortem

**Hint ladder**:
The ordered rungs of help a stuck Learner can request, from restating the failing test up to pseudocode, never reaching code for the current Stage.
_Avoid_: Help, tips

## Ownership

**Solution code**:
Code that satisfies a Stage. The Learner writes it, except where the Stage's Assistance mode lets the agent write some.
_Avoid_: Implementation, answer

**Assistance mode**:
The Learner's choice of how much code the agent may write in a Stage: **Solo** (none), **Pair** (boilerplate and plumbing around the Stage's concept, on request) or **Lead** (the code, from the Learner's Approach). Set per Project, switchable per Stage. Debugging, Drills, Concept checks and Design reviews stay the Learner's in every mode.
_Avoid_: AI level, autonomy, help setting

**Approach**:
The Learner's short written plan for a Lead Stage (decomposition, data, edge cases), written before the agent writes any code.
_Avoid_: Prompt, spec, plan (the plan is the Project's Stage list)

**Bug hunt**:
A Lead-Stage review exercise: the Learner reviews a proposed patch to the agent-written code that hides one planted defect, and must find it. The patch is never applied.
_Avoid_: Planted bug, spot-the-bug

**Walkthrough**:
The Learner's explanation of agent-written code, checked by the agent, before that code counts as done.
_Avoid_: Code reading, comprehension quiz

**Harness**:
Everything the agent provides around Solution code: Stage specs, Test suites, and the starter repo.
_Avoid_: Scaffold, boilerplate
