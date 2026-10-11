# Test suites are black-box

Test suites exercise the Learner's X only through its external interface (wire protocol, CLI, on-disk format), never by calling prescribed functions. Unit tests on named functions would dictate the Learner's architecture, which would defeat Design reviews and Pressure Stages; black-box tests leave structure as the Learner's problem and let the harness be written in one language regardless of the Learner's. Exception: unit tests may target the Skeleton for Acquisition Learners.
