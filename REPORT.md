# Flaky test detection report: iDFlakies vs NonDex

Source: `pr-data.csv` from TestingResearchIllinois/idoft.
Each project was cloned at its recorded SHA and both detectors were run over the
whole Maven project (no module restriction). Raw data: `summary.csv`.

## 1. Projects

| | Count |
|---|---|
| Attempted | 5 |
| Built and tested | 3 |
| &nbsp;&nbsp;completed normally | 2 |
| &nbsp;&nbsp;hit time limit | 1 |
| Failed | 2 |
| &nbsp;&nbsp;build_failed | 2 |

## 2. Flaky tests found

| | iDFlakies | NonDex |
|---|---|---|
| Unique tests found | 86 | 11 |
| Projects with at least one find | 1 | 2 |
| Known pr-data tests reproduced | 43 | 5 |
| New (not in pr-data) | 43 | 6 |

## 3. Comparison

| | Tests |
|---|---|
| Found by both | 0 |
| iDFlakies only | 86 |
| NonDex only | 11 |
| Total unique | 97 |

## 4. FlakeSync input

File `flakesync_input.csv` — 97 unique tests from
2 projects, ready for FlakeSync phase analysis.
