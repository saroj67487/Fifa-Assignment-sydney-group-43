"""
run_all.py
----------
Runs the full Assessment 2 pipeline end to end:
  1. Cleans the raw data (src/data_cleaning.py)
  2. Runs all 5 analytic tasks (src/q1..q5)
Regenerates data/cleaned_worldcup2026_team_stats.csv and every file in
outputs/figures and outputs/results.

Usage (from the project root):
    python run_all.py
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import data_cleaning
import q1_attacking_output
import q2_defensive_performance
import q3_team_success
import q4_draw_rate
import q5_knockout_goal_difference

if __name__ == "__main__":
    os.makedirs("outputs/figures", exist_ok=True)
    os.makedirs("outputs/results", exist_ok=True)

    print("Step 0: cleaning raw data...")
    data_cleaning.clean()

    print("Step 1: Q1 attacking output...")
    q1_attacking_output.run()

    print("Step 2: Q2 defensive performance...")
    q2_defensive_performance.run()

    print("Step 3: Q3 overall team success...")
    q3_team_success.run()

    print("Step 4: Q4 draw rate / match balance...")
    q4_draw_rate.run()

    print("Step 5: Q5 knockout impact on goal difference...")
    q5_knockout_goal_difference.run()

    print("\nAll done. See data/cleaned_data/full_population_cleaned_data.csv, "
          "data/cleaned_data/q1..q5_35_cleaned_data.csv, "
          "outputs/figures/*.png and outputs/results/*.md")
