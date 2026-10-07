# Java run — complete

Script: `src/run_language_pipeline.py --db agent_skills_release.db --lang java`
(same method as the Sprint 1 C++ run: same SQL filter, SHA-based Type-1,
TF-IDF `stop_words="english", min_df=1`, thresholds 0.85 / 0.65).

Date: 2026-10-07
Machine: Windows 11 laptop, 15.3 GB RAM
Python: conda base, Python 3.13.11, pandas 2.3.3, scikit-learn 1.8.0, matplotlib 3.10.8
Runtime: 2 min 55 s (mostly the full DB scan). Peak private memory: ~1.8 GB.

## Results

20,118 Java skill occurrences, 13,880 distinct files.
6,238 Type-1 pairs, 2,292 Type-2/3 pairs.

| Category | Count | Share | C++ share |
|---|---|---|---|
| Truly Unique | 10,058 | 50.0% | 55.6% |
| Type-1 (Verbatim) | 7,955 | 39.5% | 29.3% |
| Type-3 (Semantic) | 1,117 | 5.6% | 8.5% |
| Type-2 (Parameterized) | 988 | 4.9% | 6.6% |
| Total | 20,118 | 100% | |

All top-10 pairs score 1.0 with different SHAs: the files differ only in
things TF-IDF ignores (whitespace, case, punctuation, stop words, word order),
so they are near-verbatim copies that miss the exact SHA match.

## Files

- `clone_distribution.csv`, `java_clones.png` — category counts and chart
- `java_type1_pairs.csv` — Type-1 (identical SHA) pairs
- `java_similar_pairs.csv` — all Type-2 / Type-3 pairs
- `top10_similar_pairs.csv`, `validation_sample_30.csv`
- `extracted_skills_java.csv` (78 MB) is not committed; re-create it by running the script.
