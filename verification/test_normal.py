import sys
import os

# Add root directory to sys.path
sys.path.append(os.getcwd())

from pvf_logic import AssetManager, JSONBuilder, renderer_stub
import json

def verify_normal_mode():
    print("Verifying Normal Mode (Mode 0)...")

    # 1. Setup
    builder = JSONBuilder()
    script_text = "Coffee is life."
    style_preset = "Dopamine_Spike"
    failure_mode = 0 # Normal Test (Layer 2 Success)

    # 2. Execute
    blueprint = builder.build_blueprint(script_text, style_preset, failure_mode)
    logs = renderer_stub(blueprint)

    # 3. Analyze Blueprint
    print("\n--- Blueprint Analysis ---")
    timeline = blueprint.get("timeline", [])
    segment = timeline[0]
    visual_asset = segment.get("visual_asset", {})
    global_audio = blueprint.get("global_audio", {})
    voiceover_asset = segment.get("audio_asset", {})

    print(f"Visual Source: {visual_asset.get('source')}")
    print(f"Visual Path: {visual_asset.get('path')}")

    print(f"Global Audio Source: {global_audio.get('source')}")
    print(f"Global Audio Path: {global_audio.get('path')}")

    print(f"Voiceover Source: {voiceover_asset.get('source')}")
    print(f"Voiceover Path: {voiceover_asset.get('path')}")

    # 4. Assertions
    errors = []

    if visual_asset.get("source") != "local":
        errors.append(f"Visual: Expected source 'local', got '{visual_asset.get('source')}'")
    if "COFFEE" not in visual_asset.get("path", ""):
        errors.append("Visual: Expected 'COFFEE' in path")

    if global_audio.get("source") != "local":
        errors.append(f"Music: Expected source 'local', got '{global_audio.get('source')}'")
    # Updated expectation: Logic upcases description, so Dopamine_Spike -> DOPAMINE_SPIKE
    if "DOPAMINE_SPIKE" not in global_audio.get("path", ""):
        errors.append("Music: Expected 'DOPAMINE_SPIKE' in path")

    if voiceover_asset.get("source") != "local":
        errors.append(f"Voiceover: Expected source 'local', got '{voiceover_asset.get('source')}'")
    if "VO_" not in voiceover_asset.get("path", ""):
        errors.append("Voiceover: Expected 'VO_' in path")

    if errors:
        print("\nFAIL: Verification failed with errors:")
        for e in errors:
            print(f"- {e}")
    else:
        print("\nSUCCESS: Normal Mode logic verified.")

    # 5. Check Logs
    print("\n--- Log Analysis ---")
    print(logs)

if __name__ == "__main__":
    verify_normal_mode()
