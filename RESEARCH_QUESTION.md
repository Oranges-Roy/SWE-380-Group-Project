# Research Question & Framing: Skill Reuse & Propagation

## Primary Research Question
What we ended up coming up with for our research question:
**Research Question A1: Skill reuse and propagation (a combination of A1 and A5)**  
Our current research question is to match and rank skills for a specific language and determine their similarity. We plan to label them as clones, rank them by type, analyze their populations, and identify which ones are the most popular.

## Our specific analytical objectives are to:
1. **Match & Rank Artifacts:** Ingest raw skill records from `agent_skills_release.db` and compute lexical similarity across language corpora.
2. **Clone Classification:** Categorize artifact relationships into rigorous tiers:
   * **Type-1 (Verbatim Clones):** Exact byte matches (`file_sha`).
   * **Type-2 (Parameterized Clones):** Near-total lexical overlap ($\text{Score} \ge 0.85$) with variances limited to paths, variables, or platform adapter tags.
   * **Type-3 (Semantic Near-Duplicates):** Moderate overlap ($0.65 \le \text{Score} < 0.85$) capturing shared functional intent above the noise floor.
   * **Truly Unique:** Distinct implementations ($\text{Score} < 0.65$).
3. **Population & Popularity Analysis:** Quantify clone distribution shares, content breakdown hygiene (filtering empty templates and symlink stubs), and aggregate repository popularity (star reach and copy counts).

## Key Variables & Metrics

- **Unit of Analysis:** A single `SKILL.md` artifact occurrence within a public repository.
- **Independent Variables:** Repository programming language (`language`), file content hash (`file_sha`), and TF-IDF cosine similarity score.
- **Dependent / Outcome Measures:**
  * **Copy Count / Frequency:** Number of occurrences or repository instances sharing content signatures.
  * **Star Reach:** Aggregate GitHub stargazers of host repositories.
  * **Clone Category Distribution:** Percentage share of occurrences classified under Type-1, Type-2, Type-3, and Unique tiers.
