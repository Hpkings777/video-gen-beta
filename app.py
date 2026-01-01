import streamlit as st
import json
from pvf_logic import JSONBuilder, renderer_stub

# Page Config
st.set_page_config(
    page_title="PVF: Unbreakable Engine Demo",
    layout="wide"
)

# Title
st.title("PVF: Unbreakable Engine Demo (Zero-Cost Resilience)")
st.markdown("""
This application demonstrates the **Zero-Failure PVF Engine**.
It showcases a cascading failure logic that prioritizes local assets and procedural generation over external dependencies.
""")

# --- SIDEBAR ---
st.sidebar.header("Configuration")

# Style Preset
style_preset = st.sidebar.radio(
    "Style Preset",
    ("Dopamine_Spike", "Cinematic_Stoic"),
    help="Select the aesthetic style for the generated video."
)

# Script Input
default_script = "Coffee is life. Energy flows through the veins. The world wakes up."
script_input = st.sidebar.text_area(
    "Script Input",
    value=default_script,
    height=150,
    help="Enter the text script. Use periods to segment the timeline."
)

# Failure Mode Switch
st.sidebar.markdown("---")
st.sidebar.subheader("FAILURE MODE SWITCH (CRITICAL)")
failure_mode_label = st.sidebar.radio(
    "Select Simulation Mode:",
    (
        "0. Normal Test (Layer 1 Fail -> Local Asset Success)",
        "1. Local Fallback Test (Layer 1 Fail -> Layer 2 Fail -> Procedural)",
        "2. Bhuchal Mode (Force Layer 3 Procedural)"
    ),
    help="Simulate different failure scenarios to test resilience."
)

# Map label to integer
failure_mode_map = {
    "0. Normal Test (Layer 1 Fail -> Local Asset Success)": 0,
    "1. Local Fallback Test (Layer 1 Fail -> Layer 2 Fail -> Procedural)": 1,
    "2. Bhuchal Mode (Force Layer 3 Procedural)": 2
}
failure_mode = failure_mode_map[failure_mode_label]


# --- MAIN AREA ---

if st.button("Generate Blueprint & Simulate Render", type="primary", use_container_width=True):

    # 1. Initialize Logic
    builder = JSONBuilder()

    # 2. Build Blueprint
    with st.spinner("Generating Unbreakable Blueprint..."):
        blueprint = builder.build_blueprint(script_input, style_preset, failure_mode)

    # 3. Display Blueprint
    with st.expander("JSON Blueprint (The Intent Layer)", expanded=False):
        st.code(json.dumps(blueprint, indent=4), language="json")

    # 4. Run Render Simulation
    st.subheader("Render Simulation Log (The Action Layer)")

    with st.spinner("Simulating Renderer..."):
        render_logs = renderer_stub(blueprint)

    st.text_area("Console Output", render_logs, height=400, disabled=True)

    # Visual Feedback based on mode
    if failure_mode == 0:
        st.success("Simulation Complete: Local Assets Successfully Utilized.")
    elif failure_mode == 1:
        st.warning("Simulation Complete: System fell back to Procedural Assets due to missing local files.")
    else:
        st.error("Simulation Complete: BHUCHAL MODE - Maximum Resilience Active.")

else:
    st.info("Configure settings in the sidebar and click 'Generate' to start.")
