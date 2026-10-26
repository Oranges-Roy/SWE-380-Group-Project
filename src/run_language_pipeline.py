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
def looks_like_symlink(text: str) -> bool:
    """A git symlink is stored as a blob holding only its target path, e.g.
    '../../../.workspace-rules/skills/x/SKILL.md'; every link to the same target
    therefore shares one SHA and counts as Type-1 without being a copied skill."""
    return (0 < len(text) <= 255 and "\n" not in text and " " not in text
            and "/" in text and text.lower().endswith(".md"))


def extract(db_path: str, lang: str, csv_path: str, chunksize: int = 50_000):
    """Stream the query result to csv_path in chunks.

    Returns (df, first_content): df holds only file_sha and name for every
    occurrence (in query order), and first_content maps each SHA to the content
    of its first occurrence -- the only content the TF-IDF step uses. This keeps
    memory to one copy of the text per distinct file instead of per occurrence.
    """
    aliases = LANG_ALIASES.get(lang.lower(), [lang.lower()])
    marks = ",".join("?" * len(aliases))
    query = f"""
    SELECT a.repo_full_name, a.path, a.filename, a.name, a.file_sha,
           a.content, a.dedup_primary, r.language, r.stars
    FROM artifacts a
    JOIN repos r ON a.repo_full_name = r.full_name
    WHERE LOWER(r.language) IN ({marks});
    """
    metas, first_content = [], {}
    with sqlite3.connect(db_path) as conn:
        chunks = pd.read_sql_query(query, conn, params=aliases, chunksize=chunksize,
                                   dtype={"dedup_primary": "Int64", "stars": "Int64"})
        for k, chunk in enumerate(chunks):
            chunk["name"] = chunk["name"].fillna("[Unnamed Skill]")
            chunk["content"] = chunk["content"].fillna("").astype(str)
            chunk.to_csv(csv_path, mode="w" if k == 0 else "a", header=k == 0, index=False)
            for sha, text in zip(chunk["file_sha"], chunk["content"]):
                if sha not in first_content:
                    first_content[sha] = text
            stripped = chunk["content"].str.strip()
            chunk["has_content"] = stripped != ""
            chunk["symlink_stub"] = stripped.map(looks_like_symlink)
            metas.append(chunk[["file_sha", "name", "has_content", "symlink_stub"]])
    return pd.concat(metas, ignore_index=True), first_content


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


def tfidf_matrix(df: pd.DataFrame, first_content: dict):
    """TF-IDF over distinct SHAs (first occurrence's name and content).

    Empties first_content once the matrix is built, to free the text.
    """
    distinct = df.groupby("file_sha", sort=True).agg(skill_name=("name", "first")).reset_index()
    shas = distinct["file_sha"].to_numpy()
    X = TfidfVectorizer(stop_words="english", min_df=1).fit_transform(
        [first_content[s] for s in shas]
    )  # rows are L2-normalised, so X @ X.T is cosine similarity
    first_content.clear()
    return X, shas, distinct["skill_name"].to_numpy()


