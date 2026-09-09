"""
Q3 - OVERALL TEAM SUCCESS
==========================
Analytic question:
  Among the 48 national teams at the FIFA World Cup 2026, was the
  average points-per-match (3 for a win, 1 for a draw, 0 for a loss)
  greater than 1.2 - the points/match a team would average if wins,
  draws and losses were equally likely (a "coin-flip" benchmark of
  (3+1+0)/3 = 1.33, rounded down slightly to 1.2 to give a meaningful,
  testable hypothesis)?

Focal point: overall TOURNAMENT SUCCESS/RESULTS (points), which is
distinct from both attacking output (Q1) and defensive solidity (Q2) -
a team can score/concede a lot yet still not translate that into wins.

Method: one-sample t-test on Pts_per_match, plus a 95% CI.
"""
from utils import (load_clean_data, draw_sample, descriptive_stats,
                    confidence_interval, one_sample_ttest, normality_check,
                    plot_histogram_and_boxplot, write_report, save_question_sample)

SEED = 3
BENCHMARK = 1.2
VAR = "Pts_per_match"

def run():
    df = load_clean_data()
    sample = draw_sample(df, seed=SEED)
    sample_path = save_question_sample(sample, question_number=3)

    desc = descriptive_stats(sample[VAR])
    ci = confidence_interval(sample[VAR])
    ttest = one_sample_ttest(sample[VAR], popmean=BENCHMARK)
    norm = normality_check(sample[VAR])

    plot_histogram_and_boxplot(
        population=df[VAR], sample=sample[VAR], variable_label="Points earned per match",
        out_path="outputs/figures/q3_team_success.png",
        title="Q3: Overall Success - Points Earned per Match", benchmark=BENCHMARK)

    lines = [
        "# Q3 - Overall Team Success",
        "",
        "## 1. Analytic question",
        f"Was the average points earned per match by World Cup 2026 teams greater than {BENCHMARK}?",
        "",
        "## 2. Data wrangling",
        "- Reused the cleaned team-level dataset.",
        "- Focal variable: Pts_per_match = Pts / MP, standard football points "
        "(win=3, draw=1, loss=0) scaled to a per-match rate for cross-team comparability.",
        "",
        "## 3. Data preparation and sampling",
        f"- Population: N = {df.shape[0]} teams.",
        f"- Sample: simple random sample of n = {desc['n']} teams, WITHOUT replacement, "
        f"random_state = {SEED}.",
        f"- The exact 35 teams used in this task's sample are saved to `{sample_path}`.",
        "",
        "## 4. Descriptive statistics (sample, n=35)",
        f"- Mean: {desc['mean']:.3f} pts/match",
        f"- Median: {desc['median']:.3f}",
        f"- Std. dev.: {desc['std']:.3f}",
        f"- Min / Max: {desc['min']:.2f} / {desc['max']:.2f}",
        f"- IQR (Q1-Q3): {desc['q1']:.2f} - {desc['q3']:.2f}",
        f"- Skewness: {desc['skew']:.3f}",
        "",
        "## 5. Inferential statistics - 95% Confidence Interval",
        f"- 95% CI for the population mean pts/match: "
        f"[{ci['lower']:.3f}, {ci['upper']:.3f}] (margin of error = {ci['margin_of_error']:.3f})",
        "",
        "## 6. Inferential statistics - One-sample t-test",
        f"- H0: mu = {BENCHMARK}   |   H1: mu != {BENCHMARK}",
        f"- Sample mean = {ttest['sample_mean']:.3f}, t({desc['n']-1}) = {ttest['t_stat']:.3f}, "
        f"p = {ttest['p_value']:.4f}",
        f"- Decision (alpha = 0.05): "
        + ("Reject H0 - mean points/match is significantly different from the coin-flip benchmark."
           if ttest['p_value'] < 0.05 else
           "Fail to reject H0 - not enough evidence that the mean differs from the benchmark."),
        "",
        "## 7. Assumptions & limitations",
        f"- Shapiro-Wilk normality check: W = {norm['shapiro_stat']:.3f}, p = {norm['shapiro_p']:.3f} -> "
        + ("sample looks approximately normal." if norm['looks_normal_at_5pct']
           else "some deviation from normality; interpreted with appropriate caution."),
        "- Points-per-match compresses win/draw/loss detail into a single number; two teams "
        "with the same average could have very different win/draw mixes (explored further "
        "in Q5, which separates teams by knockout progression).",
        "",
        "## 8. Figure",
        "See outputs/figures/q3_team_success.png.",
    ]
    write_report("outputs/results/q3_team_success.md", lines)
    print("Q3 done.")
    return desc, ci, ttest, norm

if __name__ == "__main__":
    run()
