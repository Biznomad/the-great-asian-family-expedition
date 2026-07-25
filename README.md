# The Great Asian Family Expedition
## A National Geographic-Style Documentary

### Project Overview
A 25-minute family vacation destination documentary following the Akbar-Jones family as they evaluate China, Vietnam, Cambodia, and Thailand for their multi-generational trip. Features 3 couples (6 adults), Poppa & Nana (scooter), 16yo, 8yo, and toddler.

### Key Features
- Classic British National Geographic narration style
- Dramatic opening with orchestral score
- 4 chapters (Vietnam, Cambodia, Thailand, China)
- 15 infographic cards with pricing and accessibility data
- 8 narrator video scenes at key locations
- 13 B-roll images and 8 stock video clips
- Monk brick-breaking scene in Thailand chapter
- China positioned as the premier destination

### File Structure
- `documentary_script.md` - Full 852-line script with 22 scenes
- `documentary_shotlist.md` - Frame-by-frame shot list (180 shots)
- `README.md` - This file

### Final Film (COMPLETE — 2026-07-25)
`The_Great_Asian_Family_Expedition.mp4` — 10:03, 1280x720, H.264/AAC.
Rebuilt end-to-end with a vintage British natural-history narrator (Kokoro bm_george),
dry-wit rewrite of the narration (kids named: Amirah 15, Naeema 7, Aliya 1),
3-movement orchestral score (Kevin MacLeod, CC BY 4.0), Ken Burns infographics,
muted Seedance narrator scenes, PIL title + credits cards.

Rebuild: `python3 build/build_film.py` (VO: `build/gen_vo.sh`, needs local Kokoro on :8880)

### Production Assets
- Voiceover: 12 sections in `build/vo/` from `build/narration_v2.md` (original 8-min master retained in `assets/audio/`)
- Narrator scenes: 8 Seedance 2.0 Mini clips (audio is Chinese speech — muted in edit)
- Infographics: 15 cards (OpenAI Hazel; card 01 has garbled AI text — replaced by PIL title card at open)
- B-roll: 8 stock videos (the 13 B-roll images were never committed; edit covers gaps with Ken Burns)

### License
Documentation: MIT
Media assets: Various licenses (see individual sources)
