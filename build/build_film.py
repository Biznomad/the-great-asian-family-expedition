#!/usr/bin/env python3
"""Assemble 'The Great Asian Family Expedition' final documentary.
Timeline is computed from actual VO section durations. All video normalized
to 1280x720/30fps, narrator clips MUTED (they speak Chinese), stills get
Ken Burns moves, music bed in 3 movements, VO + music mixed with loudnorm.
"""
import json, math, subprocess, sys, os

ROOT = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(os.path.dirname(ROOT), "assets")
SEG = os.path.join(ROOT, "segments"); os.makedirs(SEG, exist_ok=True)
FPS = 30; W, H = 1280, 720
GAP = 1.2          # breathing room between sections
TITLE_DUR = 4.0    # infographic_01 as title card, music only
CREDITS_DUR = 12.0
GEORGIA = "/System/Library/Fonts/Supplemental/Georgia.ttf"
GEORGIA_B = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"

def dur(path):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries",
        "format=duration","-of","csv=p=0",path]).strip())

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG FAIL:", " ".join(cmd)[:400], "\n", r.stderr[-1500:]); sys.exit(1)

# ---------------- asset shorthand ----------------
N = lambda n: f"{A}/narrator_scenes/{n}.mp4"
S = lambda n: f"{A}/stock_videos/{n}.mp4"
I = lambda n: f"{A}/infographics/{n}.png"
VO = lambda n: f"{ROOT}/vo/{n}.wav"

SECTIONS = ["01_cold_open","02_the_specimens","03_criteria","04_vietnam_arrival",
    "05_vietnam_food","06_vietnam_pricing","07_cambodia","08_thailand",
    "09_china_arrival","10_china_activities","11_verdict","12_closing"]
vod = {s: dur(VO(s)) for s in SECTIONS}

# shot = (kind, src, plan_dur, opt)
#  kind: vid (opt=in-point seconds | ('slow', in, factor)) / kb (opt=KB variant)
PLAN = {
"01_cold_open": [
    ("vid", S("halong_bay_sailing"), 8.0, 0),
    ("vid", S("halong_bay_scenic"), 8.0, 0),
    ("vid", S("great_wall_mixkit"), 6.8, 0),
    ("vid", S("bangkok_evening"), 7.9, 0),
    ("vid", N("narrator_01_planning_table"), 10.0, 0)],
"02_the_specimens": [
    ("kb", I("infographic_01_family_expedition"), 14.0, "zi"),
    ("vid", N("narrator_02_vietnam_market"), 10.0, 0),
    ("vid", S("bangkok_street_food"), 13.5, 0),
    ("vid", N("narrator_03_halong_bay"), 10.0, 0),
    ("vid", S("thai_cooking_fire"), 9.3, 0)],
"03_criteria": [
    ("kb", I("infographic_02_four_pillars"), 24.0, "zo"),
    ("vid", S("halong_bay_waterways"), 3.3, 0),
    ("vid", S("bangkok_lights"), 3.3, 5),
    ("vid", S("great_wall_mixkit"), 3.3, 1.5),
    ("vid", S("thai_cooking_fire"), 3.3, 14)],
"04_vietnam_arrival": [
    ("vid", N("narrator_02_vietnam_market"), 10.0, 0),
    ("vid", S("halong_bay_waterways"), 8.0, 0),
    ("kb", I("infographic_03_hoian_access"), 14.0, "pl"),
    ("vid", S("halong_bay_scenic"), 8.0, 1),
    ("vid", N("narrator_03_halong_bay"), 10.0, 0)],
"05_vietnam_food": [
    ("vid", S("thai_cooking_fire"), 12.0, 2),
    ("kb", I("infographic_04_vietnam_activities"), 16.0, "zi"),
    ("vid", S("bangkok_street_food"), 12.0, 6),
    ("vid", S("halong_bay_sailing"), 11.5, 9)],
"06_vietnam_pricing": [
    ("kb", I("infographic_05_vietnam_pricing"), 24.0, "pr"),
    ("vid", S("halong_bay_sailing"), 9.5, 12),
    ("vid", S("halong_bay_scenic"), 6.5, 2)],
"07_cambodia": [
    ("vid", N("narrator_04_angkor"), 10.0, 0),
    ("kb", I("infographic_06_angkor_access"), 20.0, "zi"),
    ("vid", N("narrator_04_angkor"), 18.0, ("slow", 0, 0.55)),
    ("kb", I("infographic_07_cambodia_activities"), 20.0, "pl"),
    ("vid", N("narrator_04_angkor"), 5.0, 4)],
"08_thailand": [
    ("vid", N("narrator_05_bangkok"), 10.0, 0),
    ("vid", S("bangkok_street_food"), 13.5, 0),
    ("vid", N("narrator_06_chiang_mai"), 10.0, 0),
    ("vid", S("thai_cooking_fire"), 13.5, 11),
    ("kb", I("infographic_08_thailand_access"), 9.5, "zo"),
    ("kb", I("infographic_09_thailand_activities"), 9.5, "zi"),
    ("kb", I("infographic_10_thailand_pricing"), 9.5, "pr")],
"09_china_arrival": [
    ("vid", N("narrator_07_great_wall"), 10.0, 0),
    ("vid", S("great_wall_mixkit"), 7.0, 0),
    ("kb", I("infographic_11_china_access"), 22.5, "zi")],
"10_china_activities": [
    ("vid", N("narrator_08_china_corridor"), 10.0, 0),
    ("kb", I("infographic_12_china_activities"), 20.0, "pl"),
    ("kb", I("infographic_13_china_pricing"), 20.0, "zo")],
"11_verdict": [
    ("kb", I("infographic_14_final_comparison"), 22.0, "zi"),
    ("kb", I("infographic_15_why_china_wins"), 17.0, "zo")],
"12_closing": [
    ("vid", S("bangkok_lights"), 12.0, 20),
    ("vid", S("great_wall_mixkit"), 7.0, 0),
    ("vid", N("narrator_01_planning_table"), 9.5, 0)],
}

