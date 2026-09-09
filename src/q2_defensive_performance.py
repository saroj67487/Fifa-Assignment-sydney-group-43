"""
Q2 - DEFENSIVE PERFORMANCE
===========================
Analytic question:
  Among the 48 national teams at the FIFA World Cup 2026, was the
  average number of goals CONCEDED per match LESS than 1.5?

Focal point: team DEFENSIVE solidity (goals against), which is a
distinct construct from Q1's attacking output - a team can attack
well and defend poorly, or vice versa.

Method: one-sample t-test on GA_per_match, plus a 95% CI.
"""
from utils import (load_clean_data, draw_sample, descriptive_stats,
                    confidence_interval, one_sample_ttest, normality_check,
                    plot_histogram_and_boxplot, write_report, save_question_sample)

SEED = 2
BENCHMARK = 1.5
VAR = "GA_per_match"

def run():
    df = load_clean_data()
    sample = draw_sample(df, seed=SEED)
    sample_path = save_question_sample(sample, question_number=2)

    desc = descriptive_stats(sample[VAR])
    ci = confidence_interval(sample[VAR])
    ttest = one_sample_ttest(sample[VAR], popmean=BENCHMARK)
    norm = normality_check(sample[VAR])

    plot_histogram_and_boxplot(
        population=df[VAR], sample=sample[VAR], variable_label="Goals conceded per match",
        out_path="outputs/figures/q2_defensive_performance.png",
        title="Q2: Defensive Performance - Goals Conceded per Match", benchmark=BENCHMARK)

    lines = [
        "# Q2 - Defensive Performance",
        "",
        "## 1. Analytic question",
        f"Was the average goals conceded per match by World Cup 2026 teams less than {BENCHMARK}?",
        "",
        "## 2. Data wrangling",
        "- Reused the cleaned team-level dataset produced in src/data_cleaning.py.",
        "- Focal variable: GA_per_match = GA / MP (goals against per match played),",
        "  engineered so teams with different numbers of matches are comparable.",
        "",
        "## 3. Data preparation and sampling",
        f"- Population: N = {df.shape[0]} teams.",
        f"- Sample: simple random sample of n = {desc['n']} teams, WITHOUT replacement, "
        f"random_state = {SEED} (a different seed/sample from every other task).",
        f"- The exact 35 teams used in this task's sample are saved to `{sample_path}`.",
        "",
        "## 4. Descriptive statistics (sample, n=35)",
        f"- Mean: {desc['mean']:.3f} goals conceded/match",
        f"- Median: {desc['median']:.3f}",
        f"- Std. dev.: {desc['std']:.3f}",
        f"- Min / Max: {desc['min']:.2f} / {desc['max']:.2f}",
        f"- IQR (Q1-Q3): {desc['q1']:.2f} - {desc['q3']:.2f}",
        f"- Skewness: {desc['skew']:.3f}",
        "",
        "## 5. Inferential statistics - 95% Confidence Interval",
        f"- 95% CI for the population mean goals conceded/match: "
        f"[{ci['lower']:.3f}, {ci['upper']:.3f}] (margin of error = {ci['margin_of_error']:.3f})",
        "",
        "## 6. Inferential statistics - One-sample t-test",
        f"- H0: mu = {BENCHMARK}   |   H1: mu < {BENCHMARK}",
        f"- Sample mean = {ttest['sample_mean']:.3f}, t({desc['n']-1}) = {ttest['t_stat']:.3f}, "
        f"p = {ttest['p_value']:.4f} (two-sided; halve for the one-sided test above)",
        f"- Decision (alpha = 0.05): "
        + ("Reject H0 - mean goals conceded/match is significantly different from the benchmark."
           if ttest['p_value'] < 0.05 else
           "Fail to reject H0 - not enough evidence that the mean differs from the benchmark."),
        "",
        "## 7. Assumptions & limitations",
        f"- Shapiro-Wilk normality check: W = {norm['shapiro_stat']:.3f}, p = {norm['shapiro_p']:.3f} -> "
        + ("sample looks approximately normal." if norm['looks_normal_at_5pct']
           else "mild deviation from normality; t-test remains reasonably robust at n=35."),
        "- Teams eliminated early only contribute 3 matches, which may be against weaker "
        "group opposition, so GA_per_match is not perfectly comparable across all teams; "
        "this is acknowledged rather than corrected for, given the scope of the task.",
        "",
        "## 8. Figure",
        "See outputs/figures/q2_defensive_performance.png.",
    ]
    write_report("outputs/results/q2_defensive_performance.md", lines)
    print("Q2 done.")
    return desc, ci, ttest, norm

if __name__ == "__main__":
    run()
