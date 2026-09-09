# Q3 - Overall Team Success

## 1. Analytic question
Was the average points earned per match by World Cup 2026 teams greater than 1.2?

## 2. Data wrangling
- Reused the cleaned team-level dataset.
- Focal variable: Pts_per_match = Pts / MP, standard football points (win=3, draw=1, loss=0) scaled to a per-match rate for cross-team comparability.

## 3. Data preparation and sampling
- Population: N = 48 teams.
- Sample: simple random sample of n = 35 teams, WITHOUT replacement, random_state = 3.
- The exact 35 teams used in this task's sample are saved to `data/cleaned_data/q3_35_cleaned_data.csv`.

## 4. Descriptive statistics (sample, n=35)
- Mean: 1.137 pts/match
- Median: 1.000
- Std. dev.: 0.709
- Min / Max: 0.00 / 2.62
- IQR (Q1-Q3): 0.71 - 1.77
- Skewness: 0.141

## 5. Inferential statistics - 95% Confidence Interval
- 95% CI for the population mean pts/match: [0.893, 1.380] (margin of error = 0.244)

## 6. Inferential statistics - One-sample t-test
- H0: mu = 1.2   |   H1: mu != 1.2
- Sample mean = 1.137, t(34) = -0.528, p = 0.6006
- Decision (alpha = 0.05): Fail to reject H0 - not enough evidence that the mean differs from the benchmark.

## 7. Assumptions & limitations
- Shapiro-Wilk normality check: W = 0.954, p = 0.154 -> sample looks approximately normal.
- Points-per-match compresses win/draw/loss detail into a single number; two teams with the same average could have very different win/draw mixes (explored further in Q5, which separates teams by knockout progression).

## 8. Figure
See outputs/figures/q3_team_success.png.