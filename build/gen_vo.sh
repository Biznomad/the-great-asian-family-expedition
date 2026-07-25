#!/bin/bash
# Generate per-section VO via local Kokoro TTS
set -e
cd "$(dirname "$0")"
mkdir -p vo
SRC=narration_v2.md

# Extract section names in order
sections=$(grep -o '^---SECTION: [a-z0-9_]*---' $SRC | sed 's/---SECTION: //;s/---//')

for s in $sections; do
  # Pull text between this section marker and the next marker (or EOF), strip comments/blank lines
  text=$(awk -v sec="---SECTION: $s---" '
    $0 == sec {found=1; next}
    /^---SECTION:/ {found=0}
    found && !/^#/ && NF {print}
  ' $SRC)
  jq -n --arg t "$text" '{model:"kokoro", input:$t, voice:"bm_george", speed:0.88, response_format:"wav"}' > /tmp/tts_req.json
  curl -s -X POST http://localhost:8880/v1/audio/speech \
    -H "Content-Type: application/json" \
    -d @/tmp/tts_req.json -o "vo/${s}.wav"
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "vo/${s}.wav" 2>/dev/null || echo FAIL)
  echo "$s: ${d}s $(stat -f%z vo/${s}.wav) bytes"
done