KB = {  # zoompan variants (D = frame count placeholder)
 "zi": "z='1+0.10*on/(D-1)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
 "zo": "z='1.10-0.10*on/(D-1)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
 "pl": "z='1.08':x='(iw-iw/zoom)*on/(D-1)':y='ih/2-(ih/zoom/2)'",
 "pr": "z='1.08':x='(iw-iw/zoom)*(1-on/(D-1))':y='ih/2-(ih/zoom/2)'",
}
VIDF = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p"

seg_paths, seg_idx = [], 0
def render_shot(kind, src, d, opt, fade_in=0.0, fade_out=0.0):
    global seg_idx
    out = f"{SEG}/{seg_idx:03d}.ts"; seg_idx += 1
    if os.path.exists(out) and os.path.getsize(out) > 10000:
        seg_paths.append(out); return
    fades = ""
    if fade_in:  fades += f",fade=t=in:st=0:d={fade_in}"
    if fade_out: fades += f",fade=t=out:st={d-fade_out}:d={fade_out}"
    if kind == "kb":
        frames = int(round(d*FPS))
        zp = KB[opt].replace("D", str(frames))
        vf = (f"scale=3072:2048,zoompan={zp}:d={frames}:s={W}x{H}:fps={FPS},"
              f"format=yuv420p,setsar=1{fades}")
        cmd = ["ffmpeg","-y","-loop","1","-i",src,"-t",f"{d:.3f}","-vf",vf,
               "-an","-c:v","libx264","-preset","veryfast","-crf","18",out]
    else:
        if isinstance(opt, tuple) and opt[0] == "slow":
            _, inp, factor = opt
            src_need = d*factor
            vf = f"trim=start={inp}:duration={src_need:.3f},setpts=PTS/{factor},{VIDF},tpad=stop_mode=clone:stop_duration=2,trim=duration={d:.3f},setpts=PTS-STARTPTS{fades}"
        else:
            avail = dur(src) - float(opt)
            take = min(d, max(avail - 0.05, 0.5))
            vf = f"trim=start={opt}:duration={take:.3f},setpts=PTS-STARTPTS,{VIDF},tpad=stop_mode=clone:stop_duration={max(d-take,0)+0.5:.3f},trim=duration={d:.3f},setpts=PTS-STARTPTS{fades}"
        cmd = ["ffmpeg","-y","-i",src,"-vf",vf,"-an",
               "-c:v","libx264","-preset","veryfast","-crf","18",out]
    run(cmd); seg_paths.append(out)

# ---------------- timeline math ----------------
starts, t = {}, TITLE_DUR
for s in SECTIONS:
    starts[s] = t
    t += vod[s] + GAP
TOTAL = t + CREDITS_DUR
print(json.dumps({s: round(starts[s],2) for s in SECTIONS}, indent=0))
print(f"TOTAL: {TOTAL:.1f}s ({TOTAL/60:.1f} min)")

