# FlakeSync Results Report

Source: `flakesync_input.csv` (6,163 tests from iDFlakies + NonDex detection).
FlakeSync detects and repairs **timing-dependent (TD)** async flaky tests via delay injection.

## 1. Projects

| | Count |
|---|---|
| Projects processed | 1 |
| Built successfully | 0 |
| Partial build | 1 |
| Clone failed | 0 |

## 2. Test Analysis

| Phase outcome | Tests |
|---|---|
| No concurrent methods found (not TD) | 0 |
| Concurrent found but no delay locations | 0 |
| Has delay locations (TD candidate) | 0 |
| **Patch generated (repaired)** | **0** |

## 3. FlakeSync Pipeline

Each test runs through 6 sequential Maven goals:

| Step | Goal | Purpose |
|---|---|---|
| 1 | `concurrentfind` | Find concurrent methods the test touches |
| 2 | `delaylocs` | Inject delays to find locations that flip the test |
| 3 | `deltadebug` | Minimize delay locations via delta-debugging |
| 4 | `critsearch` | Find critical points (root method search) |
| 5 | `barrierpointsearch` | Find barrier points linking critical points |
| 6 | `patch` | Generate patch files to repair the flakiness |

## 4. Results

- Tests with TD behavior (delay locations found): **0** across **0** projects
- Tests with generated patch: **0**
- Full data: `Sanskriti_Tiwari_flakesync.csv`
