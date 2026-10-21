# Manual review of validation samples — Java, Rust, Python

**Status: final, spot-checked by Lucifix.**
Per-pair verdicts and reasons: `results/java/manual_review.md`,
`results/rust/manual_review.md`, `results/python/manual_review.md`.

Method: for each language, all 30 pairs in `validation_sample_30.csv`
(10 Type-1, 10 Type-2, 10 Type-3, `random_state=42`) were reviewed by reading both
files' full text and their line-by-line differences, as with
`src/inspect_pair_content.py` for C++. Categories are defined in each file.

## Results (90 pairs)

| Detected as | Verdict | Java | Rust | Python | Total |
|---|---|---|---|---|---|
| **Type-1** (same SHA) | True clone (real skill, identical copies) | 3 | 2 | 7 | **12** |
| | No content (never fetched) | 2 | 8 | 3 | **13** |
| | Symlink stub | 4 | 0 | 0 | **4** |
| | Test fixture | 1 | 0 | 0 | **1** |
| **Type-2** (≥ 0.85) | True clone | 8 | 9 | 5 | **22** |
| | True clone, type off | 1 | 1 | 1 | **3** |
| | Template sibling | 0 | 0 | 4 | **4** |
| | False positive | 1 | 0 | 0 | **1** |
| **Type-3** (0.65–0.85) | True clone | 1 | 1 | 0 | **2** |
| | True clone, type off | 1 | 1 | 0 | **2** |
| | Template sibling | 3 | 5 | 8 | **16** |
| | False positive | 5 | 3 | 1 | **9** |
| | Placeholder | 0 | 0 | 1 | **1** |

## Findings

1. **Type-2 is reliable.** 25 of 30 Type-2 pairs (83%) are genuine clones: renamed
   copies (project, product or agent names swapped), copies with small edits, or
   versions of the same upstream skill. The misses are mostly Python skills generated
   from one template (4), plus one pair of different documents about the same tool.

2. **Type-3 mostly does not find copies.** Only 4 of 30 Type-3 pairs (13%) are
   genuine copy-and-modify clones. 16 (53%) are *template siblings*: different skills
   built from the same generator or sharing large boilerplate (e.g. GSD command
   wrappers, awesome-omni-skills packaging, generated law or knowledge-base entries).
   9 (30%) are false positives driven by shared topic vocabulary. The 0.65–0.85 band
   therefore mainly measures shared templates, not copying.

3. **Type-1 is correct but often not checkable.** Every Type-1 pair is byte-identical
   by SHA, but 13 of 30 have no content in the database, so the text cannot be seen.
   This is very likely what the C++ inspection showed as "empty SKILL.md templates":
   the files are not empty, their content was never fetched.

4. **Symlinks inflate Type-1.** 4 of 10 Java Type-1 pairs are symlinks: the stored
   "file" is only a target path like `../../../.workspace-rules/skills/x/SKILL.md`,
   so every link to the same target shares one SHA (147–149 copies in a single repo).
   These are not copied skills.

5. **Placeholders are rare.** Only 1 of 90 pairs (Python Type-3) is a pair of
   placeholder stubs. The "empty template" threat in `THREATS_TO_VALIDITY.md` is
   better described as unfetched content plus symlink stubs.

6. **The 0.85 boundary is fuzzy in both directions.** Renamed copies can fall just
   below 0.85 (Type-3) and heavily edited versions can score above it (Type-2):
   5 genuine clones carry the "wrong" type.

## Suggested follow-ups

- Exclude or separately count Type-1 rows with no content, and detect symlink stubs
  (single-line content ending in `.md`) before counting Type-1.
- Treat Type-3 results as "template family / related" rather than copies, or raise the
  Type-3 threshold; consider a separate "template sibling" category.
- Review the C++ sample with the same categories so all four languages are comparable.
- Caveat: 30 pairs per language is a small sample; percentages are indicative only.
