import sys
import os

# Add root directory to sys.path
sys.path.append(os.getcwd())

from pvf_logic import AssetManager, JSONBuilder, renderer_stub
import json

def verify_bhuchal_mode():
    print("Verifying Bhuchal Mode (Mode 2)...")

    # 1. Setup
    builder = JSONBuilder()
    script_text = "Coffee is life."
    style_preset = "Dopamine_Spike"
    failure_mode = 2 # Force Layer 3

    # 2. Execute
    blueprint = builder.build_blueprint(script_text, style_preset, failure_mode)
    logs = renderer_stub(blueprint)

    # 3. Analyze Blueprint
    print("\n--- Blueprint Analysis ---")
    timeline = blueprint.get("timeline", [])
    if not timeline:
        print("FAIL: No timeline generated.")
        return

    segment = timeline[0]
    visual_asset = segment.get("visual_asset", {})
    global_audio = blueprint.get("global_audio", {})
    voiceover_asset = segment.get("audio_asset", {})

    print(f"Visual Source: {visual_asset.get('source')}")
    print(f"Visual Type: {visual_asset.get('type')}")
    print(f"Visual Text: {visual_asset.get('text')}")

    print(f"Global Audio Source: {global_audio.get('source')}")
    print(f"Global Audio Type: {global_audio.get('type')}")

    print(f"Voiceover Source: {voiceover_asset.get('source')}")
    print(f"Voiceover Type: {voiceover_asset.get('type')}")

    # 4. Assertions
    errors = []

    # Video Assertions
    if visual_asset.get("source") != "procedural":
        errors.append(f"Visual: Expected source 'procedural', got '{visual_asset.get('source')}'")
    if visual_asset.get("type") != "backup_generator::CRT_INTERFACE":
         errors.append(f"Visual: Expected type 'backup_generator::CRT_INTERFACE', got '{visual_asset.get('type')}'")
    if "SYSTEM FALLBACK" not in visual_asset.get("text", ""):
        errors.append("Visual: Expected system fallback text in asset data")

    # Music Assertions
    if global_audio.get("source") != "procedural":
        errors.append(f"Music: Expected source 'procedural', got '{global_audio.get('source')}'")
    if global_audio.get("type") != "Tension Soundscape":
        errors.append(f"Music: Expected type 'Tension Soundscape', got '{global_audio.get('type')}'")

    # Voiceover Assertions
    if voiceover_asset.get("source") != "procedural":
        errors.append(f"Voiceover: Expected source 'procedural', got '{voiceover_asset.get('source')}'")
    if voiceover_asset.get("type") != "Robotic Speech":
        errors.append(f"Voiceover: Expected type 'Robotic Speech', got '{voiceover_asset.get('type')}'")

    if errors:
        print("\nFAIL: Verification failed with errors:")
        for e in errors:
            print(f"- {e}")
    else:
        print("\nSUCCESS: Bhuchal Mode logic verified.")

    # 5. Check Logs
    print("\n--- Log Analysis ---")
    print(logs)

    # Basic Log Assertions
    log_errors = []
    if "Global Audio Track: Sine Wave Drone" not in logs:
        log_errors.append("Log: Missing Global Audio Track info")
    if "Rendering" not in logs and "Procedural backup_generator" not in logs:
        log_errors.append("Log: Missing Video Rendering info")
    if "[AUDIO] Voiceover: Basic TTS Fallback" not in logs:
        log_errors.append("Log: Missing Voiceover info")

    if log_errors:
        print("\nFAIL: Log verification failed:")
        for e in log_errors:
            print(f"- {e}")
    else:
        print("\nSUCCESS: Logs verified.")

if __name__ == "__main__":
    verify_bhuchal_mode()
