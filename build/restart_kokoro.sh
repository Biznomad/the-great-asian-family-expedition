#!/bin/bash
launchctl kickstart -k gui/501/com.voicemode.kokoro
for i in $(seq 1 20); do
  sleep 3
  if curl -s -m 3 -o /tmp/kk.json http://localhost:8880/v1/audio/voices; then
    echo "kokoro UP after ${i}x3s"
    exit 0
  fi
done
echo "kokoro still down after 60s"
launchctl print gui/501/com.voicemode.kokoro | grep -E "state|last exit" | head -4
exit 1
