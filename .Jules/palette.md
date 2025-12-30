## 2024-05-23 - Collapsing Cognitive Load
**Learning:**
Displaying raw JSON and verbose logs by default overwhelms users, making the "happy path" harder to see. Users focus better when technical details are optional (collapsed) and logs are clearly read-only (disabled).

**Action:**
Always wrap technical debug outputs (JSON, large dicts) in `st.expander(..., expanded=False)`. Explicitly disable text areas meant for logging to prevent user confusion about editability.
