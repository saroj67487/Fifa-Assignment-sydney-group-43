# Q4 - Match Balance (Draw Rate)

## 1. Analytic question
Was the average proportion of drawn matches per team different from 0.2?

## 2. Data wrangling
- Reused the cleaned team-level dataset.
- Focal variable: DrawRate = D / MP (proportion of a team's matches that ended level).

## 3. Data preparation and sampling
- Population: N = 48 teams.
- Sample: simple random sample of n = 35 teams, WITHOUT replacement, random_state = 4.
- The exact 35 teams used in this task's sample are saved to `data/cleaned_data/q4_35_cleaned_data.csv`.

## 4. Descriptive statistics (sample, n=35)
- Mean: 0.248
- Median: 0.250
- Std. dev.: 0.247
- Min / Max: 0.00 / 1.00
- IQR (Q1-Q3): 0.00 - 0.33
- Skewness: 1.087

## 5. Inferential statistics - 95% Confidence Interval
- 95% CI for the population mean draw rate: [0.163, 0.333] (margin of error = 0.085)

## 6. Inferential statistics - One-sample t-test
- H0: mu = 0.2   |   H1: mu != 0.2
- Sample mean = 0.248, t(34) = 1.146, p = 0.2600
- Decision (alpha = 0.05): Fail to reject H0 - not enough evidence that the mean differs from the benchmark.

## 7. Assumptions & limitations
- Shapiro-Wilk normality check: W = 0.866, p = 0.001 -> DrawRate is a bounded proportion (0-1) built from a small integer count (0-3 draws typically), so some non-normality is expected; the t-test is used here per the assignment's methodological scope, but a proportion-based test (e.g. a one-sample test for a proportion) would be a reasonable alternative.
- Draw rate is mechanically bounded between 0 and 1 and takes only a few discrete values for teams with few matches (e.g. group-stage-only teams played just 3 games), which limits the granularity of the estimate for those teams.

## 8. Figure
See outputs/figures/q4_draw_rate.png.