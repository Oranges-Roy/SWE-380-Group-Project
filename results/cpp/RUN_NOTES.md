# C++ run — complete

Script: `src/run_language_pipeline.py --db agent_skills_release.db --lang c++`
(same method as the Sprint 1 C++ pipeline: same SQL filter, SHA-based Type-1,
TF-IDF `stop_words="english", min_df=1`, thresholds 0.85 / 0.65).

Date: 2026-10-28
Machine: Windows 11 laptop, 15.3 GB RAM
Python: conda base, Python 3.13.11, pandas 2.3.3, scikit-learn 1.8.0, matplotlib 3.10.8
Runtime: 2 min 53 s (mostly the full DB scan). Peak private memory: ~1.6 GB.

## Results

10,737 C++ skill occurrences, 8,593 distinct files.
2,144 Type-1 pairs; 2,084 Type-2/3 pairs.

| Category | Count | Share | Java | Rust | Python |
|---|---|---|---|---|---|
| Type-1 (Verbatim) | 3,147 | 29.3% | 39.5% | 30.3% | 62.0% |
| Type-2 (Parameterized) | 643 | 6.0% | 4.9% | 7.9% | 13.6% |
| Type-3 (Semantic) | 710 | 6.6% | 5.6% | 10.5% | 5.6% |
| Truly Unique | 6,237 | 58.1% | 50.0% | 51.3% | 18.7% |
| Total | 10,737 | 100% | | | |

## Agreement with Sprint 1

- The 2,084 Type-2/3 pairs are the same pairs as the Sprint 1 file
  `results/cpp_similar_pairs.csv`, with the same labels and scores equal to
  within 1e-13. Type-1 (3,147) and the total (10,737) also match.
- The Sprint 1 chart (`figures/C++ Clones.png`) shows Type-2 709, Type-3 914 and
  Unique 5,967. Those figures cannot be reproduced from the committed Sprint 1
  pairs file or from this run, so they most likely come from an earlier run.
  The figures above (643 / 710 / 6,237) are the reproducible ones.

## Caveat: rows with no content

3,223 of 10,737 rows (**30.0%**) have no content in the database
(`content_fetched = 0`). 12 rows are symlink stubs.

| Category | Has content | No content |
|---|---|---|
| Type-1 | 733 | 2,414 |
| Type-2 | 643 | 0 |
| Type-3 | 710 | 0 |
| Unique | 5,428 | 809 |
| Total | 7,514 | 3,223 |

Counting only the 7,514 rows with content: Type-1 9.8%, Type-2 8.6%,
Type-3 9.4%, Unique 72.2%.

## Checks

`python src/verify_outputs.py --lang c++`: 20/20 checks pass.

## Files

- `clone_distribution.csv`, `cpp_clones.png`, `content_breakdown.csv`
- `cpp_type1_pairs.csv`, `cpp_similar_pairs.csv`
- `top10_similar_pairs.csv`, `validation_sample_30.csv`
- `manual_review.md` reviews the **Sprint 1** sample (`results/validation_sample_30.csv`).
  Its 10 Type-2 and 10 Type-3 pairs are identical to the ones in this folder's
  `validation_sample_30.csv`; only the Type-1 pairs differ, because Type-1 pairs are
  listed in a different order before sampling.
- `extracted_skills_cpp.csv` is not committed; re-create it by running the script.
