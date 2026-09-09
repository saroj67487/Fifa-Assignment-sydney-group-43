# Q5 - Knockout Impact on Goal Difference

## 1. Analytic question
Did teams that advanced beyond the group stage have a different average goal difference per match than teams eliminated in the group stage?

## 2. Data wrangling
- Reused the cleaned team-level dataset, including the Stage/Advanced flags engineered from the original 'Rk' column (ranks 1-4, QF, R16, R32 -> Advanced=True; GR -> Advanced=False).
- Focal variable: GD_per_match = GD / MP.

## 3. Data preparation and sampling
- Population: N = 48 teams.
- Sample: simple random sample of n = 35 teams, WITHOUT replacement, random_state = 5 (distinct from Q1-Q4).
- The sample splits naturally into two groups: Advanced (n=24) and Group-stage exit (n=11).
- The exact 35 teams used in this task's sample are saved to `data/cleaned_data/q5_35_cleaned_data.csv`.

## 4. Descriptive statistics (sample)
- Advanced group: mean=0.311, median=0.292, std=0.805, n=24
- Group-stage-exit group: mean=-1.879, median=-1.667, std=1.259, n=11

## 5. Inferential statistics - 95% Confidence Intervals
- Advanced group 95% CI: [-0.029, 0.651]
- Group-stage-exit group 95% CI: [-2.724, -1.033]

## 6. Inferential statistics - Two-sample (Welch) t-test
- H0: mu_advanced = mu_eliminated   |   H1: mu_advanced != mu_eliminated
- t = 5.296, p = 0.0001 (Welch's t-test, unequal variances assumed)
- Decision (alpha = 0.05): Reject H0 - teams that advanced have a significantly different goal difference per match than teams eliminated in the group stage.

## 7. Assumptions & limitations
- Shapiro-Wilk (Advanced): W=0.946, p=0.224
- Shapiro-Wilk (Group-stage exit): W=0.940, p=0.525
- Welch's t-test (rather than the pooled/Student's t-test) was used because the two groups plausibly have unequal variances (advancing teams range from narrow to huge goal differences, e.g. Argentina's +11 across 8 matches, whereas group-stage teams played only 3 matches each).
- Group sizes within the 35-team sample are not perfectly balanced (a consequence of random sampling from a population where more teams are eliminated in the group stage than advance), which is normal for Welch's t-test but is noted as a limitation.

## 8. Figure
See outputs/figures/q5_knockout_goal_difference.png.