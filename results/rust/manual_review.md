# Rust — manual review of validation_sample_30.csv

**Status: first pass, drafted with AI assistance. Team members should spot-check
before these verdicts are treated as final.**

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

- **Type-1:** No content 8, True clone 2
- **Type-2:** True clone 9, True clone (type off) 1
- **Type-3:** Template sibling 5, False positive 3, True clone 1, True clone (type off) 1

"Line sim." is difflib's line-level similarity of the two texts (1.0 = same lines);
it is shown to help judge pairs and is not part of the pipeline.

## Pairs

| # | Type | Score | Skill(s) | Line sim. | Same repo | Verdict | Reason |
|---|---|---|---|---|---|---|---|
| 0 | Type-1 | 1.000 | [Unnamed Skill] | – | – | **No content** | Content never fetched; SHA match only. |
| 1 | Type-1 | 1.000 | [Unnamed Skill] | – | – | **No content** | Content never fetched; SHA match only. |
| 2 | Type-1 | 1.000 | [Unnamed Skill] | – | – | **No content** | Content never fetched; SHA match only. |
| 3 | Type-1 | 1.000 | [Unnamed Skill] | – | – | **No content** | Content never fetched; SHA match only. |
| 4 | Type-1 | 1.000 | [Unnamed Skill] | – | – | **No content** | Content never fetched; SHA match only. |
| 5 | Type-1 | 1.000 | [Unnamed Skill] | – | – | **No content** | Content never fetched; SHA match only. |
| 6 | Type-1 | 1.000 | [Unnamed Skill] | – | – | **No content** | Content never fetched; SHA match only. |
| 7 | Type-1 | 1.000 | [Unnamed Skill] | 1.00 | – | **True clone** | Full 7.3k-char skill (lex-primer), identical in 3 repos. |
| 8 | Type-1 | 1.000 | ctl-review | 1.00 | – | **True clone** | Full 4.2k-char skill (ctl-review), 2 identical copies in one repo. |
| 9 | Type-1 | 1.000 | [Unnamed Skill] | – | – | **No content** | Content never fetched; SHA match only. |
| 10 | Type-2 | 0.859 | skill-creator / skill-creator | 0.56 | no | **True clone (type off)** | Anthropic `skill-creator` adapted for VT Code vs Gemini CLI (line similarity 0.56): a real clone with substantial edits; Type-3 fits better. |
| 11 | Type-2 | 0.863 | agenda / agenda-management | 0.71 | yes | **True clone** | Two test-fixture versions of an agenda skill; fields renamed. |
| 12 | Type-2 | 0.960 | plugin-creator / plugin-creator | 0.95 | no | **True clone** | Same plugin-creator skill with the product renamed (ThinWedge -> Codewith); textbook parameterized clone. |
| 13 | Type-2 | 0.983 | vibearound / vibearound | 0.88 | yes | **True clone** | Same skill for two agents (Gemini vs Codex) in one repo; agent name and details swapped. |
| 14 | Type-2 | 0.910 | gsd-resume-work / gsd-resume-work | 0.91 | yes | **True clone** | Same generated skill in two test fixtures; one has an extra paragraph. |
| 15 | Type-2 | 0.997 | openclaw-setup / openclaw-setup | 0.99 | no | **True clone** | Same skill with the product renamed (ByteTensor -> OpenHub). |
| 16 | Type-2 | 0.981 | reflect / reflect | 0.93 | no | **True clone** | Same `reflect` skill in two repos by one author; small edits. |
| 17 | Type-2 | 0.923 | using-superpowers / using-superpowers | 0.92 | no | **True clone** | `using-superpowers` adapted for a different agent (Codex); same structure and most text. |
| 18 | Type-2 | 0.959 | gsd-ship / gsd-ship | 0.97 | yes | **True clone** | Same skill; only a workflow path differs. |
| 19 | Type-2 | 0.999 | imessage / imessage | 0.99 | no | **True clone** | Same skill; only the `author` field differs. |
| 20 | Type-3 | 0.656 | gsd-update / gsd-undo | 0.70 | yes | **Template sibling** | Different GSD commands (update vs undo) generated from the same Codex wrapper template. |
| 21 | Type-3 | 0.737 | gsd-import / gsd-ship | 0.78 | yes | **Template sibling** | Different GSD commands (import vs ship) from the same wrapper template. |
| 22 | Type-3 | 0.790 | skill-creator / skill-creator | 0.39 | no | **True clone** | Cut-down vs full `skill-creator`, one with added Japanese rules: genuine copy-and-modify. |
| 23 | Type-3 | 0.672 | fret-ui-review / fret-external-app-mode | 0.39 | yes | **False positive** | Different Fret skills (UI review vs external app mode); same project vocabulary. |
| 24 | Type-3 | 0.667 | gsd-update / gsd-session-report | 0.75 | yes | **Template sibling** | Different GSD commands (update vs session-report) from the same wrapper template. |
| 25 | Type-3 | 0.668 | KSB-D12-K0001 / KSB-D12-K0006 | 0.78 | yes | **Template sibling** | Two generated knowledge-skill entries (K0001 vs K0006) from one template; different topics. |
| 26 | Type-3 | 0.799 | skill-creator / skill-creator | 0.87 | no | **True clone (type off)** | Same `skill-creator` with the product name replaced (Agere -> the agent); a parameterized clone just under 0.85. |
| 27 | Type-3 | 0.672 | decision-log-author / compensation-plan-author | 0.91 | yes | **Template sibling** | Different generated skills (decision log vs compensation plan) with an identical skeleton (line similarity 0.91). |
| 28 | Type-3 | 0.693 | canon-implementation / canon-retrieve | 0.12 | no | **False positive** | Different canon skills (implementation vs retrieve) in different repos; 0.12 line similarity. |
| 29 | Type-3 | 0.738 | gh-cli / proxysss-install | 0.25 | yes | **False positive** | Different skills in one repo (gh-cli vs install guide); 0.25 line similarity. |
