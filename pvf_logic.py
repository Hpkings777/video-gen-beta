import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AssetManager:
    """
    The Resilience Core.
    Implements 3-Layer Cascading Failure Logic.
    """

    def __init__(self, asset_dir="assets"):
        self.asset_dir = asset_dir

    def get_asset(self, asset_description, failure_mode, asset_type="video"):
        """
        Retrieves an asset based on cascading failure logic.

        failure_mode maps to:
        0: Normal Test (Layer 1 Fail -> Layer 2 Success simulation)
        1: Local Fallback Test (Layer 2 Fail -> Layer 3 Success)
        2: Bhuchal Mode (Force Layer 3)
        """

        # --- LAYER 1: EXTERNAL API ---
        # "Must be hardcoded to FAIL"
        try:
            # Simulate API call
            raise ConnectionError("External API Connection Failed (Simulated)")
        except Exception as e:
            logger.warning(f"Layer 1 Failed: {e}")
            pass # Continue to Layer 2

        # --- LAYER 2: LOCAL ASSETS ---
        if failure_mode == 0:
            # Simulate Success for Demo purposes even if file is missing
            # In a real scenario, this would check os.path.exists
            if asset_type == "video":
                asset_filename = f"{asset_description.replace(' ', '_').upper()}.mp4"
            elif asset_type == "music":
                asset_filename = f"Music_Track_{asset_description.replace(' ', '_')}.mp3"
            elif asset_type == "voiceover":
                asset_filename = f"VO_{asset_description.replace(' ', '_')}.mp3"
            else:
                asset_filename = f"Asset_{asset_description.replace(' ', '_')}.dat"

            # Simulated return for Demo Mode 0
            return {
                "source": "local",
                "path": os.path.join(self.asset_dir, asset_filename),
                "type": asset_type,
                "desc": asset_description,
                "layer_used": "Layer 2 (Local Asset)"
            }

        elif failure_mode == 1:
            # Simulate Layer 2 Failure (File not found)
            logger.warning("Layer 2 Failed: File not found (Simulated or Real)")
            pass # Continue to Layer 3

        elif failure_mode == 2:
            # Bhuchal Mode - Force skip to Layer 3
            pass

        # --- LAYER 3: PROCEDURAL BACKUP ---
        # "Never Nothing" Fallback Logic

        if asset_type == "video":
            return {
                "source": "procedural",
                "type": "backup_generator::CRT_INTERFACE",
                "color": "#FF00FF", # Default fallback, overwritten by style later if needed
                "text": "SYSTEM FALLBACK: " + asset_description,
                "layer_used": "Layer 3 (Procedural Backup)"
            }

        elif asset_type == "music":
            return {
                "source": "procedural",
                "type": "Tension Soundscape",
                "details": "60Hz Sine Wave Drone",
                "layer_used": "Layer 3 (Procedural Backup)"
            }

        elif asset_type == "voiceover":
            return {
                "source": "procedural",
                "type": "Robotic Speech",
                "engine": "espeak_local",
                "text": asset_description,
                "layer_used": "Layer 3 (Procedural Backup)"
            }

        else:
            # Generic fallback
             return {
                "source": "procedural",
                "type": "generic_fallback",
                "text": asset_description,
                "layer_used": "Layer 3 (Procedural Backup)"
            }

