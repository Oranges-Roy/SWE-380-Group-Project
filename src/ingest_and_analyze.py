"""
GitSkills C++ Clone Detection & Analysis Pipeline
Course: SWE 380 / CSC 580
Description: Ingests C++ skill records, computes clone taxonomies (Types 1–3),
             and generates validation/top-match exports.
"""

import os
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_validated_input_path(
    default_path: str = "data/extracted_skills_sample.csv",
) -> str:
  """Prompts the user for the extracted CSV dataset path, applying fallback checks

  and filename extraction if the direct path fails.
  """
  while True:
    user_input = (
        input(
            f"Enter path to extracted C++ skills CSV (press Enter for default"
            f" '{default_path}'): "
        )
        .strip()
        .strip("'\"")
    )

    raw_path = user_input if user_input else default_path

    # Check 1: Direct path match
    if os.path.isfile(raw_path):
      print(f"Loading CSV data from: {raw_path}")
      return raw_path

    # Check 2: Filename extraction recovery
    filename = os.path.basename(raw_path)

    if os.path.isfile(filename):
      print(
          f"Path '{raw_path}' not found, but found '{filename}' in current"
          " directory."
      )
      return filename
    elif os.path.isfile(os.path.join("data", filename)):
      resolved_path = os.path.join("data", filename)
      print(
          f"Path '{raw_path}' not found, but found '{filename}' inside 'data/'"
          " directory."
      )
      return resolved_path
    elif os.path.isfile(os.path.join("results", filename)):
      resolved_path = os.path.join("results", filename)
      print(
          f"Path '{raw_path}' not found, but found '{filename}' inside"
          " 'results/' directory."
      )
      return resolved_path

    print(
        f"Error: File '{raw_path}' not found. Please enter a valid path to"
        " your CSV file.\n"
    )


