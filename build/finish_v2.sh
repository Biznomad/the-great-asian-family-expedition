#!/bin/bash
set -e
cd /Users/biznomad/Projects/Personal/the-great-asian-family-expedition
ffmpeg -y -v error -i The_Great_Asian_Family_Expedition.mp4 \
  -c:v libx264 -preset medium -crf 28 -c:a aac -b:a 128k \
  -movflags +faststart The_Great_Asian_Family_Expedition_share.mp4
cp The_Great_Asian_Family_Expedition_share.mp4 guide/film.mp4
echo "master: $(stat -f%z The_Great_Asian_Family_Expedition.mp4) bytes"
echo "share:  $(stat -f%z The_Great_Asian_Family_Expedition_share.mp4) bytes"
netlify deploy --prod --dir=guide --site=0d265d85-000f-48e2-9c7d-c7b16e9b63b2 2>&1 | grep -E "Deployed to production|Unique deploy" | head -2
curl -s -o /dev/null "https://asian-family-expedition.netlify.app/" -w "site: %{http_code}\n"
