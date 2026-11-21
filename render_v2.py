#!/usr/bin/env python3
"""Rebuild entry.png for the-passport-page-of-a-countr-2-20261121-0318 (v2).

DRAFT — written 21 Nov 2026 ~11:50 WIB, NOT yet run. The rebuild was
blocked by an execution-risk check on the repo/competition content, so
this script is staged here for the parent to copy into the repo and run
after Joni gives the go-ahead in plain words.

What v2 changes vs v1 (commit ac9ce401):
  * Holder portrait: photorealistic photo of a fictional woman
    (Mara Iversen), generated with the image tool — NOT the flat-vector
    cartoon of v1. Source file: portrait-mara-iversen.webp (bundled in
    the repo next to this script).
  * Data page rebuilt to a real passport format: Indonesian passport /
    ICAO Doc 9303 TD3 data page. Photo on the left, personal-data
    fields beside it (bilingual Indonesian/English labels, as on a real
    Indonesian passport), MRZ (2 x 44 chars) at the bottom. The
    REMARKS block is dropped from the data page (a real biodata page
    has none); the story now lives on the visa page as before.

What v2 KEEPS exactly (all verified in v1 — do not change):
  * Country: Republic of Caelmar, tide republic, capital Lowtown.
  * Holder: Mara Iversen, Warden of the Sands; born 12 JUN 1988,
    Lowtown; issued 14 MAR 2024, expires 14 MAR 2034; doc CAE004821.
  * 4 stamps, all after issue, in travel order: Bergen 02 JUN 2024,
    Esbjerg 21 JUN 2024, Harwich 19 SEP 2025, Lowtown 03 OCT 2025.
  * Schengen transit visa 02 JUN 2024 - 02 DEC 2024, multiple entries,
    issued Bergen, fee 35 EUR.
  * CONDITIONS OF ISSUE — valid only while the territory is above
    water (unchanged text).
  * MRZ lines (ICAO 9303, all five check digits recomputed by hand
    21 Nov 2026 and correct — doc 5, birth 7, expiry 1, personal 0,
    composite 0):
        P<CAEIVERSEN<<MARA<<<<<<<<<<<<<<<<<<<<<<<<
        CAE0048215CAE8806127F3403141<<<<<<<<<<<<<<00
  * Right (visa) page: unchanged from v1.

Rendering: Pillow at 3x supersample, LANCZOS downscale to 1024x1024,
PNG. The script FAILS LOUDLY (exit 1) if the output is not 1024x1024
or is over 1,048,576 bytes, or if the portrait file is missing.
Long lines (masthead, stamp lines) auto-shrink to fit their boxes.

Usage (from the repo root, after copying this script + the portrait in):
    python3 render_v2.py            # writes entry.png in the repo root
    python3 render_v2.py --out /tmp/entry-v2.png
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
PORTRAIT = HERE / "portrait-mara-iversen.webp"

# ---- geometry (final 1024x1024 coordinates; rendered at SS=3) ----
SS = 3
W = H = 1024

NAVY = (31, 58, 95)
NAVY_DARK = (22, 44, 74)
INK = (32, 40, 56)
CREAM = (250, 246, 236)
DESK = (46, 52, 64)
DESK_DARK = (36, 41, 52)
RED = (178, 44, 44)
BLUE = (28, 84, 160)
TEAL = (16, 120, 110)
GREY_LABEL = (96, 104, 118)
MAP_BG = (226, 236, 244)
MAP_LAND = (196, 205, 180)

# Pages: left x 62..478, right x 505..962, y 60..964 (v1 geometry).
PAGE_L = (62, 60, 478, 964)
PAGE_R = (505, 60, 962, 964)


def S(v):
    return v * SS


def font(name, size):
    """DejaVu by name, falling back to PIL's built-in bitmap font."""
    candidates = {
        "serif-bold": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
            "/usr/share/fonts/dejavu/DejaVuSerif-Bold.ttf",
        ],
        "serif-italic": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
            "/usr/share/fonts/dejavu/DejaVuSerif-Italic.ttf",
        ],
        "sans": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/dejavu/DejaVuSans.ttf",
        ],
        "sans-bold": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
        ],
        "mono": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/usr/share/fonts/dejavu/DejaVuSansMono.ttf",
        ],
    }
    for path in candidates[name]:
        try:
            return ImageFont.truetype(path, S(size))
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def text_w(s, f, size):
    """Width of s in final-scale pixels."""
    probe = Image.new("RGB", (8, 8))
    d = ImageDraw.Draw(probe)
    box = d.textbbox((0, 0), s, font=font(f, size))
    return (box[2] - box[0]) / SS


