
import sys
import os

# Add parent directory to path to import pvf_logic
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pvf_logic import JSONBuilder, renderer_stub

def verify_layer3_resilience():
    print("Verifying Layer 3 Resilience (Bhuchal Mode)...")

    # Initialize Builder
    builder = JSONBuilder()

    # Force Failure Mode 2 (Bhuchal Mode)
    # This guarantees Layer 3 Procedural Assets
    failure_mode = 2
    script_text = "Testing resilience. Verification is key."
    style_preset = "Dopamine_Spike"

    blueprint = builder.build_blueprint(script_text, style_preset, failure_mode)

    # 1. Verify Global Audio (Music) Fallback
    audio = blueprint.get("global_audio")
    assert audio is not None, "Global Audio missing from blueprint"
    assert audio["type"] == "backup_generator::SINE_WAVE", f"Incorrect Music Fallback: {audio['type']}"
    assert audio["layer_used"] == "Layer 3 (Procedural Backup)", "Incorrect Layer for Music"
    print("✓ Music Fallback Verified: backup_generator::SINE_WAVE")

    # 2. Verify Segment Fallbacks (Visual & Voiceover)
    for segment in blueprint["timeline"]:
        # Visual
        visual = segment["visual_asset"]
        assert visual["type"] == "backup_generator::CRT_INTERFACE", f"Incorrect Visual Fallback: {visual['type']}"
        assert visual["layer_used"] == "Layer 3 (Procedural Backup)", "Incorrect Layer for Visual"

        # Voiceover
        vo = segment["voiceover_asset"]
        assert vo["type"] == "TTS_ROBOTIC", f"Incorrect Voiceover Fallback: {vo['type']}"
        assert vo["layer_used"] == "Layer 3 (Procedural Backup)", "Incorrect Layer for Voiceover"

    print("✓ Segment Fallbacks Verified: CRT_INTERFACE and TTS_ROBOTIC")

    # 3. Verify Renderer Output Logs
    logs = renderer_stub(blueprint)

    assert "Global Audio Track: backup_generator::SINE_WAVE" in logs, "Renderer Log missing Music"
    assert "Rendering" in logs and "Procedural backup_generator::CRT_INTERFACE" in logs, "Renderer Log missing Visual Action"
    assert "[AUDIO] Voiceover: TTS_ROBOTIC" in logs, "Renderer Log missing Voiceover"

    print("✓ Renderer Logs Verified")
    print("All Layer 3 Resilience Checks Passed!")

if __name__ == "__main__":
    try:
        verify_layer3_resilience()
    except AssertionError as e:
        print(f"❌ Verification Failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)
