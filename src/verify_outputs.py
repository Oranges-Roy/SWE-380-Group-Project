"""
Verify the outputs of run_language_pipeline.py for one language.

Re-derives every summary from the raw outputs and checks it against what the
pipeline wrote. Prints PASS / FAIL per check and exits non-zero on any failure.

Usage:
    python src/verify_outputs.py --lang java
    python src/verify_outputs.py --lang python --write-breakdown   # create content_breakdown.csv if missing
"""

import argparse
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_language_pipeline import TYPE1, TYPE2, TYPE3, UNIQUE, looks_like_symlink  # noqa: E402

ORDER = [TYPE1, TYPE2, TYPE3, UNIQUE]
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail else ""))


def read_csv(path, **kw):
    # round_trip parsing: the default parser can change the last digit of a score
    return pd.read_csv(path, float_precision="round_trip", **kw)


def first_existing(*paths):
    return next((p for p in paths if os.path.exists(p)), None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", required=True)
    ap.add_argument("--results", default="results", help="results root (default: results)")
    ap.add_argument("--type3", type=float, default=0.65)
    ap.add_argument("--type2", type=float, default=0.85)
    ap.add_argument("--write-breakdown", action="store_true",
                    help="write content_breakdown.csv from the outputs if it does not exist")
    args = ap.parse_args()

    tag = args.lang.lower().replace("+", "p").replace("#", "sharp")
    d = os.path.join(args.results, tag)
    paths = {
        "distribution": os.path.join(d, "clone_distribution.csv"),
        "pairs": os.path.join(d, f"{tag}_similar_pairs.csv"),
        "type1": first_existing(os.path.join(d, f"{tag}_type1_pairs.csv"),
                                os.path.join(d, f"{tag}_type1_pairs.csv.gz")),
        "top10": os.path.join(d, "top10_similar_pairs.csv"),
        "validation": os.path.join(d, "validation_sample_30.csv"),
        "extracted": os.path.join(d, f"extracted_skills_{tag}.csv"),
        "breakdown": os.path.join(d, "content_breakdown.csv"),
    }
    print(f"Verifying {d}")

    print("files")
    for key in ("distribution", "pairs", "type1", "top10", "validation"):
        check(f"{key} file present", paths[key] and os.path.exists(paths[key]), paths[key] or "missing")
    if not all(results):
        sys.exit(1)
    have_extracted = os.path.exists(paths["extracted"])
    if not have_extracted:
        print(f"  note: {paths['extracted']} not found; checks that need it are skipped")

    dist = read_csv(paths["distribution"], index_col=0)
    pairs = read_csv(paths["pairs"])
    t1 = read_csv(paths["type1"])
    t2mask = pairs["clone_type"] == TYPE2

    print("Type-2 / Type-3 pairs")
    s = pairs["similarity_score"]
    bad2 = int((t2mask & (s < args.type2)).sum())
    bad3 = int((~t2mask & ((s >= args.type2) | (s < args.type3))).sum())
    check("every label matches its score", bad2 + bad3 == 0, f"{len(pairs):,} pairs, {bad2 + bad3} wrong")
    check("only Type-2 / Type-3 labels", pairs["clone_type"].isin([TYPE2, TYPE3]).all())
    check("no self-pairs", (pairs["skill_a_sha"] != pairs["skill_b_sha"]).all())
    check("no duplicate pairs", not pairs.duplicated(["skill_a_sha", "skill_b_sha"]).any())
    check("pairs ordered (a < b)", (pairs["skill_a_sha"] < pairs["skill_b_sha"]).all())

    print("Type-1 pairs")
    check("both sides share the SHA", (t1["skill_a_sha"] == t1["skill_b_sha"]).all(), f"{len(t1):,} pairs")
    check("score is 1.0 and label Type-1", ((t1["similarity_score"] == 1.0) & (t1["clone_type"] == TYPE1)).all())

    ext = None
    if have_extracted:
        parts = []
        for chunk in pd.read_csv(paths["extracted"], usecols=["file_sha", "content"], dtype=str, chunksize=100_000):
            text = chunk["content"].fillna("").str.strip()
            parts.append(pd.DataFrame({"file_sha": chunk["file_sha"], "has_content": text != "",
                                       "symlink_stub": text.map(looks_like_symlink)}))
        ext = pd.concat(parts, ignore_index=True)
        n, distinct = len(ext), ext["file_sha"].nunique()
        check("Type-1 pair count = occurrences - distinct files", len(t1) == n - distinct,
              f"{len(t1):,} vs {n - distinct:,}")

        print("categories")
        counts = ext["file_sha"].value_counts()
        s1 = set(counts[counts > 1].index)
        s2 = set(pairs.loc[t2mask, "skill_a_sha"]) | set(pairs.loc[t2mask, "skill_b_sha"])
        s3 = set(pairs.loc[~t2mask, "skill_a_sha"]) | set(pairs.loc[~t2mask, "skill_b_sha"])
        ext["overall_category"] = ext["file_sha"].map(
            lambda x: TYPE1 if x in s1 else TYPE2 if x in s2 else TYPE3 if x in s3 else UNIQUE)
        rebuilt = ext["overall_category"].value_counts()
        same = all(int(rebuilt.get(k, 0)) == int(dist.loc[k, "count"]) for k in ORDER if k in dist.index)
        check("rebuilt categories match clone_distribution.csv", same and int(dist.loc["Total", "count"]) == n)
        shares_ok = all(round(rebuilt.get(k, 0) / n * 100, 1) == dist.loc[k, "share_%"] for k in ORDER if k in dist.index)
        check("shares match", shares_ok)

    print("top-10 and validation sample")
    top = read_csv(paths["top10"])
    expect = pairs.sort_values(["similarity_score", "skill_a_name"], ascending=[False, True]).head(10)
    check("top10 = pairs re-sorted by score", top.shape == expect.shape and (top.values == expect.values).all())
    v = read_csv(paths["validation"])
    by = v["clone_type"].value_counts()
    check("validation sample has <= 10 per type", all(by.get(k, 0) <= 10 for k in (TYPE1, TYPE2, TYPE3)), by.to_dict())
    keys = set(zip(pairs["skill_a_sha"], pairs["skill_b_sha"]))
    vs = v[v["clone_type"] != TYPE1]
    check("validation Type-2/3 rows exist in pairs file",
          all((a, b) in keys for a, b in zip(vs["skill_a_sha"], vs["skill_b_sha"])))
    vt1 = v[v["clone_type"] == TYPE1]
    check("validation Type-1 rows exist in Type-1 file", vt1["skill_a_sha"].isin(set(t1["skill_a_sha"])).all())

    if ext is not None:
        print("content breakdown")
        sym_shas = set(ext.loc[ext["symlink_stub"], "file_sha"])  # same SHA = same bytes
        g = ext.assign(symlink=ext["file_sha"].isin(sym_shas)).groupby("overall_category")
        bd = pd.DataFrame({"total": g.size(), "has_content": g["has_content"].sum(),
                           "no_content": g.size() - g["has_content"].sum(),
                           "symlink_stub": g["symlink"].sum()}).reindex(ORDER).fillna(0).astype(int)
        bd.loc["Total"] = bd.sum()
        bd["content_only_share_%"] = (bd["has_content"] / max(bd.at["Total", "has_content"], 1) * 100).round(1)
        bd.index.name = "overall_category"
        if os.path.exists(paths["breakdown"]):
            written = pd.read_csv(paths["breakdown"], index_col=0)
            check("content_breakdown.csv matches recomputation",
                  written.shape == bd.shape and (written.values == bd.values).all())
        elif args.write_breakdown:
            bd.to_csv(paths["breakdown"])
            print(f"  wrote {paths['breakdown']}")
        else:
            print("  content_breakdown.csv not found (use --write-breakdown to create it)")
        nc, n_all, sl = (int(bd.at["Total", c]) for c in ("no_content", "total", "symlink_stub"))
        print(f"  no content: {nc:,} of {n_all:,} ({nc / n_all * 100:.1f}%), symlink stubs: {sl:,}")

    failed = results.count(False)
    print(f"\n{len(results) - failed}/{len(results)} checks passed" + ("" if not failed else f", {failed} FAILED"))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
