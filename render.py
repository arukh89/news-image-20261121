#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news front page, 1024x1024 PNG.

Build-time only (needs Pillow). The grader runs only main.py, which
copies the committed entry.png. Deterministic: fixed text, fixed
geometry, no network, no clock, no randomness. Run: python3 render.py
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (185, 28, 28)
BLUE = (29, 78, 216)
TEAL = (15, 118, 110)
GOLD = (251, 191, 36)
GREY = (90, 90, 90)
LIGHT = (232, 226, 210)
SKY = (214, 231, 240)

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_S = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=18):
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def panel(draw, x, y, w, h, accent, kicker, headline, body, hsize=17):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                   outline=(180, 175, 160), width=1)
    draw.rectangle([x, y, x + w, y + 5], fill=accent)
    draw.text((x + 10, y + 12), kicker, font=font(FONT_B, 11), fill=accent)
    yy = para(draw, x + 10, y + 30, headline, font(FONT_B, hsize),
              w - 20, leading=hsize + 3)
    para(draw, x + 10, yy + 4, body, font(FONT_R, 12), w - 20, leading=15)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 118], fill=INK)
    d.text((24, 14), "THE WORLD IN ONE DAY",
           font=font(FONT_S, 46), fill=(255, 255, 255))
    d.text((24, 78), "SATURDAY 21 NOVEMBER 2026  •  36 STORIES  •  7 REGIONS",
           font=font(FONT_B, 19), fill=GOLD)

    # Lead row
    panel(d, 24, 126, 620, 168, RED, "MIDDLE EAST — LEAD",
          "RIYADH WAKES TO SIRENS AS 3 HOUTHI MISSILES ARE SHOT DOWN",
          "Saudi defences intercept three ballistic missiles fired at the "
          "capital before dawn on Saturday, the second attack on Riyadh in "
          "days after its tallest skyscraper was struck on Thursday. "
          "Civil-defence alerts sound at 01:53; no casualties reported.",
          hsize=24)
    panel(d, 652, 126, 348, 168, TEAL, "CLIMATE — ANTALYA",
          "COP31 IN OVERTIME: NO DEAL, NO FOSSIL-FUEL LINE",
          "Talks run past Friday's deadline with ~200 countries split over "
          "fossil fuels. Thursday's draft drops the phase-out and a $120bn "
          "adaptation target; a third draft is due Saturday.", hsize=20)

    # Five illustrated panels
    panels = [
        (BLUE, "PERU — QUAKE",
         "M6.7 SHAKES JUNIN, FELT IN LIMA",
         "Deep quake strikes at 00:09 UTC on Saturday. Minor damage to "
         "homes, power cuts and road limits; no deaths reported."),
        (RED, "UKRAINE — POLAND",
         "400+ DRONES, 110+ MISSILES; 2 LAND IN POLAND",
         "Friday night's barrage kills 8 and damages 3 Kyiv bridges. "
         "NATO calls the spillover a grave violation; jets scramble."),
        (INK, "KRYVYI RIH",
         "MISSILE HITS ZELENSKYY'S HOMETOWN: 2 DEAD, 60 HURT",
         "A ballistic strike on Saturday wounds scores, including "
         "children, local officials say."),
        (TEAL, "SPACE — MERCURY",
         "BEPICOLOMBO REACHES MERCURY ORBIT",
         "The joint European-Japanese probe arrives at the innermost "
         "planet after its long cruise across the Solar System."),
        (BLUE, "PHILIPPINES — DAVAO",
         "JET LANDS IN EMERGENCY; ALL 146 SAFE",
         "Air Niugini flight PX19 diverts to Davao on an engine-fire "
         "warning; passengers leave by slides, none hurt."),
    ]
    px = 24
    for accent, kicker, head, body in panels:
        panel(d, px, 302, 188, 158, accent, kicker, head, body, hsize=15)
        px += 196

    # Map strip: schematic continents with numbered pins
    d.rectangle([24, 468, 1000, 588], fill=SKY, outline=(180, 175, 160))
    d.text((36, 476), "WHERE IT HAPPENED — 7 REGIONS",
           font=font(FONT_B, 14), fill=INK)
    continents = [
        (60, 505, 120, 44), (200, 530, 90, 40),
        (330, 500, 90, 40), (430, 530, 100, 40),
        (560, 500, 110, 40), (690, 505, 120, 44),
        (850, 540, 90, 26),
    ]
    for x, y, w, h in continents:
        d.ellipse([x, y, x + w, y + h], fill=(255, 255, 255),
                  outline=(120, 120, 120))
    pins = [(615, 518, "1"), (372, 518, "2"), (242, 548, "3"),
            (352, 512, "4"), (745, 525, "5"), (478, 548, "6"),
            (892, 552, "7")]
    for x, y, n in pins:
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=RED, outline=(255, 255, 255))
        d.text((x - 3, y - 6), n, font=font(FONT_B, 11), fill=(255, 255, 255))
    d.text((36, 566), "1 Riyadh  2 Antalya  3 Peru  4 Kyiv / Poland  "
           "5 Davao  6 Gaza  7 Brussels",
           font=font(FONT_R, 12), fill=INK)

    # Numbers strip
    nums = [("3", "missiles over Riyadh"),
            ("M6.7", "Peru quake"),
            ("146", "safe at Davao"),
            ("400+", "drones, Fri barrage"),
            ("200", "countries at COP31")]
    nx = 24
    for val, label in nums:
        d.rectangle([nx, 596, nx + 188, 648], fill=(255, 255, 255),
                    outline=(180, 175, 160))
        d.text((nx + 10, 602), val, font=font(FONT_B, 22), fill=RED)
        d.text((nx + 10, 628), label, font=font(FONT_R, 11), fill=INK)
        nx += 196

    # Briefs
    d.text((24, 656), "ALSO TODAY — 29 MORE STORIES",
           font=font(FONT_B, 15), fill=INK)
    d.line([24, 678, 1000, 678], fill=INK, width=2)
    briefs = [
        ("GAZA", "Israeli strike kills 3 Palestinians in Gaza City on Saturday."),
        ("HORMUZ", "Tankers hit near the strait as US-Iran talks stall."),
        ("MARKETS", "Nikkei -5.1%; S&P slides into correction in an AI-led sell-off."),
        ("TECH", "Anthropic trades as a ~$2tn company after its record debut."),
        ("HEALTH", "Pancreatic pill makes tumours undetectable in 1 of 12 patients."),
        ("USA", "FBI crime database and USDA payment system reportedly hacked."),
        ("EUROPE", "UK and EU sign three post-Brexit deals in Brussels."),
        ("DENMARK", "Russian defence attache expelled over alleged rapper murder plot."),
        ("EUROPE", "Cost-of-living protests spread across European capitals."),
        ("MEXICO", "Cartel boss 'El Chapo Isidro' detained; FBI top-10 fugitive."),
        ("S. AFRICA", "Phumzile Mlambo-Ngcuka, ex-deputy president, dies at 71."),
        ("ASIA", "EU and Indonesia sign CEPA and IPA trade deals."),
        ("FINLAND", "Russian cargo ship on fire in the Gulf of Finland."),
        ("IRAQ", "Hartha power-station fire in Basra: 4 dead, 35 hurt."),
        ("HAITI", "Salvadoran troops lose 3 soldiers after an explosion."),
        ("INDIA", "Suspected toxic alcohol in Manipur: 11 dead, 180+ in hospital."),
        ("JUSTICE", "World Court: Myanmar committed genocide against the Rohingya."),
        ("CHINA", "Trump, Xi, Putin sign 4-point peace declaration; no Ukraine deal."),
        ("N. KOREA", "IAEA: Yongbyon uranium enrichment plant expanding."),
        ("BANGLADESH", "Violence flares ahead of Hasina's planned return."),
        ("VENEZUELA", "US signs new military deal, 10 months after Maduro's removal."),
        ("SPAIN", "Snap election set for 29 Nov; banking-tax extension planned."),
        ("ITALY", "Tesla self-driving gets conditional approval."),
        ("JAPAN", "Core inflation rises to 2.2% in October."),
        ("PACIFIC", "Cyclone Xavier: marine warnings for the Cook Islands."),
        ("SAUDI", "Orange rain warnings across 34 governorates."),
        ("MONGOLIA", "President resigns; early elections loom."),
        ("MALI", "Russia's Africa Corps flies a new drone against militants."),
        ("ETHIOPIA", "Displacement rises; aid groups warn of a new crisis."),
    ]
    f_tag = font(FONT_B, 12)
    f_txt = font(FONT_R, 12)
    for i, (tag, text) in enumerate(briefs):
        col = 0 if i < 15 else 1
        row = i if i < 15 else i - 15
        x = 24 if col == 0 else 516
        y = 688 + row * 20
        d.text((x, y), f"{i + 8}. {tag} — ", font=f_tag, fill=RED)
        tw = d.textlength(f"{i + 8}. {tag} — ", font=f_tag)
        d.text((x + tw, y), text, font=f_txt, fill=INK)

    # Footer
    d.line([24, 992, 1000, 992], fill=GREY, width=1)
    d.text((24, 996), "Sources: Reuters  •  AP  •  BBC  •  Al Jazeera  •  USGS  •  IAEA  —  "
           "Stories happened or were first reported 21 Nov 2026. Drawn from code; no photos.",
           font=font(FONT_R, 11), fill=GREY)

    img.save("entry.png", format="PNG")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