class JSONBuilder:
    """
    The Intent Layer.
    Translates script and style into the final JSON Blueprint.
    """

    STYLE_PRESETS = {
        "Dopamine_Spike": {
            "min_duration": 1.5,
            "max_duration": 3.0,
            "font": "Montserrat-Black",
            "font_size": 80,
            "primary_color": "#00FF00", # Neon Green
            "background_color": "#111111",
            "effects": ["shake", "flash", "glitch"],
            "transition": "cut_fast",
            "video_generator": {"color": "#FF00FF"} # Magenta
        },
        "Cinematic_Stoic": {
            "min_duration": 4.0,
            "max_duration": 8.0,
            "font": "Garamond",
            "font_size": 50,
            "primary_color": "#E0E0E0", # Off-white
            "background_color": "#050505", # Deep black
            "effects": ["slow_zoom", "film_grain"],
            "transition": "fade_cross",
            "video_generator": {"color": "#222222"} # Dark Grey
        }
    }

    def __init__(self):
        self.asset_manager = AssetManager()

    def build_blueprint(self, script_text, style_preset_name, failure_mode):
        """
        Generates the JSON blueprint.
        """
        style = self.STYLE_PRESETS.get(style_preset_name, self.STYLE_PRESETS["Dopamine_Spike"])

        # Parse script into segments
        segments = [s.strip() for s in script_text.split('.') if s.strip()]
        if not segments:
            segments = [script_text]

        timeline = []

        # 1. Global Audio Track (Music)
        music_asset = self.asset_manager.get_asset(style_preset_name, failure_mode, asset_type="music")

        for idx, text in enumerate(segments):
            # Determine duration
            base_duration = len(text.split()) * 0.5
            duration = max(style["min_duration"], min(base_duration, style["max_duration"]))

            # Get Visual Asset
            # Use first 3 words as desc
            asset_desc = " ".join(text.split()[:3])
            visual_asset = self.asset_manager.get_asset(asset_desc, failure_mode, asset_type="video")

            # Apply Style specific procedural overrides
            if visual_asset["source"] == "procedural" and visual_asset["type"] == "backup_generator::CRT_INTERFACE":
                if "video_generator" in style:
                    visual_asset["color"] = style["video_generator"]["color"]

            # Get Voiceover Asset
            vo_asset = self.asset_manager.get_asset(text[:20], failure_mode, asset_type="voiceover")

            segment_data = {
                "id": f"seg_{idx:03d}",
                "text_content": text,
                "duration": round(duration, 2),
                "visual_asset": visual_asset,
                "audio_asset": vo_asset,
                "style_config": {
                    "font": style["font"],
                    "font_size": style["font_size"],
                    "text_color": style["primary_color"],
                    "effect": style["effects"][idx % len(style["effects"])], # Cycle effects
                    "transition": style["transition"]
                }
            }
            timeline.append(segment_data)

        blueprint = {
            "project_name": "PVF_Demo_Project",
            "style_preset": style_preset_name,
            "total_duration": sum(s["duration"] for s in timeline),
            "global_audio": music_asset,
            "timeline": timeline
        }

        return blueprint

def renderer_stub(blueprint):
    """
    Iterates through the JSON timeline and output a step-by-step log.
    DO NOT execute ffmpeg.
    """
    logs = []
    logs.append(f"Starting Render Simulation for: {blueprint['project_name']}")
    logs.append(f"Style Preset: {blueprint['style_preset']}")

    # Global Audio Log
    audio = blueprint.get("global_audio", {})
    logs.append(f"Global Audio Track: {audio.get('type', 'Unknown')}")
    if audio.get("source") == "procedural":
        logs.append(f"  > Details: {audio.get('details', 'Generated')}")
    else:
        logs.append(f"  > Source: {audio.get('path', 'Unknown')}")

    logs.append("-" * 40)

    for segment in blueprint["timeline"]:
        v_asset = segment["visual_asset"]
        a_asset = segment["audio_asset"]

        logs.append(f"[Segment {segment['id']}] Duration: {segment['duration']}s")

        # Visual Log
        logs.append(f"  > [VIDEO] Requesting Asset: '{v_asset.get('desc', v_asset.get('type'))}'")
        logs.append(f"  > Layer Used: {v_asset['layer_used']}")

        if v_asset["source"] == "local":
            action = f"Rendering {segment['duration']}s of Local File: {v_asset['path']}"
        else:
            action = f"Rendering {segment['duration']}s of Procedural {v_asset['type']} (Color: {v_asset.get('color', 'N/A')})"
        logs.append(f"  > Action: {action}")
        logs.append(f"  > Applied Effect: {segment['style_config']['effect']}")

        # Audio Log
        logs.append(f"  > [AUDIO] Voiceover: {a_asset.get('type', 'Unknown')}")
        if a_asset["source"] == "procedural":
             logs.append(f"  > Details: {a_asset.get('text', 'TTS')}")
        else:
             logs.append(f"  > Source: {a_asset.get('path', 'Unknown')}")

        logs.append("-" * 20)

    logs.append("Render Simulation Complete.")
    return "\n".join(logs)
