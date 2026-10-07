# Python run — partial (stopped during TF-IDF)

Script: `src/run_language_pipeline.py --db agent_skills_release.db --lang python`
(same method as the Sprint 1 C++ run: same SQL filter, SHA-based Type-1,
TF-IDF `stop_words="english", min_df=1`, thresholds 0.85 / 0.65).

Date: 2026-10-07
Machine: Windows 11 laptop, 15.3 GB RAM, 29 GB pagefile
Python: conda base, Python 3.13.11, pandas 2.3.3, scikit-learn 1.8.0, matplotlib 3.10.8

## Results so far

| Step | Status | Result |
|---|---|---|
| 1. Extract | done (~7 min, full 44 GB scan) | **1,657,440** Python skill occurrences, **769,920** distinct files (`file_sha`) |
| 2. Type-1 (identical SHA) | done | **887,520** Type-1 pairs from **140,596** SHAs that occur more than once; those groups hold **1,028,116** occurrences (**62.0%** of all Python skill occurrences = the Type-1 category count). Largest group: 1,026 identical copies. See `python_type1_pairs.csv.gz`. |
| 3. Type-2 / Type-3 (TF-IDF) | **stopped manually** while fitting the vectoriser, before any chunk was compared | — |
| 4. Categorise + plot | not reached | — |

Total runtime before stop: ~11.5 min. Peak private memory: **~16.2 GB**
(peak working set ~7.9 GB; the rest was paged out to the pagefile).

### Type-1 output

`python_type1_pairs.csv.gz` (6.6 MB; 122 MB uncompressed, over GitHub's 100 MB
limit) was generated afterwards from `extracted_skills_python.csv` using the
script's own `type1_pairs()` on the `file_sha` and `name` columns, without
re-scanning the DB. Row order is the same as in the extraction, so the pairs
are identical to what the pipeline builds in memory. Read it with
`pd.read_csv("python_type1_pairs.csv.gz")`. The script now also writes
`<lang>_type1_pairs.csv` right after step 2, so future runs keep it even if
TF-IDF does not finish.

The Type-1 category share (62.0%) is final; it does not depend on TF-IDF.
The Type-2 / Type-3 / Unique split of the remaining 629,324 occurrences
needs step 3.

The run was stopped on purpose because it was exceeding physical RAM.
`clone_distribution.csv` and `top10_similar_pairs.csv` were therefore **not produced**.
`extracted_skills_python.csv` (5.6 GB) was written locally but is not committed
(over GitHub's 100 MB file limit).

## Why Python doesn't fit where C++ did

| | C++ (Sprint 1) | Python |
|---|---|---|
| Skill occurrences | 10,737 | 1,657,440 (~154x) |
| Distinct files compared by TF-IDF | < ~8k | 769,920 |
| Pairwise comparisons (n^2/2) | ~tens of millions | ~296 billion |

The whole-DB scan streams from disk; memory is driven by the size of the matching
subset, and the TF-IDF step grows with the square of the distinct-file count.

## Options for finishing (not yet applied)

Method-preserving changes (identical results, less memory / time):
1. Load `content` only once per `file_sha` instead of for every occurrence.
2. Store matched pairs in NumPy arrays instead of a list of dicts.
3. Raise `max_cells` (fewer, larger chunks); this changes batching only.

Even with these, the ~296 billion comparisons would likely take hours on a laptop.
A larger-memory machine (e.g. U-M ARC Great Lakes, or a Colab Pro high-RAM runtime)
is the practical route. Any change to the method itself (sampling, approximate
nearest neighbours) would break comparability with the C++ results and needs a
team decision.

The C++ sanity re-run (expected 10,737 rows; Type-1 3,147 / Type-2 709 /
Type-3 914 / Unique 5,967) was not run in this session.