# ---------------- render video segments ----------------
# Title card: PIL-rendered (infographic_01 text is garbled), slow zoom, fade in/out
run(["python3", f"{ROOT}/make_title.py"])
render_shot("kb", f"{ROOT}/title.png", TITLE_DUR, "zi", fade_in=0.8, fade_out=0.6)
for s in SECTIONS:
    shots = PLAN[s]
    target = vod[s] + GAP
    plan_sum = sum(x[2] for x in shots)
    k = target / plan_sum
    ds = [x[2]*k for x in shots]
    ds[-1] += target - sum(ds)  # rounding remainder
    for j,(kind,src,_,opt) in enumerate(shots):
        fi = 0.5 if j == 0 else 0.0
        fo = 0.4 if j == len(shots)-1 else 0.0
        render_shot(kind, src, ds[j], opt, fi, fo)
    print(f"rendered {s}: {len(shots)} shots -> {target:.1f}s")

# Credits card (PNG pre-rendered by make_credits.py — ffmpeg lacks drawtext)
credits = f"{SEG}/credits.ts"
run(["python3", f"{ROOT}/make_credits.py"])
run(["ffmpeg","-y","-loop","1","-i",f"{ROOT}/credits.png","-t",f"{CREDITS_DUR}",
 "-vf",f"fps={FPS},format=yuv420p,fade=t=in:st=0:d=1,fade=t=out:st={CREDITS_DUR-1.5}:d=1.5",
 "-an","-c:v","libx264","-preset","veryfast","-crf","18",credits])
seg_paths.append(credits)

# ---------------- concat video ----------------
with open(f"{SEG}/list.txt","w") as f:
    for p in seg_paths: f.write(f"file '{p}'\n")
run(["ffmpeg","-y","-f","concat","-safe","0","-i",f"{SEG}/list.txt","-c","copy",f"{ROOT}/video_track.mp4"])

# ---------------- audio: VO placed at section starts ----------------
ins, fl = [], []
for i,s in enumerate(SECTIONS):
    ins += ["-i", VO(s)]
    ms = int((starts[s]+0.25)*1000)
    fl.append(f"[{i}:a]aresample=48000,pan=mono|c0=.5*c0+.5*c1,adelay={ms}|{ms}[v{i}]")
mix = "".join(f"[v{i}]" for i in range(len(SECTIONS)))
fl.append(f"{mix}amix=inputs={len(SECTIONS)}:normalize=0,apad=whole_dur={TOTAL}[vo]")
run(["ffmpeg","-y",*ins,"-filter_complex",";".join(fl),"-map","[vo]",
     "-t",f"{TOTAL}","-c:a","pcm_s16le",f"{ROOT}/vo_track.wav"])

# ---------------- audio: music bed in 3 movements ----------------
M = f"{ROOT}/music"
t_china = starts["09_china_arrival"]
lenA = 98.0                      # Prelude and Action, natural length
lenB = t_china - lenA            # Ascending the Vale (looped)
lenC = TOTAL - t_china           # Impact Prelude to end
fl = [
 f"[0:a]aresample=48000,atrim=duration={lenA},afade=t=in:d=1.5,afade=t=out:st={lenA-3}:d=3,volume=0.13[m0]",
 f"[1:a]aloop=loop=-1:size=2e9,aresample=48000,atrim=duration={lenB},afade=t=in:d=3,afade=t=out:st={lenB-3}:d=3,volume=0.11[m1]",
 f"[2:a]aresample=48000,atrim=duration={lenC},afade=t=in:d=2,afade=t=out:st={lenC-5}:d=5,volume=0.14[m2]",
 "[m0][m1][m2]concat=n=3:v=0:a=1[mus]",
]
run(["ffmpeg","-y","-i",f"{M}/Prelude_and_Action.mp3","-i",f"{M}/Ascending_the_Vale.mp3",
     "-i",f"{M}/Impact_Prelude.mp3","-filter_complex",";".join(fl),"-map","[mus]",
     "-t",f"{TOTAL}","-c:a","pcm_s16le",f"{ROOT}/music_track.wav"])

# ---------------- final mux ----------------
run(["ffmpeg","-y","-i",f"{ROOT}/video_track.mp4","-i",f"{ROOT}/vo_track.wav",
     "-i",f"{ROOT}/music_track.wav","-filter_complex",
     "[1:a]volume=1.6[v];[2:a][v]amix=inputs=2:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=11[a]",
     "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k",
     "-movflags","+faststart",f"{ROOT}/../The_Great_Asian_Family_Expedition.mp4"])
print("DONE:", f"{ROOT}/../The_Great_Asian_Family_Expedition.mp4")
