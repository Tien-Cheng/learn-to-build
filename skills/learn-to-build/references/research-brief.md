# Research brief: how X really works

You are researching X so that a tutor can write Primers, black-box tests and Design reviews for someone building their own X. You receive: X, the Learner's language, their Goal, and an output directory. Write four Markdown files there.

## Sources

Use primary sources: official documentation, specifications and RFCs, the real X's source code (cite a file at a commit or tag), and the authors' own design writing. Put a link on every claim. Where only a secondary source exists, say so next to the claim.

## Files

### `overview.md`

- What X is, in three sentences.
- Its external interfaces: CLI, wire protocol, file format, API. Name the one the Project should be tested through, and why.
- The **buildable subset**: the smallest slice of X that is still recognisably X and takes roughly 5 to 15 hours to build, with what is deliberately left out.
- **Oracle**: whether the real X (or a reference tool) can be run locally to produce expected outputs for tests, and the exact command to check it is installed.

### `spec.md`

The externally observable behaviour of the buildable subset, precise enough to write tests from: input and output formats, byte layouts, command syntax, error behaviour, edge cases. Give concrete examples (exact input, exact output). Leave out how X is built inside.

### `architecture.md`

Start the file with this line:

> SPOILER: how the real X is structured. The Learner should design their own first; this file is for Design reviews and Retrospectives.

Then: the real X's main components and their responsibilities, how data flows between them, and the key design decisions with the reasons the authors gave.

### `history.md`

Requirement changes the real X went through (new features, format versions, scaling problems, compatibility breaks), oldest first. For each: when, what changed, what it forced in the design, and a source. These become Pressure Stages, so prefer changes that a poorly structured implementation would find painful.

## Done when

All four files exist, every claim has a link, `history.md` lists at least three changes, and `overview.md` names the test interface, the buildable subset and the oracle status. Return a five-line summary and the file paths.
