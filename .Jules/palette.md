## 2024-05-23 - Output Readability & Input Clarity
**Learning:** Users often confuse large text output areas for input fields in Streamlit if they aren't explicitly disabled. Collapsing large technical JSON blobs by default drastically improves the "Action Layer" visibility (the logs).
**Action:** Always set `disabled=True` for log/output text areas and wrap debugging JSON/Configs in `st.expander` by default.
