# Reference brief

You prove that a new Stage's tests are correct by writing a throwaway Reference solution that passes them. Nobody will see your solution: it is deleted when you finish.

## Inputs

The Project root, the staged Stage directory `.ltb/staging/NN-slug/`, the Primers of all earlier Stages (`.ltb/stages/*/primer.md`) plus the staged one, `.ltb/research/spec.md`, and an empty temp directory outside the Project.

## Steps

1. In the temp directory, write a minimal program that implements the behaviour of Stages 01 to NN as the Primers and `spec.md` describe it. Use whichever language you write fastest; the tests are black-box.
2. Write `<temp>/ltb.ini`:
   ```ini
   [project]
   x = reference
   [commands]
   build = <build command, or empty>
   run = <command that runs your program, relative to the temp dir>
   ```
3. From the Project root, run `./ltb test --staging --upto NN --config <temp>/ltb.ini`.
4. Fix your solution until it is green, or until you are sure a test is wrong: its expected value contradicts the Primer, `spec.md`, or the oracle named in `.ltb/research/overview.md`.
5. Delete the temp directory.

Write only inside the temp directory; the Project stays untouched.

## Report

- `green` or `red`, with the pass count.
- For each test you believe is wrong: the test name (or, for a `[hidden]` test, its description only), what it expects, what the spec says instead, and the citation.
- Confirmation that the temp directory is gone.

Keep your solution's code and the Hidden tests' inputs out of the report.

## Done when

The run is green, or every red test is explained as a test defect with a citation; and the temp directory no longer exists.
