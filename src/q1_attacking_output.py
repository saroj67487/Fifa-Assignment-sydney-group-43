"""
Q1 - ATTACKING OUTPUT
======================
Analytic question:
  Among the 48 national teams at the FIFA World Cup 2026, was the
  average number of goals scored per match GREATER than 1.5 (a common
  historical World Cup benchmark for goals-for per team per match)?

Focal point: team ATTACKING output (goals scored), independent of
match count, win/loss record, or knockout stage reached.

Method: one-sample t-test on GF_per_match, plus a 95% CI.
"""
from utils import (load_clean_data, draw_sample, descriptive_stats,
                    confidence_interval, one_sample_ttest, normality_check,
                    plot_histogram_and_boxplot, write_report, save_question_sample)

SEED = 1
BENCHMARK = 1.5
VAR = "GF_per_match"

def run():
    df = load_clean_data()
    sample = draw_sample(df, seed=SEED)
    sample_path = save_question_sample(sample, question_number=1)

    desc = descriptive_stats(sample[VAR])
    ci = confidence_interval(sample[VAR])
    ttest = one_sample_ttest(sample[VAR], popmean=BENCHMARK)
    norm = normality_check(sample[VAR])

    plot_histogram_and_boxplot(
        population=df[VAR], sample=sample[VAR], variable_label="Goals scored per match",
        out_path="outputs/figures/q1_attacking_output.png",
        title="Q1: Attacking Output - Goals Scored per Match", benchmark=BENCHMARK)

    lines = [
        "# Q1 - Attacking Output",
        "",
        "## 1. Analytic question",
        f"Was the average goals scored per match by World Cup 2026 teams greater than {BENCHMARK}?",
        "",
        "## 2. Data wrangling",
        "- Loaded the cleaned team-level dataset (48 teams, 21 tidy variables).",
        "- Focal variable engineered during cleaning: GF_per_match = GF / MP, so teams",
        "  that played a different number of matches (3 to 8, depending on how far they",
        "  advanced) are placed on a comparable per-match scale.",
        "",
        "## 3. Data preparation and sampling",
        f"- Population: all N = {df.shape[0]} teams that competed in the tournament.",
        f"- Sample: simple random sample of n = {desc['n']} teams drawn WITHOUT replacement",
        f"  (pandas .sample, random_state = {SEED}). This is a distinct random draw from",
        "  every other task in this assignment.",
        f"- The exact 35 teams used in this task's sample are saved to `{sample_path}`.",
        "",
        "## 4. Descriptive statistics (sample, n=35)",
        f"- Mean: {desc['mean']:.3f} goals/match",
        f"- Median: {desc['median']:.3f}",
        f"- Std. dev.: {desc['std']:.3f}",
        f"- Min / Max: {desc['min']:.2f} / {desc['max']:.2f}",
        f"- IQR (Q1-Q3): {desc['q1']:.2f} - {desc['q3']:.2f}",
        f"- Skewness: {desc['skew']:.3f}",
        "",
        "## 5. Inferential statistics - 95% Confidence Interval",
        f"- 95% CI for the population mean goals/match: "
        f"[{ci['lower']:.3f}, {ci['upper']:.3f}]  (margin of error = {ci['margin_of_error']:.3f})",
        "",
        "## 6. Inferential statistics - One-sample t-test",
        f"- H0: mu = {BENCHMARK}   |   H1: mu > {BENCHMARK}",
        f"- Sample mean = {ttest['sample_mean']:.3f}, t({desc['n']-1}) = {ttest['t_stat']:.3f}, "
        f"p = {ttest['p_value']:.4f} (two-sided; halve for the one-sided test above)",
        f"- Decision (alpha = 0.05): "
        + ("Reject H0 - mean goals/match is significantly different from the benchmark."
           if ttest['p_value'] < 0.05 else
           "Fail to reject H0 - not enough evidence that the mean differs from the benchmark."),
        "",
        "## 7. Assumptions & limitations",
        f"- Shapiro-Wilk normality check on the sample: W = {norm['shapiro_stat']:.3f}, "
        f"p = {norm['shapiro_p']:.3f} -> "
        + ("sample looks approximately normal." if norm['looks_normal_at_5pct']
           else "some deviation from normality detected; with n=35 the t-test is still "
                "reasonably robust via the Central Limit Theorem, but results should be "
                "interpreted with caution."),
        "- The population itself is only 48 teams, so a sample of 35 is a large fraction "
        "(~73%) of the population; a finite population correction could tighten the CI "
        "further, but was not applied here to keep the method consistent with the "
        "standard t-based CI taught in this course.",
        "- GF_per_match rewards attacking teams that also progressed further (more matches",
        "  played against tougher opposition), which is a potential confound.",
        "",
        "## 8. Figure",
        "See outputs/figures/q1_attacking_output.png (histogram of the full 48-team ",
        "population + boxplot comparing population vs. the drawn sample).",
    ]
    write_report("outputs/results/q1_attacking_output.md", lines)
    print("Q1 done.")
    return desc, ci, ttest, norm

if __name__ == "__main__":
    run()
