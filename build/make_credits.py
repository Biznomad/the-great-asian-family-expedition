#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
im = Image.new("RGB", (1280, 720), (10, 10, 10))
d = ImageDraw.Draw(im)
G = "/System/Library/Fonts/Supplemental/Georgia.ttf"
GB = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
GI = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
C = (237, 230, 214)
lines = [
    ("The Great Asian Family Expedition", GB, 44, 180),
    ("For the Akbar-Jones family — ages one to seventy-two", G, 23, 268),
    ("Narrated in the finest tradition of British understatement", G, 23, 306),
    ("Music: Kevin MacLeod (incompetech.com) — CC BY 4.0", G, 19, 396),
    ("Footage: Mixkit · Narrator scenes: Seedance · Infographics: OpenAI", G, 19, 430),
    ("The chickens of Tra Que village were notified, and remain at large.", GI, 19, 520),
    ("MMXXVI", G, 21, 600),
]
for txt, fp, fs, y in lines:
    f = ImageFont.truetype(fp, fs)
    w = d.textlength(txt, font=f)
    d.text(((1280 - w) / 2, y), txt, font=f, fill=C)
im.save("/Users/biznomad/Projects/Personal/the-great-asian-family-expedition/build/credits.png")
print("credits.png written")