def similar_pairs(X, shas, names, low: float, high: float,
                  max_cells: int = 20_000_000) -> pd.DataFrame:
    """TF-IDF cosine over distinct SHAs, computed chunk by chunk.

    Matches are kept as NumPy index/score arrays rather than one dict per pair,
    so tens of millions of pairs fit in memory. Pair order and scores are the
    same as building the rows one at a time.
    """
    n = X.shape[0]
    XT = X.T.tocsc()
    chunk = max(1, max_cells // max(n, 1))

    found_i, found_j, found_s, total = [], [], [], 0
    for start in range(0, n, chunk):
        stop = min(start + chunk, n)
        sims = (X[start:stop] @ XT).toarray()
        ii, jj = np.where(sims >= low)
        gi = ii + start
        keep = jj > gi  # upper triangle, no self-pairs
        found_i.append(gi[keep].astype(np.int32))
        found_j.append(jj[keep].astype(np.int32))
        found_s.append(sims[ii[keep], jj[keep]])
        total += int(keep.sum())
        if stop == n or (start // chunk) % max(1, (n // chunk) // 20) == 0:
            print(f"  compared {stop:,}/{n:,} distinct files, {total:,} pairs so far")

    i = np.concatenate(found_i) if found_i else np.empty(0, np.int32)
    j = np.concatenate(found_j) if found_j else np.empty(0, np.int32)
    s = np.concatenate(found_s) if found_s else np.empty(0)
    return pd.DataFrame({
        "skill_a_sha": shas[i], "skill_a_name": names[i],
        "skill_b_sha": shas[j], "skill_b_name": names[j],
        "similarity_score": s,
        "clone_type": pd.Categorical.from_codes((s < high).astype(np.int8), [TYPE2, TYPE3]),
    })


def estimate_pairs(X, low: float, sample: int, max_cells: int = 20_000_000):
    """Dry run: compare a random sample of distinct files against all of them and
    extrapolate the total pair count, pair memory and comparison time."""
    import time

    n = X.shape[0]
    rows = np.sort(np.random.default_rng(42).choice(n, size=min(sample, n), replace=False))
    XT = X.T.tocsc()
    chunk = max(1, max_cells // max(n, 1))
    matches, t0 = 0, time.time()
    for start in range(0, len(rows), chunk):
        part = rows[start:start + chunk]
        sims = (X[part] @ XT).toarray()
        sims[np.arange(len(part)), part] = 0  # ignore self-similarity
        matches += int((sims >= low).sum())
    elapsed = time.time() - t0
    pairs = matches * n / len(rows) / 2  # each pair is seen from both sides
    print(f"  sampled {len(rows):,} of {n:,} distinct files in {elapsed:.1f}s")
    print(f"  estimated pairs >= {low}: {pairs:,.0f}")
    print(f"  estimated memory for pairs: {pairs * 70 / 1e9:.1f} GB")
    print(f"  estimated comparison time: {elapsed * n / len(rows) / 3600:.1f} h "
          f"(at --max-cells {max_cells:,})")


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


def content_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Split each category into rows with fetched content, rows with none
    (content_fetched = 0: SHA known, text never stored) and symlink stubs, plus the
    category shares counting only rows that have content. A symlink is flagged per
    SHA: most copies of a symlink have no stored content, but they share its SHA."""
    order = [TYPE1, TYPE2, TYPE3, UNIQUE]
    symlink = df["file_sha"].isin(set(df.loc[df["symlink_stub"], "file_sha"]))
    g = df.assign(symlink=symlink).groupby("overall_category")
    out = pd.DataFrame({
        "total": g.size(),
        "has_content": g["has_content"].sum(),
        "no_content": g.size() - g["has_content"].sum(),
        "symlink_stub": g["symlink"].sum(),
    }).reindex(order).fillna(0).astype(int)
    out.loc["Total"] = out.sum()
    out["content_only_share_%"] = (out["has_content"] / max(out.at["Total", "has_content"], 1) * 100).round(1)
    out.index.name = "overall_category"
    return out


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
    ap.add_argument("--max-cells", type=int, default=20_000_000,
                    help="similarity cells per chunk; larger = faster, more RAM (~8 bytes each)")
    ap.add_argument("--dry-run", action="store_true",
                    help="estimate pair count, memory and time from a sample, then stop")
    ap.add_argument("--sample", type=int, default=2000, help="distinct files sampled by --dry-run")
    args = ap.parse_args()

    lang = args.lang.lower()
    tag = lang.replace("+", "p").replace("#", "sharp")
    out = args.out or os.path.join("results", tag)
    os.makedirs(out, exist_ok=True)

    print(f"[1/4] Extracting {lang} skills from {args.db} ...")
    df, first_content = extract(args.db, lang, os.path.join(out, f"extracted_skills_{tag}.csv"))
    print(f"      {len(df):,} skill occurrences, {df['file_sha'].nunique():,} distinct files")

    print("[2/4] Type-1 (identical SHA) ...")
    t1 = type1_pairs(df)
    t1.to_csv(os.path.join(out, f"{tag}_type1_pairs.csv"), index=False)
    print(f"      {len(t1):,} Type-1 pairs saved")

    print("[3/4] Type-2 / Type-3 (TF-IDF cosine) ...")
    X, shas, names = tfidf_matrix(df, first_content)
    if args.dry_run:
        estimate_pairs(X, args.type3, args.sample, args.max_cells)
        print("Dry run: stopping before the full comparison.")
        return
    pairs = similar_pairs(X, shas, names, args.type3, args.type2, args.max_cells)
    del X
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

    breakdown = content_breakdown(df)
    breakdown.to_csv(os.path.join(out, "content_breakdown.csv"))

    print("\n" + summary.to_string())
    print(f"\nType-1 pairs: {len(t1):,} | Type-2/3 pairs: {len(pairs):,}")
    nc, sl = breakdown.at["Total", "no_content"], breakdown.at["Total", "symlink_stub"]
    print(f"No content (never fetched): {nc:,} of {len(df):,} ({nc / len(df) * 100:.1f}%) | "
          f"symlink stubs: {sl:,} -- see content_breakdown.csv")
    print(f"All outputs in: {os.path.abspath(out)}")


if __name__ == "__main__":
    main()
