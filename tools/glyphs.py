"""Extract SVG path data for the headline from the site's own display face."""
import json
import os
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform

FONT = os.environ.get(
    "OCTAVUS_TTF",
    os.path.expanduser("~/Portfolio_Website/public/octavus/Octavus-Black-FFP.ttf"),
)


def render(text, font_size):
    font = TTFont(FONT)
    upem = font["head"].unitsPerEm
    glyphset = font.getGlyphSet()
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    scale = font_size / upem

    pen_out = SVGPathPen(glyphset)
    x = 0.0
    for ch in text:
        name = cmap.get(ord(ch))
        if name is None:
            x += font_size * 0.4
            continue
        # y is flipped: font coords go up, SVG coords go down.
        t = Transform(scale, 0, 0, -scale, x, 0)
        glyphset[name].draw(TransformPen(pen_out, t))
        x += hmtx[name][0] * scale
    return pen_out.getCommands(), x


if __name__ == "__main__":
    font = TTFont(FONT)
    print("unitsPerEm:", font["head"].unitsPerEm, file=sys.stderr)
    os2 = font["OS/2"]
    print("capHeight:", getattr(os2, "sCapHeight", "n/a"), file=sys.stderr)
    print("ascender:", font["hhea"].ascent, "descender:", font["hhea"].descent, file=sys.stderr)

    out = {}
    for word in ("VAIBHAV", "REDDY"):
        d, width = render(word, 100.0)
        out[word] = {"d": d, "width": width}
        print(f"{word}: advance at 100px = {width:.2f}", file=sys.stderr)

    with open("glyphs.json", "w") as f:
        json.dump(out, f)
    print("wrote glyphs.json", file=sys.stderr)
