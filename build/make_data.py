#!/usr/bin/env python3
"""Consolidate the 4 research JSONs into guide/data.js (normalized for filters)."""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
GUIDE = os.path.join(os.path.dirname(ROOT), "guide")

def norm_type(t):
    t = t.lower()
    if "villa" in t and "hotel" not in t and "resort - family" not in t: return "villa"
    if "apartment" in t or "serviced" in t or "residence" in t: return "apartment"
    return "hotel"

def infer_access(p):
    if "access_certain" in p: return p["access_certain"]
    a = p.get("accessibility", "").lower()
    uncertain = re.search(r"confirm|request ground|email|no elevator|not scooter|many stairs", a)
    positive = re.search(r"step-free|elevator|flat|accessible|ramp", a)
    return bool(positive and not uncertain)

QUOTES = {
 "Vietnam": "If Nana cannot roll through it, it does not make the cut.",
 "Cambodia": "To walk these corridors is to walk in the shadow of giants — at a fraction of London prices.",
 "Thailand": "Thailand's value is, frankly, showing off.",
 "China": "Somewhere in Beijing, an engineer thought of Nana personally — and one is rather moved.",
}

countries = []
for cname, fname in [("Vietnam","research_vietnam.json"), ("Cambodia","research_cambodia.json"),
                     ("Thailand","research_thailand.json"), ("China","research_china.json")]:
    d = json.load(open(f"{ROOT}/{fname}"))
    props = []
    for p in d["properties"]:
        props.append({
            "city": p.get("city",""), "name": p["name"], "type": norm_type(p["type"]),
            "tier": p["tier"], "sleeps": p["sleeps"], "nightly_usd": p["nightly_usd"],
            "rate_status": "listed" if str(p.get("rate_status","")).startswith("listed") else "estimated",
            "fits_9": p.get("fits_9",""), "accessibility": p.get("accessibility",""),
            "access_certain": infer_access(p), "booking_url": p["booking_url"],
            "tour_url": (p.get("tour_url") or "").split(" ")[0] or None,
            "image_urls": p.get("image_urls",[]),
        })
    acts = []
    for a in d["activities"]:
        acts.append({
            "city": a.get("city",""), "name": a["name"],
            "price_pp_usd": a["price_pp_usd"],
            "rate_status": "listed" if str(a.get("rate_status","")).startswith("listed") else "estimated",
            "ages": a.get("ages",""), "accessibility": a.get("accessibility",""),
            "booking_url": a["booking_url"],
        })
    countries.append({"name": cname, "quote": QUOTES[cname],
                      "properties": props, "activities": acts, "notes": d.get("notes","")})

out = "const DATA = " + json.dumps({"countries": countries}, indent=1, ensure_ascii=False) + ";\n"
open(f"{GUIDE}/data.js","w").write(out)
tp = sum(len(c["properties"]) for c in countries)
ta = sum(len(c["activities"]) for c in countries)
print(f"data.js written: {tp} properties, {ta} activities")
for c in countries:
    print(f"  {c['name']}: {len(c['properties'])} props ({sum(1 for p in c['properties'] if p['rate_status']=='listed')} listed) / {len(c['activities'])} acts")
