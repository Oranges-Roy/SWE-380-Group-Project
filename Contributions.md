### Individual Contribution Highlights
* **Roy**  Updated all documents for sprint 2 deliverables and designed the Sprint 3 roadmap for the interactive Streamlit user interface (`app.py`) and the external custom skill-checking feature.
* **Roshkrishna** Built `src/run_language_pipeline.py`, which runs the same method as the C++ pipeline (same SQL filter, SHA-based Type-1, TF-IDF settings and 0.85 / 0.65 thresholds) for any repository language, and used it to analyze Java, Python and Rust.
* **Roshkrishna** Scaled the pipeline to Python (1,657,440 skills, 769,920 distinct files): streamed extraction, compact pair storage, `--max-cells` and `--dry-run` options, with Java outputs verified byte-for-byte unchanged; ran the full Python analysis (8,065,074 similar pairs) on a 64 GB lab machine.
* **Roshkrishna** Manually reviewed the 30-pair validation samples for Java, Python and Rust (90 pairs): Type-2 pairs are mostly genuine clones (25 of 30), Type-3 pairs are mostly template siblings or topic overlap (4 of 30 genuine), and symlink stubs and unfetched content inflate Type-1.
* **Roshkrishna** Conducted database schema audit on `content_fetched` flags across C++ (30% null), Java (44% null), Python (57% null) and Rust (37% null) records; identified "Truly Unique" bucket inflation; verified validity of Type-1 SHA matches and high-similarity Type-2/3 pairs.
* **Roy** Pipeline architecture and vectorization implementation (`ingest_and_analyze.py`), pair inspection tool (`inspect_pair_content.py`), data dictionary definitions, and documentation framing. Ran these for the language C++
* **Roy** Created and managed backlog, Readme, and other important documentation including Contributions.md 
* **Roy** Created repo and Formatted it for the project
