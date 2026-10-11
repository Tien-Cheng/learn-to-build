# Research brief: how X really works

You are researching X so that a tutor can write Primers, black-box tests and Design reviews for someone building their own X. You receive: X, the Learner's language, their Goal, an output directory, and the files to write there (some of the four below). Other researchers write the rest in parallel.

## Sources

Use primary sources: official documentation, specifications and RFCs, the real X's source code (cite a file at a commit or tag), and the authors' own design writing. Put a link on every claim. Where only a secondary source exists, say so next to the claim.

Download anything you need to run (an oracle, source to grep) into a fresh temporary directory (`mktemp -d`), and delete it before you report; the oracle's commands in `overview.md` say how to fetch it again. Write only the files you were given, and only in the output directory.

## Examples

Take every exact example (input and expected output) from a source or from running the oracle. Where neither gives one, state the rule precisely, with a small example you can follow by hand. Checking expected values at scale is done later, Stage by Stage, by the Reference solution against the oracle; your job ends at naming the oracle, so spend your time on sources rather than on writing an implementation of X.

## Files

Write tersely: tables, lists and examples over prose, each fact stated once. Length limits keep the files cheap for every later reader.

### `overview.md` (under 60 lines)

- What X is, in three sentences.
- Its external interfaces: CLI, wire protocol, file format, API. Name the one the Project should be tested through, and why. When X has no fixed external interface (a scheduler, an algorithm), propose one here and define it in `spec.md`.
- The **buildable subset**: the smallest slice of X that is still recognisably X and takes roughly 5 to 15 hours to build, with what is deliberately left out.
- **Oracle**: something runnable that produces expected outputs for tests: the real X, or an existing independent implementation (a reference tool, a course simulator). Give the command that runs it and the command that checks it is installed, or "none".

### `spec.md` (as long as the buildable subset needs; aim under 300 lines)

The externally observable behaviour of the buildable subset, precise enough to write tests from: input and output formats, byte layouts, command syntax, error behaviour, edge cases, with examples as in **Examples**. Leave out how X is built inside.

### `architecture.md` (under 120 lines)

Start the file with this line:

> SPOILER: how the real X is structured. The Learner should design their own first; this file is for Design reviews and Retrospectives.

Then: the real X's main components and their responsibilities, how data flows between them, and the key design decisions with the reasons the authors gave.

### `history.md` (under 120 lines)

Three to eight requirement changes the real X went through (new features, format versions, scaling problems, compatibility breaks), oldest first. For each: when, what changed, what it forced in the design, and a source. These become Pressure Stages, so prefer changes that a poorly structured implementation would find painful.

## Done when

Every file you were given exists within its length limit, every claim has a link, and every exact example comes from a source, the oracle, or a rule you can follow by hand. `overview.md`, if yours, names the test interface, the buildable subset and the oracle status; `history.md`, if yours, lists at least three changes. Return a five-line summary and the file paths.
