import os
import json

# --- MOCK LOGIC FOR DEMONSTRATION ---

class AssetManager:
    """
    Simulates the Asset Retrieval Layer.
    Layer 1: External API (Simulated Fail)
    Layer 2: Local Assets (Simulated Success/Fail)
    Layer 3: Procedural Backup (Always Success)
    """
    def __init__(self, asset_dir="assets"):
        self.asset_dir = asset_dir

    def get_asset(self, asset_description, failure_mode, asset_type="video"):
        """
        Retrieves an asset based on cascading failure logic.

        failure_mode:
        0: Normal Test (Layer 1 Fail -> Layer 2 Success simulation)
        1: Local Fallback Test (Layer 2 Fail -> Layer 3 Success)
        2: Bhuchal Mode (Force Layer 3)

        asset_type: "video", "music", "voiceover"
        """

        # --- LAYER 1: EXTERNAL API ---
        # In this demo, we assume Layer 1 always fails (API down, rate limit, etc.)
        # Real logic would be: try_fetch_api(asset_description)
        # logging.warning("Layer 1 (External API) Failed...")

        # --- LAYER 2: LOCAL ASSETS ---
        if failure_mode == 0:
            # Simulate Success for Demo purposes even if file is missing
            # In a real scenario, this would check os.path.exists
            # For this demo, we pretend we found a file in 'assets' if mode is 0

            ext = ".mp4"
            if asset_type in ["music", "voiceover"]:
                ext = ".mp3"

            asset_filename = f"{asset_description.replace(' ', '_').upper()}{ext}"
            # real check: file_path = os.path.join(self.asset_dir, asset_filename)
            # if os.path.exists(file_path): ...

            return {
                "source": "local",
                "path": os.path.join(self.asset_dir, asset_filename),
                "type": asset_type,
                "layer_used": "Layer 2 (Local Asset)"
            }

        if failure_mode == 1:
            # Simulate File Missing -> Fallthrough to Layer 3
            pass

        if failure_mode == 2:
            # Force Fallthrough
            pass

        # --- LAYER 3: PROCEDURAL BACKUP ---
        # Generates simple data structure

        if asset_type == "music":
             return {
                "source": "procedural",
                "type": "sine_wave",
                "desc": "Tension Soundscape",
                "layer_used": "Layer 3 (Procedural Backup)"
            }

        elif asset_type == "voiceover":
            return {
                "source": "procedural",
                "type": "tts_robotic",
                "desc": "Robotic Speech",
                "layer_used": "Layer 3 (Procedural Backup)"
            }

        else: # Default to video
            return {
                "source": "procedural",
                "type": "solid_color",
                "color": "#000000", # Default black
                "text": "SYSTEM FALLBACK: " + asset_description,
                "layer_used": "Layer 3 (Procedural Backup)"
            }

class JSONBuilder:
    """
    Simulates the Logic Layer that builds the project blueprint.
    """
    def __init__(self):
        self.asset_manager = AssetManager()

    def build_blueprint(self, script_text, style_preset_name, failure_mode):

        # Simple segmentation by period
        segments = [s.strip() for s in script_text.split('.') if s.strip()]

        # Default if empty
        if not segments:
            segments = [script_text]

        # Request Global Audio Track
        music_asset = self.asset_manager.get_asset(f"Background_Track_{style_preset_name}", failure_mode, asset_type="music")

        timeline = []

        for idx, text in enumerate(segments):

            # Style Logic (Mock)
            style = {
                "font": "Roboto" if style_preset_name == "Cinematic_Stoic" else "Impact",
                "font_size": 40,
                "effect": "None"
            }

            if style_preset_name == "Dopamine_Spike":
                duration = max(2.0, len(text.split()) * 0.3) # Fast cuts
            else:
                duration = max(4.0, len(text.split()) * 0.6) # Slow pace

            # Asset Request
            asset_desc = " ".join(text.split()[:3])
            asset_data = self.asset_manager.get_asset(asset_desc, failure_mode)

            # Get Voiceover
            vo_asset = self.asset_manager.get_asset(text, failure_mode, asset_type="voiceover")

            # Apply Style specific procedural overrides if needed
            if asset_data["source"] == "procedural":
                if style_preset_name == "Dopamine_Spike":
                    asset_data["color"] = "#FF00FF" # Neon Magenta
                    style["effect"] = "Glitch"
                else:
                    asset_data["color"] = "#222222" # Dark Grey
                    style["effect"] = "Grain"

            timeline.append({
                "id": idx + 1,
                "text_content": text,
                "duration": round(duration, 2),
                "visual_asset": asset_data,
                "audio_asset": vo_asset,
                "style_config": {
                    "font": style["font"],
                    "font_size": style["font_size"],
                    "effect": style["effect"]
                }
            })

        blueprint = {
            "project_name": "PVF_Demo_Project",
            "style_preset": style_preset_name,
            "global_audio": music_asset,
            "total_duration": sum(s["duration"] for s in timeline),
            "timeline": timeline
        }

        return blueprint

def renderer_stub(blueprint):
    """
    Simulates the Renderer consuming the blueprint.
    Output: Console logs as a string.
    """
    logs = []
    logs.append(f"Starting Render Simulation for: {blueprint['project_name']}")
    logs.append(f"Style Preset: {blueprint['style_preset']}")

    # Global Audio Log
    audio = blueprint.get("global_audio")
    if audio:
        desc = audio.get("desc", audio.get("path", "Unknown"))
        logs.append(f"Global Audio Track: {desc} ({audio.get('type')})")
        logs.append(f"  > Layer Used: {audio['layer_used']}")

    logs.append("-" * 40)

    for segment in blueprint["timeline"]:
        asset = segment["visual_asset"]
        vo_asset = segment.get("audio_asset")

        logs.append(f"[Segment {segment['id']}] Duration: {segment['duration']}s")

        # Video Log
        logs.append(f"  [VIDEO] Requesting: '{asset.get('path', asset.get('desc', 'PROCEDURAL'))}'")
        logs.append(f"  > Layer Used: {asset['layer_used']}")

        if asset["source"] == "local":
            action = f"Rendering Video from Local File: {asset['path']}"
        elif asset["source"] == "procedural":
             action = f"Rendering Procedural Video {asset['type']} (Color: {asset.get('color', 'N/A')})"
        else:
            action = f"Rendering External Video from {asset.get('source', 'Unknown')}"

        logs.append(f"  > Action: {action}")

        # Audio Log
        if vo_asset:
             logs.append(f"  [AUDIO] Voiceover: '{vo_asset.get('desc', vo_asset.get('path', 'Unknown'))}'")
             logs.append(f"  > Layer Used: {vo_asset['layer_used']}")

        logs.append(f"  > Applied Effect: {segment['style_config']['effect']}")
        logs.append("-" * 20)

    return "\n".join(logs)
