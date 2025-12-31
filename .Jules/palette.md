## 2024-05-22 - Collapsing Technical Artifacts for Cognitive Load
**Learning:** Exposing raw JSON blueprints by default overwhelmed the user and distracted from the primary "action" logs. Users care more about the result (the render) than the intermediate data structure (the blueprint).
**Action:** Wrap technical/intermediate artifacts (like JSON, XML, or config dumps) in collapsed-by-default containers (e.g., `st.expander(expanded=False)`) to keep the primary interface clean while maintaining accessibility for debugging.
