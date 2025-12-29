## 2025-02-14 - Collapsing Technical Detail
**Learning:**
Streamlit applications that target both technical and non-technical users often suffer from "data dump" fatigue.
I found that `st.expander` is not just for hiding optional information, but critical for managing cognitive load when displaying intermediate data structures (like JSON blueprints).
This allows the user to focus on the primary action (generating/rendering) and the primary output (the simulation log) without being overwhelmed by the internal state.

**Action:**
When building technical demos, always wrap intermediate JSON/XML/Debug outputs in `st.expander(expanded=False)` by default. This preserves the ability to debug ("The Intent Layer") without obstructing the primary workflow ("The Action Layer").
