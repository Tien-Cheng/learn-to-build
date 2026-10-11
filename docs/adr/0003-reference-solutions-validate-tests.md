# Reference solutions validate every Test suite, in isolation

Before a Stage is released, an isolated subagent (assumed available in every supported harness) writes a throwaway Reference solution outside the Project repo, confirms the Test suite passes on it and fails on the starting code, then deletes it. Generated tests can be wrong, and a broken test costs a Learner far more than the extra generation. This does not contradict ADR 0001: the Reference solution is never Solution code, and the tutoring agent never sees it, so it cannot leak into hints.
