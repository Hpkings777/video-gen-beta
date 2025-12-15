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

    def get_video_asset(self, asset_description, failure_mode):
        """
        Retrieves a video asset based on cascading failure logic.
        """
        # --- LAYER 1: EXTERNAL API ---
        try:
            # Simulate API call
            raise ConnectionError("External API Connection Failed (Simulated)")
        except Exception as e:
            logger.warning(f"Layer 1 (Video) Failed: {e}")
            pass

        # --- LAYER 2: LOCAL ASSETS ---
        if failure_mode == 0:
            asset_filename = f"{asset_description.replace(' ', '_').upper()}.mp4"
            return {
                "source": "local",
                "path": os.path.join(self.asset_dir, asset_filename),
                "type": "video",
                "layer_used": "Layer 2 (Local Asset)"
            }
        elif failure_mode == 1:
            logger.warning("Layer 2 (Video) Failed: File not found (Simulated or Real)")
            pass

        # --- LAYER 3: PROCEDURAL BACKUP ---
        # Bhuchal Mode or Last Resort
        return {
            "source": "procedural",
            "type": "procedural_glitch",
            "details": "CRT_INTERFACE",
            "text_overlay": "BINARY_OVERLAY",
            "color": "#000000", # Default base
            "text": "SYSTEM FALLBACK: " + asset_description,
            "layer_used": "Layer 3 (Procedural Backup)"
        }

    def get_music_asset(self, failure_mode):
        """
        Retrieves a music asset based on cascading failure logic.
        """
        # --- LAYER 1: EXTERNAL API ---
        try:
            raise ConnectionError("External Music API Connection Failed (Simulated)")
        except Exception as e:
            logger.warning(f"Layer 1 (Music) Failed: {e}")
            pass

        # --- LAYER 2: LOCAL ASSETS ---
        if failure_mode == 0:
            return {
                "source": "local",
                "path": os.path.join(self.asset_dir, "music_track_01.mp3"),
                "type": "music",
                "layer_used": "Layer 2 (Local Asset)"
            }
        elif failure_mode == 1:
            logger.warning("Layer 2 (Music) Failed: File not found")
            pass

        # --- LAYER 3: PROCEDURAL BACKUP ---
        return {
            "source": "procedural",
            "type": "procedural_audio",
            "details": "SINE_WAVE_DRONE",
            "frequency": "low_tension",
            "layer_used": "Layer 3 (Procedural Backup)"
        }

    def get_asset(self, asset_description, failure_mode):
        """
        Legacy wrapper for video assets to maintain backward compatibility if needed,
        though JSONBuilder will be updated to use specific methods.
        """
        return self.get_video_asset(asset_description, failure_mode)


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
            "transition": "cut_fast"
        },
        "Cinematic_Stoic": {
            "min_duration": 4.0,
            "max_duration": 8.0,
            "font": "Garamond",
            "font_size": 50,
            "primary_color": "#E0E0E0", # Off-white
            "background_color": "#050505", # Deep black
            "effects": ["slow_zoom", "film_grain"],
            "transition": "fade_cross"
        }
    }

    def __init__(self):
        self.asset_manager = AssetManager()

    def build_blueprint(self, script_text, style_preset_name, failure_mode):
        """
        Generates the JSON blueprint.
        """
        style = self.STYLE_PRESETS.get(style_preset_name, self.STYLE_PRESETS["Dopamine_Spike"])

        # 1. Global Audio Selection
        music_asset = self.asset_manager.get_music_asset(failure_mode)

        # 2. Parse script into segments
        segments = [s.strip() for s in script_text.split('.') if s.strip()]
        if not segments:
            segments = [script_text]

        timeline = []

        for idx, text in enumerate(segments):
            base_duration = len(text.split()) * 0.5
            duration = max(style["min_duration"], min(base_duration, style["max_duration"]))

            asset_desc = " ".join(text.split()[:3])
            asset_data = self.asset_manager.get_video_asset(asset_desc, failure_mode)

            # Apply Style specific procedural overrides if needed
            if asset_data["source"] == "procedural":
                if style_preset_name == "Dopamine_Spike":
                    asset_data["color"] = "#FF00FF" # Neon Pink for fallback
                else:
                    asset_data["color"] = "#222222" # Dark Grey for fallback

            segment_data = {
                "id": f"seg_{idx:03d}",
                "text_content": text,
                "duration": round(duration, 2),
                "visual_asset": asset_data,
                "style_config": {
                    "font": style["font"],
                    "font_size": style["font_size"],
                    "text_color": style["primary_color"],
                    "effect": style["effects"][idx % len(style["effects"])],
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
    audio = blueprint.get('global_audio', {})
    logs.append(f"Global Audio Track: {audio.get('type', 'Unknown')}")
    logs.append(f"  > Source: {audio.get('source', 'Unknown')}")
    logs.append(f"  > Layer Used: {audio.get('layer_used', 'Unknown')}")
    if audio.get('source') == 'procedural':
        logs.append(f"  > Details: {audio.get('details', 'Unknown')} (Freq: {audio.get('frequency', 'Unknown')})")

    logs.append("-" * 40)

    for segment in blueprint["timeline"]:
        asset = segment["visual_asset"]
        logs.append(f"[Segment {segment['id']}] Duration: {segment['duration']}s")

        # Determine how to display path/type
        if asset["source"] == "local":
            asset_ref = asset.get('path', 'UNKNOWN_PATH')
        else:
            asset_ref = f"PROCEDURAL_{asset.get('type', 'Unknown')}"

        logs.append(f"  > Requesting Asset: '{asset_ref}'")
        logs.append(f"  > Layer Used: {asset['layer_used']}")

        if asset["source"] == "local":
            action = f"Rendering {segment['duration']}s of Local File: {asset['path']}"
        elif asset["type"] == "procedural_glitch":
             action = f"Rendering {segment['duration']}s of Procedural Glitch (Details: {asset.get('details', 'CRT')} - {asset.get('text_overlay', 'BIN')})"
        else:
            action = f"Rendering {segment['duration']}s of Procedural Generic (Color: {asset.get('color', '#000')})"

        logs.append(f"  > Action: {action}")
        logs.append(f"  > Applied Effect: {segment['style_config']['effect']}")
        logs.append("-" * 20)

    logs.append("Render Simulation Complete.")
    return "\n".join(logs)
