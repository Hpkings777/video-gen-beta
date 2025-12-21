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
        # Determine filename extension based on asset type
        ext = ".mp4"
        if asset_type == "music" or asset_type == "voiceover":
            ext = ".mp3"

        asset_filename = f"{asset_description.replace(' ', '_').upper()}{ext}"
        file_path = os.path.join(self.asset_dir, asset_filename)

        # Check actual file existence
        file_exists = os.path.exists(file_path)

        # Apply Simulation Override based on failure_mode
        if failure_mode == 0:
            file_exists = True # Simulate found
        elif failure_mode == 1:
            file_exists = False # Simulate missing
        elif failure_mode == 2:
            file_exists = False # Force Layer 3

        if file_exists:
            return {
                "source": "local",
                "path": file_path,
                "type": asset_type,
                "layer_used": "Layer 2 (Local Asset)"
            }
        else:
            logger.warning(f"Layer 2 Failed: File {file_path} not found.")

        # --- LAYER 3: PROCEDURAL BACKUP ---
        # Generates simple data structure based on asset_type
        if asset_type == "video":
            return {
                "source": "procedural",
                "type": "solid_color",
                "color": "#000000", # Default black
                "text": "SYSTEM FALLBACK: " + asset_description,
                "layer_used": "Layer 3 (Procedural Backup)"
            }
        elif asset_type == "music":
            return {
                "source": "procedural",
                "type": "generated_audio",
                "details": "Tension Soundscape (Sine Wave Drone)",
                "layer_used": "Layer 3 (Procedural Backup)"
            }
        elif asset_type == "voiceover":
            return {
                "source": "procedural",
                "type": "tts",
                "details": "Robotic TTS",
                "text": asset_description,
                "layer_used": "Layer 3 (Procedural Backup)"
            }

        # Default fallback
        return {
            "source": "procedural",
            "type": "unknown",
            "details": "Generic Backup",
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

        # --- GLOBAL AUDIO ---
        # Get global music track
        music_desc = f"Background_Track_{style_preset_name}"
        global_audio = self.asset_manager.get_asset(music_desc, failure_mode, asset_type="music")

        timeline = []

        for idx, text in enumerate(segments):
            # Determine duration based on style
            # Simple logic: shorter text -> shorter duration, but clamped by style limits
            base_duration = len(text.split()) * 0.5
            duration = max(style["min_duration"], min(base_duration, style["max_duration"]))

            # Get Visual Asset
            # We use a keyword from the text as the asset description or ID
            # For simplicity, let's take the first noun-like word or just the first few words
            asset_desc = " ".join(text.split()[:3])
            visual_asset = self.asset_manager.get_asset(asset_desc, failure_mode, asset_type="video")

            # Get Audio Asset (Voiceover)
            # Use the text content as the description for TTS fallback
            voiceover_asset = self.asset_manager.get_asset(text, failure_mode, asset_type="voiceover")

            # Apply Style specific procedural overrides if needed
            if visual_asset["source"] == "procedural":
                if style_preset_name == "Dopamine_Spike":
                    visual_asset["color"] = "#FF00FF" # Neon Pink for fallback in dopamine
                else:
                    visual_asset["color"] = "#222222" # Dark Grey for fallback in stoic

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

        blueprint = {
            "project_name": "PVF_Demo_Project",
            "style_preset": style_preset_name,
            "total_duration": sum(s["duration"] for s in timeline),
            "global_audio": global_audio,
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
    logs.append("-" * 40)

    # Log Global Audio
    global_audio = blueprint.get("global_audio")
    if global_audio:
        logs.append(f"Global Audio Track: {global_audio.get('details', global_audio.get('path'))}")
        logs.append(f"  > Source: {global_audio['source']} | Layer Used: {global_audio['layer_used']}")
    logs.append("-" * 40)

    for segment in blueprint["timeline"]:
        visual_asset = segment["visual_asset"]
        audio_asset = segment["audio_asset"]

        logs.append(f"[Segment {segment['id']}] Duration: {segment['duration']}s")

        # Visuals
        logs.append(f"  > Visual Asset: '{visual_asset.get('path', 'PROCEDURAL')}'")
        logs.append(f"    - Layer: {visual_asset['layer_used']}")
        if visual_asset["source"] == "local":
            visual_action = f"Rendering Local File: {visual_asset['path']}"
        else:
            visual_action = f"Rendering Procedural {visual_asset['type']} (Color: {visual_asset['color']})"
        logs.append(f"    - Action: {visual_action}")

        # Voiceover
        logs.append(f"  > Voiceover: '{audio_asset.get('details', audio_asset.get('path'))}'")
        logs.append(f"    - Layer: {audio_asset['layer_used']}")

        logs.append(f"  > Applied Effect: {segment['style_config']['effect']}")
        logs.append("-" * 20)

    logs.append("Render Simulation Complete.")
    return "\n".join(logs)