def run_production_pipeline(input_csv: str, output_dir: str):
  """Refactored production pipeline.

  - Performs null-safety filling on text content and skill names.
  - Generates Type-1 verbatim clone pairs.
  - Runs TF-IDF Vectorization and cosine similarity for Types 2 & 3.
  - Exports top 10 similarity matches and a 30-pair stratified sample.
  """
  print("\n--- Running Refactored Production Pipeline ---")
  os.makedirs(output_dir, exist_ok=True)

  # 1. Load raw data
  raw_df = pd.read_csv(input_csv)
  raw_df["name"] = raw_df["name"].fillna("[Unnamed Skill]")
  raw_df["content"] = raw_df["content"].fillna("").astype(str)
  print(f"Loaded {len(raw_df)} raw records from {input_csv}.")

  # 2. Step 1: Type-1 (Verbatim) SHA Aggregation & Pair Extraction
  sha_counts = raw_df["file_sha"].value_counts()
  verbatim_shas = sha_counts[sha_counts > 1].index

  type1_pairs = []
  for sha in verbatim_shas:
    group = raw_df[raw_df["file_sha"] == sha].reset_index(drop=True)
    for i in range(len(group)):
      for j in range(i + 1, min(i + 2, len(group))):
        type1_pairs.append({
            "skill_a_sha": sha,
            "skill_a_name": group.loc[i, "name"],
            "skill_b_sha": sha,
            "skill_b_name": group.loc[j, "name"],
            "similarity_score": 1.0,
            "clone_type": "Type-1 (Verbatim)",
        })
  type1_df = pd.DataFrame(type1_pairs)

  # 3. Step 2: Distinct Content Aggregation & TF-IDF Cosine Similarity (Types 2 & 3)
  type1_clusters = (
      raw_df.groupby("file_sha")
      .agg(
          copy_count=("repo_full_name", "count"),
          total_star_reach=("stars", "sum"),
          skill_name=("name", "first"),
          sample_content=("content", "first"),
      )
      .reset_index()
  )

  distinct_skills = type1_clusters.copy()
  distinct_skills["sample_content"] = (
      distinct_skills["sample_content"].fillna("").astype(str)
  )
  contents = distinct_skills["sample_content"].tolist()

  # TF-IDF Vectorization
  vectorizer = TfidfVectorizer(stop_words="english", min_df=1)
  tfidf_matrix = vectorizer.fit_transform(contents)

  sim_matrix = cosine_similarity(tfidf_matrix)
  np.fill_diagonal(sim_matrix, 0)

  # Extract pairwise similarity matches (Types 2 & 3)
  pairs = []
  for i, j in zip(*np.where(sim_matrix >= 0.65)):
    if i < j:
      score = sim_matrix[i, j]
      clone_type = (
          "Type-2 (Parameterized)" if score >= 0.85 else "Type-3 (Semantic)"
      )
      pairs.append({
          "skill_a_sha": distinct_skills.loc[i, "file_sha"],
          "skill_a_name": distinct_skills.loc[i, "skill_name"],
          "skill_b_sha": distinct_skills.loc[j, "file_sha"],
          "skill_b_name": distinct_skills.loc[j, "skill_name"],
          "similarity_score": score,
          "clone_type": clone_type,
      })

  similar_pairs_df = pd.DataFrame(pairs)
  if not similar_pairs_df.empty:
    similar_pairs_df["skill_a_name"] = similar_pairs_df["skill_a_name"].fillna(
        "[Unnamed Skill]"
    )
    similar_pairs_df["skill_b_name"] = similar_pairs_df["skill_b_name"].fillna(
        "[Unnamed Skill]"
    )

  # Export main pairwise output
  pairs_csv_path = os.path.join(output_dir, "cpp_similar_pairs.csv")
  similar_pairs_df.to_csv(pairs_csv_path, index=False)
  print(f"Saved {len(similar_pairs_df)} similar pairs to {pairs_csv_path}.")

  # 4. Export Top 10 Highest Similarity Matches
  top10_df = (
      similar_pairs_df.sort_values(
          by=["similarity_score", "skill_a_name"], ascending=[False, True]
      ).head(10)
      if not similar_pairs_df.empty
      else pd.DataFrame()
  )
  top10_path = os.path.join(output_dir, "top10_similar_pairs.csv")
  top10_df.to_csv(top10_path, index=False)
  print(f"Saved Top 10 high-similarity pairs to {top10_path}.")

  # 5. Generate Balanced 3-Tier Validation Sample (10 per tier -> 30 total)
  n_per_group = 10
  t1_sample = (
      type1_df.sample(n=min(n_per_group, len(type1_df)), random_state=42)
      if not type1_df.empty
      else pd.DataFrame()
  )

  t2_pairs = similar_pairs_df[
      similar_pairs_df["clone_type"] == "Type-2 (Parameterized)"
  ]
  t2_sample = (
      t2_pairs.sample(n=min(n_per_group, len(t2_pairs)), random_state=42)
      if not t2_pairs.empty
      else pd.DataFrame()
  )

  t3_pairs = similar_pairs_df[
      similar_pairs_df["clone_type"] == "Type-3 (Semantic)"
  ]
  t3_sample = (
      t3_pairs.sample(n=min(n_per_group, len(t3_pairs)), random_state=42)
      if not t3_pairs.empty
      else pd.DataFrame()
  )

  val_sample = pd.concat([t1_sample, t2_sample, t3_sample]).reset_index(
      drop=True
  )
  val_sample_path = os.path.join(output_dir, "validation_sample_30.csv")
  val_sample.to_csv(val_sample_path, index=False)
  print(f"Saved balanced validation sample to {val_sample_path}.")

  print("--- Production Execution Complete ---\n")
  return similar_pairs_df, val_sample


# =============================================================================
# MAIN EXECUTION ENTRY POINT
# =============================================================================
if __name__ == "__main__":
  OUTPUT_DIR = "results"

  # Prompt user for path with fallback resolution
  input_path = get_validated_input_path()

  # Run the pipeline directly
  run_production_pipeline(input_path, OUTPUT_DIR)