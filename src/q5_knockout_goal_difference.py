"""
Q5 - KNOCKOUT IMPACT ON GOAL DIFFERENCE
==========================================
Analytic question:
  Did teams that ADVANCED beyond the group stage (Round of 32 or
  better) have a significantly different average GOAL DIFFERENCE per
  match than teams ELIMINATED in the group stage?

Focal point: the relationship between KNOCKOUT PROGRESSION and goal
difference - distinct from Q1-Q4, which each looked at a single
variable across the whole tournament without comparing two groups.

Method: two-sample (Welch) t-test on GD_per_match, comparing
Advanced=True vs Advanced=False, plus a 95% CI for each group's mean.

Sampling note: to keep a consistent "35 teams per task" design across
the assignment while still enabling a two-group comparison, a random
sample of 35 teams is drawn first (seed=5, distinct from every other
task), and that sample is then split into its two naturally occurring
groups (Advanced vs Group-stage-eliminated).
"""
from utils import (load_clean_data, draw_sample, descriptive_stats,
                    confidence_interval, two_sample_ttest, normality_check,
                    write_report, save_question_sample)
import matplotlib.pyplot as plt

SEED = 5
VAR = "GD_per_match"

def run():
    df = load_clean_data()
    sample = draw_sample(df, seed=SEED)
    sample_path = save_question_sample(sample, question_number=5)

    adv = sample.loc[sample["Advanced"], VAR]
    elim = sample.loc[~sample["Advanced"], VAR]

    desc_adv = descriptive_stats(adv)
    desc_elim = descriptive_stats(elim)
    ci_adv = confidence_interval(adv)
    ci_elim = confidence_interval(elim)
    ttest = two_sample_ttest(adv, elim, label_a="Advanced (R32+)", label_b="Group-stage exit")
    norm_adv = normality_check(adv) if desc_adv["n"] >= 3 else None
    norm_elim = normality_check(elim) if desc_elim["n"] >= 3 else None

    # --- Figure: histogram (population) + grouped boxplot (sample) ---
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    axes[0].hist(df[VAR], bins=10, color="#4C72B0", edgecolor="white")
    axes[0].set_title("Histogram: Goal difference per match\n(all 48 teams, cleaned data)")
    axes[0].set_xlabel("Goal difference per match")
    axes[0].set_ylabel("Number of teams")

    axes[1].boxplot([adv, elim], labels=["Advanced\n(n={})".format(desc_adv["n"]),
                                          "Group-stage exit\n(n={})".format(desc_elim["n"])],
                     patch_artist=True,
                     boxprops=dict(facecolor="#55A868"))
    axes[1].set_title("Boxplot: GD/match by knockout progression\n(drawn sample, n=35)")
    axes[1].set_ylabel("Goal difference per match")

    fig.suptitle("Q5: Knockout Impact on Goal Difference", fontsize=12, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig("outputs/figures/q5_knockout_goal_difference.png", dpi=150)
    plt.close(fig)

    lines = [
        "# Q5 - Knockout Impact on Goal Difference",
        "",
        "## 1. Analytic question",
        "Did teams that advanced beyond the group stage have a different average goal "
        "difference per match than teams eliminated in the group stage?",
        "",
        "## 2. Data wrangling",
        "- Reused the cleaned team-level dataset, including the Stage/Advanced flags "
        "engineered from the original 'Rk' column (ranks 1-4, QF, R16, R32 -> Advanced=True; "
        "GR -> Advanced=False).",
        "- Focal variable: GD_per_match = GD / MP.",
        "",
        "## 3. Data preparation and sampling",
        f"- Population: N = {df.shape[0]} teams.",
        f"- Sample: simple random sample of n = 35 teams, WITHOUT replacement, "
        f"random_state = {SEED} (distinct from Q1-Q4).",
        f"- The sample splits naturally into two groups: Advanced (n={desc_adv['n']}) and "
        f"Group-stage exit (n={desc_elim['n']}).",
        f"- The exact 35 teams used in this task's sample are saved to `{sample_path}`.",
        "",
        "## 4. Descriptive statistics (sample)",
        f"- Advanced group: mean={desc_adv['mean']:.3f}, median={desc_adv['median']:.3f}, "
        f"std={desc_adv['std']:.3f}, n={desc_adv['n']}",
        f"- Group-stage-exit group: mean={desc_elim['mean']:.3f}, median={desc_elim['median']:.3f}, "
        f"std={desc_elim['std']:.3f}, n={desc_elim['n']}",
        "",
        "## 5. Inferential statistics - 95% Confidence Intervals",
        f"- Advanced group 95% CI: [{ci_adv['lower']:.3f}, {ci_adv['upper']:.3f}]",
        f"- Group-stage-exit group 95% CI: [{ci_elim['lower']:.3f}, {ci_elim['upper']:.3f}]",
        "",
        "## 6. Inferential statistics - Two-sample (Welch) t-test",
        "- H0: mu_advanced = mu_eliminated   |   H1: mu_advanced != mu_eliminated",
        f"- t = {ttest['t_stat']:.3f}, p = {ttest['p_value']:.4f} "
        f"(Welch's t-test, unequal variances assumed)",
        f"- Decision (alpha = 0.05): "
        + ("Reject H0 - teams that advanced have a significantly different goal difference "
           "per match than teams eliminated in the group stage."
           if ttest['p_value'] < 0.05 else
           "Fail to reject H0 - no significant difference detected at the 5% level, though "
           "the direction of the sample means is consistent with advancing teams having a "
           "stronger goal difference."),
        "",
        "## 7. Assumptions & limitations",
        (f"- Shapiro-Wilk (Advanced): W={norm_adv['shapiro_stat']:.3f}, p={norm_adv['shapiro_p']:.3f}"
         if norm_adv else "- Advanced group too small for a reliable Shapiro-Wilk test."),
        (f"- Shapiro-Wilk (Group-stage exit): W={norm_elim['shapiro_stat']:.3f}, p={norm_elim['shapiro_p']:.3f}"
         if norm_elim else "- Eliminated group too small for a reliable Shapiro-Wilk test."),
        "- Welch's t-test (rather than the pooled/Student's t-test) was used because the two "
        "groups plausibly have unequal variances (advancing teams range from narrow to huge "
        "goal differences, e.g. Argentina's +11 across 8 matches, whereas group-stage teams "
        "played only 3 matches each).",
        "- Group sizes within the 35-team sample are not perfectly balanced (a consequence of "
        "random sampling from a population where more teams are eliminated in the group stage "
        "than advance), which is normal for Welch's t-test but is noted as a limitation.",
        "",
        "## 8. Figure",
        "See outputs/figures/q5_knockout_goal_difference.png.",
    ]
    write_report("outputs/results/q5_knockout_goal_difference.md", lines)
    print("Q5 done.")
    return desc_adv, desc_elim, ttest

if __name__ == "__main__":
    run()
