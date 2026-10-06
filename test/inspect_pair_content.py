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
  """Loads the validation CSV and raw skills dataset with clean quote handling."""
  # Strip quotes if initial defaults contain quotes
  val_path = val_path.strip().strip("'\"")
  raw_path = raw_path.strip().strip("'\"")

  # Check validation CSV path
  if not os.path.exists(val_path):
    user_input = input(
        f"Validation file '{val_path}' not found. Enter path to validation CSV:"
    )
    val_path = user_input.strip().strip("'\"")

  # Check raw dataset path
  if not os.path.exists(raw_path):
    user_input = input(
        f"Raw data file '{raw_path}' not found. Enter path to extracted skills"
        " CSV:"
    )
    raw_path = user_input.strip().strip("'\"")

  # Read clean CSV paths
  val_df = pd.read_csv(val_path)
  raw_df = pd.read_csv(raw_path)

  # Ensure string formatting on raw content and skill names
  raw_df["content"] = raw_df["content"].fillna("").astype(str)
  raw_df["name"] = raw_df["name"].fillna("[Unnamed Skill]")

  return val_df, raw_df


def inspect_pair_by_index(val_df: pd.DataFrame, raw_df: pd.DataFrame, idx: int):
  """Looks up and displays full code content and metadata for a pair at a given index."""
  if idx < 0 or idx >= len(val_df):
    print(f"Index {idx} out of range (0 to {len(val_df)-1}).")
    return

  pair = val_df.iloc[idx]
  sha_a = pair["skill_a_sha"]
  sha_b = pair["skill_b_sha"]

  # Locate raw records
  match_a = raw_df[raw_df["file_sha"] == sha_a]
  match_b = raw_df[raw_df["file_sha"] == sha_b]

  # Dynamically identify the code column
  code_col = None
  for possible_col in [
      "content",
      "code",
      "skill_content",
      "body",
      "raw_content",
  ]:
    if possible_col in raw_df.columns:
      code_col = possible_col
      break

  print("\n" + "=" * 80)
  print(f" INSPECTING PAIR #{idx} | Clone Type: {pair['clone_type']}")
  print(f" Similarity Score: {pair['similarity_score']}")
  print("=" * 80)

  # --- DISPLAY SKILL A ---
  print(f"\n>>> SKILL A: {pair['skill_a_name']} (SHA: {sha_a}) <<<")
  if not match_a.empty:
    rec_a = match_a.iloc[0]
    # Print non-code metadata first
    for col, val in rec_a.items():
      if col != code_col:
        print(f"  {col}: {val}")

    print("\n--- SKILL A CODE CONTENT ---")
    code_a = (
        rec_a[code_col]
        if code_col and pd.notna(rec_a[code_col])
        else "[No Code Found]"
    )
    print(code_a)
  else:
    print("  [Record Not Found in Raw Dataset]")

  print("\n" + "-" * 80)

  # --- DISPLAY SKILL B ---
  print(f"\n>>> SKILL B: {pair['skill_b_name']} (SHA: {sha_b}) <<<")
  if not match_b.empty:
    rec_b = match_b.iloc[0]
    # Print non-code metadata first
    for col, val in rec_b.items():
      if col != code_col:
        print(f"  {col}: {val}")

    print("\n--- SKILL B CODE CONTENT ---")
    code_b = (
        rec_b[code_col]
        if code_col and pd.notna(rec_b[code_col])
        else "[No Code Found]"
    )
    print(code_b)
  else:
    print("  [Record Not Found in Raw Dataset]")

  print("=" * 80 + "\n")


def interactive_inspector():
  """Runs an interactive loop allowing users to browse pair contents."""
  val_df, raw_df = load_datasets()

  print(f"\nLoaded {len(val_df)} pairs from validation sample.")
  print(
      f"Enter a pair row index (0 to {len(val_df)-1}) to inspect, or 'q' to"
      " quit.\n"
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