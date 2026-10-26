# Manual review of validation samples — C++, Java, Rust, Python

**Status: final, spot-checked by Lucifix.**

Per-pair verdicts and reasons: `results/cpp/manual_review.md`,
`results/java/manual_review.md`, `results/rust/manual_review.md`,
`results/python/manual_review.md`.

Method: for each language, all 30 pairs in its `validation_sample_30.csv`
(10 Type-1, 10 Type-2, 10 Type-3, `random_state=42`) were reviewed by reading both
files' full text and their line-by-line differences, as with
`src/inspect_pair_content.py`. The C++ sample is the Sprint 1 one
(`results/validation_sample_30.csv`). Categories are defined in each file.

## Results (120 pairs)

| Detected as | Verdict | C++ | Java | Rust | Python | Total |
|---|---|---|---|---|---|---|
| **Type-1** (same SHA) | True clone (real skill, identical copies) | 5 | 3 | 2 | 7 | **17** |
| | No content (never fetched) | 5 | 2 | 8 | 3 | **18** |
| | Symlink stub | 0 | 4 | 0 | 0 | **4** |
| | Test fixture | 0 | 1 | 0 | 0 | **1** |
| **Type-2** (≥ 0.85) | True clone | 8 | 8 | 9 | 5 | **30** |
| | True clone, type off | 2 | 1 | 1 | 1 | **5** |
| | Template sibling | 0 | 0 | 0 | 4 | **4** |
| | False positive | 0 | 1 | 0 | 0 | **1** |
| **Type-3** (0.65–0.85) | True clone | 1 | 1 | 1 | 0 | **3** |
| | True clone, type off | 0 | 1 | 1 | 0 | **2** |
| | Template sibling | 6 | 3 | 5 | 8 | **22** |
| | False positive | 3 | 5 | 3 | 1 | **12** |
| | Placeholder | 0 | 0 | 0 | 1 | **1** |

## Findings

1. **Type-2 is reliable.** 35 of 40 Type-2 pairs (88%) are genuine clones: renamed
   copies (project, product or agent names swapped), copies with small edits, the same
   skill packaged for different agent tools, or versions of the same upstream skill.
   The misses are mostly Python skills generated from one template (4), plus one pair
   of different documents about the same tool.

2. **Type-3 mostly does not find copies.** Only 5 of 40 Type-3 pairs (13%) are
   genuine copy-and-modify clones. 22 (55%) are *template siblings*: different skills
   built from the same generator or sharing large boilerplate (e.g. GSD command
   wrappers, awesome-omni-skills packaging, generated law or knowledge-base entries).
   12 (30%) are false positives driven by shared topic vocabulary. The 0.65–0.85 band
   therefore mainly measures shared templates, not copying. The pattern is the same
   in all four languages.

3. **Type-1 is correct but often not checkable.** Every Type-1 pair is byte-identical
   by SHA, but 18 of 40 have no content in the database, so the text cannot be seen.
   This is very likely what the Sprint 1 C++ inspection read as "empty SKILL.md
   templates": the files are not empty, their content was never fetched.

4. **Symlinks inflate Type-1.** 4 of 10 Java Type-1 pairs are symlinks: the stored
   "file" is only a target path like `../../../.workspace-rules/skills/x/SKILL.md`,
   so every link to the same target shares one SHA (147–149 copies in a single repo).
   Across the whole Java dataset, 2,948 of 7,955 Type-1 rows (37%) are symlinks
   (see `results/java/content_breakdown.csv`); for the other languages it is under 1%.

5. **Placeholders are rare.** Only 1 of 120 pairs (Python Type-3) is a pair of
   placeholder stubs. The "empty template" threat in `THREATS_TO_VALIDITY.md` is
   better described as unfetched content plus symlink stubs.

6. **The 0.85 boundary is fuzzy in both directions.** Renamed copies can fall just
   below 0.85 (Type-3) and heavily edited versions can score above it (Type-2); one
   C++ Type-2 pair differs only in Windows vs Unix line endings, which changes the SHA
   but not the text. 7 genuine clones carry the "wrong" type.

## Suggested follow-ups

- Report Type-1 with and without rows that have no content or are symlink stubs
  (both are counted in each language's `content_breakdown.csv`).
- Treat Type-3 results as "template family / related" rather than copies, or raise the
  Type-3 threshold; consider a separate "template sibling" category.
- Normalise line endings before hashing if Type-1 should ignore them.
- Caveat: 30 pairs per language is a small sample; percentages are indicative only.
