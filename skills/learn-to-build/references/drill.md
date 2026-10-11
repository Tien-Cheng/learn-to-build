# drill: a timed rebuild from memory

A Drill deletes the Learner's own files for one concept on a throwaway branch and gives them 15 minutes to rebuild them until that Stage's tests pass. It fights Atrophy through spaced retrieval. "Due" means ready, never owed.

## 1. What is ready

Run `./ltb drill list`. If nothing is ready, tell the Learner when the next one is, and stop.

**Done when** you have the suggested Drill (marked `*`).

## 2. Offer it

**ask** whether they want to do the suggested Drill now. Explain the rules in three lines: their files for that concept are removed on a throwaway branch; they get 15 minutes with no notes and no AI; their real branch is untouched and restored afterwards. They need a clean tree first (commit or stash).

**Done when** they said yes, or no (then stop).

## 3. Run it

Ask the Learner to run, in their own terminal:

- `./ltb drill start <concept>`, which starts the clock;
- `./ltb drill check` whenever they want to see where they stand;
- `./ltb drill finish` when green or when time is up (`./ltb drill discard` abandons it with nothing recorded).

While the Drill runs, help with nothing about the code: retrieval is the point. You can answer questions about the rules.

**Done when** they have run `finish` or `discard`.

## 4. Afterwards

Relay the result and when the next Drill is ready. After a fail, suggest re-reading that Stage's Primer; the Drill comes back in a day.

**Done when** the Learner has the result.
