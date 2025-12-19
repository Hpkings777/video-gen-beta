# Palette's Design Journal 🎨

## Design Philosophy
- Users notice the little things
- Accessibility is not optional
- Every interaction should feel smooth
- Good UX is invisible - it just works

## Journal Entries

## 2024-05-23 - Clean Result Presentation
**Learning:** Large technical outputs (like JSON blobs) in the main flow can overwhelm users and bury the actual results. Hiding them behind an expander by default respects the user's cognitive load while keeping the data accessible for debugging. Similarly, read-only logs should be explicitly disabled to prevent false affordances.
**Action:** Always wrap debug/technical outputs in `st.expander` and mark log outputs as `disabled=True`.
