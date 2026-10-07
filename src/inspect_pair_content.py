"""GitSkills Pair Content Inspector Tool

Course: SWE 380 / CSC 580
Description: Utility script to look up and inspect full text/code content
             for skill pairs present in validation samples or pairwise results.
"""

import os
import pandas as pd


def load_datasets(
    val_path: str = "results/validation_sample_30.csv",
    raw_path: str = "data/extracted_skills_sample.csv",
):
  """Loads the validation CSV and raw skills dataset with path checks."""
  if not os.path.exists(val_path):
    val_path = input(
        f"Validation file '{val_path}' not found. Enter path to validation CSV:"
    ).strip()

  if not os.path.exists(raw_path):
    raw_path = input(
        f"Raw data file '{raw_path}' not found. Enter path to extracted skills"
        " CSV:"
    ).strip()

  val_df = pd.read_csv(val_path)
  raw_df = pd.read_csv(raw_path)

  # Ensure string formatting on raw content
  raw_df["content"] = raw_df["content"].fillna("").astype(str)
  raw_df["name"] = raw_df["name"].fillna("[Unnamed Skill]")

  return val_df, raw_df


def inspect_pair_by_index(val_df: pd.DataFrame, raw_df: pd.DataFrame, idx: int):
  """Looks up and displays full content for a pair at a given index in the validation sample."""
  if idx < 0 or idx >= len(val_df):
    print(f"Index {idx} out of range (0 to {len(val_df)-1}).")
    return

  pair = val_df.iloc[idx]
  sha_a = pair["skill_a_sha"]
  sha_b = pair["skill_b_sha"]

  # Lookup raw records by SHA
  match_a = raw_df[raw_df["file_sha"] == sha_a]
  match_b = raw_df[raw_df["file_sha"] == sha_b]

  content_a = (
      match_a["content"].values[0]
      if not match_a.empty
      else "[Content Not Found]"
  )
  content_b = (
      match_b["content"].values[0]
      if not match_b.empty
      else "[Content Not Found]"
  )

  print("\n" + "=" * 80)
  print(f" INSPECTING PAIR #{idx} | Clone Type: {pair['clone_type']}")
  print(f" Similarity Score: {pair['similarity_score']}")
  print("=" * 80)

  print(f"\n--- SKILL A: {pair['skill_a_name']} (SHA: {sha_a}) ---")
  print(content_a)

  print(
      f"\n" + "-" * 80 + f"\n--- SKILL B: {pair['skill_b_name']} (SHA:"
      f" {sha_b}) ---"
  )
  print(content_b)
  print("=" * 80 + "\n")


def interactive_inspector():
  """Runs an interactive loop allowing users to browse pair contents."""
  val_df, raw_df = load_datasets()

  print(f"\nLoaded {len(val_df)} pairs from validation sample.")
  print(
      "Enter a pair row index (0 to"
      f" {len(val_df)-1}) to inspect, or 'q' to quit.\n"
  )

  while True:
    user_input = input("Enter index to inspect (or 'q' to exit): ").strip()
    if user_input.lower() in ["q", "exit", "quit"]:
      print("Exiting pair inspector.")
      break

    if user_input.isdigit():
      idx = int(user_input)
      inspect_pair_by_index(val_df, raw_df, idx)
    else:
      print("Please enter a valid numeric index or 'q'.")


if __name__ == "__main__":
  interactive_inspector()