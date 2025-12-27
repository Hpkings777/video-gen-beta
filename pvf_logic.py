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

        asset_type: "video", "music", "voiceover"
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
                asset_filename = f"{asset_description.replace(' ', '_')}.dat"

            # real check: file_path = os.path.join(self.asset_dir, asset_filename)
            # if os.path.exists(file_path): ...

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
        # Generates specific data structure based on asset_type

        layer_info = "Layer 3 (Procedural Backup)"

        if asset_type == "video":
            return {
                "source": "procedural",
                "type": "video_generator",
                "desc": "backup_generator::CRT_INTERFACE",
                "color": "#000000", # Default black, overridden by style
                "text": "SYSTEM FALLBACK: " + asset_description,
                "layer_used": layer_info
            }

        elif asset_type == "music":
            return {
                "source": "procedural",
                "type": "tone_generator",
                "desc": "Tension Soundscape",
                "details": "60Hz Sine Wave Drone",
                "layer_used": layer_info
            }

        elif asset_type == "voiceover":
             return {
                "source": "procedural",
                "type": "tts_engine",
                "desc": "Robotic Speech",
                "details": "Local espeak/festival fallback",
                "text_content": asset_description,
                "layer_used": layer_info
            }

        else:
            # Generic fallback
            return {
                "source": "procedural",
                "type": "unknown",
                "desc": "Generic Fallback",
                "layer_used": layer_info
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

        timeline = []

        for idx, text in enumerate(segments):
            # Determine duration based on style
            # Simple logic: shorter text -> shorter duration, but clamped by style limits
            base_duration = len(text.split()) * 0.5
            duration = max(style["min_duration"], min(base_duration, style["max_duration"]))

            # Get Visual Asset
            # We use a keyword from the text as the asset description or ID
            asset_desc = " ".join(text.split()[:3])
            visual_asset = self.asset_manager.get_asset(asset_desc, failure_mode, asset_type="video")

            # Apply Style specific procedural overrides if needed
            if visual_asset["source"] == "procedural" and visual_asset["type"] == "video_generator":
                if style_preset_name == "Dopamine_Spike":
                    visual_asset["color"] = "#FF00FF" # Neon Pink for fallback in dopamine
                else:
                    visual_asset["color"] = "#222222" # Dark Grey for fallback in stoic

            # Get Voiceover Asset
            # Use the text content itself as the description
            voiceover_asset = self.asset_manager.get_asset(text[:20], failure_mode, asset_type="voiceover")

            segment_data = {
                "id": f"seg_{idx:03d}",
                "text_content": text,
                "duration": round(duration, 2),
                "visual_asset": visual_asset,
                "audio_asset": voiceover_asset,
                "style_config": {
                    "font": style["font"],
                    "font_size": style["font_size"],
                    "text_color": style["primary_color"],
                    "effect": style["effects"][idx % len(style["effects"])], # Cycle effects
                    "transition": style["transition"]
                }
            }
            timeline.append(segment_data)

        # Get Global Music Asset
        music_asset = self.asset_manager.get_asset(style_preset_name, failure_mode, asset_type="music")

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
    Iterates through the JSON timeline and output a step-by-step log.
    DO NOT execute ffmpeg.
    """
    logs = []
    logs.append(f"Starting Render Simulation for: {blueprint['project_name']}")
    logs.append(f"Style Preset: {blueprint['style_preset']}")

    # Global Audio Log
    global_audio = blueprint.get("global_audio")
    if global_audio:
         logs.append(f"Global Audio Track: {global_audio.get('desc', 'Unknown')}")
         if global_audio["source"] == "procedural":
             logs.append(f"  > Details: {global_audio.get('details')}")
         else:
             logs.append(f"  > Source: {global_audio.get('path')}")

    logs.append("-" * 40)

    for segment in blueprint["timeline"]:
        visual = segment["visual_asset"]
        audio = segment.get("audio_asset")

        logs.append(f"[Segment {segment['id']}] Duration: {segment['duration']}s")

        # Visuals
        logs.append(f"  > Requesting Visual: '{visual.get('path', 'PROCEDURAL')}'")
        logs.append(f"  > Layer Used: {visual['layer_used']}")

        if visual["source"] == "local":
            action = f"Rendering {segment['duration']}s of Local File: {visual['path']}"
        else:
            # Procedural
            desc = visual.get('desc', visual.get('type'))
            action = f"Rendering {segment['duration']}s of Procedural {desc} (Color: {visual.get('color', 'N/A')})"

        logs.append(f"  > Action: {action}")
        logs.append(f"  > Applied Effect: {segment['style_config']['effect']}")

        # Voiceover
        if audio:
            logs.append(f"  > [AUDIO] Voiceover: {audio.get('desc')}")
            if audio["source"] == "procedural":
                 logs.append(f"    > Details: {audio.get('details')}")
            else:
                 logs.append(f"    > Source: {audio.get('path')}")

        logs.append("-" * 20)

    logs.append("Render Simulation Complete.")
    return "\n".join(logs)
