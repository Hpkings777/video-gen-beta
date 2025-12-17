## 2024-05-23 - Micro-UX: Tooltips & Read-Only Logs
**Learning:** Users often mistake log outputs for editable fields if they aren't explicitly disabled. Streamlit's `disabled=True` provides a clear visual cue (greyed out) that reinforces the system status nature of the output.
**Action:** Always set output-only text areas to `disabled=True` to prevent user frustration and clarify intent.
