# The Trade — Scene 1 rebuild (handoff to Claude Code)

## What Claude Code needs before starting
1. The OpenArt connector (MCP) set up in Claude Code. Without it, no images or video can be made.
2. Python with ffmpeg, opencv, open_clip, faster-whisper, resemblyzer, praat-parselmouth, jiwer (for the QC tools in /qc).
3. This folder unzipped as the project folder.

## Paste this as the first message in Claude Code
Read START_HERE.md, skill/SKILL.md, the-trade-performance-script.md, Scene1_shot_ledger.md and plates/LOCKED_PLATES.md. Follow skill/SKILL.md exactly. Rebuild Scene 1 of The Trade (CGI, narration off), all 14 shots, as a chain: each shot's opening still made from the previous shot's last frame + the locked plate for its angle (see the ledger and plan/floorplan_v5.png). All stills at 1K low quality (regenerate freely). Video drafts at 480p from the approved 1K still, with a fixed seed per shot; QC every draft (film_qc.py, cut check, eye pass) and fix before moving on. Say "Tuh-VIK" for Tavique everywhere. No music, no ambience. Before spending credits, tell me which shots and roughly what it costs. Stop after the 480p drafts pass and show me the cut sheet and the rough cut for approval. Do not start Scene 2.

## Locked references (OpenArt links)
Prefix 2026-10: https://cdn.openart.ai/openart-ai/production/2026-10/create-image/sKzm6Mb8mw10m819HD7k/gpt-image-2.5-sunburst-edit-1_
- PANORAMA (looks N): 1790878419259_398c0639.png
- RIGHT (looks NE): 1790878178851_f09015c2.png
- WEST (looks W): 1790879907702_48707ae6.png
- LEFT (looks NW): plates/03_LEFT_looks_NW.jpg — has a hand fix (extra pot removed); upload this file, do not use the older link
Prefix 2026-09: https://cdn.openart.ai/openart-ai/production/2026-09/create-image/sKzm6Mb8mw10m819HD7k/
- CENTER (looks N): gpt-image-2.5-sunburst-1_1790558672670_365bb676.png
- Dad: gpt-image-2.5-sunburst-edit-1_1790558698107_7da75f2e.png
- Shopkeeper: gpt-image-2.5-sunburst-edit-1_1790558732325_24f0e46b.png
- Props A: gpt-image-2.5-sunburst-1_1790558732157_64f6cae4.png
- Props B: gpt-image-2.5-sunburst-1_1790558742773_d5c2da29.png
Cast (2026-07): https://cdn.openart.ai/openart-ai/production/2026-07/create-image/sKzm6Mb8mw10m819HD7k/
- Tavique: image_1785291334042_11997141_1785291334088_b8b7fce9.png
- Vessa: image_1785291288931_cc8e25d4_1785291289399_655e3a40.png

## Locked voices (OpenArt audio upload ids; files also in /voices)
- Tavique: LOdVRizOsBzWjjM01gq3 (tavik.wav)
- Vessa: Y8hUGTTJCylkzhiq4faI (vessa.wav)
- Dad: y5QgLykITWN5b0bZyfCy (dad.wav, 9.2 s) / short: iQOXR3ZpGoZz6G106WMu (dad_s.wav, 8.5 s — use in two-speaker shots so total voice audio stays under 15 s)

## Key facts
- Images: GPT Image 2.5 Sunburst, image2image, 1K, low quality (about 6 credits each). No 2K remakes.
- Video: Seedance 2.0 (byte-plus-seedance-2), element2video, generateAudio on. 1K still -> 480p drafts until right -> one final at 720p; Chad upscales finals in Topaz.
- Fridge is on the WEST wall, doors facing the table. Drawer is LEFT of the sink. Hook is right of the back door. Stairs run east to west through the hallway doorway on the west wall.
- The old REVERSE plate and the old LEFT/RIGHT/PANO versions are retired.
