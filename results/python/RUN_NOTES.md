# Python run — complete

Script: `src/run_language_pipeline.py --db agent_skills_release.db --lang python --max-cells 300000000`
(same method as the Sprint 1 C++ run: same SQL filter, SHA-based Type-1,
TF-IDF `stop_words="english", min_df=1`, thresholds 0.85 / 0.65).

Run: 2026-10-20 to 2026-10-21 on a 64 GB lab desktop (Python 3.12.10).
A first attempt on a 15.3 GB laptop (2026-10-07) was stopped during TF-IDF
because it exceeded physical RAM; the script was then changed to stream the
extraction and store pairs compactly (results identical, verified on Java).

- Memory: ~13.5 GB while building the TF-IDF matrix.
- Time: ~19 h 20 min from the Type-1 step finishing to the pairs file being
  written (file timestamps). The `--dry-run` estimate was ~11 h; the gap may
  include time the machine was idle or paused.

## Results

1,657,440 Python skill occurrences, 769,920 distinct files.
887,520 Type-1 pairs; 8,065,074 Type-2/3 pairs (1,819,692 Type-2, 6,245,382 Type-3).
The `--dry-run` estimate was 8.56 M pairs (6% high).

| Category | Count | Share | Java | C++ |
|---|---|---|---|---|
| Type-1 (Verbatim) | 1,028,116 | 62.0% | 39.5% | 29.3% |
| Truly Unique | 310,190 | 18.7% | 50.0% | 55.6% |
| Type-2 (Parameterized) | 225,534 | 13.6% | 4.9% | 6.6% |
| Type-3 (Semantic) | 93,600 | 5.6% | 5.6% | 8.5% |
| Total | 1,657,440 | 100% | | |

All top-10 pairs score 1.0 (33,470 pairs score >= 0.9999): files that differ
only in things TF-IDF ignores (whitespace, case, punctuation, stop words, word order).

## Caveat: rows with no content

947,882 of 1,657,440 rows (**57.2%**) have no content in the database
(`content_fetched = 0`). Their SHA is still valid, so they can be Type-1, but
they cannot be compared by TF-IDF.

| Category | Has content | No content |
|---|---|---|
| Type-1 | 112,950 | 915,166 |
| Type-2 | 225,534 | 0 |
| Type-3 | 93,600 | 0 |
| Unique | 277,474 | 32,716 |
| Total | 709,558 | 947,882 |

89% of Type-1 rows have no content. Counting only the 709,558 rows with
content: Type-1 15.9%, Type-2 31.8%, Type-3 13.2%, Unique 39.1%.

## Checks

- Type-1 pairs identical (MD5) between the laptop and lab runs.
- Categories rebuilt from the pairs file match `clone_distribution.csv`.
- Every pair's label matches its score; no self-pairs, duplicates or misordered pairs.
- `top10_similar_pairs.csv` matches the pairs file re-sorted by score.
- Validation sample: 10 per type; all Type-2/3 rows present in the pairs file.

## Files

- `clone_distribution.csv`, `python_clones.png` — category counts and chart
- `top10_similar_pairs.csv`, `validation_sample_30.csv`
- `python_type1_pairs.csv.gz` — Type-1 pairs (122 MB uncompressed)
- `run_python.log` — console output of the run

Not committed (over GitHub's 100 MB limit): `python_similar_pairs.csv`
(1.2 GB, all 8,065,074 pairs), `python_type1_pairs.csv`, `extracted_skills_python.csv`.
Re-create them by running the script.
