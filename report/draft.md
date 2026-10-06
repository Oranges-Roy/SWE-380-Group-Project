## Current Findings/Sprint 1 report

> **Note:** The metrics presented below reflect preliminary findings based on initial threshold configurations and baseline dataset parsing. These numbers are subject to refinement in future project iterations as pre-processing filters and threshold calibrations are updated.

Our initial evaluation identified **10,737 C++ skill file occurrences** within the dataset[cite: 5].

### Clone Type Distribution

| Clone Type | Count | Share (%) |
| :--- | :--- | :--- |
| **Type-1 (Verbatim)** | 3,147 | 29.3% |
| **Type-2 (Parameterized)** | 709 | 6.6% |
| **Type-3 (Semantic)** | 914 | 8.5% |
| **Unique Skills** | 5,967 | 55.6% |
| **Total** | **10,737** | **100.0%** |

I want to address the threats to validity by doing some pre processing to the initial dataset and see what is causing the false positives. As SKILL.md is missing or blank potentially creating more clones than there actually are.  
Then repopulate current .csv datasets and create our ranking, skill clone populations, and test data again. 
