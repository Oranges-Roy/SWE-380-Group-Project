## Group Motivation & Practical Impact



While this repository fulfills our course project deliverables, our research is driven by two broader motivations that sit at the intersection of modern empirical software engineering and open-source ethics:



---



### 1. Direct Alignment with the MSR 2027 Research Agenda

Our work directly contributes to the research directions established by the **24th International Conference on Mining Software Repositories (MSR 2027) Mining Challenge**. 



By analyzing the newly released **GitSkills** dataset, we are studying the rapid emergence of **AI-native software artifacts**—natural-language instructions (`SKILL.md` files) that dictate how AI coding agents execute complex engineering tasks. Traditional software engineering relies on package managers (`npm`, `pip`, `vcpkg`) to track code lineage and dependency chains. AI skills, however, spread organically across public repositories through copy-paste adaptation without formal dependency management.



**Our Research Contribution:** We are building an open-source, fully reproducible mining pipeline that creates **clone genealogies, by using TF-IDF lexical thresholds, and natural-language code metrics** for AI-native artifacts. This provides a foundational, empirical baseline for future researchers studying agentic software engineering ecosystems.


---



### 2. Safeguarding Original Content & Author Attribution

Beyond raw dataset metrics, our team is passionate about **intellectual provenance and developer credit** in the age of generative AI. 



As AI tools proliferate, original human-authored prompt strategies, domain workflows, and skill implementations are frequently copied, adapted, or re-wrapped without attribution. By establishing rigorous clone detection techniques (separating verbatim Type-1 copies, parameterized Type-2 adaptations, and semantic Type-3 near-duplicates), our pipeline helps answer critical questions regarding content:

**Distinguishing Value from Noise:** How do we isolate original, highly customized domain logic from generic, automated template boilerplate?
**Promoting Fair Attribution:** How can we trace adapted skills back to their original creators so open-source contributors receive proper credit for their foundational work?


Ultimately, we hope this pipeline contributes to a future where open-source AI artifacts remain transparent, traceable, and ethically credited across the software engineering community. 