def text(d, xy, s, f, size, fill, anchor="la"):
    d.text((S(xy[0]), S(xy[1])), s, font=font(f, size), fill=fill,
           anchor=anchor)


def fit_text(d, xy, s, f, size, max_w, fill, anchor="la"):
    """Draw s, shrinking the font until it fits max_w final px."""
    while size > 8 and text_w(s, f, size) > max_w:
        size -= 1
    text(d, xy, s, f, size, fill, anchor=anchor)
    return size


def wrap(d, s, f, size, max_w, xy, fill, leading=None):
    """Word-wrap s into lines of at most max_w final px; returns lines used."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(trial, f, size) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    lh = leading if leading is not None else int(size * 1.45)
    y = xy[1]
    for line in lines:
        text(d, (xy[0], y), line, f, size, fill)
        y += lh
    return len(lines)


def double_border(d, box, color=NAVY, outer=2, gap=5):
    x0, y0, x1, y1 = box
    d.rectangle([S(x0), S(y0), S(x1), S(y1)], outline=color, width=S(outer))
    d.rectangle(
        [S(x0 + gap), S(y0 + gap), S(x1 - gap), S(y1 - gap)],
        outline=color, width=S(1),
    )


def hrule(d, x0, x1, y, color=NAVY, width=1):
    d.line([S(x0), S(y), S(x1), S(y)], fill=color, width=S(width))


def emblem(d, cx, cy, r):
    """Caelmar seal: concentric rings, horizon lines, low-tide sun."""
    d.ellipse(
        [S(cx - r), S(cy - r), S(cx + r), S(cy + r)],
        outline=NAVY, width=S(2),
    )
    d.ellipse(
        [S(cx - r + 6), S(cy - r + 6), S(cx + r - 6), S(cy + r - 6)],
        outline=NAVY, width=S(1),
    )
    d.ellipse(
        [S(cx - 9), S(cy - 16), S(cx + 9), S(cy + 2)],
        fill=(232, 164, 32),
    )
    for i, yy in enumerate((cy + 6, cy + 12, cy + 18)):
        d.arc(
            [S(cx - r + 10), S(yy - 8), S(cx + r - 10), S(yy + 8)],
            start=0, end=180, fill=NAVY, width=S(2 if i == 1 else 1),
        )


def stamp(d, box, color, lines):
    """A rubber stamp: double rounded border, centred lines, auto-fit."""
    x0, y0, x1, y1 = box
    d.rounded_rectangle(
        [S(x0), S(y0), S(x1), S(y1)], radius=S(10),
        outline=color, width=S(2),
    )
    d.rounded_rectangle(
        [S(x0 + 5), S(y0 + 5), S(x1 - 5), S(y1 - 5)], radius=S(7),
        outline=color, width=S(1),
    )
    inner_w = (x1 - x0) - 16
    total_h = sum(sz * 1.5 for _, sz in lines)
    y = y0 + (y1 - y0 - total_h) / 2
    for s, sz in lines:
        while sz > 9 and text_w(s, "sans-bold", sz) > inner_w:
            sz -= 1
        w = text_w(s, "sans-bold", sz)
        text(d, (x0 + (x1 - x0 - w) / 2, y), s, "sans-bold", sz, color)
        y += sz * 1.5


def draw_data_page(d):
    x0, y0, x1, y1 = PAGE_L
    d.rectangle([S(x0), S(y0), S(x1), S(y1)], fill=CREAM)
    double_border(d, PAGE_L)

    # ---- masthead (unchanged from v1) ----
    emblem(d, 118, 128, 34)
    fit_text(d, (168, 100), "REPUBLIC OF CAELMAR", "serif-bold", 26,
             x1 - 22 - 168, NAVY)
    fit_text(d, (168, 132), "P A S S P O R T", "serif-bold", 26,
             x1 - 22 - 168, NAVY)
    text(d, (168, 160), "PASPOR  ·  PASSPORT", "sans", 11, GREY_LABEL)
    hrule(d, x0 + 22, x1 - 22, 188)

    # ---- photo (left): load + centre-crop to the photo-box aspect ----
    photo = (85, 208, 235, 400)  # 150 x 192, passport ratio
    px0, py0, px1, py1 = photo
    portrait = Image.open(PORTRAIT).convert("RGB")
    tw, th = px1 - px0, py1 - py0
    iw, ih = portrait.size
    target = tw / th
    if iw / ih > target:  # too wide: crop sides
        nw = int(ih * target)
        off = (iw - nw) // 2
        portrait = portrait.crop((off, 0, off + nw, ih))
    else:  # too tall: crop top/bottom, keeping the face (crop more top)
        nh = int(iw / target)
        off = int((ih - nh) * 0.35)
        portrait = portrait.crop((0, off, iw, off + nh))
    portrait = portrait.resize((S(tw), S(th)), Image.LANCZOS)
    return portrait, photo  # pasted by caller (needs the base image)


def draw_data_page_fields(d):
    x0, y0, x1, y1 = PAGE_L
    px0, py0, px1, py1 = 85, 208, 235, 400

    # signature under the photo (real biodata pages carry it here)
    text(d, (px0, 414), "Mara Iversen", "serif-italic", 20, INK)
    hrule(d, px0, px1, 446, color=INK)
    text(d, (px0, 452), "TANDA TANGAN PEMEGANG /", "sans", 9, GREY_LABEL)
    text(d, (px0, 466), "HOLDER'S SIGNATURE", "sans", 9, GREY_LABEL)

    # data fields, right of the photo (bilingual labels, Indonesian first)
    fx = 252
    fields = [
        ("JENIS / TYPE", "P"),
        ("KODE NEGARA / COUNTRY CODE", "CAE"),
        ("NO. PASPOR / PASSPORT NO.", "CAE004821"),
        ("NAMA / NAME", "MARA IVERSEN"),
        ("KEWARGANEGARAAN / NATIONALITY", "CAELMAR"),
        ("TEMPAT LAHIR / PLACE OF BIRTH", "LOWTOWN"),
        ("TANGGAL LAHIR / DATE OF BIRTH", "12 JUN 1988"),
        ("JENIS KELAMIN / SEX", "F"),
    ]
    y = 208
    for label, value in fields:
        text(d, (fx, y), label, "sans", 10, GREY_LABEL)
        text(d, (fx, y + 13), value, "sans-bold", 15, NAVY_DARK)
        y += 33
    # fields end ~467; signature block ends ~480 — aligned.

    # ---- issue / expiry / authority (full width, two-line labels) ----
    hrule(d, x0 + 22, x1 - 22, 500)
    text(d, (x0 + 22, 514), "TANGGAL PENGELUARAN", "sans", 10, GREY_LABEL)
    text(d, (x0 + 22, 526), "DATE OF ISSUE", "sans", 10, GREY_LABEL)
    text(d, (x0 + 22, 540), "14 MAR 2024", "sans-bold", 15, NAVY_DARK)
    text(d, (x0 + 258, 514), "TANGGAL HABIS BERLAKU", "sans", 10, GREY_LABEL)
    text(d, (x0 + 258, 526), "DATE OF EXPIRY", "sans", 10, GREY_LABEL)
    text(d, (x0 + 258, 540), "14 MAR 2034", "sans-bold", 15, NAVY_DARK)
    text(d, (x0 + 22, 576), "PEJABAT YANG MENGELUARKAN", "sans", 10, GREY_LABEL)
    text(d, (x0 + 22, 588), "ISSUING AUTHORITY", "sans", 10, GREY_LABEL)
    text(d, (x0 + 22, 602), "TIDE WARDEN'S OFFICE", "sans-bold", 15, NAVY_DARK)

    # ---- MRZ (unchanged, verified) ----
    hrule(d, x0 + 22, x1 - 22, 630)
    text(d, (x0 + 22, 646), "P<CAEIVERSEN<<MARA<<<<<<<<<<<<<<<<<<<<<<<<",
         "mono", 13, INK)
    text(d, (x0 + 22, 670), "CAE0048215CAE8806127F3403141<<<<<<<<<<<<<<00",
         "mono", 13, INK)

    text(d, (x0 + (x1 - x0) / 2, 930), "1", "sans", 11, GREY_LABEL,
         anchor="ma")


def draw_visa_page(d):
    x0, y0, x1, y1 = PAGE_R
    d.rectangle([S(x0), S(y0), S(x1), S(y1)], fill=CREAM)
    double_border(d, PAGE_R)

    text(d, (x0 + 22, 92), "VISAS", "serif-bold", 26, NAVY)
    text(d, (x1 - 22, 100), "PAGES 3-4 · STAMPS", "sans", 10, GREY_LABEL,
         anchor="ra")
    hrule(d, x0 + 22, x1 - 22, 128)

    # ---- map: WHERE IT IS — THE NORTH SEA (unchanged from v1) ----
    mx0, my0, mx1, my1 = x0 + 22, 146, x1 - 22, 296
    d.rectangle([S(mx0), S(my0), S(mx1), S(my1)], fill=MAP_BG,
                outline=NAVY, width=S(1))
    text(d, (mx0 + 10, my0 + 8), "WHERE IT IS — THE NORTH SEA",
         "sans-bold", 12, NAVY_DARK)
    # stylised landmasses (same shapes as v1)
    d.polygon([(S(mx0 + 52), S(my0 + 112)), (S(mx0 + 92), S(my0 + 60)),
               (S(mx0 + 118), S(my0 + 112)), (S(mx0 + 80), S(my0 + 136))],
              fill=MAP_LAND)
    d.polygon([(S(mx1 - 118), S(my0 + 18)), (S(mx1 - 22), S(my0 + 30)),
               (S(mx1 - 34), S(my0 + 78)), (S(mx1 - 108), S(my0 + 62))],
              fill=MAP_LAND)
    text(d, (mx0 + 10, my1 - 24), "UNITED", "sans", 10, GREY_LABEL)
    text(d, (mx0 + 10, my1 - 12), "KINGDOM", "sans", 10, GREY_LABEL)
    text(d, (mx1 - 96, my0 + 34), "NORWAY", "sans", 10, GREY_LABEL)
    text(d, (mx1 - 66, my1 - 34), "DENMARK", "sans", 10, GREY_LABEL)
    # Caelmar: red ring on the sandbank
    ccx, ccy = mx0 + 190, my0 + 78
    d.ellipse([S(ccx - 26), S(ccy - 12), S(ccx + 26), S(ccy + 12)],
              outline=RED, width=S(2))
    d.ellipse([S(ccx - 4), S(ccy - 4), S(ccx + 4), S(ccy + 4)], fill=RED)
    text(d, (ccx + 32, ccy - 10), "CAELMAR", "sans-bold", 14, RED)
    text(d, (ccx + 32, ccy + 6), "LOWTOWN — LOW TIDE ONLY", "sans", 11, RED)

    # ---- four stamps (unchanged from v1) ----
    sy, sh, gap = 316, 108, 16
    sw = (x1 - x0 - 44 - gap) // 2
    stamp(d, (x0 + 22, sy, x0 + 22 + sw, sy + sh), BLUE, [
        ("BERGEN · NORWAY", 15), ("ENTRY", 13), ("02 JUN 2024", 15)])
    stamp(d, (x0 + 22 + sw + gap, sy, x1 - 22, sy + sh), TEAL, [
        ("ESBJERG · DENMARK", 15), ("DEPARTURE", 13), ("21 JUN 2024", 15)])
    stamp(d, (x0 + 22, sy + sh + 14, x0 + 22 + sw, sy + 2 * sh + 14), NAVY, [
        ("HARWICH · UNITED KINGDOM", 13), ("ENTRY", 13), ("19 SEP 2025", 15)])
    stamp(d, (x0 + 22 + sw + gap, sy + sh + 14, x1 - 22, sy + 2 * sh + 14),
          RED, [
        ("LOWTOWN · CAELMAR", 15), ("RE-ENTRY — LOW TIDE", 13),
        ("03 OCT 2025", 15)])

    # ---- CONDITIONS OF ISSUE (unchanged text from v1) ----
    cy0 = sy + 2 * sh + 34
    cy1 = cy0 + 168
    d.rectangle([S(x0 + 22), S(cy0), S(x1 - 22), S(cy1)],
                outline=RED, width=S(2))
    text(d, (x0 + 34, cy0 + 12), "CONDITIONS OF ISSUE", "sans-bold", 14, RED)
    wrap(d, "This passport is valid only while the territory of Caelmar "
            "is above water. The holder must arrive by boat at low tide "
            "and depart before high water. No airport exists in Caelmar.",
         "sans", 15, x1 - x0 - 68, (x0 + 34, cy0 + 42), INK)

    # ---- tide line (unchanged from v1) ----
    ty = cy1 + 18
    text(d, (x0 + 22, ty), "LOW WATER — LOWTOWN   03 OCT 2025",
         "sans-bold", 13, NAVY_DARK)
    text(d, (x0 + 22, ty + 22), "LOW 04:12   ·   HIGH 10:31   ·   LOW 16:47",
         "mono", 13, INK)

    # ---- Schengen transit visa (unchanged from v1) ----
    vy0 = ty + 56
    vy1 = vy0 + 96
    d.rectangle([S(x0 + 22), S(vy0), S(x1 - 22), S(vy1)],
                outline=NAVY, width=S(1))
    text(d, (x0 + 34, vy0 + 10), "VISA — TRANSIT · SCHENGEN AREA",
         "sans-bold", 13, NAVY_DARK)
    text(d, (x0 + 34, vy0 + 38),
         "VALID 02 JUN 2024 – 02 DEC 2024   ·   ENTRIES: MULTIPLE",
         "sans", 12, INK)
    text(d, (x0 + 34, vy0 + 64), "ISSUED BERGEN   ·   FEE PAID 35 EUR",
         "sans", 12, INK)

    text(d, (x0 + (x1 - x0) / 2, 930), "2", "sans", 11, GREY_LABEL,
         anchor="ma")


def render():
    if not PORTRAIT.is_file():
        print("portrait missing: %s" % PORTRAIT, file=sys.stderr)
        return None
    base = Image.new("RGB", (S(W), S(H)), DESK)
    d = ImageDraw.Draw(base)
    d.rectangle([0, 0, S(W) - 1, S(H) - 1], outline=DESK_DARK, width=S(2))

    portrait, photo = draw_data_page(d)
    base.paste(portrait, (S(photo[0]), S(photo[1])))
    d = ImageDraw.Draw(base)  # redraw handle after paste
    d.rectangle([S(photo[0]), S(photo[1]), S(photo[2]), S(photo[3])],
                outline=NAVY, width=S(2))
    draw_data_page_fields(d)
    draw_visa_page(d)

    out = base.resize((W, H), Image.LANCZOS)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(HERE / "entry.png"))
    args = ap.parse_args()

    img = render()
    if img is None:
        return 1
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    size = out.stat().st_size
    print("wrote %s (%d bytes, %dx%d)" % (out, size, img.width, img.height))
    if img.width != 1024 or img.height != 1024:
        print("FAIL: output is not 1024x1024", file=sys.stderr)
        return 1
    if size > 1_048_576:
        print("FAIL: output over the 1 MiB gate", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
