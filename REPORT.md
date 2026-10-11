# Flaky test detection report: iDFlakies vs NonDex

Source: `pr-data.csv` from TestingResearchIllinois/idoft.
Each project was cloned at its recorded SHA and both detectors were run over the
whole Maven project (no module restriction). Raw data: `summary.csv`.

## 1. Projects

| | Count |
|---|---|
| Attempted | 7 |
| Built and tested | 6 |
| &nbsp;&nbsp;completed normally | 0 |
| &nbsp;&nbsp;hit time limit | 6 |
| Failed | 1 |
| &nbsp;&nbsp;build_failed | 1 |

## 2. Flaky tests found

| | iDFlakies | NonDex |
|---|---|---|
| Unique tests found | 48 | 20 |
| Projects with at least one find | 1 | 1 |
| Known pr-data tests reproduced | 1 | 13 |
| New (not in pr-data) | 47 | 7 |

## 3. Comparison

| | Tests |
|---|---|
| Found by both | 2 |
| iDFlakies only | 46 |
| NonDex only | 18 |
| Total unique | 66 |

## 4. FlakeSync input

File `flakesync_input.csv` — 66 unique tests from
1 projects, ready for FlakeSync phase analysis.
