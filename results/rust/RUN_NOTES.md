# Rust run — complete

Script: `src/run_language_pipeline.py --db agent_skills_release.db --lang rust`
(same method as the Sprint 1 C++ run: same SQL filter, SHA-based Type-1,
TF-IDF `stop_words="english", min_df=1`, thresholds 0.85 / 0.65).

Date: 2026-10-21
Machine: Windows 11 laptop, 15.3 GB RAM
Python: conda base, Python 3.13.11, pandas 2.3.3, scikit-learn 1.8.0, matplotlib 3.10.8
Runtime: 5 min 53 s (mostly the full DB scan). Peak private memory: ~1.9 GB.

## Results

56,391 Rust skill occurrences, 45,710 distinct files.
10,681 Type-1 pairs; 30,597 Type-2/3 pairs (5,668 Type-2, 24,929 Type-3).

| Category | Count | Share | C++ | Java | Python |
|---|---|---|---|---|---|
| Type-1 (Verbatim) | 17,092 | 30.3% | 29.3% | 39.5% | 62.0% |
| Type-2 (Parameterized) | 4,428 | 7.9% | 6.6% | 4.9% | 13.6% |
| Type-3 (Semantic) | 5,937 | 10.5% | 8.5% | 5.6% | 5.6% |
| Truly Unique | 28,934 | 51.3% | 55.6% | 50.0% | 18.7% |
| Total | 56,391 | 100% | | | |

All top-10 pairs score 1.0: files that differ only in things TF-IDF ignores
(whitespace, case, punctuation, stop words, word order). Some are generic,
non-Rust skills stored in Rust repos (e.g. `golang-testing`,
`analyzing-dotnet-performance`).

## Caveat: rows with no content

20,793 of 56,391 rows (**36.9%**) have no content in the database
(`content_fetched = 0`). Their SHA is still valid, so they can be Type-1, but
they cannot be compared by TF-IDF.

| Category | Has content | No content |
|---|---|---|
| Type-1 | 3,063 | 14,029 |
| Type-2 | 4,428 | 0 |
| Type-3 | 5,937 | 0 |
| Unique | 22,170 | 6,764 |
| Total | 35,598 | 20,793 |

Counting only the 35,598 rows with content: Type-1 8.6%, Type-2 12.4%,
Type-3 16.7%, Unique 62.3%.

## Checks

- Type-1 pairs = occurrences − distinct files (10,681).
- Categories rebuilt from the pairs file match `clone_distribution.csv`.
- Every pair's label matches its score; no self-pairs, duplicates or misordered pairs.
- `top10_similar_pairs.csv` matches the pairs file re-sorted by score (read the
  CSV with `float_precision="round_trip"`; the default parser can round the
  last digit and create false ties).
- Validation sample: 10 per type; all Type-2/3 rows present in the pairs file.

## Files

- `clone_distribution.csv`, `rust_clones.png` — category counts and chart
- `rust_type1_pairs.csv` — Type-1 (identical SHA) pairs
- `rust_similar_pairs.csv` — all Type-2 / Type-3 pairs
- `top10_similar_pairs.csv`, `validation_sample_30.csv`
- `extracted_skills_rust.csv` (247 MB) is not committed; re-create it by running the script.
