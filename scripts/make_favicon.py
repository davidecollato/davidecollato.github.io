"""Generate the site favicons from the "DC" monogram of the editorial theme.

The letters are converted to outlines (EB Garamond Bold), so the SVG favicon
does not depend on fonts installed on the visitor's machine. PNG sizes are
rasterised with Inkscape, the .ico is assembled with Pillow.

Usage:  python3 scripts/make_favicon.py
Needs:  fontTools, Pillow, inkscape, the EB Garamond font (fonts-ebgaramond).
"""

import subprocess
import tempfile
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from PIL import Image

FONT = "/usr/share/fonts/truetype/ebgaramond/EBGaramond12-Bold.ttf"
TEXT = "DC"

# colours of the editorial theme (_sass/theme/_editorial_light.scss)
PAPER = "#f7f4ee"
TEAL = "#1b7f7a"
INK = "#2f2c27"

SIZE = 64          # SVG viewBox
CAP_HEIGHT = 21    # height of the letters in viewBox units
LETTER_GAP = -1.0  # tighten the pair slightly (font units are rescaled)

IMAGES = Path(__file__).resolve().parent.parent / "images"


def letters_path():
    font = TTFont(FONT)
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    names = [cmap[ord(ch)] for ch in TEXT]

    # lay out the glyphs and measure the ink bounding box
    x, placed = 0, []
    bounds = BoundsPen(glyphs)
    for name in names:
        pen = TransformPen(bounds, (1, 0, 0, 1, x, 0))
        glyphs[name].draw(pen)
        placed.append((name, x))
        x += glyphs[name].width
    xmin, ymin, xmax, ymax = bounds.bounds

    scale = CAP_HEIGHT / (ymax - ymin)
    gap = LETTER_GAP / scale
    width = (xmax - xmin + gap * (len(names) - 1)) * scale
    ox = (SIZE - width) / 2 - xmin * scale
    oy = (SIZE + CAP_HEIGHT) / 2 + ymin * scale   # baseline, y axis flipped

    svg_pen = SVGPathPen(glyphs)
    for i, (name, gx) in enumerate(placed):
        dx = gx + i * gap
        pen = TransformPen(svg_pen, (scale, 0, 0, -scale, ox + dx * scale, oy))
        glyphs[name].draw(pen)
    return svg_pen.getCommands()


def favicon_svg():
    c = SIZE / 2
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}">'
        f'<title>Davide Collato</title>'
        f'<circle cx="{c}" cy="{c}" r="30" fill="{PAPER}" stroke="{TEAL}" stroke-width="3.5"/>'
        f'<circle cx="{c}" cy="{c}" r="25.2" fill="none" stroke="{TEAL}" stroke-width="1.2" opacity="0.55"/>'
        f'<path fill="{INK}" d="{letters_path()}"/>'
        f'</svg>\n'
    )


def main():
    svg = favicon_svg()
    (IMAGES / "favicon.svg").write_text(svg)

    pngs = {
        "favicon-32x32.png": 32,
        "favicon-192x192.png": 192,
        "favicon-512x512.png": 512,
        "apple-touch-icon-180x180.png": 180,
    }
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "icon.svg"
        src.write_text(svg)
        for name, px in pngs.items():
            subprocess.run(
                ["inkscape", str(src), "--export-type=png", f"--export-filename={IMAGES / name}",
                 f"--export-width={px}", f"--export-height={px}"],
                check=True, capture_output=True,
            )
        # iOS ignores transparency: give the touch icon a paper background
        touch = Image.open(IMAGES / "apple-touch-icon-180x180.png").convert("RGBA")
        bg = Image.new("RGBA", touch.size, PAPER)
        Image.alpha_composite(bg, touch).convert("RGB").save(IMAGES / "apple-touch-icon-180x180.png")

        big = Image.open(IMAGES / "favicon-512x512.png").convert("RGBA")
        big.save(IMAGES / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("favicons written to", IMAGES)


if __name__ == "__main__":
    main()
