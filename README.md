# GitSkills C++ Clone Detection & Analysis Pipeline

**Course:** SWE 380 / CSC 580  
**Sprint:** Sprint 1 — Research Framing & Data Foundation (Due: October 7, 2026)  
**Target Ecosystem:** C++ / `c++` Repositories (`agent_skills_release.db`)

---

## Executive Summary & Research Framing

* **Research Question (RQ):** Within C++ repositories, how are GitSkills artifacts (`SKILL.md`) reused and propagated, how do near-duplicate clones cluster across different clone types (Type-1, Type-2, Type-3), and which skill contents maintain the largest populations and star reach?
* **Unit of Analysis:** A single `SKILL.md` artifact occurrence within a public C++ repository.
* **Target Population & Sample:** Extracted from the `agent_skills_release.db` SQLite database by filtering for C++ projects (`LOWER(r.language) IN ('c++', 'cpp')`). This yields an initial sample of **10,737 skill occurrences** across C++ projects.

---

## Research Question

**Skill reuse and propagation (a combination of A1 and A5):**  
Our current research question is to match and rank skills for a specific language and determine their similarity. We plan to label them as clones, rank them by type, analyze their populations, and identify which ones are the most popular. 

*Inspired by the MSR 2027 Mining Challenge, implement a working mining or analysis pipeline, and produce evidence-based findings about AI-native software-engineering artifacts.*

---
## Scrum assignments
Roy- Oranges-Roy **Product owner/Scrum Master**

**Developers/Contributors**

Roshkrishna- _Lucifix_ 

William-

Pranjal-

---
## Steps to Reproduce Findings

1. Download `agent_skills_release.db` from [Zenodo](https://zenodo.org/records/21875637).
2. Place the file in a manageable directory.
3. Run the extractor script `git_cpp_skill_extractor.py` and paste the file path for `agent_skills_release.db` into the terminal when prompted.
4. `git_cpp_skill_extractor.py` outputs `extracted_skills_sample.csv`, containing 10,737 skills.
5. Run `src/ingest_and_analyze.py`, which processes `extracted_skills_sample.csv` and outputs clone types.

### Pipeline Execution Details (`src/ingest_and_analyze.py`)

`src/ingest_and_analyze.py` serves as the core execution pipeline for detecting duplicate and similar `SKILL.md` records within C++ repositories. It operates through the following steps:

* **Flexible Path Resolution:** Interactively prompts for the extracted C++ skills CSV (`extracted_skills_sample.csv`), automatically resolving paths across local directories, quotation styles, or `data/` / `results/` subfolders.
* **Type-1 Clone Extraction:** Performs verbatim match analysis by grouping records with identical SHA hashes (`file_sha`) to generate exact duplicate pairs.
* **TF-IDF & Cosine Similarity Analysis:** Vectorizes distinct skill contents using TF-IDF and computes pairwise cosine similarity scores ($\ge 0.65$) to classify near-duplicates into:
  * **Type-2 (Parameterized):** Similarity score of $0.85$ or higher.
  * **Type-3 (Semantic):** Similarity score between $0.65$ and less than $0.85$.
# Methodology: Threshold Selection & Rationalization

# Purely based our reasoning  on established software engineering literature and empirical TF-IDF vector properties: 

## 1. Overview of Metric & Lexical Properties
In text-based clone detection, term frequency-inverse document frequency (TF-IDF) vectorization combined with cosine similarity measures lexical and token-level overlap across skill documents. Because TF-IDF penalizes common, ubiquitous words while heavily weighting unique domain terminology, cosine similarity serves as a reliable proxy for structural and functional alignment.

---

## 2. Threshold Justifications

### Type-2 Clones (Parameterized) — Similarity $\ge 0.85$
A cosine similarity threshold of **$0.85$ or higher** requires near-total lexical alignment across the entire document. 

* **Characteristics:** At or above $0.85$, the core instructional body, structural workflow, and Markdown headings remain identical between the two skills.
* **Permissible Variance:** Differences in this tier are strictly limited to parameterized values, localized variables, environment file paths, or platform adapter tags (e.g., `<codex_skill_adapter>` vs. `<cursor_skill_adapter>`).
* **Interpretation:** Skills scoring $\ge 0.85$ represent true parameterized clones where a single base template was adapted for different platforms or execution environments.

### Type-3 Clones (Semantic Near-Duplicates) — $0.65 \le \text{Similarity} < 0.85$
A lower bound of **$0.65$** was established for Type-3 semantic clones to isolate functional intent from coincidental structural boilerplate.

* **Noise Floor Suppression:** Cosine similarity scores below $0.65$ frequently capture accidental token overlap between completely unrelated skills (e.g., standard Markdown formatting elements, common English stop words, or identical YAML front-matter keys like `name:`, `description:`, or `version:`).
* **Functional Alignment:** Setting $0.65$ as the baseline floor ensures that pairs flagged as Type-3 share meaningful domain vocabulary and conceptual purpose rather than superficial template formatting.

---

## 3. Empirical Calibration & Validation Protocol

These threshold cutoffs were initially selected as standard baseline heuristics and were subsequently evaluated through empirical sampling:

1. **Stratified Sampling:** We extracted a **30-pair balanced validation sample** (15 Type-2 pairs, 15 Type-3 pairs) from the pipeline output using `src/inspect_pair_content.py`.
2. **Manual Inspection:** Each pair was manually audited to compare raw document contents side-by-side.
3. **Key Finding & Calibration Value:** This manual inspection directly led to our discovery of empty-template false positives (`content_fetched = 0` / unfetched records). While unfetched records yielded all-zero vectors that artificially skewed uniqueness metrics, verifying the non-empty records confirmed that $0.85$ and $0.65$ accurately distinguish parameterized variants from broader semantic clones without introducing false positives from generic boilerplate.

---

## 4. Summary Table

| Clone Tier | Similarity Threshold | Lexical Alignment | Primary Differences |
| :--- | :--- | :--- | :--- |
| **Type-1 (Verbatim)** | `SHA-1 Match` | $100\%$ Exact Byte Match | None (Identical files) |
| **Type-2 (Parameterized)** | $\text{Score} \ge 0.85$ | Near-Total Overlap | Parameter values, adapters, paths, line endings |
| **Type-3 (Semantic)** | $0.65 \le \text{Score} < 0.85$ | Moderate–High Overlap | Rephrased instructions, alternate domain logic |
| **Truly Unique** | $\text{Score} < 0.65$ | Low / Noise Floor | Distinct functionality; overlap limited to syntax |



  
* **Automated Exporting:** Generates three structured output files in the `results/` folder:
  * `cpp_similar_pairs.csv`: Full catalog of identified similarity pairs.
  * `top10_similar_pairs.csv`: Top 10 highest-similarity clone pairs sorted by score.
  * `validation_sample_30.csv`: A balanced 30-pair stratified sample (10 Type-1, 10 Type-2, 10 Type-3) used for manual inspection and threshold calibration.

6. Run `inspect_pair_content.py`, which uses `validation_sample_30.csv` and `extracted_skills_sample.csv` to visually display the extracted pair content. *(This step revealed the primary threat to validity noted in [THREATS_TO_VALIDITY.md](THREATS_TO_VALIDITY.md))*
