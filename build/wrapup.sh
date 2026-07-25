#!/bin/bash
set -e
cd /Users/biznomad/Projects/Personal/the-great-asian-family-expedition
git add build/narration_v2.md build/build_film.py build/gen_vo.sh build/make_data.py \
  build/make_shortlist_cards.py build/shortlist.json build/research_vietnam.json \
  build/research_cambodia.json build/research_thailand.json build/research_china.json \
  build/make_credits.py build/make_title.py build/finish_v2.sh build/restart_kokoro.sh \
  build/wrapup.sh guide/index.html guide/data.js README.md 2>/dev/null || true
git -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -q -m "Add Booking File chapter + interactive field guide

- 4-country live accommodation/activity research (41 properties, 36 activities,
  winter 2026-27 rates, scooter-accessibility verdicts, verified booking URLs)
- guide/: interactive Netlify field guide (tiers/type/step-free filters,
  embedded documentary) -> asian-family-expedition.netlify.app
- Film extended to 12:04 with narrated Booking File chapter (4 PIL price
  cards + property Ken Burns); aspect-safe zoompan; looped finale music

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01LTUjnV11mYi8PaYsKxNXrK"
git push origin HEAD 2>&1 | tail -1
git log --oneline -1
