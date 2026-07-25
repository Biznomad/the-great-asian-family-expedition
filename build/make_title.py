#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
im = Image.new("RGB", (1280, 720), (10, 10, 10))
d = ImageDraw.Draw(im)
G = "/System/Library/Fonts/Supplemental/Georgia.ttf"
GB = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
GI = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
GOLD = (201, 169, 78)
CREAM = (237, 230, 214)

def center(txt, fp, fs, y, fill):
    f = ImageFont.truetype(fp, fs)
    w = d.textlength(txt, font=f)
    d.text(((1280 - w) / 2, y), txt, font=f, fill=fill)

# thin gold rules
d.rectangle([440, 250, 840, 252], fill=GOLD)
d.rectangle([440, 468, 840, 470], fill=GOLD)
center("A  N A T U R A L   H I S T O R Y   O F   T H E   F A M I L Y   H O L I D A Y", G, 17, 282, GOLD)
center("The Great Asian", GB, 62, 316, CREAM)
center("Family Expedition", GB, 62, 388, CREAM)
center("Four countries · Three generations · One scooter", GI, 22, 494, CREAM)
im.save("/Users/biznomad/Projects/Personal/the-great-asian-family-expedition/build/title.png")
print("title.png written")
