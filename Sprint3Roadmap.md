## Key Deliverables & Features

### 1. Interactive Web Dashboard (`app.py`)
* **Goal:** Provide a visual, user-friendly interface to explore clone distributions and similarity metrics without needing to run command-line scripts.
   Streamlit (chosen for rapid Python-based UI development and interactive charting).
* **Core UI Components:**
  * **Language Selector Dropdown:** Switch between Python, C++, and other mined languages.
  * **Interactive Sliders:** Adjust similarity thresholds dynamically (e.g., tweaking Type-2 $\ge 0.85$ and Type-3 $0.65\text{--}0.84$ cutoffs).
  * **Visual Dashboards:** Render clone distribution charts and top similar pairs directly in the browser.

### 2. External Skill Checker ("Bring Your Own Skill")
* **Goal:** Enable developers to evaluate custom or external `SKILL.md` files against the pre-computed database (`agent_skills_release.db`).
* **Workflow:**
  1. **Upload/Input:** User uploads or pastes a custom `SKILL.md` file into the UI (or passes it via CLI).
  2. **Vectorization:** The script tokenizes and vectorizes the input file using the same TF-IDF vectorizer model configuration from our pipeline.
  3. **Cosine Similarity Matching:** Computes similarity scores against the existing corpus.
  4. **Classification Output:** Returns whether the external skill is a **Type-1 Exact Match**, **Type-2 Parameterized Clone**, **Type-3 Semantic Near-Duplicate**, or **Truly Unique**.
---
