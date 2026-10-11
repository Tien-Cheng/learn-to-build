# Planning: the Core path

Draft `.ltb/plan.md` from `.ltb/research/` and the Learner's Goal.

## Shape of a good Core path

- **8 to 15 Stages**, covering the buildable subset in `overview.md`.
- **Each Stage is one rep of 20 to 45 minutes** for this Learner. When the Goal is Language, or the language Dial is low, aim for the short end and split Stages more finely.
- **Each Stage adds behaviour visible through the external interface**, so a black-box test can tell it is there. "Parse the page header" is visible only if some command reports it; phrase Stages as behaviour ("`.dbinfo` prints the page size").
- **Each Stage carries one concept tag**: the idea it teaches (`varint`, `b-tree-page`, `resp-parsing`). Concepts later become Drills.
- **Stage 01 is tiny**: a program that starts, takes input and responds. It proves the build, run and test loop works.
- **Order by dependency**: every Stage builds on behaviour earlier Stages made testable.
- **Goal shapes the emphasis**: Domain Projects spend Stages on X's internals; Design Projects favour Stages that extend existing components, where structure starts to matter.
- **1 to 3 Pressure Stages** (Kind `pressure`), each a real requirement change from `history.md`, placed after the Stage that built the component the change strains. Design Goals get the most.
- **0 to 3 Branches**: optional runs of 2 to 5 Stages (persistence, a write path, a second protocol) that leave the Core path after a named Stage. Domain Goals favour Branches into X's internals.

## `.ltb/plan.md` format

```markdown
# Plan: build your own <X>
Goal: <goal> · Language: <language> · Locked: <YYYY-MM-DD>

## Core path
| Plan # | Stage | Concept | Kind | Released as | Status |
|---|---|---|---|---|---|
| C1 | <behaviour, one line> | <concept tag> | core | | planned |

## Branches
### B1 <name> (leaves after C<n>)
| Plan # | Stage | Concept | Kind | Released as | Status |
|---|---|---|---|---|---|
| B1.1 | <behaviour> | <concept tag> | core | | planned |
```

- **Kind**: `core`, or `pressure` for a Pressure Stage (name the `history.md` change in the Stage column).
- **Released as**: the Stage number (`01`, `02`, ...) once released; Stages are numbered in release order.
- **Status**: `planned`, then `current` when released, `green` when its tests pass, `reviewed` after its Design review; `cut` if the Learner drops it.
- Add the `Locked:` date only after the Learner's single round of edits.

## Done when

The Core path table has 8 to 15 rows including 1 to 3 Pressure Stages, each with a behaviour, a concept tag and Status `planned`, and every row is testable through the interface named in `overview.md`.
