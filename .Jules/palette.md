## 2024-05-23 - [Reducing Cognitive Load in Demos]
**Learning:** Technical demos often overwhelm users with raw data. Hiding intermediate data structures (like JSON blueprints) behind an expander (`st.expander`) drastically reduces initial cognitive load while keeping the "under the hood" details accessible for those who want them.
**Action:** Always wrap large JSON blobs or debug info in collapsible elements. Use primary buttons (`type="primary"`) to guide the user to the single most important action.
