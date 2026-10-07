"""
GitSkills Clone Detection Pipeline (any repo language)
Course: SWE 380 / CSC 580

Same method as the Sprint 1 C++ pipeline (git_cpp_skill_extractor.py +
src/ingest_and_analyze.py + figures/C++Clones.py), parameterised by language
and with the TF-IDF similarity computed in chunks so large ecosystems such as
Python fit in memory.

Usage:
    python run_language_pipeline.py --db path/to/agent_skills_release.db --lang python
"""

import argparse
import os
import sqlite3

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

LANG_ALIASES = {
    "python": ["python"],
    "c++": ["c++", "cpp"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "java": ["java"],
    "go": ["go", "golang"],
    "rust": ["rust"],
    "c#": ["c#", "csharp"],
}
TYPE1, TYPE2, TYPE3, UNIQUE = (
    "Type-1 (Verbatim)",
    "Type-2 (Parameterized)",
    "Type-3 (Semantic)",
    "Truly Unique",
)


# ---------------------------------------------------------------- 1. extract
def extract(db_path: str, lang: str) -> pd.DataFrame:
    aliases = LANG_ALIASES.get(lang.lower(), [lang.lower()])
    marks = ",".join("?" * len(aliases))
    query = f"""
    SELECT a.repo_full_name, a.path, a.filename, a.name, a.file_sha,
           a.content, a.dedup_primary, r.language, r.stars
    FROM artifacts a
    JOIN repos r ON a.repo_full_name = r.full_name
    WHERE LOWER(r.language) IN ({marks});
    """
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(query, conn, params=aliases)
    return df


# ------------------------------------------------------- 2. clone detection
def type1_pairs(df: pd.DataFrame) -> pd.DataFrame:
    """Identical file_sha; one pair per consecutive copy (same as Sprint 1)."""
    rows = []
    for sha, group in df.groupby("file_sha", sort=False):
        if len(group) < 2:
            continue
        names = group["name"].tolist()
        for i in range(len(names) - 1):
            rows.append({
                "skill_a_sha": sha, "skill_a_name": names[i],
                "skill_b_sha": sha, "skill_b_name": names[i + 1],
                "similarity_score": 1.0, "clone_type": TYPE1,
            })
    return pd.DataFrame(rows)


def similar_pairs(df: pd.DataFrame, low: float, high: float,
                  max_cells: int = 20_000_000) -> pd.DataFrame:
    """TF-IDF cosine over distinct SHAs, computed chunk by chunk."""
    distinct = (
        df.groupby("file_sha", sort=True)
        .agg(skill_name=("name", "first"), sample_content=("content", "first"))
        .reset_index()
    )
    X = TfidfVectorizer(stop_words="english", min_df=1).fit_transform(
        distinct["sample_content"].tolist()
    )  # rows are L2-normalised, so X @ X.T is cosine similarity
    n = X.shape[0]
    XT = X.T.tocsc()
    chunk = max(1, max_cells // max(n, 1))
    shas = distinct["file_sha"].to_numpy()
    names = distinct["skill_name"].to_numpy()

    out = []
    for start in range(0, n, chunk):
        stop = min(start + chunk, n)
        sims = (X[start:stop] @ XT).toarray()
        ii, jj = np.where(sims >= low)
        gi = ii + start
        keep = jj > gi  # upper triangle, no self-pairs
        for i, j, s in zip(gi[keep], jj[keep], sims[ii[keep], jj[keep]]):
            out.append({
                "skill_a_sha": shas[i], "skill_a_name": names[i],
                "skill_b_sha": shas[j], "skill_b_name": names[j],
                "similarity_score": float(s),
                "clone_type": TYPE2 if s >= high else TYPE3,
            })
        if stop == n or (start // chunk) % max(1, (n // chunk) // 20) == 0:
            print(f"  compared {stop:,}/{n:,} distinct files, {len(out):,} pairs so far")
    return pd.DataFrame(out, columns=["skill_a_sha", "skill_a_name", "skill_b_sha",
                                      "skill_b_name", "similarity_score", "clone_type"])


# ------------------------------------------------------- 3. categorise + plot
def categorise(df: pd.DataFrame, pairs: pd.DataFrame) -> pd.Series:
    counts = df["file_sha"].value_counts()
    t1 = set(counts[counts > 1].index)

    def shas(kind):
        p = pairs[pairs["clone_type"] == kind]
        return set(p["skill_a_sha"]) | set(p["skill_b_sha"])

    t2, t3 = shas(TYPE2), shas(TYPE3)
    return df["file_sha"].map(
        lambda s: TYPE1 if s in t1 else TYPE2 if s in t2 else TYPE3 if s in t3 else UNIQUE
    )


def plot(categories: pd.Series, lang_label: str, path: str):
    counts = categories.value_counts()
    total = int(counts.sum())
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.Blues(np.linspace(0.85, 0.25, len(counts)))
    bars = ax.bar(counts.index, counts.values, color=colors)
    for b, v in zip(bars, counts.values):
        ax.annotate(f"{v:,}\n({v / total * 100:.1f}%)",
                    (b.get_x() + b.get_width() / 2, v), ha="center", va="bottom",
                    xytext=(0, 5), textcoords="offset points")
    ax.set_title(f"Complete Categorization of {lang_label} Skills (N = {total:,})", fontsize=14)
    ax.set_xlabel("Clone / Uniqueness Category", fontsize=12)
    ax.set_ylabel("Number of Skill File Occurrences", fontsize=12)
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


# ------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True, help="path to agent_skills_release.db")
    ap.add_argument("--lang", default="python")
    ap.add_argument("--out", default=None, help="output folder (default results/<lang>)")
    ap.add_argument("--type3", type=float, default=0.65)
    ap.add_argument("--type2", type=float, default=0.85)
    args = ap.parse_args()

    lang = args.lang.lower()
    tag = lang.replace("+", "p").replace("#", "sharp")
    out = args.out or os.path.join("results", tag)
    os.makedirs(out, exist_ok=True)

    print(f"[1/4] Extracting {lang} skills from {args.db} ...")
    df = extract(args.db, lang)
    df["name"] = df["name"].fillna("[Unnamed Skill]")
    df["content"] = df["content"].fillna("").astype(str)
    df.to_csv(os.path.join(out, f"extracted_skills_{tag}.csv"), index=False)
    print(f"      {len(df):,} skill occurrences, {df['file_sha'].nunique():,} distinct files")

    print("[2/4] Type-1 (identical SHA) ...")
    t1 = type1_pairs(df)

    print("[3/4] Type-2 / Type-3 (TF-IDF cosine) ...")
    pairs = similar_pairs(df, args.type3, args.type2)
    pairs.to_csv(os.path.join(out, f"{tag}_similar_pairs.csv"), index=False)
    pairs.sort_values(["similarity_score", "skill_a_name"], ascending=[False, True]) \
         .head(10).to_csv(os.path.join(out, "top10_similar_pairs.csv"), index=False)

    samples = [t1.sample(n=min(10, len(t1)), random_state=42) if len(t1) else t1]
    for kind in (TYPE2, TYPE3):
        p = pairs[pairs["clone_type"] == kind]
        samples.append(p.sample(n=min(10, len(p)), random_state=42) if len(p) else p)
    pd.concat(samples).reset_index(drop=True).to_csv(
        os.path.join(out, "validation_sample_30.csv"), index=False)

    print("[4/4] Categorising and plotting ...")
    df["overall_category"] = categorise(df, pairs)
    summary = df["overall_category"].value_counts().rename("count").to_frame()
    summary["share_%"] = (summary["count"] / len(df) * 100).round(1)
    summary.loc["Total"] = [len(df), 100.0]
    summary["count"] = summary["count"].astype(int)
    summary.to_csv(os.path.join(out, "clone_distribution.csv"))
    label = {"python": "Python", "c++": "C++"}.get(lang, args.lang)
    plot(df["overall_category"], label, os.path.join(out, f"{tag}_clones.png"))

    print("\n" + summary.to_string())
    print(f"\nType-1 pairs: {len(t1):,} | Type-2/3 pairs: {len(pairs):,}")
    print(f"All outputs in: {os.path.abspath(out)}")


if __name__ == "__main__":
    main()
