# FIFA World Cup 2026 - Assessment 2 (Team Analytics)

Statistical analysis of team-level results from the FIFA World Cup 2026, built
around five distinct, independently-sampled analytic tasks. Each task follows
the same pipeline: **data wrangling -> sampling (35 teams) -> descriptive
statistics -> 95% confidence interval -> hypothesis test (t-test)**.

## Team members and question ownership

| Question | Focal point | Student | Student ID |
|----------|-------------|---------|------------|
| Q1 - Attacking output | Goals scored per match | Saroj Poudel | s396872 |
| Q2 - Defensive performance | Goals conceded per match | Rajiv Sadula | s399118 |
| Q3 - Overall team success | Points earned per match | Raju Chaulagain | s398426 |
| Q4 - Match balance (draw rate) | Proportion of matches drawn | Saad Mahmud Osmaniu | s400601 |
| Q5 - Knockout impact on goal difference | Advanced vs. group-stage-exit teams | Group task (all members) | - |

> Note: the assignment brief requires 4 analytic tasks; this project includes
> a 5th (Q5) as a bonus/extension covering a two-sample t-test, completed
> collaboratively by the group. If only 4 tasks are required for submission,
> Q1-Q4 alone satisfy every rubric requirement.

## Project structure
```
worldcup2026-assessment2/
├── data/
│   ├── rawdata/
│   │   └── raw_data.csv                        # data exactly as provided (48 teams)
│   └── cleaned_data/
│       ├── full_population_cleaned_data.csv     # all 48 teams, cleaned & wrangled
│       ├── q1_35_cleaned_data.csv               # Q1's own random sample of 35 teams
│       ├── q2_35_cleaned_data.csv               # Q2's own random sample of 35 teams
│       ├── q3_35_cleaned_data.csv               # Q3's own random sample of 35 teams
│       ├── q4_35_cleaned_data.csv               # Q4's own random sample of 35 teams
│       └── q5_35_cleaned_data.csv               # Q5's own random sample of 35 teams
├── src/
│   ├── data_cleaning.py                         # wrangles rawdata/raw_data.csv -> full_population_cleaned_data.csv
│   ├── utils.py                                  # sampling / stats / plotting helpers, shared by every question
│   ├── q1_attacking_output.py                    # Q1 analysis (produces q1_35_cleaned_data.csv + figure + report)
│   ├── q2_defensive_performance.py               # Q2 analysis
│   ├── q3_team_success.py                        # Q3 analysis
│   ├── q4_draw_rate.py                           # Q4 analysis
│   └── q5_knockout_goal_difference.py            # Q5 analysis
├── outputs/
│   ├── figures/     # histogram + boxplot PNG for each task
│   └── results/     # a full Markdown report per task (question -> conclusion)
├── run_all.py       # regenerates everything end to end
├── requirements.txt
└── README.md
```

## How to run the project

**1. Install Python 3.9+** (pandas 2.x requires it; if you're on an older
Python, `pip install pandas numpy scipy matplotlib` without version pins
will still install the newest compatible versions).

**2. Install dependencies** (from the project root, the folder containing
this README):
```bash
pip install -r requirements.txt
```

**3. Run the full pipeline:**
```bash
python run_all.py
```

That single command:
- reads `data/rawdata/raw_data.csv`,
- cleans it and writes `data/cleaned_data/full_population_cleaned_data.csv`,
- for each of the 5 questions: draws its own independent random sample of 35
  teams, saves that exact sample to `data/cleaned_data/qX_35_cleaned_data.csv`,
  runs the full statistical analysis, saves a figure to `outputs/figures/`,
  and writes a Markdown report to `outputs/results/`.

**To run just one question** (e.g. Q3), from the project root:
```bash
cd src
python q3_team_success.py
```

## What each script outputs

| Script | Console output | Files it writes |
|--------|-----------------|------------------|
| `src/data_cleaning.py` | Prints the cleaned dataset's shape and first 5 rows | `data/cleaned_data/full_population_cleaned_data.csv` |
| `src/q1_attacking_output.py` | Prints `"Q1 done."` | `data/cleaned_data/q1_35_cleaned_data.csv`, `outputs/figures/q1_attacking_output.png`, `outputs/results/q1_attacking_output.md` |
| `src/q2_defensive_performance.py` | Prints `"Q2 done."` | `data/cleaned_data/q2_35_cleaned_data.csv`, `outputs/figures/q2_defensive_performance.png`, `outputs/results/q2_defensive_performance.md` |
| `src/q3_team_success.py` | Prints `"Q3 done."` | `data/cleaned_data/q3_35_cleaned_data.csv`, `outputs/figures/q3_team_success.png`, `outputs/results/q3_team_success.md` |
| `src/q4_draw_rate.py` | Prints `"Q4 done."` | `data/cleaned_data/q4_35_cleaned_data.csv`, `outputs/figures/q4_draw_rate.png`, `outputs/results/q4_draw_rate.md` |
| `src/q5_knockout_goal_difference.py` | Prints `"Q5 done."` | `data/cleaned_data/q5_35_cleaned_data.csv`, `outputs/figures/q5_knockout_goal_difference.png`, `outputs/results/q5_knockout_goal_difference.md` |
| `run_all.py` | Runs all of the above in order, prints a step-by-step log | Everything above, regenerated in one go |

