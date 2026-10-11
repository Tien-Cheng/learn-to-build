# Diagnostic

Sets the starting Dials. Quick, and skippable: a Learner who knows their level can just say so.

## 1. Offer it

**ask**: "Two-minute placement check, or set your levels yourself?"

1. Placement check
2. I'll rate myself (then **ask** for language and domain, each 1 to 5, using the level descriptions in [dials.md](dials.md))
3. Skip (both start at 3)

**Done when** the Learner has chosen; for options 2 and 3, record the values and skip to step 4.

## 2. Language fluency

An adaptive "what does this print" quiz in the Project's language. Write each question yourself: a snippet of 3 to 10 lines and four choices (one correct). Difficulty levels:

1. basic syntax, control flow, strings
2. standard collections, functions, errors
3. idioms: iteration protocols, comprehension or closure semantics, ownership or references as the language has them
4. subtle semantics: mutability and aliasing, evaluation order, integer and float edges
5. corner cases experts trip on

Start at level 3. After a correct answer go one level up, after a wrong one go one level down. Stop after 6 questions, or earlier once the Learner has answered right at some level and wrong at the next level up twice. **ask** each question; reveal the right answer after each one.

**Done when** the language Dial is the highest level answered correctly (1 if none).

## 3. Domain familiarity

Ask 2 or 3 short questions about X's core concepts from `.ltb/research/overview.md` (for SQLite: what a page is, what a B-tree is for, what a schema table holds), easiest first.

**Done when** the domain Dial is set: 1 for none right, 3 for most right, 4 for all right with confident answers.

## 4. Record

Design skill is not quizzed; Stage 01's Design review sets it, so it starts at 3. Keep the three values for `new` to write into `.ltb/config`, and tell the Learner their starting Dials in one line.

**Done when** the Learner has seen all three values.
