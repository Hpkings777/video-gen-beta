## 2024-05-23 - [Reducing Cognitive Load in Technical Demos]
**Learning:** In technical demos, showing raw data (like JSON) is crucial for trust but overwhelming for UX. Hiding it behind an `expander` by default keeps the focus on the "action" (visual simulation) while still allowing deep-dive inspection.
**Action:** When displaying intermediate data structures in future tools, always wrap them in `st.expander` unless they are the primary output.
