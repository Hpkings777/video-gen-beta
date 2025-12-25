## 2024-05-23 - Initial Palette Setup
**Learning:** This repo didn't have a palette file, so I created one to track UX learnings.
**Action:** Always check for .Jules directory and create if missing.

## 2024-05-23 - Asset Manager Resilience Layer 3

**Learning:** Implementing distinct fallback types (music vs voice vs video) in the AssetManager allows for a more immersive failure state ("Bhuchal Mode"). By ensuring every asset type has a procedural backup (Sine wave, TTS, Glitch pattern), we uphold the "Never Nothing" principle while providing auditable feedback via the "desc" field in logs.

**Action:** Implemented Layer 3 Procedural Fallbacks and updated renderer logs to explicitly show which layer and asset description is being used.
