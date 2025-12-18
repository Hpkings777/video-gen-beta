## 2024-05-23 - [Streamlit Log Display]
**Learning:** Users often mistake `st.text_area` for an input field when it's used for logs, causing confusion when they try to edit it.
**Action:** Always set `disabled=True` for read-only log outputs in Streamlit to enforce the "Output Only" mental model.

## 2024-05-23 - [Technical Detail Disclosure]
**Learning:** Displaying large JSON blobs by default creates visual noise and pushes primary content (like logs) below the fold.
**Action:** Wrap technical details like blueprints in `st.expander` (default collapsed) to keep the interface clean while keeping data accessible.
