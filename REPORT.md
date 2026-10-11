# Flaky test detection report: iDFlakies vs NonDex

Source: `pr-data.csv` from TestingResearchIllinois/idoft.
Each project was cloned at its recorded SHA and both detectors were run over the
whole Maven project (no module restriction). Raw data: `summary.csv`.

## 1. Projects

| | Count |
|---|---|
| Attempted | 702 |
| Built and tested | 358 |
| &nbsp;&nbsp;completed normally | 260 |
| &nbsp;&nbsp;hit time limit | 98 |
| Failed | 344 |
| &nbsp;&nbsp;build_failed | 331 |
| &nbsp;&nbsp;checkout_failed | 7 |
| &nbsp;&nbsp;clone_failed | 6 |

## 2. Flaky tests found

| | iDFlakies | NonDex |
|---|---|---|
| Unique tests found | 2424 | 3754 |
| Projects with at least one find | 73 | 193 |
| Known pr-data tests reproduced | 235 | 1134 |
| New (not in pr-data) | 2189 | 2620 |

## 3. Comparison

| | Tests |
|---|---|
| Found by both | 15 |
| iDFlakies only | 2409 |
| NonDex only | 3739 |
| Total unique | 6163 |

## 4. FlakeSync input

File `flakesync_input.csv` — 6163 unique tests from
215 projects, ready for FlakeSync phase analysis.
