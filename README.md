# The Marxian Dialectic 🏛️

> **Karl Marx, Historical Materialism & The Critique of Political Economy**  
> Automated longform video and audio essay production system.

---

## 🎯 Architecture & Specifications

- **Format**: 16:9 Widescreen (1920x1080 @ 30 FPS).
- **Audio Synthesis**: Deep neural voiceover via Kokoro TTS (`bm_lewis` @ 0.85x speed).
- **Typography & Highlighting**: Single-line phrase subtitles with active radiant gold word highlighting.
- **Audio Spectrum**: Sleek 24-bar floating spectrum visualizer.
- **Asset Normalization**: 10 authentic Karl Marx portraits cleaned and color-graded.

---

## 🚀 Execution Commands

```bash
# Rapid 30-second verification preview
python auto_pipeline.py --preview 30 --dry-run

# Full 20-minute production episode
python auto_pipeline.py --target-minutes 20.0

# Deploy via GitHub Actions
# Triggers automatically via .github/workflows/generate_video.yml
```
