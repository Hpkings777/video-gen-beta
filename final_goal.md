UNBREAKABLE ENGINE
Project Name: Phorix Video Framework (PVF) - Resilience Edition
Core Mission: 100% Guaranteed Output. Video render must complete, regardless of network failure, API key expiration, or missing local assets. Quality is allowed to degrade, but output must never be zero (The "Never Nothing" Principle).
Target Persona: Rapid prototyping and zero-cost, auditable demos.
I. 🛡️ PVF ARCHITECTURE: THE CASCADING DEFENSE
The system uses a Three-Layer Asset Resolution Model. The AssetManager proceeds sequentially. If Layer N fails, it automatically falls back to Layer N+1.
| Layer | Name | Source Reliability | Asset Cost | Output Quality |
|---|---|---|---|---|
| Layer 1 | The Dream (External) | Unstable (Network, API Key Risk) | High (Paid APIs) / Low (Free APIs) | Highest (4K, Cinematic) |
| Layer 2 | The Backup (Owned) | High (Local Filesystem) | Zero (Curated Downloads) | Medium (High-quality CC0 clips) |
| Layer 3 | The Bunker (Procedural) | Absolute (Code Logic) | Zero (Runtime Generation) | Lowest (Branded/Abstract) |
II. 🧱 THE RESILIENCE MATRIX (ASSET FALLBACK LOGIC)
The ultimate power of the PVF lies in how each asset type resolves its fallback in Layer 3.
| Asset Type | Layer 1 (Pexels API) | Layer 2 (Local) | Layer 3 (BHUCHAL MODE - MAX POWER) |
|---|---|---|---|
| Video Clips | Pexels clip_id:: fetched. | Local asset_id::V_00X found. | Procedural Glitch Screen: backup_generator::CRT_INTERFACE with animated binary text overlay. |
| Music Track | FMA audio_id:: fetched. | Local music_id::M_00Y found. | Tension Soundscape: Code-generated, low-frequency Sine Wave Drone to hold tension. |
| Voiceover | Basic TTS API call. | Local tts_ref::S_00Z found. | Robotic Speech: Local, self-hosted basic TTS (e.g., Festival/basic Python library) or, if that fails, Subtitled Text Only. |
| Overlay/Text | Dynamic (Based on Style Preset). | Static Text Overlay. | System Status Log: Forced text: [PROTOCOL OVERRIDE], [L3 ACTIVE], [DATA_MISSING]. (Looks like intentional status report). |
III. 💥 BHUCHAL MODE: MAX POWER DEFINITION
The goal of Layer 3 is to make the failure look like a high-tech, intentional system diagnostic interface, fulfilling the desire for intentional design.
| Feature | Design/Intent | Why it's powerful |
|---|---|---|
| Visuals | Branded Glitch Interface: Forced CRT scan lines, chromatic aberration effect, and a dark color palette. | It communicates failure, but with a unique, high-vibe aesthetic. It converts an error into a feature. |
| Pacing | Beat Detection: If music/audio fails, the visuals still pulse/flash based on the hardcoded beat map of the fallback sine wave. | The Dopamine pacing rules are upheld even without real music. |
| Text Layer | Status Text Injection: The script text is split and framed with error codes and system status updates. | Auditable Resilience: The video itself informs the user why the quality dropped. (e.g., "ASSET FAILURE: V_003"). |
| Audio | System Alert SFX: Simple, procedurally generated short beeps, ticks, and static bursts synced to the segment cuts. | Prevents the video from being silent and keeps the user engaged with low-cost feedback. |
IV. 💻 PRODUCTION-READY STACK (ZERO COST)
This stack ensures the PVF is deployable and testable without infrastructure cost or phishing risk.
| Component | Tool / Technology | Role in PVF |
|---|---|---|
| Backend & Logic | Python | Host the core AssetManager and JSONBuilder. |
| UI & App Server | Streamlit | Rapidly generate the user interface (Zero-cost frontend). |
| Deployment | Streamlit Community Cloud | Free public hosting for the demo/testing environment. |
| Rendering Engine | FFmpeg (Simulated) | Executes the final JSON blueprint (Self-hosted/Simulated for testing). |
Final Instruction for Jules: Build the Streamlit application (app.py) that allows users to test the Bhuchal Mode explicitly using a radio button, proving the 100% output guarantee via the rendered simulation log.
