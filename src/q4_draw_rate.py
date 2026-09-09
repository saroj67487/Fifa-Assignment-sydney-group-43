"""
Q4 - MATCH BALANCE (DRAW RATE)
================================
Analytic question:
  Among the 48 national teams at the FIFA World Cup 2026, was the
  average proportion of matches drawn per team different from 0.20
  (a commonly cited historical World Cup draw rate of roughly 1 in 5
  matches)?

Focal point: MATCH BALANCE / COMPETITIVENESS (how often games end level),
which is distinct from attacking output (Q1), defensive solidity (Q2)
and overall points success (Q3) - draw rate captures how tightly
contested a team's matches were, independent of whether they ultimately
won or lost those closely fought games.

Method: one-sample t-test on DrawRate, plus a 95% CI.
"""
from utils import (load_clean_data, draw_sample, descriptive_stats,
                    confidence_interval, one_sample_ttest, normality_check,
                    plot_histogram_and_boxplot, write_report, save_question_sample)

SEED = 4
BENCHMARK = 0.20
VAR = "DrawRate"

def run():
    df = load_clean_data()
    sample = draw_sample(df, seed=SEED)
    sample_path = save_question_sample(sample, question_number=4)

    desc = descriptive_stats(sample[VAR])
    ci = confidence_interval(sample[VAR])
    ttest = one_sample_ttest(sample[VAR], popmean=BENCHMARK)
    norm = normality_check(sample[VAR])

    plot_histogram_and_boxplot(
        population=df[VAR], sample=sample[VAR], variable_label="Draw rate (proportion of matches drawn)",
        out_path="outputs/figures/q4_draw_rate.png",
        title="Q4: Match Balance - Draw Rate per Team", benchmark=BENCHMARK)

    lines = [
        "# Q4 - Match Balance (Draw Rate)",
        "",
        "## 1. Analytic question",
        f"Was the average proportion of drawn matches per team different from {BENCHMARK}?",
        "",
        "## 2. Data wrangling",
        "- Reused the cleaned team-level dataset.",
        "- Focal variable: DrawRate = D / MP (proportion of a team's matches that ended level).",
        "",
        "## 3. Data preparation and sampling",
        f"- Population: N = {df.shape[0]} teams.",
        f"- Sample: simple random sample of n = {desc['n']} teams, WITHOUT replacement, "
        f"random_state = {SEED}.",
        f"- The exact 35 teams used in this task's sample are saved to `{sample_path}`.",
        "",
        "## 4. Descriptive statistics (sample, n=35)",
        f"- Mean: {desc['mean']:.3f}",
        f"- Median: {desc['median']:.3f}",
        f"- Std. dev.: {desc['std']:.3f}",
        f"- Min / Max: {desc['min']:.2f} / {desc['max']:.2f}",
        f"- IQR (Q1-Q3): {desc['q1']:.2f} - {desc['q3']:.2f}",
        f"- Skewness: {desc['skew']:.3f}",
        "",
        "## 5. Inferential statistics - 95% Confidence Interval",
        f"- 95% CI for the population mean draw rate: "
        f"[{ci['lower']:.3f}, {ci['upper']:.3f}] (margin of error = {ci['margin_of_error']:.3f})",
        "",
        "## 6. Inferential statistics - One-sample t-test",
        f"- H0: mu = {BENCHMARK}   |   H1: mu != {BENCHMARK}",
        f"- Sample mean = {ttest['sample_mean']:.3f}, t({desc['n']-1}) = {ttest['t_stat']:.3f}, "
        f"p = {ttest['p_value']:.4f}",
        f"- Decision (alpha = 0.05): "
        + ("Reject H0 - mean draw rate is significantly different from the historical benchmark."
           if ttest['p_value'] < 0.05 else
           "Fail to reject H0 - not enough evidence that the mean differs from the benchmark."),
        "",
        "## 7. Assumptions & limitations",
        f"- Shapiro-Wilk normality check: W = {norm['shapiro_stat']:.3f}, p = {norm['shapiro_p']:.3f} -> "
        + ("sample looks approximately normal." if norm['looks_normal_at_5pct']
           else "DrawRate is a bounded proportion (0-1) built from a small integer count "
                "(0-3 draws typically), so some non-normality is expected; the t-test is used "
                "here per the assignment's methodological scope, but a proportion-based test "
                "(e.g. a one-sample test for a proportion) would be a reasonable alternative."),
        "- Draw rate is mechanically bounded between 0 and 1 and takes only a few discrete "
        "values for teams with few matches (e.g. group-stage-only teams played just 3 games), "
        "which limits the granularity of the estimate for those teams.",
        "",
        "## 8. Figure",
        "See outputs/figures/q4_draw_rate.png.",
    ]
    write_report("outputs/results/q4_draw_rate.md", lines)
    print("Q4 done.")
    return desc, ci, ttest, norm

if __name__ == "__main__":
    run()
