## 2024-05-23 - Text Area as Log Viewer
**Learning:** In Streamlit, `st.text_area` defaults to editable, which is confusing for output logs. Users might try to type in it.
**Action:** Always set `disabled=True` when using `st.text_area` for displaying system logs or read-only content to reinforce its purpose and prevent user error.

## 2024-05-23 - Hiding Technical Details
**Learning:** Large JSON blobs or debug outputs can overwhelm the primary user interface.
**Action:** Use `st.expander` to hide technical "blueprint" data by default, allowing power users to inspect it without cluttering the view for standard users.
