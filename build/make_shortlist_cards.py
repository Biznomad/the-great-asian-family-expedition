#!/usr/bin/env python3
"""Render film-style 'Booking File' cards (1536x1024, dark+gold) from research data.
Usage: python3 make_shortlist_cards.py  (reads shortlist.json next to this file)
shortlist.json: [{country, picks:[{name, detail, price}], activities:[{name, price}]}]
"""
import json, os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
G = "/System/Library/Fonts/Supplemental/Georgia.ttf"
GB = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
GI = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
GOLD, CREAM, DIM = (201, 169, 78), (237, 230, 214), (150, 143, 125)
W, H = 1536, 1024

def f(path, size): return ImageFont.truetype(path, size)

def card(country, picks, activities, out):
    im = Image.new("RGB", (W, H), (12, 11, 9))
    d = ImageDraw.Draw(im)
    # gold frame
    d.rectangle([40, 40, W-40, H-40], outline=GOLD, width=2)
    d.rectangle([48, 48, W-48, H-48], outline=(70, 60, 35), width=1)
    # header
    t = "THE BOOKING FILE"
    ft = f(G, 30); d.text(((W - d.textlength(t, font=ft))/2, 86), t, font=ft, fill=GOLD)
    ft = f(GB, 64); d.text(((W - d.textlength(country.upper(), font=ft))/2, 130), country.upper(), font=ft, fill=CREAM)
    d.rectangle([W/2-200, 220, W/2+200, 222], fill=GOLD)
    y = 260
    ft_n, ft_d, ft_p = f(GB, 34), f(GI, 24), f(GB, 34)
    for p in picks:
        d.text((120, y), p["name"], font=ft_n, fill=CREAM)
        pw = d.textlength(p["price"], font=ft_p)
        d.text((W-120-pw, y), p["price"], font=ft_p, fill=GOLD)
        d.text((120, y+46), p["detail"], font=ft_d, fill=DIM)
        y += 108
    y += 10
    d.rectangle([120, y, W-120, y+1], fill=(70, 60, 35)); y += 28
    t = "PURSUITS WORTH BOOKING"
    ft = f(G, 24); d.text((120, y), t, font=ft, fill=GOLD); y += 52
    ft_a, ft_ap = f(G, 27), f(G, 27)
    for a in activities:
        d.text((120, y), "·  " + a["name"], font=ft_a, fill=CREAM)
        pw = d.textlength(a["price"], font=ft_ap)
        d.text((W-120-pw, y), a["price"], font=ft_ap, fill=DIM)
        y += 46
    im.save(out); print("wrote", out)

data = json.load(open(f"{ROOT}/shortlist.json"))
for c in data:
    card(c["country"], c["picks"], c["activities"],
         f"{ROOT}/card_booking_{c['country'].lower()}.png")
