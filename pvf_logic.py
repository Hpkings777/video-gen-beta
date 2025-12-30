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
            # For this demo, we pretend we found a file in 'assets' if mode is 0

            ext_map = {
                "video": ".mp4",
                "music": ".mp3",
                "voiceover": ".mp3"
            }
            ext = ext_map.get(asset_type, ".dat")

            asset_filename = f"{asset_description.replace(' ', '_').upper()}{ext}"

            # Special prefix handling for better simulation logs
            if asset_type == "music":
                asset_filename = f"Music_Track_{asset_description.replace(' ', '_')}{ext}"
            elif asset_type == "voiceover":
                asset_filename = f"VO_{asset_description.replace(' ', '_')}{ext}"

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
        # Generates simple data structure

        if asset_type == "video":
            return {
                "source": "procedural",
                "type": "backup_generator::CRT_INTERFACE",
                "details": "Animated binary text overlay",
                "layer_used": "Layer 3 (Procedural Backup)"
            }
        elif asset_type == "music":
             return {
                "source": "procedural",
                "type": "backup_generator::SINE_WAVE",
                "details": "Low-freq 60Hz Sine Wave",
                "layer_used": "Layer 3 (Procedural Backup)"
            }
        elif asset_type == "voiceover":
             return {
                "source": "procedural",
                "type": "TTS_ROBOTIC",
                "details": "Subtitled Text Only",
                "layer_used": "Layer 3 (Procedural Backup)"
            }

        # Fallback for unknown types
        return {
            "source": "procedural",
            "type": "unknown_static",
            "details": "Static noise",
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

        # Parse script into segments (simple sentence/line split)
        segments = [s.strip() for s in script_text.split('.') if s.strip()]
        if not segments:
            segments = [script_text]

        # 1. Global Audio Track (Music)
        # Using style name as a keyword for music
        music_asset = self.asset_manager.get_asset(style_preset_name, failure_mode, asset_type="music")

        timeline = []

        for idx, text in enumerate(segments):
            # Determine duration based on style
            # Simple logic: shorter text -> shorter duration, but clamped by style limits
            base_duration = len(text.split()) * 0.5
            duration = max(style["min_duration"], min(base_duration, style["max_duration"]))

            # Get Video Asset
            # We use a keyword from the text as the asset description or ID
            asset_desc = " ".join(text.split()[:3])
            video_asset = self.asset_manager.get_asset(asset_desc, failure_mode, asset_type="video")

            # Apply Style specific procedural overrides if needed for video
            if video_asset["source"] == "procedural" and "color" not in video_asset:
                 # Although we changed the fallback to CRT_INTERFACE, let's keep color if needed or add it
                 if style_preset_name == "Dopamine_Spike":
                     video_asset["color"] = "#FF00FF" # Neon Pink
                 else:
                     video_asset["color"] = "#222222" # Dark Grey

            # Get Voiceover Asset
            # Using the text segment itself as the description reference
            vo_desc = text[:20]
            vo_asset = self.asset_manager.get_asset(vo_desc, failure_mode, asset_type="voiceover")

            segment_data = {
                "id": f"seg_{idx:03d}",
                "text_content": text,
                "duration": round(duration, 2),
                "visual_asset": video_asset,
                "voiceover": vo_asset,
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

    # Log Global Audio
    bg_music = blueprint.get("global_audio", {})
    logs.append("-" * 40)
    logs.append(f"Global Audio Track: {bg_music.get('type', 'UNKNOWN')}")
    if bg_music.get('source') == 'procedural':
        logs.append(f"  > Details: {bg_music.get('details')}")
    logs.append(f"  > Layer Used: {bg_music.get('layer_used')}")

    logs.append("-" * 40)

    for segment in blueprint["timeline"]:
        asset = segment["visual_asset"]
        vo = segment.get("voiceover", {})

        logs.append(f"[Segment {segment['id']}] Duration: {segment['duration']}s")

        # Video Log
        logs.append(f"  > [VIDEO] Requesting Asset: '{asset.get('path', asset.get('type', 'PROCEDURAL'))}'")
        logs.append(f"  > Layer Used: {asset['layer_used']}")

        if asset["source"] == "local":
            action = f"Rendering {segment['duration']}s of Local File: {asset['path']}"
        else:
            color_info = f" (Color: {asset.get('color', 'N/A')})" if 'color' in asset else ""
            action = f"Rendering {segment['duration']}s of Procedural {asset['type']} ({asset.get('details', '')}){color_info}"

        logs.append(f"  > Action: {action}")

        # Audio/VO Log
        logs.append(f"  > [AUDIO] Voiceover: {vo.get('type', 'UNKNOWN')}")
        if vo.get('source') == 'procedural':
             logs.append(f"  > Details: {vo.get('details')}")
        logs.append(f"  > Layer Used: {vo.get('layer_used')}")

        logs.append(f"  > Applied Effect: {segment['style_config']['effect']}")
        logs.append("-" * 20)

    logs.append("Render Simulation Complete.")
    return "\n".join(logs)
