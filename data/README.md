# GitSkills Data Dictionary (`agent_skills_release.db`) 

This document provides a comprehensive data dictionary for the full `agent_skills_release.db` SQLite database, containing all 4 core tables: `artifacts`, `repos`, `artifact_siblings`, and `mining_runs`.

---

## 1. `artifacts` Table
**Total Records:** 3,797,117 rows  
**Description:** Contains one record for every discovered `SKILL.md` file occurrence across public GitHub repositories.

| Column Name | Data Type | Key Constraint | Description |
| :--- | :--- | :--- | :--- |
| `repo_full_name` | `TEXT` | **Primary Key (1/2)** | Repository name in `owner/repo` format |
| `path` | `TEXT` | **Primary Key (2/2)** | Relative path to the file within the repository |
| `filename` | `TEXT` | — | Exact basename of the file as returned by code search (case-preserved) |
| `location_class` | `TEXT` | — | Location classification: `canonical` (`.claude/skills/<name>/SKILL.md`), `skills-dir` (under a `skills/` directory), or `other` |
| `file_sha` | `TEXT` | — | Git blob hash of the content (identical hashes represent identical byte contents) |
| `discovered_at` | `TEXT` | — | ISO-8601 UTC timestamp when recorded during collection |
| `dedup_primary` | `INTEGER` | — | `1` for the single representative instance of a distinct content group; `0` for duplicate copies |
| `content` | `TEXT` | — | Full text payload of `SKILL.md` (populated for representative records where `dedup_primary = 1`, `NULL` otherwise) |
| `content_fetched` | `INTEGER` | — | Retrieval status flag (bookkeeping) |
| `content_sha_ok` | `INTEGER` | — | Content verification status (`1` = downloaded bytes match `file_sha`, `2` = repaired via blob API) |
| `frontmatter_valid` | `INTEGER` | — | `1` if YAML front matter was validly parsed; `0` otherwise |
| `name` | `TEXT` | — | Skill name parsed from YAML front matter |
| `description` | `TEXT` | — | Skill description parsed from YAML front matter |
| `body_chars` | `INTEGER` | — | Total character count of the body text |
| `sibling_count` | `INTEGER` | — | Count of sibling files and folders bundled in the skill directory |
| `sibling_bytes` | `INTEGER` | — | Total aggregate size in bytes of all bundled sibling files |
| `has_scripts` | `INTEGER` | — | `1` if folder contains executable scripts/code; `0` otherwise |
| `has_references` | `INTEGER` | — | `1` if folder contains reference/documentation files; `0` otherwise |
| `composition_fetched` | `INTEGER` | — | Folder listing fetch status flag (bookkeeping) |
| `composition_truncated` | `INTEGER` | — | `1` if folder item count exceeds the listing cap; `0` otherwise |
| `first_commit_at` | `TEXT` | — | ISO-8601 UTC timestamp of first commit for file at current path |
| `last_commit_at` | `TEXT` | — | ISO-8601 UTC timestamp of last commit for file at current path |
| `commit_count` | `INTEGER` | — | Total commit count for file at current path |
| `first_commit_author` | `TEXT` | — | Anonymized author identifier code for first commit |
| `last_commit_author` | `TEXT` | — | Anonymized author identifier code for last commit |
| `first_commit_author_type` | `TEXT` | — | Account type (`User`, `Bot`, `Organization`, or empty) |
| `last_commit_author_type` | `TEXT` | — | Account type (`User`, `Bot`, `Organization`, or empty) |
| `first_commit_message` | `TEXT` | — | First commit message with personal names and emails masked |
| `last_commit_message` | `TEXT` | — | Last commit message with personal names and emails masked |
| `history_fetched` | `INTEGER` | — | Commit history fetch status flag (bookkeeping) |

---

## 2. `repos` Table
**Total Records:** 282,200 rows  
**Description:** Metadata for every public GitHub repository present in the dataset.

| Column Name | Data Type | Key Constraint | Description |
| :--- | :--- | :--- | :--- |
| `full_name` | `TEXT` | **Primary Key** | Repository name in `owner/repo` format |
| `owner` | `TEXT` | — | Repository owner login name or ID |
| `stars` | `INTEGER` | — | GitHub stargazer count |
| `forks` | `INTEGER` | — | GitHub fork count |
| `is_fork` | `INTEGER` | — | `1` if repository is a fork; `0` otherwise |
| `language` | `TEXT` | — | Primary programming language of the repository (e.g., `C++`, `Python`) |
| `license` | `TEXT` | — | Open-source license identifier |
| `description` | `TEXT` | — | Repository description with personal information masked |
| `created_at` | `TEXT` | — | ISO-8601 UTC repository creation timestamp |
| `pushed_at` | `TEXT` | — | ISO-8601 UTC timestamp of last push to repository |
| `metadata_fetched` | `INTEGER` | — | Metadata retrieval status flag (bookkeeping) |

---

## 3. `artifact_siblings` Table
**Total Records:** 7,264,865 rows  
**Description:** Stores individual script and reference files stored alongside representative skill artifacts.

| Column Name | Data Type | Key Constraint | Description |
| :--- | :--- | :--- | :--- |
| `repo_full_name` | `TEXT` | — | Repository name hosting the representative skill |
| `path` | `TEXT` | — | Relative path to the sibling file within the repository |
| `skill_path` | `TEXT` | — | Relative path of parent `SKILL.md` artifact |
| `file_sha` | `TEXT` | — | Git blob hash of sibling file content |
| `size_bytes` | `INTEGER` / `TEXT` | — | Sibling file size in bytes |
| `is_binary` | `INTEGER` | — | `1` if binary file; `0` if text file |
| `content` | `TEXT` | — | File contents (populated for text siblings under threshold) |

---

## 4. `mining_runs` Table
**Total Records:** 7 rows  
**Description:** Collection logs and provenance tracking for dataset mining runs.

| Column Name | Data Type | Key Constraint | Description |
| :--- | :--- | :--- | :--- |
| `run_id` | `INTEGER` / `TEXT` | **Primary Key** | Unique identifier for collection run |
| `started_at` | `TEXT` | — | ISO-8601 UTC timestamp when run started |
| `completed_at` | `TEXT` | — | ISO-8601 UTC timestamp when run completed |
| `target_query` | `TEXT` | — | Search query parameter used during mining pass |
| `total_discovered` | `INTEGER` | — | Aggregate count of artifacts collected in the run |
