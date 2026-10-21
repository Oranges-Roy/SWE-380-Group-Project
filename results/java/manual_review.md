# Java — manual review of validation_sample_30.csv

**Status: final, spot-checked by Lucifix.**

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

- **Type-1:** Symlink stub 4, True clone 3, No content 2, Test fixture 1
- **Type-2:** True clone 8, False positive 1, True clone (type off) 1
- **Type-3:** False positive 5, Template sibling 3, True clone 1, True clone (type off) 1

"Line sim." is difflib's line-level similarity of the two texts (1.0 = same lines);
it is shown to help judge pairs and is not part of the pipeline.

## Pairs

| # | Type | Score | Skill(s) | Line sim. | Same repo | Verdict | Reason |
|---|---|---|---|---|---|---|---|
| 0 | Type-1 | 1.000 | [Unnamed Skill] | 1.00 | – | **Symlink stub** | File is only the symlink target `../../../.workspace-rules/skills/scaffold-client-extension/SKILL.md`; 147 copies in one repo (liferay). |
| 1 | Type-1 | 1.000 | [Unnamed Skill] | 1.00 | – | **Test fixture** | 6-line test fixture (`name: test-skill`, `test content`) from langchain4j test resources, copied in 3 repos. |
| 2 | Type-1 | 1.000 | [Unnamed Skill] | 1.00 | – | **Symlink stub** | Symlink target path only (`.../deploy-and-verify/SKILL.md`); 149 copies in one repo. |
| 3 | Type-1 | 1.000 | jewel-pr-preparer | 1.00 | – | **True clone** | Full 17.7k-char skill (jewel-pr-preparer), identical in 2 repos. |
| 4 | Type-1 | 1.000 | [Unnamed Skill] | 1.00 | – | **True clone** | Full 3.5k-char skill, 23 identical copies across workspaces of one repo. |
| 5 | Type-1 | 1.000 | [Unnamed Skill] | 1.00 | – | **Symlink stub** | Symlink target path only (`.../manage-roles-permissions/SKILL.md`); 147 copies in one repo. |
| 6 | Type-1 | 1.000 | [Unnamed Skill] | 1.00 | – | **Symlink stub** | Symlink target path only (`.../manage-environments/SKILL.md`); 149 copies in one repo. |
| 7 | Type-1 | 1.000 | [Unnamed Skill] | 1.00 | – | **True clone** | Full 15k-char skill (test-quality), identical in 7 repos. |
| 8 | Type-1 | 1.000 | [Unnamed Skill] | – | – | **No content** | Content never fetched; SHA match only. |
| 9 | Type-1 | 1.000 | [Unnamed Skill] | – | – | **No content** | Content never fetched; SHA match only. |
| 10 | Type-2 | 0.958 | xunzhi-ai-runtime / interview-pilot-ai-runtime | 0.91 | no | **True clone** | Same skill with the project renamed (xunzhi -> interview-pilot, 答辩 -> 面试); textbook parameterized clone. |
| 11 | Type-2 | 0.999 | open-issue / open-issue | 0.98 | no | **True clone** | Same skill in two repos; one adds an `analysis` issue type. |
| 12 | Type-2 | 0.932 | claude-doc-review / claude-doc-review | 0.81 | no | **True clone** | Same skill with service renamed (billing-api -> checkout-api) plus a few added lines. |
| 13 | Type-2 | 0.991 | grill-me / grill-me | 0.74 | no | **True clone** | Same `grill-me` skill; one line removed and wording tweaks. |
| 14 | Type-2 | 0.987 | frontend-design / frontend-design | 0.94 | no | **True clone** | Anthropic `frontend-design` skill; `Claude` replaced, license line dropped. |
| 15 | Type-2 | 0.958 | [Unnamed Skill] / agent-browser | 0.40 | no | **False positive** | Both document the agent-browser CLI but are different texts (10k vs 28k chars, line similarity 0.40); shared command vocabulary, not a parameterized copy. |
| 16 | Type-2 | 0.997 | refactor-module / refactor-module | 0.97 | yes | **True clone** | Same skill in `.claude/` and `.agents/` of one repo; `CLAUDE.md` -> `AGENTS.md`. |
| 17 | Type-2 | 0.943 | [Unnamed Skill] / [Unnamed Skill] | 0.97 | yes | **True clone** | Same debug skill in two example projects of one repo; project-specific commands swapped. |
| 18 | Type-2 | 0.870 | xlsx / xlsx | 0.35 | no | **True clone (type off)** | Two versions of the Anthropic `xlsx` skill (old vs new, line similarity 0.35): a real clone, but heavily edited, so Type-3 fits better than Type-2. |
| 19 | Type-2 | 0.997 | create-architectural-decision-record / create-architectural-decision-record | 0.99 | no | **True clone** | Same ADR skill; one sentence differs. |
| 20 | Type-3 | 0.705 | connect-chrome / plan-eng-review | 0.43 | yes | **Template sibling** | Different gstack skills (connect-chrome vs plan-eng-review) sharing the large gstack preamble. |
| 21 | Type-3 | 0.651 | s1disasm-guide / s3k-disasm-guide | 0.34 | yes | **True clone** | Sonic 1 guide adapted into a Sonic 3&K guide: same structure, game-specific content. Genuine copy-and-modify. |
| 22 | Type-3 | 0.677 | primefaces-menu / primefaces-button | 0.29 | yes | **Template sibling** | Different PrimeFaces component skills (menu vs button) from the same skill template. |
| 23 | Type-3 | 0.693 | refactorizar-screenplay-rest / crear-proyecto-base-rest | 0.13 | yes | **False positive** | Different tasks (refactor vs create project) in the same repo; shared Serenity/Screenplay vocabulary only (line similarity 0.13). |
| 24 | Type-3 | 0.668 | korus-ui-role-designer / korus-ui-orchestrator | 0.16 | yes | **False positive** | Different roles of one UI workflow (designer vs orchestrator); little shared text (0.16). |
| 25 | Type-3 | 0.655 | aif-plan / aif-improve | 0.08 | yes | **False positive** | Different commands of one toolkit (aif-plan vs aif-improve); 0.08 line similarity. |
| 26 | Type-3 | 0.835 | visual-audit / visual-audit | 0.89 | no | **True clone (type off)** | Same skill with the project renamed (Baryx -> Kipu); this is a parameterized clone just under the 0.85 threshold. |
| 27 | Type-3 | 0.835 | deepgram-java-speech-to-text / deepgram-java-audio-intelligence | 0.43 | yes | **Template sibling** | Sibling Deepgram SDK skills (speech-to-text vs audio intelligence) sharing structure and SDK boilerplate. |
| 28 | Type-3 | 0.835 | spring-junit / spring-testing | 0.14 | yes | **False positive** | Two different testing skills (JUnit vs Spring testing) in one repo; same topic, different text (0.14). |
| 29 | Type-3 | 0.696 | speckit-plan / speckit-analyze | 0.11 | no | **False positive** | Different spec-kit commands (plan vs analyze) in different repos; shared spec-kit vocabulary (0.11). |
