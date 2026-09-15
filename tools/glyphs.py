"""Extract SVG path data and true ink bounds for the headline.

The ink bounds matter as much as the paths: Octavus Black is steeply slanted, so
a glyph's outline overhangs its own advance box by roughly a third of an em. Any
geometry derived from advance widths alone (a clip box, say) will slice the last
letter of a word clean off.
"""
import json
import os
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform

FONT = os.environ.get(
    "OCTAVUS_TTF",
    os.path.expanduser("~/Portfolio_Website/public/octavus/Octavus-Black-FFP.ttf"),
)
HERE = os.path.dirname(os.path.abspath(__file__))


def render(text, font_size):
    """Returns (path data, advance width, ink bbox) in one coordinate space."""
    font = TTFont(FONT)
    upem = font["head"].unitsPerEm
    glyphset = font.getGlyphSet()
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    scale = font_size / upem

    pen_out = SVGPathPen(glyphset)
    bounds = BoundsPen(glyphset)
    x = 0.0
    for ch in text:
        name = cmap.get(ord(ch))
        if name is None:
            x += font_size * 0.4
            continue
        # y is flipped: font coords go up, SVG coords go down.
        t = Transform(scale, 0, 0, -scale, x, 0)
        glyphset[name].draw(TransformPen(pen_out, t))
        glyphset[name].draw(TransformPen(bounds, t))
        x += hmtx[name][0] * scale
    return pen_out.getCommands(), x, bounds.bounds


if __name__ == "__main__":
    font = TTFont(FONT)
    print("unitsPerEm:", font["head"].unitsPerEm, file=sys.stderr)

    out = {}
    for word in ("VAIBHAV", "REDDY"):
        d, width, bbox = render(word, 100.0)
        out[word] = {"d": d, "width": width, "bbox": list(bbox)}
        x0, y0, x1, y1 = bbox
        print(
            f"{word}: advance={width:.2f}  ink x {x0:.2f}..{x1:.2f}  y {y0:.2f}..{y1:.2f}"
            f"  (overhangs advance by {x1 - width:.2f})",
            file=sys.stderr,
        )

    path = os.path.join(HERE, "glyphs.json")
    with open(path, "w") as f:
        json.dump(out, f)
    print(f"wrote {path}", file=sys.stderr)
