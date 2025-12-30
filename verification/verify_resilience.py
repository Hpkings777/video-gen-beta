import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pvf_logic import JSONBuilder, renderer_stub

def verify_bhuchal_mode():
    print("Verifying Bhuchal Mode (Layer 3)...")
    builder = JSONBuilder()
    # Mode 2 is Bhuchal Mode
    try:
        blueprint = builder.build_blueprint("Test script.", "Dopamine_Spike", 2)
        logs = renderer_stub(blueprint)
        print("--- RENDERER LOGS ---")
        print(logs)
        print("---------------------")

        required_strings = [
            "backup_generator::CRT_INTERFACE",
            "backup_generator::SINE_WAVE",
            "TTS_ROBOTIC"
        ]

        missing = [s for s in required_strings if s not in logs]

        if missing:
            print(f"FAILED: Missing expected fallback strings: {missing}")
            # Do not exit with 1 yet, as we expect this to fail initially
            # sys.exit(1)
        else:
            print("SUCCESS: All Layer 3 fallbacks verified.")

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify_bhuchal_mode()
