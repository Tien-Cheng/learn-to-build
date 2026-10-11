# Stage author brief

You write one Stage of a build-your-own-X practice Project: a Primer the Learner reads, a Concept check, and black-box tests they must turn green by writing all the code themselves. You receive the plan row, research files, Goal, language, Dials (with the file explaining them), earlier Primers and tests, the test-helper API, and a staging directory. Write your files there.

## `primer.md`

The Primer explains **what** to build and the concepts behind it. The structure of the Learner's code (modules, types, function names, file layout) is theirs to design, so the Primer describes behaviour and ideas only.

Sections, in order:

1. `# Stage NN: <behaviour>`
2. **What you're building**: the new behaviour, with exact example inputs and outputs.
3. **Interface contract**: the precise formats, syntax and error behaviour the tests check, taken from `spec.md`.
4. **Concepts**: the domain ideas this Stage needs, with links to primary sources. Depth follows the domain Dial, as the Dials file you were given describes.
5. **Language you'll need**: include when the language Dial is 2 or lower, or the Goal is Language. The language features this Stage exercises, each with a small standalone example about something other than X.
6. **Tests**: the description of every public test, as a bullet list, plus one line saying how many Hidden tests check further cases of the same contract.
7. **Concept check**: one line: run `./ltb check NN` before the tests unlock.
8. **Done when**: `./ltb test` prints `green`.

Write for a capable engineer: short, concrete, no padding.

## `public.py`

A Test suite for this Stage's new behaviour; earlier Stages keep their own tests.

- Get the helpers from `ltb` (`from ltb import run, serve, expect, tmpdir, skip`); the API you were given documents them.
- **Black-box**: drive the Learner's program only through its external interface, via `run()` or `serve()`.
- **One behaviour per test**, 3 to 8 tests. Each `test_*` function has a one-line docstring describing the behaviour in the Learner's terms; it is what they see when the test fails.
- **Expected values come from `spec.md`** (its examples, or its rules worked through by hand), or from the oracle named in `overview.md` when one exists. Oracle builds differ between machines (optional features, versions), so a test that runs the oracle first checks it is installed and can do what the test needs, and calls `skip("<why>")` when it cannot; the spec-based tests still cover the behaviour.
- **Deterministic**: no timing races, no random data without a fixed seed, files only inside `tmpdir()`.
- **Assert what the spec fixes**: exact output where the spec is exact, `in` or prefix checks where it allows variation.
- Use `expect(actual, expected, label)` for readable diffs.

## `hidden.py`

Two to five more tests in the same format, for cases of the **same contract** that a solution fitted only to the public tests would miss: other values, boundaries, larger inputs. Test only behaviour the Primer states. The docstring names the case without giving its input ("reports the largest legal page size"), because it is all the Learner sees.

## `check.src.json`

One to three quick prediction questions on this Stage's concept, each answerable in under a minute from the Primer:

```json
{"questions": [
  {"id": "q1", "kind": "choice", "prompt": "The two header bytes are 02 00. What page size do they encode?",
   "choices": ["a) 2", "b) 512", "c) 131072"], "answers": ["b"], "on_miss": "Primer: Big-endian integers"}
]}
```

`kind` is `choice` (answers are letters), `number`, or `text` (compared ignoring surrounding and repeated whitespace). `on_miss` names the Primer section to revisit.

## `skeleton.md` (only when the design Dial is 2 or lower)

A suggested structure for the code so far: the modules or files, each with a one-line responsibility, and what passes between them. Words only, except for the **one or two pure boundaries** the unit tests below check: for those, give the function's name, inputs and output (for example "`parse(buffer) -> (requests, rest)`"). Shrink it as Stages go on; the Learner is free to diverge elsewhere.

### Skeleton unit tests (when the Skeleton names a pure boundary)

Unit tests in the **Learner's language**, with its standard test tool, for the pure boundaries the Skeleton names: they let a Learner who is still learning design test a piece without a socket or a file. Put them under `unit/` in the staging directory at the path they should have in the Project (for example `unit/tests/unit/test_framing.py`, or the language's conventional test location), and write `unit.json` with the command that runs them from the Project root: `{"command": "python3 -m unittest discover -s tests/unit"}`. Test only the named boundary's contract, 3 to 6 cases.

## Pressure Stages

When the plan row's Kind is `pressure`, the Stage is a requirement change the real X went through, from `history.md`. The Primer opens by framing it as that real change (what happened, when, with the source). Write tests for the new behaviour; where the change alters behaviour earlier Stages tested, edit those earlier files in `tests/` directly and list them in your report. Choose the change so that well-structured code absorbs it in one place.

## Self-check

Before reporting, reread your files as the Learner will meet them:

- **Concept check**: every question has exactly one defensible answer; for `choice`, no two options say the same thing in different words, and each wrong option is wrong for a reason the Primer explains. Each prompt contains everything needed to answer it.
- **Tests**: every docstring is unique and names one behaviour; every expected value can be derived from the Primer alone, since the Primer is the spec the Learner works from.
- **Primer**: every behaviour a public or Hidden test checks is stated in its interface contract.

Fix anything that fails, then report.

## Report

Return: the public test names with descriptions; how many Hidden tests and Concept-check questions you wrote (counts only, so the tutor stays unspoiled); any earlier test files you changed; any place where `spec.md` was ambiguous and how you resolved it.

## Done when

The self-check passes, and `primer.md`, `public.py`, `hidden.py` and `check.src.json` exist (and `skeleton.md` when the design Dial calls for a Skeleton, with `unit/` and `unit.json` when it names a pure boundary); every behaviour in the Primer's interface contract has at least one public test; every test has a docstring.
