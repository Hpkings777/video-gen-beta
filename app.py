import streamlit as st
import time
import json
from pvf_logic import JSONBuilder, renderer_stub

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="PVF Unbreakable Engine Demo",
    page_icon="🛡️",
    layout="wide"
)

# --- SIDEBAR ---
st.sidebar.title("🛡️ PVF Control Center")
st.sidebar.markdown("**Project: Bolt (Resilience Layer)**")

# Defaults
default_script = "The hero stands on the edge of the world. The wind howls through the silence. A decision is made."

# Style Preset
style_preset = st.sidebar.radio(
    "Style Preset",
    ("Dopamine_Spike", "Cinematic_Stoic")
)

# Script Input
script_input = st.sidebar.text_area(
    "Script Input",
    value=default_script,
    height=150,
    help="Enter the script text. The engine segments scenes based on periods."
)

# Failure Mode Switch
failure_mode_option = st.sidebar.selectbox(
    "System Failure Simulation",
    (
        "0. Normal Test (Layer 1 Fail -> Local Asset Success)",
        "1. Local Fallback Test (Layer 1 Fail -> Layer 2 Fail -> Procedural)",
        "2. Bhuchal Mode (Force Layer 3 Procedural)"
    )
)

# Extract the integer mode from the string
failure_mode = int(failure_mode_option.split(".")[0])

st.sidebar.markdown("---")
st.sidebar.info(
    "**Core Philosophy: Never Nothing.**\n"
    "Even if all external APIs and local files fail, "
    "the engine MUST produce a video."
)

# --- MAIN AREA ---

st.title("🛡️ PVF Unbreakable Engine")
st.markdown("### The 'Never Nothing' Rendering Pipeline")

if st.button("Generate Blueprint & Simulate Render", type="primary", use_container_width=True):

    # 1. Initialize Logic
    builder = JSONBuilder()

    # 2. Build Blueprint
    with st.spinner("Analyzing Script & Assembling Blueprint..."):
        blueprint = builder.build_blueprint(script_input, style_preset, failure_mode)

    # 3. Display Blueprint
    with st.expander("View JSON Blueprint (The Intent Layer)", expanded=False):
        st.code(json.dumps(blueprint, indent=4), language="json")

    # 4. Run Render Simulation
    st.subheader("Render Simulation Log (The Action Layer)")

    with st.spinner("Simulating Renderer..."):
        render_logs = renderer_stub(blueprint)

    st.text_area("Console Output", render_logs, height=400)

    # Visual Feedback based on mode
    if failure_mode == 0:
        st.success("✅ Render Complete (Normal Operation)")
    elif failure_mode == 1:
        st.warning("⚠️ Render Complete (Local Fallback Active)")
    else:
        st.error("🛡️ Render Complete (Bhuchal Mode: Maximum Resilience Active)")
