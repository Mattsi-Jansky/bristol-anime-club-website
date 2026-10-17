"""Build the club logo, public/logo.svg.

usage: python3 tools/logo/build_logo.py [latin-font.ttf jp-font.ttf out.svg]

With no arguments it reads the fonts from tools/logo/fonts/ (see the README there)
and writes public/logo.svg. Geometry is hand-placed on a 1000x1000 canvas, traced
from the original hand-drawn logo. Text is converted to outlines, so the SVG
needs no fonts to display.
"""
import sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

HERE = Path(__file__).resolve().parent
if len(sys.argv) == 4:
    latin_path, jp_path, out_path = sys.argv[1:4]
else:
    latin_path = HERE / "fonts" / "LuckiestGuy.ttf"
    jp_path = HERE / "fonts" / "NotoSansJP.ttf"
    out_path = HERE.parent.parent / "public" / "logo.svg"

RING = "#f3d038"
SKY = "#7cbdd9"
TOWER = "#b7212a"
RED = "#eb2537"
ORANGE = "#dd7327"
CAP = "#fce644"
INK = "#231f20"
CABLE = "#f7f7f2"
STRIPE = "#b9c6cf"


def text_path(font, text, x, baseline, width=None, size=None, tracking=0.0):
    """Outline `text` as one SVG path. Give either a target width or a font size."""
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    upm = font["head"].unitsPerEm
    names = [cmap[ord(c)] for c in text]
    advances = [font["hmtx"][n][0] for n in names]
    total = sum(advances) + tracking * upm * (len(names) - 1)
    scale = (width / total) if width else (size / upm)
    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
    cursor = 0.0
    for n, adv in zip(names, advances):
        # font units are y-up; flip and move onto the baseline
        t = TransformPen(pen, (scale, 0, 0, -scale, x + cursor * scale, baseline))
        gs[n].draw(t)
        cursor += adv + tracking * upm
    return pen.getCommands(), scale


def text_bounds(font, text, scale):
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    bp = BoundsPen(gs)
    cursor = 0
    for c in text:
        n = cmap[ord(c)]
        gs[n].draw(TransformPen(bp, (1, 0, 0, 1, cursor, 0)))
        cursor += font["hmtx"][n][0]
    xmin, ymin, xmax, ymax = bp.bounds
    return ymax * scale  # cap height above baseline, in canvas units


def cable(d, w):
    """A white cable with two thin grey stripes, like the logo's striped ropes."""
    return (f'<path d="{d}" stroke="{CABLE}" stroke-width="{w}"/>'
            f'<path d="{d}" stroke="{STRIPE}" stroke-width="{w * 0.55:.1f}"/>'
            f'<path d="{d}" stroke="{CABLE}" stroke-width="{w * 0.3:.1f}"/>')


latin = TTFont(latin_path)
jp = TTFont(jp_path)

# --- lettering, laid out to the original's footprint
title, s1 = text_path(latin, "NIME CLUB", 552, 0, width=380)
cap_h = text_bounds(latin, "NIME CLUB", s1)
title_base = 482 + cap_h  # top of the letters sits at y=482
title, _ = text_path(latin, "NIME CLUB", 552, title_base, width=380)

sub, s2 = text_path(latin, "BRISTOL & BEYOND", 560, 0, width=320)
sub_h = text_bounds(latin, "BRISTOL & BEYOND", s2)
sub_base = title_base + 20 + sub_h
sub, _ = text_path(latin, "BRISTOL & BEYOND", 560, sub_base, width=320)

kana, _ = text_path(jp, "日本のアニメ", 552, 470, width=236)

