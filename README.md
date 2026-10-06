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

## Steps to Reproduce Findings

1. Download `agent_skills_release.db` from [Zenodo](https://zenodo.org/records/21875637).
2. Place the file in a manageable directory.
3. Run the extractor script `git_cpp_skill_extractor.py` and paste the file path for `agent_skills_release.db` into the terminal when prompted.
4. `git_cpp_skill_extractor.py` outputs `extracted_skills_sample.csv`, containing 10,737 skills.
5. Run `src/ingest_and_analyze.py`, which processes `extracted_skills_sample.csv` and outputs clone types.

### Pipeline Execution Details (`src/ingest_and_analyze.py`)

`src/ingest_and_analyze.py` serves as the core execution pipeline for detecting duplicate and similar `SKILL.md` records within C++ repositories. It operates through the following steps:

* **Flexible Path Resolution:** Interactively prompts for the extracted C++ skills CSV (`extracted_skills_sample.csv`), automatically resolving paths across local directories, quotation styles, or `data/` / `results/` subfolders.
* **Type-1 Clone Extraction:** Performs verbatim match analysis by grouping records with identical SHA hashes (`file_
