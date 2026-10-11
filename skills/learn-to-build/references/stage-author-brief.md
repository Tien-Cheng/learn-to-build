# Stage author brief

You write one Stage of a build-your-own-X practice Project: a Primer the Learner reads and a black-box Test suite they must turn green by writing all the code themselves. You receive the plan row, research files, Goal, language, Dials, earlier Primers, the test-helper API, and a staging directory. Write two files there.

## `primer.md`

The Primer explains **what** to build and the concepts behind it. The structure of the Learner's code (modules, types, function names, file layout) is theirs to design, so the Primer describes behaviour and ideas only.

Sections, in order:

1. `# Stage NN: <behaviour>`
2. **What you're building**: the new behaviour, with exact example inputs and outputs.
3. **Interface contract**: the precise formats, syntax and error behaviour the tests check, taken from `spec.md`.
4. **Concepts**: the domain ideas this Stage needs, explained from first principles, with links to primary sources. Go deeper when the domain Dial is low or the Goal is Domain.
5. **Language you'll need**: include when the Goal is Language or the language Dial is 2 or lower. The language features this Stage exercises (for example ownership and slices in Rust), each with a small standalone example about something other than X.
6. **Tests**: the description of every test, as a bullet list, so the Learner knows the target.
7. **Done when**: `./ltb test` prints `green`.

Write for a capable engineer: short, concrete, no padding.

## `public.py`

A Test suite for this Stage's new behaviour only; earlier Stages keep their own tests.

- Get the helpers from `ltb` (`from ltb import run, serve, expect, tmpdir`); the API you were given documents them.
- **Black-box**: drive the Learner's program only through its external interface, via `run()` or `serve()`.
- **One behaviour per test**, 3 to 8 tests. Each `test_*` function has a one-line docstring describing the behaviour in the Learner's terms; it is what they see when the test fails.
- **Expected values come from `spec.md`**, or from the oracle named in `overview.md` when one exists. When a test runs the oracle, check it is installed with `shutil.which` and fail with an install instruction if not.
- **Deterministic**: no timing races, no random data without a fixed seed, files only inside `tmpdir()`.
- **Assert what the spec fixes**: exact output where the spec is exact, `in` or prefix checks where it allows variation.
- Use `expect(actual, expected, label)` for readable diffs.

## Done when

Both files exist; every behaviour in the Primer's interface contract has at least one test; every test has a docstring. Return the test names with their descriptions, plus any place where `spec.md` was ambiguous and how you resolved it.
