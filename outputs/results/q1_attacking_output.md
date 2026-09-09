# Q1 - Attacking Output

## 1. Analytic question
Was the average goals scored per match by World Cup 2026 teams greater than 1.5?

## 2. Data wrangling
- Loaded the cleaned team-level dataset (48 teams, 21 tidy variables).
- Focal variable engineered during cleaning: GF_per_match = GF / MP, so teams
  that played a different number of matches (3 to 8, depending on how far they
  advanced) are placed on a comparable per-match scale.

## 3. Data preparation and sampling
- Population: all N = 48 teams that competed in the tournament.
- Sample: simple random sample of n = 35 teams drawn WITHOUT replacement
  (pandas .sample, random_state = 1). This is a distinct random draw from
  every other task in this assignment.
- The exact 35 teams used in this task's sample are saved to `data/cleaned_data/q1_35_cleaned_data.csv`.

## 4. Descriptive statistics (sample, n=35)
- Mean: 1.233 goals/match
- Median: 1.250
- Std. dev.: 0.724
- Min / Max: 0.00 / 2.75
- IQR (Q1-Q3): 0.67 - 1.71
- Skewness: 0.451

## 5. Inferential statistics - 95% Confidence Interval
- 95% CI for the population mean goals/match: [0.984, 1.482]  (margin of error = 0.249)

## 6. Inferential statistics - One-sample t-test
- H0: mu = 1.5   |   H1: mu > 1.5
- Sample mean = 1.233, t(34) = -2.182, p = 0.0362 (two-sided; halve for the one-sided test above)
- Decision (alpha = 0.05): Reject H0 - mean goals/match is significantly different from the benchmark.

## 7. Assumptions & limitations
- Shapiro-Wilk normality check on the sample: W = 0.953, p = 0.142 -> sample looks approximately normal.
- The population itself is only 48 teams, so a sample of 35 is a large fraction (~73%) of the population; a finite population correction could tighten the CI further, but was not applied here to keep the method consistent with the standard t-based CI taught in this course.
- GF_per_match rewards attacking teams that also progressed further (more matches
  played against tougher opposition), which is a potential confound.

## 8. Figure
See outputs/figures/q1_attacking_output.png (histogram of the full 48-team 
population + boxplot comparing population vs. the drawn sample).