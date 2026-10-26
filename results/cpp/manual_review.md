# C++ — manual review of validation_sample_30.csv

**Status: final, spot-checked by Lucifix.**

Source: the Sprint 1 sample `results/validation_sample_30.csv` with text from
`data/samples/extracted_skills_sample.csv`.

Each of the 30 pairs in `validation_sample_30.csv` (10 Type-1, 10 Type-2, 10 Type-3,
sampled with `random_state=42`) was reviewed by reading both files' full text and
their line-by-line differences, in the same spirit as `src/inspect_pair_content.py`.

## Verdict categories

- **True clone**: one file is a copy or adaptation of the other (or both of a common source), same purpose.
- **True clone (type off)**: a genuine clone, but the Type-2 / Type-3 label looks wrong (e.g. a renamed copy just under 0.85, or a heavily edited copy above it).
- **Template sibling**: different skills built from the same template or generator, or sharing large boilerplate; same structure, different purpose.
- **False positive**: different skills; the score comes from shared topic vocabulary, with little shared text.
- **Placeholder**: stub files with no real content.
- **Symlink stub** (Type-1): the file is only a symlink target path such as `../../../x/SKILL.md`, so all links to the same target share a SHA.
- **Test fixture** (Type-1): a trivial file from a test suite.
- **No content**: content was never fetched (`content_fetched = 0`); the SHA match is real but the text cannot be checked.

## Summary

- **Type-1:** No content 5, True clone 5
- **Type-2:** True clone 8, True clone (type off) 2
- **Type-3:** Template sibling 6, False positive 3, True clone 1

"Line sim." is difflib's line-level similarity of the two texts (1.0 = same lines);
it is shown to help judge pairs and is not part of the pipeline.

## Pairs

| # | Type | Score | Skill(s) | Line sim. | Same repo | Verdict | Reason |
|---|---|---|---|---|---|---|---|
| 0 | Type-1 | 1.000 | [Unnamed Skill] | – | – | **No content** | Content never fetched; SHA match only. |
| 1 | Type-1 | 1.000 | [Unnamed Skill] | 1.00 | – | **True clone** | Full 4.3k-char skill (dev-design), identical in 2 repos. |
| 2 | Type-1 | 1.000 | [Unnamed Skill] | – | – | **No content** | Content never fetched; 166 copies across 2 repos (benchmark result folders). |
| 3 | Type-1 | 1.000 | [Unnamed Skill] | – | – | **No content** | Content never fetched; SHA match only. |
| 4 | Type-1 | 1.000 | [Unnamed Skill] | 1.00 | – | **True clone** | Short real skill (feature-implementation, 375 chars); 3 copies in one repo. |
| 5 | Type-1 | 1.000 | pm-bugfix | 1.00 | – | **True clone** | Short real skill (pm-bugfix, 507 chars); identical in 2 repos. |
| 6 | Type-1 | 1.000 | [Unnamed Skill] | – | – | **No content** | Content never fetched; 13 copies across 11 repos. |
| 7 | Type-1 | 1.000 | [Unnamed Skill] | – | – | **No content** | Content never fetched; 13 copies across 11 repos. |
| 8 | Type-1 | 1.000 | expert-reset | 1.00 | – | **True clone** | Full 7.5k-char skill (expert-reset), identical in 2 repos. |
| 9 | Type-1 | 1.000 | [Unnamed Skill] | 1.00 | – | **True clone** | Full 6.2k-char `plan` skill; 84 copies inside benchmark result folders of one repo. |
| 10 | Type-2 | 0.989 | gsd-reapply-patches / gsd-reapply-patches | 0.88 | no | **True clone** | Same GSD skill packaged for Codex vs Cursor; adapter block swapped. |
| 11 | Type-2 | 0.959 | splitting-pr / splitting-pr | 0.96 | no | **True clone** | Same splitting-pr skill adapted from Bazel BUILD files to xmake. |
| 12 | Type-2 | 0.965 | gsd-code-review-fix / gsd-code-review-fix | 0.98 | no | **True clone** | Same GSD skill; only the absolute workflow path differs. |
| 13 | Type-2 | 0.997 | checkout-pr / checkout-pr | 0.96 | no | **True clone** | Same checkout-pr skill; two small edits. |
| 14 | Type-2 | 0.866 | gsd-next / gsd-next | 0.94 | no | **True clone** | Same GSD skill; workflow path and one sentence differ. |
| 15 | Type-2 | 1.000 | map-blockout / map-blockout | 1.00 | no | **True clone (type off)** | Text identical apart from Windows vs Unix line endings, which changes the SHA: effectively a verbatim copy labelled Type-2. |
| 16 | Type-2 | 0.885 | graphify / [Unnamed Skill] | 0.38 | no | **True clone (type off)** | Two versions of the graphify skill (38k vs 47k chars, line similarity 0.38): a real clone, heavily diverged; Type-3 fits better. |
| 17 | Type-2 | 0.973 | swift-mlx / swift-mlx | 0.96 | no | **True clone** | mlx-swift skill in a fork vs upstream; the upstream adds sections. |
| 18 | Type-2 | 0.998 | analyzing-source-truth-gap / analyzing-source-truth-gap | 0.97 | yes | **True clone** | Same skill in `.claude/` and `.agents/` of one repo; one path differs. |
| 19 | Type-2 | 0.960 | module-status / module-status | 0.93 | yes | **True clone** | Same skill in `.claude/` and `.opencode/` of one repo; small edits. |
| 20 | Type-3 | 0.651 | gsd-help / gsd-ui-phase | 0.76 | no | **Template sibling** | Different GSD commands (help vs ui-phase) from the same Codex wrapper template. |
| 21 | Type-3 | 0.698 | gsd-manager / gsd-progress | 0.76 | yes | **Template sibling** | Different GSD commands (manager vs progress) from the same wrapper template. |
| 22 | Type-3 | 0.650 | gsd-resume-work / gsd-next | 0.72 | no | **Template sibling** | Different GSD commands (resume-work vs next) from the same wrapper template. |
| 23 | Type-3 | 0.717 | logosdb-memory / ldb-search | 0.14 | yes | **False positive** | Different LogosDB skills (memory vs search) in one repo; 0.14 line similarity. |
| 24 | Type-3 | 0.667 | gsd-update / gsd-fast | 0.73 | no | **Template sibling** | Different GSD commands (update vs fast) from the same wrapper template. |
| 25 | Type-3 | 0.813 | retrospective / retrospective | 0.95 | no | **True clone** | Fork of Alibaba MNN's retrospective skill with edited trigger conditions: genuine copy-and-modify. |
| 26 | Type-3 | 0.662 | speckit-implement / speckit-plan | 0.37 | no | **False positive** | Different spec-kit commands (implement vs plan) in different repos; shared spec-kit vocabulary (0.37). |
| 27 | Type-3 | 0.651 | gsd-fast / gsd-cleanup | 0.79 | yes | **Template sibling** | Different GSD commands (fast vs cleanup) from the same Cursor wrapper template. |
| 28 | Type-3 | 0.696 | smsim-pdc-momentum-reco / smsim-nn-target-momentum | 0.61 | yes | **Template sibling** | Sibling SMSimulator workflow skills from one author with the same structure; different stages. |
| 29 | Type-3 | 0.723 | [Unnamed Skill] / [Unnamed Skill] | 0.16 | yes | **False positive** | Different Valdi skills (setup vs testing) in one repo; 0.16 line similarity. |
