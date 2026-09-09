# Q2 - Defensive Performance

## 1. Analytic question
Was the average goals conceded per match by World Cup 2026 teams less than 1.5?

## 2. Data wrangling
- Reused the cleaned team-level dataset produced in src/data_cleaning.py.
- Focal variable: GA_per_match = GA / MP (goals against per match played),
  engineered so teams with different numbers of matches are comparable.

## 3. Data preparation and sampling
- Population: N = 48 teams.
- Sample: simple random sample of n = 35 teams, WITHOUT replacement, random_state = 2 (a different seed/sample from every other task).
- The exact 35 teams used in this task's sample are saved to `data/cleaned_data/q2_35_cleaned_data.csv`.

## 4. Descriptive statistics (sample, n=35)
- Mean: 1.540 goals conceded/match
- Median: 1.333
- Std. dev.: 0.825
- Min / Max: 0.12 / 4.00
- IQR (Q1-Q3): 1.00 - 2.00
- Skewness: 0.975

## 5. Inferential statistics - 95% Confidence Interval
- 95% CI for the population mean goals conceded/match: [1.257, 1.824] (margin of error = 0.283)

## 6. Inferential statistics - One-sample t-test
- H0: mu = 1.5   |   H1: mu < 1.5
- Sample mean = 1.540, t(34) = 0.288, p = 0.7747 (two-sided; halve for the one-sided test above)
- Decision (alpha = 0.05): Fail to reject H0 - not enough evidence that the mean differs from the benchmark.

## 7. Assumptions & limitations
- Shapiro-Wilk normality check: W = 0.932, p = 0.032 -> mild deviation from normality; t-test remains reasonably robust at n=35.
- Teams eliminated early only contribute 3 matches, which may be against weaker group opposition, so GA_per_match is not perfectly comparable across all teams; this is acknowledged rather than corrected for, given the scope of the task.

## 8. Figure
See outputs/figures/q2_defensive_performance.png.