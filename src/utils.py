"""
utils.py
--------
Shared helper functions used by every analytic task script (q1..q5):
  - sampling 35 teams from the cleaned population with a task-specific
    random seed (so each task analyses a *different* random sample)
  - descriptive statistics
  - a 95% confidence interval for the mean
  - one-sample and two-sample (Welch) t-tests
  - a simple normality check (Shapiro-Wilk) to acknowledge assumptions
  - plotting helpers (histogram of the full cleaned population +
    boxplot of the drawn sample)
"""
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

CLEAN_PATH = "data/cleaned_data/full_population_cleaned_data.csv"
SAMPLE_N = 35


def load_clean_data(path: str = CLEAN_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["Stage"] = pd.Categorical(df["Stage"],
                                  categories=["Final4", "QF", "R16", "R32", "GR"],
                                  ordered=True)
    return df


def draw_sample(df: pd.DataFrame, seed: int, n: int = SAMPLE_N) -> pd.DataFrame:
    """Simple random sample of n teams, without replacement, from the
    population of 48 teams. A different seed per task => a different
    random sample per task, as required."""
    return df.sample(n=n, random_state=seed).reset_index(drop=True)


def save_question_sample(sample: pd.DataFrame, question_number: int,
                          out_dir: str = "data/cleaned_data") -> str:
    """Saves the exact 35-team sample used by a given question to its own
    CSV file, e.g. data/cleaned_data/q1_35_cleaned_data.csv, so every
    question's underlying sampled data is inspectable/reproducible on its own."""
    import os
    os.makedirs(out_dir, exist_ok=True)
    path = f"{out_dir}/q{question_number}_35_cleaned_data.csv"
    sample.to_csv(path, index=False)
    return path


def descriptive_stats(series: pd.Series) -> dict:
    s = series.dropna()
    return {
        "n": int(s.shape[0]),
        "mean": float(s.mean()),
        "median": float(s.median()),
        "std": float(s.std(ddof=1)),
        "min": float(s.min()),
        "max": float(s.max()),
        "q1": float(s.quantile(0.25)),
        "q3": float(s.quantile(0.75)),
        "skew": float(s.skew()),
    }


def confidence_interval(series: pd.Series, confidence: float = 0.95) -> dict:
    s = series.dropna()
    n = s.shape[0]
    mean = s.mean()
    sem = stats.sem(s)  # standard error of the mean
    t_crit = stats.t.ppf((1 + confidence) / 2, df=n - 1)
    margin = t_crit * sem
    return {"confidence": confidence, "mean": float(mean), "sem": float(sem),
            "t_crit": float(t_crit), "margin_of_error": float(margin),
            "lower": float(mean - margin), "upper": float(mean + margin)}


def one_sample_ttest(series: pd.Series, popmean: float) -> dict:
    s = series.dropna()
    t_stat, p_val = stats.ttest_1samp(s, popmean)
    return {"test": "one-sample t-test", "H0_mean": popmean,
            "t_stat": float(t_stat), "p_value": float(p_val),
            "sample_mean": float(s.mean()), "n": int(s.shape[0])}


def two_sample_ttest(group_a: pd.Series, group_b: pd.Series,
                      label_a: str = "A", label_b: str = "B") -> dict:
    a, b = group_a.dropna(), group_b.dropna()
    t_stat, p_val = stats.ttest_ind(a, b, equal_var=False)  # Welch's t-test
    return {"test": "two-sample Welch t-test", "group_a": label_a, "group_b": label_b,
            "mean_a": float(a.mean()), "mean_b": float(b.mean()),
            "n_a": int(a.shape[0]), "n_b": int(b.shape[0]),
            "t_stat": float(t_stat), "p_value": float(p_val)}


def normality_check(series: pd.Series) -> dict:
    s = series.dropna()
    stat, p_val = stats.shapiro(s)
    return {"shapiro_stat": float(stat), "shapiro_p": float(p_val),
            "looks_normal_at_5pct": bool(p_val > 0.05)}


def plot_histogram_and_boxplot(population: pd.Series, sample: pd.Series,
                                variable_label: str, out_path: str,
                                title: str, benchmark: float = None):
    """One figure, two panels:
       (left)  histogram of the variable across the FULL cleaned
               population of 48 teams (raw, post-cleaning data)
       (right) boxplot comparing the population vs. the drawn 35-team
               sample, to visually sanity-check the sample."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    axes[0].hist(population.dropna(), bins=10, color="#4C72B0",
                 edgecolor="white")
    if benchmark is not None:
        axes[0].axvline(benchmark, color="crimson", linestyle="--",
                         label=f"Benchmark = {benchmark}")
        axes[0].legend()
    axes[0].set_title(f"Histogram: {variable_label}\n(all 48 teams, cleaned data)")
    axes[0].set_xlabel(variable_label)
    axes[0].set_ylabel("Number of teams")

    axes[1].boxplot([population.dropna(), sample.dropna()],
                     labels=[f"Population (n={population.dropna().shape[0]})",
                             f"Sample (n={sample.dropna().shape[0]})"],
                     patch_artist=True,
                     boxprops=dict(facecolor="#DD8452"))
    axes[1].set_title(f"Boxplot: {variable_label}\npopulation vs. drawn sample")
    axes[1].set_ylabel(variable_label)

    fig.suptitle(title, fontsize=12, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def write_report(path: str, lines: list):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
