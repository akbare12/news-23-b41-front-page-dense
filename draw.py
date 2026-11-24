#!/usr/bin/env python3
"""news-23 b41 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def f(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

BLACK = (10, 10, 10)
NAVY = (16, 32, 86)
TEAL = (0, 128, 128)
GOLD = (184, 134, 11)
RED = (178, 24, 24)
PURPLE = (110, 44, 140)
GREEN = (28, 110, 44)
BLUE = (28, 80, 170)
BROWN = (122, 74, 18)
GREY = (90, 90, 90)
LIGHT = (238, 238, 238)

def wrap(text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def chip(x, y, label, color):
    font = f(FB, 9)
    tw = d.textlength(label, font=font)
    w_ = tw + 10
    d.rounded_rectangle([x, y, x + w_, y + 14], radius=2, fill=color)
    d.text((x + 5, y + 2), label, font=font, fill="white")
    return w_

def trunc(text, font, maxw):
    if d.textlength(text, font=font) <= maxw:
        return text
    t = text
    while t and d.textlength(t + "\u2026", font=font) > maxw:
        t = t[:-1]
    return t + "\u2026"

# ---------- masthead ----------
d.rectangle([0, 0, W, 56], fill=BLACK)
d.text((12, 6), "THE WORLD TODAY", font=f(FB, 40), fill="white")
d.text((1012, 18), "MONDAY 23 NOVEMBER 2026", font=f(FB, 19), fill=(255, 196, 0), anchor="ra")

# ---------- kicker ----------
d.text((12, 60), "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
       font=f(FB, 13), fill=RED)

# ---------- number strip: 2 rows x 5 ----------
nums = [
    [("-3.3%", "KOSPI", RED), ("5.3", "US-CHINA POWER GAP", NAVY), ("11,762", "EBOLA CASES, DRC", GREEN),
     ("10T won", "SEOUL STABILISATION FUND", BROWN), ("2%", "BILLIONAIRE TAX IN PARIS", PURPLE)],
    [("$450M", "SKUBAL DEAL", PURPLE), ("165", "RUSSIAN MISSILES IN A WEEK", RED), ("12,000", "CLEARED IN MANCHESTER", BLUE),
     ("264 kg", "EXPLOSIVES SEIZED IN LEBANON", BROWN), ("$107.3B", "ANTHROPIC IPO \u2014 LARGEST", PURPLE)],
]
colw = 1008 / 5
for r, row in enumerate(nums):
    y0 = 80 + r * 34
    for i, (num, lab, col) in enumerate(row):
        x = 12 + i * colw
        d.text((x, y0), num, font=f(FB, 20), fill=col)
        d.text((x, y0 + 21), lab, font=f(FB, 8), fill=BLACK)

# ---------- region bar ----------
regions = [("ASIA-PACIFIC 7", TEAL, 208), ("AMERICAS 8", NAVY, 208), ("MIDDLE EAST 6", GOLD, 178),
           ("EUROPE 5", PURPLE, 158), ("AFRICA 3", RED, 140), ("WORLD 2", GREY, 116)]
x = 8
for name, col, w_ in regions:
    d.rectangle([x, 150, x + w_, 164], fill=col)
    if name == "WORLD 2":
        d.text((x + w_ - 6, 152), name, font=f(FB, 10), fill="white", anchor="ra")
    else:
        d.text((x + w_ / 2, 152), name, font=f(FB, 10), fill="white", anchor="ma")
    x += w_

# ---------- UTC strip ----------
d.rectangle([0, 166, W, 180], fill=NAVY)
d.text((12, 169), "THE DAY IN UTC    ~00:00 Kospi dives    ~06:30 Guterres opens    ~09:00 Power Index    ~12:00 Paris 2% tax    ~15:00 Kyiv missiles    ~18:00 IPO $97.17",
       font=f(FB, 9), fill="white")
d.text((1012, 169), "~ APPROX", font=f(FB, 9), fill=(200, 200, 200), anchor="ra")

# ---------- hero scenes ----------
HX = [8, 348, 688]
HW = [332, 332, 328]
SY, SH = 182, 128

# scene 1: Kospi chart
d.rectangle([HX[0], SY, HX[0] + HW[0], SY + SH], fill=(12, 24, 64))
d.text((HX[0] + 8, SY + 4), "-3.3%", font=f(FB, 26), fill=(255, 64, 64))
# skyline
import random
random.seed(41)
bx = HX[0] + 10
while bx < HX[0] + HW[0] - 14:
    bw = random.randint(16, 26)
    bh = random.randint(28, 62)
    d.rectangle([bx, SY + SH - bh, bx + bw, SY + SH], fill=(38, 58, 110))
    for wy in range(SY + SH - bh + 5, SY + SH - 4, 9):
        for wx in range(bx + 3, bx + bw - 3, 7):
            if random.random() < 0.5:
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 210, 90))
    bx += bw + 4
# descending chart line
pts = [(HX[0] + 12 + i * 30, SY + 52 + (i * 7 if i < 5 else 40 + (i - 5) * 4)) for i in range(11)]
pts[-1] = (pts[-1][0], SY + 96)
d.line(pts, fill=(255, 90, 90), width=3)
for px, py in pts:
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 210, 90))
d.rectangle([HX[0], SY + SH, HX[0] + HW[0], SY + SH + 16], fill=BLACK)
d.text((HX[0] + 8, SY + SH + 2), "KOSPI 4,708.54  \u00b7  -161 PTS", font=f(FB, 11), fill="white")

# scene 2: Guterres globe
d.rectangle([HX[1], SY, HX[1] + HW[1], SY + SH], fill=(0, 122, 122))
d.text((HX[1] + 10, SY + 6), "150 DELEGATES", font=f(FB, 27), fill=(255, 205, 0))
d.text((HX[1] + 10, SY + 38), "BACK A RISK", font=f(FB, 27), fill="white")
d.text((HX[1] + 10, SY + 70), "FRAMEWORK", font=f(FB, 27), fill="white")
# globe bottom-right
gx, gy, gr = HX[1] + HW[1] - 34, SY + SH - 30, 20
d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(180, 235, 235), outline="white", width=2)
d.ellipse([gx - 8, gy - gr, gx + 8, gy + gr], outline=(0, 90, 90), width=1)
d.line([gx - gr, gy, gx + gr, gy], fill=(0, 90, 90), width=1)
d.rectangle([HX[1], SY + SH, HX[1] + HW[1], SY + SH + 16], fill=BLACK)
d.text((HX[1] + 8, SY + SH + 2), "UN  \u00b7  BRIDGETOWN", font=f(FB, 11), fill="white")

# scene 3: power index bars
d.rectangle([HX[2], SY, HX[2] + HW[2], SY + SH], fill=(250, 244, 224))
d.text((HX[2] + 8, SY + 4), "NARROWEST SINCE 2018", font=f(FB, 11), fill=BLACK)
d.text((HX[2] + HW[2] - 8, SY + 4), "GAP 5.3", font=f(FB, 11), fill=GOLD, anchor="ra")
bars = [("78.9", "US", NAVY, 92), ("73.6", "CHINA", RED, 86), ("40.5", "INDIA", GOLD, 48)]
base = SY + SH - 18
bx = HX[2] + 16
for val, lab, col, bh in bars:
    d.rectangle([bx, base - bh, bx + 76, base], fill=col)
    d.text((bx + 38, base - bh + 8), val, font=f(FB, 15), fill="white", anchor="ma")
    d.text((bx + 38, base + 2), lab, font=f(FB, 10), fill=BLACK, anchor="ma")
    bx += 100
d.rectangle([HX[2], SY + SH, HX[2] + HW[2], SY + SH + 16], fill=BLACK)
d.text((HX[2] + 8, SY + SH + 2), "ASIA POWER INDEX 2026", font=f(FB, 11), fill="white")

# ---------- hero text ----------
heroes = [
    (1, "AI ROUT HITS ASIA", "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5.", "KOREA EXCHANGE"),
    (2, "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE", "UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.", "UNITED NATIONS"),
    (3, "US LEAD OVER CHINA AT RECORD LOW", "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.", "LOWY INSTITUTE"),
]
TY = SY + SH + 20
for i, (n, head, body, src) in enumerate(heroes):
    x = HX[i]
    w_ = HW[i]
    d.ellipse([x, TY, x + 20, TY + 20], fill=RED)
    d.text((x + 10, TY + 3), str(n), font=f(FB, 12), fill="white", anchor="ma")
    hl = wrap(head, f(FB, 15), w_ - 26)
    hy = TY
    for ln in hl[:2]:
        d.text((x + 26, hy), ln, font=f(FB, 15), fill=BLACK)
        hy += 17
    by = TY + 36
    for ln in wrap(body, f(FR, 11), w_)[:2]:
        d.text((x, by), ln, font=f(FR, 11), fill=BLACK)
        by += 13
    d.text((x, TY + 66), src, font=f(FR, 9), fill=GREY)
    chip(x + w_ - 62, TY + 64, "REPORTED", NAVY)

# ---------- MORE bar ----------
d.rectangle([0, 414, W, 430], fill=BLACK)
d.text((12, 417), "MORE OF THE DAY  \u2014  10 STORIES", font=f(FB, 12), fill="white")

# ---------- 10 cards ----------
cards = [
    ("AMERICAS", TEAL, "BESSENT: NVIDIA ANSWERS", "Treasury chief wants China answers.", "Reuters", "REPORTED", NAVY),
    ("FBI", PURPLE, "FBI PROBES NCIC HACK", "Hackers hit police NCIC database.", "AP", "REPORTED", NAVY),
    ("WHITE HOUSE", GOLD, "TRUMP: IRAN STRIKES MAY RESUME", "Strikes may resume in New Year.", "Reuters", "REPORTED", NAVY),
    ("MARKETS", GREEN, "US FUTURES JUMP 3%", "Holiday rally lifts futures 3%.", "Bloomberg", "REPORTED", NAVY),
    ("SPORT", RED, "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED", NAVY),
    ("SPORT", RED, "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice, dies.", "ESPN", "REPORTED", NAVY),
    ("LEGAL", PURPLE, "STATES SUE SPACEX", "Ten states challenge AI claims.", "AP", "REPORTED", NAVY),
    ("TECH", NAVY, "ANTHROPIC IPO: $107.3B", "Raised at $83; closes $97.17.", "WSJ", "REPORTED", NAVY),
    ("EUROPE", GOLD, "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: three Kh-101s crossed.", "AP", "CLAIM", RED),
    ("SPACE", GREY, "RUSSIAN NUCLEAR SATELLITE", "Intel: satellite may carry a nuke.", "Reuters", "CLAIM", RED),
]
CW = 200
CGAP = 4
for idx, (cat, ccol, head, body, src, chip_lab, chip_col) in enumerate(cards):
    r, c = divmod(idx, 5)
    x = 8 + c * (CW + CGAP)
    y = 434 + r * 66
    d.rectangle([x, y, x + CW, y + 62], outline=(200, 200, 200), width=1)
    d.rectangle([x, y, x + CW, y + 14], fill=ccol)
    d.text((x + 4, y + 1), cat, font=f(FB, 9), fill="white")
    d.text((x + CW - 4, y + 1), str(idx + 1), font=f(FB, 9), fill="white", anchor="ra")
    hl = wrap(head, f(FB, 11), CW - 8)
    hy = y + 17
    for ln in hl[:2]:
        d.text((x + 4, hy), ln, font=f(FB, 11), fill=BLACK)
        hy += 12
    d.text((x + 4, y + 43), trunc(body, f(FR, 9), CW - 72), font=f(FR, 9), fill=BLACK)
    d.text((x + 4, y + 52), src, font=f(FR, 8), fill=GREY)
    chip(x + CW - 62, y + 50, chip_lab, chip_col)

# ---------- map + ALSO ----------
d.rectangle([0, 570, W, 586], fill=BLACK)
d.text((12, 573), "WHERE IT HAPPENED", font=f(FB, 12), fill="white")
d.text((348, 573), "ALSO ON MONDAY", font=f(FB, 12), fill="white")

# map area
d.rectangle([8, 590, 336, 786], fill=(220, 232, 245))
for gx in range(8, 336, 16):
    d.line([gx, 590, gx, 786], fill=(200, 214, 232), width=1)
for gy in range(590, 786, 16):
    d.line([8, gy, 336, gy], fill=(200, 214, 232), width=1)
# stylised continents
d.ellipse([20, 600, 130, 700], fill=(140, 190, 120))
d.ellipse([60, 690, 140, 760], fill=(140, 190, 120))
d.ellipse([150, 600, 250, 690], fill=(140, 190, 120))
d.ellipse([180, 700, 250, 770], fill=(140, 190, 120))
d.ellipse([255, 600, 330, 670], fill=(140, 190, 120))
d.ellipse([270, 720, 330, 770], fill=(140, 190, 120))
pins = [(70, 612), (105, 745), (300, 622), (60, 660), (95, 640), (190, 668),
        (55, 628), (45, 690), (80, 700), (95, 720), (185, 612), (205, 630), (245, 608)]
for i, (px, py) in enumerate(pins, 1):
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline="white", width=1)
    d.text((px, py - 6), str(i), font=f(FB, 9), fill="white", anchor="ma")
d.text((12, 790), "Pins 1\u201313: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing", font=f(FR, 8), fill=BLACK)
d.text((12, 801), "4 Washington \u00b7 5 New York \u00b7 6 Tehran \u00b7 7 Chicago", font=f(FR, 8), fill=BLACK)
d.text((12, 812), "8 San Francisco \u00b7 9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 Kyiv \u00b7 13 Moscow", font=f(FR, 8), fill=BLACK)

# ALSO list, 2 columns x 9
also = [
    "14. Paris: 100+ back 2% billionaire tax", "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week", "17. COP31: the day after pact rejected",
    "18. Benghazi: UN demands port probe", "19. Israel unity talks resume",
    "20. Gaza: two killed in Israeli strike", "21. West Bank settler attacks",
    "22. Iran war: no deal in sight", "23. Lebanon seizes 264 kg explosives",
    "24. Bahrain: strike hits plant, 2 hurt", "25. Sudan: defences down drones",
    "26. DRC: fighting traps Ebola teams", "27. Bangladesh: Hasina jailed if she returns",
    "28. Seoul minister quits in exam row", "29. SK Telecom -7.3% as hype cools",
    "30. China eases margin rules", "31. Seoul readies 10T-won fund",
]
for i, item in enumerate(also):
    col = i // 9
    row = i % 9
    x = 348 + col * 336
    y = 594 + row * 25
    d.text((x, y), item, font=f(FR, 11), fill=BLACK)

# ---------- DATE CHECK ----------
d.rectangle([8, 832, 1016, 916], outline=RED, width=2)
d.text((16, 838), "DATE CHECK", font=f(FB, 13), fill=RED)
d.text((1008, 840), "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY", font=f(FB, 8), fill=RED, anchor="ra")
d.text((16, 858), "LEFT OUT \u2014 NOT 23 NOV: Democrats reach 258 seats (22 Nov) \u00b7 Sparta II fire (22 Nov) \u00b7 El Chapo Isidro", font=f(FR, 11), fill=BLACK)
d.text((16, 873), "captured (22 Nov) \u00b7 EU-Indonesia pact (21 Nov) \u00b7 Nigeria boat (21 Nov) \u00b7 ICJ Myanmar ruling (19 Nov)", font=f(FR, 11), fill=BLACK)
d.text((16, 892), "NOT YET: Dymer search continues (14 missing) \u00b7 4 House races uncalled \u00b7 COP32 venue not set \u00b7 WHO evacuating trapped Ebola staff", font=f(FR, 11), fill=BLACK)

# ---------- sources + footer ----------
d.text((12, 924), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 NYT \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).", font=f(FR, 9), fill=BLACK)
d.text((12, 938), "CHIPS: REPORTED = confirmed by wires \u00b7 CLAIM = one side's claim, not independently confirmed \u00b7 ONGOING = still developing", font=f(FR, 9), fill=BLACK)
d.text((12, 952), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.", font=f(FR, 9), fill=GREY)
d.rectangle([0, 972, W, 1024], fill=BLACK)
d.text((512, 984), "THE WORLD TODAY  \u2014  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions", font=f(FB, 14), fill=(255, 196, 0), anchor="ma")

img.save("/home/hatch/workspace/makefun/news-23-b41-dense-build/entry.png")
print("saved entry.png", img.size)