Each `outputs/results/qX_*.md` report is self-contained and follows the
exact structure the assignment asks for: **1. Analytic question, 2. Data
wrangling, 3. Data preparation and sampling, 4. Descriptive statistics,
5. Confidence interval, 6. t-test, 7. Assumptions & limitations, 8. Figure.**

## Dataset
The source table is the FIFA World Cup 2026 final team standings (48 teams),
covering matches played (MP), wins/draws/losses (W/D/L), goals for/against
(GF/GA), goal difference (GD), points (Pts), top scorer, and starting
goalkeeper, plus the stage each team was eliminated in (final ranking 1-4,
Quarter-final, Round of 16, Round of 32, or Group stage).

## The five analytic tasks

| # | Question | Focal point | Variable | Test |
|---|----------|-------------|----------|------|
| Q1 | Was average goals scored/match > 1.5? | Attacking output | `GF_per_match` | One-sample t-test |
| Q2 | Was average goals conceded/match < 1.5? | Defensive solidity | `GA_per_match` | One-sample t-test |
| Q3 | Was average points/match > 1.2? | Overall tournament success | `Pts_per_match` | One-sample t-test |
| Q4 | Was average draw rate different from 0.20? | Match balance/competitiveness | `DrawRate` | One-sample t-test |
| Q5 | Do teams that advanced past the group stage have a different goal difference/match than group-stage exits? | Knockout progression impact | `GD_per_match` | Two-sample (Welch) t-test |

Each task draws its **own independent random sample of 35 of the 48 teams**
(a different `random_state` per task — 1 through 5) and saves that exact
sample to its own CSV under `data/cleaned_data/`, so no two tasks analyse
identical data and every result is fully reproducible/inspectable on its own.
Full working — descriptive statistics, the 95% CI, the t-test
statistic/p-value, a decision at alpha = 0.05, and an explicit discussion of
assumptions/limitations — is written out in each task's report under
`outputs/results/`.

## Data wrangling notes
The raw scrape needed non-trivial cleaning before analysis:
- Removed blank "spacer" rows separating stage groups.
- Split the combined `"es Spain"`-style Squad field into a country code and
  a clean country name.
- Cast `GD` (stored as a signed string like `"+13"`) and all other numeric
  columns to proper numeric types.
- Recoded the `Rk` column (which mixes final placements `1-4` with stage
  labels `QF`/`R16`/`R32`/`GR`) into an ordered `Stage` category and a
  binary `Advanced` flag used in Q5.
- Engineered seven per-match rate variables (`GF_per_match`, `GA_per_match`,
  `GD_per_match`, `Pts_per_match`, `WinRate`, `DrawRate`, `LossRate`) so that
  teams eliminated after only 3 group matches are fairly comparable to teams
  that played all 8 matches at the tournament.

## Notes on methodology
- **Population vs. sample**: the population is all 48 competing teams; each
  task treats this as a sampling frame and draws a simple random sample of
  n = 35 without replacement.
- **Confidence intervals** use the t-distribution (`scipy.stats.t`), correct
  given the small sample size and unknown population standard deviation.
- **t-tests**: Q1-Q4 use one-sample t-tests against a stated benchmark; Q5
  uses Welch's two-sample t-test (unequal variances) to compare teams that
  advanced past the group stage against those eliminated in it.
- **Assumption checks**: each report includes a Shapiro-Wilk normality check
  on the sample and a discussion of what it implies for the validity of the
  t-test.
- **Limitations**: acknowledged in every report — e.g. the population is
  small (48), so a 35-team sample is a large fraction (~73%) of it; per-match
  rate variables partly confound attacking/defensive strength with how far a
  team progressed (better teams play more matches, but also face tougher
  opposition).

## Data source citation
Team statistics adapted from public World Cup coverage (FIFA official site,
FBref, and The Stats Don't Lie), per the course-provided data sources.
