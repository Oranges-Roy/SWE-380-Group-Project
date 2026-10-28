# GitSkills Multi-Language Clone Detection & Analysis Pipeline

**Course:** SWE 380 / CSC 580  
**Ecosystem:** GitSkills / `agent_skills_release.db` (`SKILL.md` artifacts across Python, C++, Java, JS/TS, Go, Rust, C#)  
**Sprint:** Sprint 2 — Multi-Language Scaling, Validation & Pipeline Verification

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

1. **Download the Database:** Download `agent_skills_release.db` from [Zenodo](https://zenodo.org/records/21875637) (DOI: `10.5281/zenodo.21875637`).
2. **Place the Database:** Move the file into your local project directory or a designated data folder.
3. **Execute the Multi-Language Pipeline:** Run `run_language_pipeline.py`

### Pipeline Execution Details (`run_language_pipeline.py`)

`run_language_pipeline.py` serves as the core execution engine for detecting duplicate and similar `SKILL.md` records across multi-language repository ecosystems. It operates through the following steps:

- **Chunked Database Extraction & Filtering:** Streams query results from `agent_skills_release.db` in configurable chunks (default: 50,000 rows) to prevent out-of-memory errors on large ecosystems like Python or JavaScript. It automatically flags unfetched content (`content_fetched = 0`) and filters Git symlink stubs (`looks_like_symlink`) to eliminate non-functional noise prior to vectorization.
- **Type-1 Clone Extraction:** Performs verbatim match analysis by grouping records with identical SHA hashes (`file_sha`) to generate exact duplicate pairs.
- **Chunked TF-IDF & Cosine Similarity Analysis:** Constructs a memory-efficient sparse TF-IDF matrix over distinct content SHAs only (using English stop-word removal) and computes pairwise cosine similarity scores via matrix multiplication (`X @ XT`) in controlled memory blocks (`--max-cells`) to classify near-duplicates into:
  - **Type-2 (Parameterized):** Similarity score of $0.85$ or higher (representing near-total lexical alignment with variance limited to parameters, paths, or platform adapter tags).
  - **Type-3 (Semantic):** Similarity score between $0.65$ and less than $0.85$ (capturing shared functional intent above the lexical noise floor).
- **Automated Exporting & Validation Sampling:** Generates complete metric catalogs, sorted top-10 similarity lists, content breakdown audits, distribution plots, and a balanced **30-pair stratified validation sample** (`validation_sample_30.csv`) for manual inspection via `src/inspect_pair_content.py`.
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

1. **Stratified Sampling:** We extracted a balanced validation sample (covering Type-2 and Type-3 pairs) from the pipeline output using `src/inspect_pair_content.py`.
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


## 5.**Automated Exporting & Outputs:**
  
- **Automated Exporting & Outputs:** Generates a complete suite of structured files within the language-specific output directory (`results/<lang>/`):
  * `extracted_skills_<lang>.csv`: Streamed dataset metadata and extracted content.
  * `<lang>_type1_pairs.csv`: Full catalog of exact byte-match SHA pairs.
  * `<lang>_similar_pairs.csv`: Full catalog of identified Type-2 and Type-3 similarity pairs.
  * `top10_similar_pairs.csv`: Top 10 highest-similarity clone pairs sorted deterministically by score.
  * `validation_sample_30.csv`: A balanced 30-pair stratified sample used for manual inspection and threshold calibration.
  * `clone_distribution.csv` & `content_breakdown.csv`: Summary tables and audits tracking data hygiene (such as unfetched records and symlink stubs).
  * `<lang>_clones.png`: High-resolution distribution bar chart visualizing ecosystem breakdown.

6. **Manual Inspection via `inspect_pair_content.py`:** Run script utilities to visually display and audit extracted pair contents. *(Empirical reviews using this script revealed key dataset insights regarding template boilerplate and unfetched content, directly informing our [THREATS_TO_VALIDITY.md](THREATS_TO_VALIDITY.md) evaluation).*
## Pipeline Architecture & Execution

The Sprint 2 unified pipeline (`run_language_pipeline.py`) replaces single-language scripts with a scalable, chunked architecture capable of processing large language corpora without out-of-memory errors.
