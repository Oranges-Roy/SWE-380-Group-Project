# Python — manual review of validation_sample_30.csv

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

- **Type-1:** True clone 7, No content 3
- **Type-2:** True clone 5, Template sibling 4, True clone (type off) 1
- **Type-3:** Template sibling 8, Placeholder 1, False positive 1

"Line sim." is difflib's line-level similarity of the two texts (1.0 = same lines);
it is shown to help judge pairs and is not part of the pipeline.

## Pairs

| # | Type | Score | Skill(s) | Line sim. | Same repo | Verdict | Reason |
|---|---|---|---|---|---|---|---|
| 0 | Type-1 | 1.000 | [Unnamed Skill] | 1.00 | – | **True clone** | Full 16k-char shadcn skill; 100 identical copies across 55 repos. |
| 1 | Type-1 | 1.000 | [Unnamed Skill] | 1.00 | – | **True clone** | Full 10k-char docstring skill; 24 copies across 22 repos. |
| 2 | Type-1 | 1.000 | [Unnamed Skill] | – | – | **No content** | Content never fetched; SHA match only. |
| 3 | Type-1 | 1.000 | [Unnamed Skill] | 1.00 | – | **True clone** | Full 6.7k-char malware-analyst skill; 14 copies across 11 repos. |
| 4 | Type-1 | 1.000 | [Unnamed Skill] | – | – | **No content** | Content never fetched; SHA match only. |
| 5 | Type-1 | 1.000 | [Unnamed Skill] | 1.00 | – | **True clone** | Full 7.3k-char skill; 9 copies across 3 repos. |
| 6 | Type-1 | 1.000 | [Unnamed Skill] | 1.00 | – | **True clone** | Full 3.4k-char skill; identical in 2 repos. |
| 7 | Type-1 | 1.000 | [Unnamed Skill] | 1.00 | – | **True clone** | Full 8.1k-char skill; 43 copies across 26 repos. |
| 8 | Type-1 | 1.000 | [Unnamed Skill] | – | – | **No content** | Content never fetched; SHA match only. |
| 9 | Type-1 | 1.000 | coordinator-orchestration | 1.00 | – | **True clone** | Full 13.8k-char skill; 2 identical copies in one repo. |
| 10 | Type-2 | 0.936 | using-git-worktrees / using-git-worktrees | 0.87 | no | **True clone** | Same skill; one adds a Chinese tag and drops a section. |
| 11 | Type-2 | 0.899 | upcycling-repair-alteration / employment-creatives-fashion | 0.88 | yes | **Template sibling** | Two different German fashion-law skills generated from one template; topic words swapped. |
| 12 | Type-2 | 0.975 | webapp-testing / webapp-testing | 0.75 | no | **True clone** | Two versions of the Anthropic `webapp-testing` skill; wording edits. |
| 13 | Type-2 | 0.852 | protocol-reverse-engineering-v2 / security-requirement-extraction-v2 | 0.90 | yes | **Template sibling** | Two different skills wrapped in the same awesome-omni-skills packaging template. |
| 14 | Type-2 | 0.914 | covenant-waiver-crr-crd-kapitalanforderungen / zag-ausnahmen-limited-network-commercial-agent | 0.87 | yes | **Template sibling** | Two different German banking-law skills from one template; different legal content. |
| 15 | Type-2 | 0.937 | [Unnamed Skill] / microservices-patterns | 0.80 | no | **True clone** | Same microservices-patterns text; one adds YAML front matter. |
| 16 | Type-2 | 0.910 | swiftui-expert-skill / swiftui-expert-skill | 0.29 | no | **True clone (type off)** | Two versions of `swiftui-expert-skill` (line similarity 0.29): a real clone, heavily diverged; Type-3 fits better. |
| 17 | Type-2 | 0.998 | x-twitter-growth / x-twitter-growth | 0.99 | no | **True clone** | Same skill; one adds an author and permissions section. |
| 18 | Type-2 | 0.996 | linux-privilege-escalation / linux-privilege-escalation | 0.98 | no | **True clone** | Same skill; front-matter fields reformatted. |
| 19 | Type-2 | 0.874 | gute-wissenschaftliche-praxis / promotion-promotionsordnung | 0.81 | yes | **Template sibling** | Two different German university-law skills from one template. |
| 20 | Type-3 | 0.697 | [Unnamed Skill] / [Unnamed Skill] | 0.13 | no | **Placeholder** | Both are placeholder stubs (`[skill-name]` template vs `# Skill 1 / Description of Skill 1`); no real content. |
| 21 | Type-3 | 0.660 | [Unnamed Skill] / [Unnamed Skill] | 0.88 | yes | **Template sibling** | Auto-generated openclaw stubs (ignore-rust vs prometheus-monitoring); identical skeleton, name swapped. |
| 22 | Type-3 | 0.735 | [Unnamed Skill] / [Unnamed Skill] | 0.88 | yes | **Template sibling** | Auto-generated openclaw stubs (tailwind-css vs api-testing); identical skeleton. |
| 23 | Type-3 | 0.675 | [Unnamed Skill] / project-session-management | 0.02 | yes | **False positive** | Different skills (project workflow vs session management) in one repo; 0.02 line similarity. |
| 24 | Type-3 | 0.691 | analytics-tracking-v3 / screen-reader-testing | 0.33 | yes | **Template sibling** | Different skills in the awesome-omni-skills packaging template (analytics vs screen-reader testing). |
| 25 | Type-3 | 0.665 | c-pro-v2 / makepad-dsl | 0.54 | yes | **Template sibling** | Different skills in the awesome-omni-skills template (C vs Makepad DSL). |
| 26 | Type-3 | 0.818 | [Unnamed Skill] / [Unnamed Skill] | 0.84 | yes | **Template sibling** | Generated 'skill factory' files (hardware_optics_067 vs future_research_147); only IDs and coordinates differ. |
| 27 | Type-3 | 0.671 | fp-pipe-ref / code-documentation-doc-generate-v2 | 0.55 | yes | **Template sibling** | Different skills in the awesome-omni-skills template (fp-ts pipe vs doc generation). |
| 28 | Type-3 | 0.668 | agent-manager-skill / vulnerability-scanner-v3 | 0.40 | yes | **Template sibling** | Different skills in the awesome-omni-skills template (agent manager vs vulnerability scanner). |
| 29 | Type-3 | 0.652 | wiki-changelog / quant-analyst | 0.82 | yes | **Template sibling** | Generated marketplace registry entries (wiki-changelog vs quant-analyst); same skeleton. |