# --- tower geometry
# Seen from below and to the left (a worm's-eye view, as in the original), so
# every block recedes the same way: back = front + (-30, +14). Back edges sit
# lower than front edges, which shows the undersides and hides the tops.
# The legs bow outward (convex), giving the A its full, rounded stance.
OUTER = "M216,738 Q213,515 270,306 L300,292 L480,292 Q545,515 552,738 Z"
SIDE = "M216,738 Q213,515 270,306 L300,292 Q243,515 246,738 Z"
# arch opening: legs that soften into a round head peaking just right of centre
ARCH = "M350,738 Q345,590 352,420 C354,366 382,336 412,338 C442,340 462,372 462,424 Q466,590 464,738 Z"

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" role="img" aria-labelledby="t">
  <title id="t">The Anime Club – Bristol &amp; Beyond</title>
  <defs>
    <clipPath id="sky"><circle cx="500" cy="500" r="468"/></clipPath>
    <clipPath id="arch"><path d="{ARCH}"/></clipPath>
  </defs>

  <circle cx="500" cy="500" r="497" fill="{RING}"/>
  <circle cx="500" cy="500" r="468" fill="{SKY}"/>

  <!-- The deck runs through the A's arch: left of the picture is the far end of the
       bridge, right is the near end. Two cables run along it, side by side over the
       front of the cap, each passing from its far section to its near one.
       cable 1 crosses the cap at the middle of the leftmost window (331,283),
       cable 2 at the middle of the rightmost window (468,283).
       Far sections first: cable 2's passes behind the tower and comes out low on the left. -->
  <g clip-path="url(#sky)" fill="none">
    {cable("M468,283 Q260,405 20,464", 18)}
    {cable("M331,283 Q170,392 20,410", 18)}
  </g>

  <!-- black outline on the back of the tower only, as in the original: the silhouette
       with the arch cut out, offset down-left, so each leg gets its own edge -->
  <path d="{OUTER} {ARCH}" fill="{INK}" fill-rule="evenodd" transform="translate(-8 8)"/>
  <!-- the orange inner wall belongs to the right leg, so its base line runs under it too -->
  <rect x="404" y="738" width="60" height="8" fill="{INK}"/>

  <!-- tower, drawn as the letter A: darker front, bright lit side face -->
  <!-- solid body: what shows through the arch is painted on top, so the shared edges
       blend into matching red instead of letting the background seep through -->
  <path d="{OUTER}" fill="{TOWER}"/>
  <path d="{SIDE}" fill="{RED}"/>
  <!-- through the arch: the inner wall in orange, then sky beyond it -->
  <path d="{ARCH}" fill="{ORANGE}"/>
  <g clip-path="url(#arch)">
    <!-- the far side of the arch, seen through the near one (depth -56, +30),
         with its black outline showing along the top and right of the sky -->
    <path d="{ARCH}" fill="{SKY}" stroke="{INK}" stroke-width="7" transform="translate(-56 30)"/>
    <!-- crossbar, with its underside showing because we look up at it; the far
         crossbar's bottom edge carries the same black line -->
    <path d="M300,522 L464,522 L408,552 L244,552 Z" fill="{RED}"/>
    <path d="M244,552 L408,552" stroke="{INK}" stroke-width="7"/>
  </g>
  <!-- the crossbar is the body's own red, so it runs on into the legs unclipped:
       no edge at all where it meets them. It overlaps the top of its underside. -->
  <rect x="330" y="476" width="155" height="48" fill="{TOWER}"/>
  <!-- trace the arch's sides and head in the tower's red: hides the anti-aliasing seams
       where the clipped layers inside meet the body (the open base is left untraced) -->
  <path d="M350,738 Q345,590 352,420 C354,366 382,336 412,338 C442,340 462,372 462,424 Q466,590 464,738" fill="none" stroke="{TOWER}" stroke-width="5"/>
  <!-- open sky under the arch runs straight on past the base, with no seam -->
  <rect x="351" y="732" width="53" height="10" fill="{SKY}"/>

  <!-- brick band: same block construction as the tower, tall enough that a row of
       windows shows above the cables crossing its front -->
  <g transform="translate(0 8)">
  <path d="M266,272 L296,258 L296,292 L266,306 Z" fill="#f0a64f"/>
  <rect x="296" y="258" width="190" height="34" fill="{ORANGE}"/>
  <g fill="#f6c27e">
    <rect x="316" y="264" width="30" height="22" rx="3"/>
    <rect x="366" y="264" width="30" height="22" rx="3"/>
    <rect x="416" y="264" width="30" height="22" rx="3"/>
    <rect x="460" y="264" width="16" height="22" rx="3"/>
  </g>
  <!-- window reveals: shadowed top and left edges make them read as recesses -->
  <g fill="#a9471a">
    <path d="M316,264 h30 v5 h-25 v17 h-5 Z"/>
    <path d="M366,264 h30 v5 h-25 v17 h-5 Z"/>
    <path d="M416,264 h30 v5 h-25 v17 h-5 Z"/>
    <path d="M460,264 h16 v5 h-11 v17 h-5 Z"/>
  </g>
  </g>

  <!-- roof: two cornice tiers, each overhanging the one below, then a sloped roof
       rising to a short ridge. Seen from below and to the left like the rest of the
       tower: lit left faces, darker fronts, and shaded undersides only where a tier
       overhangs what's beneath it. Drawn for a band top at y=218, moved down 48
       to sit on the band's top front edge at y=266. -->
  <g transform="translate(0 48)">
    <!-- lower tier -->
    <path d="M286,212 L500,212 L486,218 L296,218 L266,232 L256,226 Z" fill="#c99a22"/>
    <path d="M256,214 L286,200 L286,212 L256,226 Z" fill="{CAP}"/>
    <rect x="286" y="200" width="214" height="12" fill="{RING}"/>
    <!-- upper tier, wider -->
    <path d="M278,196 L510,196 L500,200 L286,200 L256,214 L248,210 Z" fill="#c99a22"/>
    <path d="M248,198 L278,184 L278,196 L248,210 Z" fill="{CAP}"/>
    <rect x="278" y="184" width="232" height="12" fill="{RING}"/>
    <!-- sloped roof: front slope and the brighter left slope meeting at the ridge -->
    <path d="M278,184 L510,184 L474,160 L316,160 Z" fill="#f7da4a"/>
    <path d="M248,198 L278,184 L316,160 L292,170 Z" fill="#fff0a0"/>
    <path d="M318,160 L472,160" stroke="#fde98a" stroke-width="2"/>
  </g>

  <!-- near sections, coming toward us: both cables ride over the front of the cap,
       drawn above every part of it -->
  <g clip-path="url(#sky)" fill="none">
    {cable("M468,283 Q650,360 1000,386", 26)}
    {cable("M331,283 Q560,395 1000,432", 26)}
  </g>

  <!-- lettering -->
  <path d="{kana}" fill="#ffffff"/>
  <path d="{title}" fill="{INK}" transform="translate(5 6)"/>
  <path d="{title}" fill="{RED}"/>
  <path d="{sub}" fill="{INK}" transform="translate(3 4)"/>
  <path d="{sub}" fill="{ORANGE}"/>
</svg>
'''
open(out_path, "w").write(svg)
print(out_path, len(svg), "bytes")
