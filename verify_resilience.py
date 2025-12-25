from pvf_logic import JSONBuilder, renderer_stub
import json

def verify():
    print("--- Verifying All Failure Modes ---")
    builder = JSONBuilder()

    # Use a simple script
    script = "System failure."

    modes = {
        0: "Normal Test (Layer 2 Success)",
        1: "Local Fallback Test (Layer 3 Success)",
        2: "Bhuchal Mode (Force Layer 3)"
    }

    for mode, desc in modes.items():
        print(f"\n\n=== Mode {mode}: {desc} ===")
        blueprint = builder.build_blueprint(script, "Dopamine_Spike", mode)

        # print(json.dumps(blueprint, indent=2))
        logs = renderer_stub(blueprint)
        print(logs)

        # specific checks
        if mode == 0:
            if "Layer 2 (Local Asset)" not in logs:
                print("FAIL: Expected Layer 2 in Mode 0")
            if "Background_Track_Dopamine_Spike" not in logs:
                 print("FAIL: Expected Background_Track_Dopamine_Spike in logs")
        elif mode == 2:
             if "Layer 3 (Procedural Backup)" not in logs:
                print("FAIL: Expected Layer 3 in Mode 2")
             if "Tension Soundscape" not in logs:
                print("FAIL: Expected Tension Soundscape in logs")

if __name__ == "__main__":
    verify()
