"""Generate the README's SVG assets in the portfolio's own design language.

Animation is CSS-only (never SMIL) so that a prefers-reduced-motion block can
actually switch it off — SMIL cannot be disabled from a media query. Every
animated property therefore has its FINAL state as the CSS base value, with the
keyframes running from the initial state, so `animation: none` lands on the
finished frame rather than an empty one.
"""
import json
import os

OUT = "assets"

P = {
    "blueprint": "#3e6ca0",
    "bone": "#ede6d6",
    "bone_dk": "#dcd2bc",
    "navy": "#14142a",
    "amber": "#e8a33c",
    "rust": "#c1462f",
    "crt": "#0a0d08",
    "phosphor": "#f0a030",
}

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono',monospace"

glyphs = json.load(open(os.path.join(os.path.dirname(__file__), "glyphs.json")))

# Hero geometry
W, H = 1200, 440
PAD = 56
FS = 72.0                      # headline size
CAP = 0.768 * FS               # cap height from the font's OS/2 table
L1_W = glyphs["VAIBHAV"]["width"] / 100.0 * FS
L2_W = glyphs["REDDY"]["width"] / 100.0 * FS
L1_Y, L2_Y = 196.0, 298.0
RULE_Y = 338


def headline_paths(scale):
    """Both headline words as path data, scaled from the 100px extraction."""
    k = scale / 100.0
    return (
        f'<g transform="translate({PAD},{L1_Y}) scale({k})">'
        f'<path d="{glyphs["VAIBHAV"]["d"]}"/></g>',
        f'<g transform="translate({PAD},{L2_Y}) scale({k})">'
        f'<path d="{glyphs["REDDY"]["d"]}"/></g>',
    )


def hero(dark: bool) -> str:
    if dark:
        bg, ink, dim, accent = P["crt"], P["phosphor"], "#8a5e1e", P["amber"]
        rule, led = P["phosphor"], [P["phosphor"], P["amber"], P["rust"]]
        grid_op, scan_op, sweep_op = 0.05, 0.14, 0.07
        grid_c = P["phosphor"]
    else:
        bg, ink, dim, accent = P["bone"], P["navy"], "#7c7360", P["rust"]
        rule, led = P["blueprint"], [P["rust"], P["amber"], P["blueprint"]]
        grid_op, scan_op, sweep_op = 0.10, 0.0, 0.05
        grid_c = P["blueprint"]

    l1, l2 = headline_paths(FS)
    sfx = "dark" if dark else "light"

    scanlines = ""
    if scan_op:
        scanlines = (
            f'<rect width="{W}" height="{H}" fill="url(#scan-{sfx})" '
            f'opacity="{scan_op}"/>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Vaibhav Reddy — Designer and AI/ML engineer, Bengaluru, India">
<title>Vaibhav Reddy — Designer &amp; AI/ML engineer</title>
<defs>
  <pattern id="grid-{sfx}" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0H0V40" fill="none" stroke="{grid_c}" stroke-width="1" opacity="{grid_op}"/>
  </pattern>
  <pattern id="scan-{sfx}" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="{ink}" opacity="0.5"/>
  </pattern>
  <linearGradient id="sweep-{sfx}" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{ink}" stop-opacity="0"/>
    <stop offset="50%" stop-color="{ink}" stop-opacity="{sweep_op}"/>
    <stop offset="100%" stop-color="{ink}" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="vig-{sfx}" cx="50%" cy="50%" r="75%">
    <stop offset="55%" stop-color="{bg}" stop-opacity="0"/>
    <stop offset="100%" stop-color="{P['crt'] if dark else P['bone_dk']}" stop-opacity="{0.85 if dark else 0.5}"/>
  </radialGradient>
  <clipPath id="clip1-{sfx}"><rect class="rv" x="{PAD}" y="{L1_Y - CAP - 8}" width="{L1_W}" height="{CAP + 16}"/></clipPath>
  <clipPath id="clip2-{sfx}"><rect class="rv2" x="{PAD}" y="{L2_Y - CAP - 8}" width="{L2_W}" height="{CAP + 16}"/></clipPath>
</defs>
<style>
  .rv  {{ transform: translateX(0); animation: t1 .9s steps(7,end) .3s both; }}
  .rv2 {{ transform: translateX(0); animation: t2 .7s steps(5,end) 1.25s both; }}
  @keyframes t1 {{ from {{ transform: translateX(-{L1_W:.1f}px) }} to {{ transform: translateX(0) }} }}
  @keyframes t2 {{ from {{ transform: translateX(-{L2_W:.1f}px) }} to {{ transform: translateX(0) }} }}
  .cur1 {{ opacity: 0; animation: cur1 1.25s steps(1,end) .3s; }}
  @keyframes cur1 {{ 0%,100% {{ opacity:0 }} 2%,98% {{ opacity:1 }} }}
  .cur2 {{ opacity: 1; animation: blink 1.1s steps(1,end) 1.95s infinite; }}
  @keyframes blink {{ 0%,49% {{ opacity:1 }} 50%,100% {{ opacity:0 }} }}
  .c1mv {{ animation: c1mv .9s steps(7,end) .3s both; }}
  @keyframes c1mv {{ from {{ transform: translateX(-{L1_W:.1f}px) }} to {{ transform: translateX(0) }} }}
  .c2mv {{ animation: c2mv .7s steps(5,end) 1.25s both; }}
  @keyframes c2mv {{ from {{ transform: translateX(-{L2_W:.1f}px); opacity: 0 }} to {{ transform: translateX(0); opacity: 1 }} }}
  .sweep {{ animation: sweep 7s linear infinite; }}
  @keyframes sweep {{ from {{ transform: translateY(-120px) }} to {{ transform: translateY({H + 40}px) }} }}
  .radar {{ transform-origin: 1074px 168px; animation: spin 4s linear infinite; }}
  @keyframes spin {{ to {{ transform: rotate(360deg) }} }}
  .led1 {{ animation: pulse 2.4s ease-in-out infinite; }}
  .led2 {{ animation: pulse 2.4s ease-in-out .8s infinite; }}
  .led3 {{ animation: pulse 2.4s ease-in-out 1.6s infinite; }}
  @keyframes pulse {{ 0%,100% {{ opacity:.35 }} 50% {{ opacity:1 }} }}
  .star {{ animation: tw 3.2s ease-in-out infinite; }}
  .star2 {{ animation: tw 3.2s ease-in-out 1.1s infinite; }}
  .star3 {{ animation: tw 3.2s ease-in-out 2.2s infinite; }}
  @keyframes tw {{ 0%,100% {{ opacity:.2 }} 50% {{ opacity:.75 }} }}
  .rule {{ stroke-dasharray: {W}; stroke-dashoffset: 0; animation: draw 1.1s ease-out .35s both; }}
  @keyframes draw {{ from {{ stroke-dashoffset: {W} }} to {{ stroke-dashoffset: 0 }} }}
  .fade {{ opacity: 1; animation: fade .7s ease-out 1.8s both; }}
  @keyframes fade {{ from {{ opacity:0 }} to {{ opacity:1 }} }}
  @media (prefers-reduced-motion: reduce) {{
    .rv,.rv2,.c1mv,.c2mv,.cur1,.cur2,.sweep,.radar,.led1,.led2,.led3,
    .star,.star2,.star3,.rule,.fade {{ animation: none !important; }}
    .sweep {{ display: none; }}
    .cur1 {{ opacity: 0; }}
  }}
</style>

<rect width="{W}" height="{H}" fill="{bg}"/>
<rect width="{W}" height="{H}" fill="url(#grid-{sfx})"/>
{scanlines}
<rect class="sweep" x="0" y="0" width="{W}" height="120" fill="url(#sweep-{sfx})"/>
<rect width="{W}" height="{H}" fill="url(#vig-{sfx})"/>

<!-- eyebrow -->
<g font-family="{MONO}" font-size="15" letter-spacing="4.5" fill="{ink}">
  <text x="{PAD}" y="66" opacity=".85">AI</text>
  <text x="{PAD + 46}" y="66" opacity=".4">//</text>
  <text x="{PAD + 78}" y="66" opacity=".85">DESIGN</text>
  <text x="{PAD + 190}" y="66" opacity=".4">//</text>
  <text x="{PAD + 222}" y="66" opacity=".85">LEADERSHIP</text>
</g>

<!-- headline, outlined from Octavus Black -->
<g fill="{ink}">
  <g clip-path="url(#clip1-{sfx})">{l1}</g>
  <g clip-path="url(#clip2-{sfx})">{l2}</g>
</g>
<g class="c1mv"><rect class="cur1" x="{PAD + L1_W + 10:.1f}" y="{L1_Y - CAP:.1f}" width="{FS * 0.42:.1f}" height="{CAP:.1f}" fill="{accent}"/></g>
<g class="c2mv"><rect class="cur2" x="{PAD + L2_W + 10:.1f}" y="{L2_Y - CAP:.1f}" width="{FS * 0.42:.1f}" height="{CAP:.1f}" fill="{accent}"/></g>

<!-- rule -->
<line class="rule" x1="{PAD}" y1="{RULE_Y}" x2="{W - PAD}" y2="{RULE_Y}" stroke="{rule}" stroke-width="2" opacity=".55"/>

<g class="fade">
  <g font-family="{MONO}" font-size="16" letter-spacing="2.6" fill="{ink}">
    <text x="{PAD}" y="374" opacity=".9">DESIGNER &amp; AI/ML ENGINEER</text>
    <text x="{PAD}" y="406" font-size="14" fill="{dim}">&gt; status: open to opportunities</text>
  </g>
  <g font-family="{MONO}" font-size="13" letter-spacing="2.2" fill="{dim}" text-anchor="end">
    <text x="{W - PAD}" y="374">BENGALURU, IN</text>
    <text x="{W - PAD}" y="406">VR-2026-GH</text>
  </g>
</g>

<!-- radar -->
<g opacity=".7">
  <circle cx="1074" cy="168" r="66" fill="none" stroke="{rule}" stroke-width="1" opacity=".35"/>
  <circle cx="1074" cy="168" r="44" fill="none" stroke="{rule}" stroke-width="1" opacity=".28"/>
  <circle cx="1074" cy="168" r="22" fill="none" stroke="{rule}" stroke-width="1" opacity=".22"/>
  <line x1="1008" y1="168" x2="1140" y2="168" stroke="{rule}" stroke-width="1" opacity=".2"/>
  <line x1="1074" y1="102" x2="1074" y2="234" stroke="{rule}" stroke-width="1" opacity=".2"/>
  <g class="radar"><path d="M1074 168 L1074 102 A66 66 0 0 1 1130 134 Z" fill="{accent}" opacity=".3"/></g>
  <circle cx="1074" cy="168" r="3" fill="{accent}"/>
</g>

<!-- LEDs -->
<g>
  <circle class="led1" cx="1092" cy="61" r="5" fill="{led[0]}"/>
  <circle class="led2" cx="1112" cy="61" r="5" fill="{led[1]}"/>
  <circle class="led3" cx="1132" cy="61" r="5" fill="{led[2]}"/>
</g>

<!-- starbursts -->
<g fill="{ink}">
  <path class="star"  d="M300 78 L305 92 L319 97 L305 102 L300 116 L295 102 L281 97 L295 92 Z"/>
  <path class="star2" d="M878 250 L881 259 L890 262 L881 265 L878 274 L875 265 L866 262 L875 259 Z"/>
  <path class="star3" d="M916 282 L920 293 L931 297 L920 301 L916 312 L912 301 L901 297 L912 293 Z"/>
</g>

<rect x="1" y="1" width="{W - 2}" height="{H - 2}" fill="none" stroke="{rule}" stroke-width="2" opacity=".45"/>
</svg>
'''


def ticker() -> str:
    items = ["Figma", "Photoshop", "Illustrator", "Next.js", "React",
             "TypeScript", "Tailwind CSS", "Python", "PyTorch", "Supabase",
             "AI / ML", "UI/UX"]
    fs, pitch = 17, 0.6 * 17
    x, parts = 0.0, []
    for it in items:
        parts.append((x, it))
        x += len(it) * pitch + 34
        parts.append((x, "◆"))
        x += pitch + 34
    track_w = x

    def row(offset):
        out = []
        for px, txt in parts:
            fill = P["amber"] if txt == "◆" else P["bone"]
            op = "1" if txt == "◆" else ".88"
            out.append(f'<text x="{px + offset:.1f}" y="36" fill="{fill}" opacity="{op}">{txt}</text>')
        return "".join(out)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 56" width="1200" height="56" role="img" aria-label="Tooling: Figma, Photoshop, Illustrator, Next.js, React, TypeScript, Tailwind CSS, Python, PyTorch, Supabase, AI/ML, UI/UX">
<title>Tooling ticker</title>
<style>
  .track {{ animation: run 26s linear infinite; }}
  @keyframes run {{ from {{ transform: translateX(0) }} to {{ transform: translateX(-{track_w:.1f}px) }} }}
  @media (prefers-reduced-motion: reduce) {{ .track {{ animation: none; }} }}
</style>
<rect width="1200" height="56" fill="{P['navy']}"/>
<clipPath id="tc"><rect width="1200" height="56"/></clipPath>
<g clip-path="url(#tc)">
  <g class="track" font-family="{MONO}" font-size="{fs}" letter-spacing="2.4">
    {row(0)}{row(track_w)}
  </g>
</g>
<rect x="0" y="0" width="1200" height="2" fill="{P['amber']}" opacity=".8"/>
<rect x="0" y="54" width="1200" height="2" fill="{P['amber']}" opacity=".8"/>
</svg>
'''


def plate(num: str, label: str) -> str:
    ticks = "".join(
        f'<rect x="{1128 - i * 11}" y="{26 if i % 2 else 22}" width="2" '
        f'height="{20 if i % 2 else 28}" fill="{P["bone"]}" opacity=".3"/>'
        for i in range(9)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 72" width="1200" height="72" role="img" aria-label="{num} — {label}">
<title>{num} // {label}</title>
<rect width="1200" height="72" fill="{P['navy']}"/>
<rect x="0" y="0" width="8" height="72" fill="{P['amber']}"/>
<g font-family="{MONO}" letter-spacing="4">
  <text x="34" y="46" font-size="22" fill="{P['amber']}">{num}</text>
  <text x="86" y="46" font-size="22" fill="{P['bone']}" opacity=".35">//</text>
  <text x="128" y="46" font-size="22" fill="{P['bone']}">{label}</text>
</g>
{ticks}
<rect x="0" y="70" width="1200" height="2" fill="{P['blueprint']}" opacity=".7"/>
</svg>
'''


def divider() -> str:
    ticks = "".join(
        f'<rect x="{i * 40}" y="10" width="1" height="{6 if i % 3 else 10}" '
        f'fill="{P["blueprint"]}" opacity=".45"/>'
        for i in range(31)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 28" width="1200" height="28" role="img" aria-hidden="true">
<line x1="0" y1="9" x2="1200" y2="9" stroke="{P['blueprint']}" stroke-width="1" opacity=".5"/>
{ticks}
<path d="M600 4 L606 10 L600 16 L594 10 Z" fill="{P['amber']}"/>
</svg>
'''


def footer() -> str:
    import hashlib
    seed = hashlib.sha256(b"Vaibhav-Reddy560").digest()
    bars, x = [], 34.0
    for i in range(56):
        w = 1.5 + (seed[i % len(seed)] % 4)
        bars.append(f'<rect x="{x:.1f}" y="82" width="{w:.1f}" height="26" fill="{P["bone"]}" opacity=".8"/>')
        x += w + 2.2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 124" width="1200" height="124" role="img" aria-label="Designing. Building. Learning. Growing.">
<title>Designing. Building. Learning. Growing.</title>
<style>
  .l1 {{ animation: p 2.4s ease-in-out infinite; }}
  .l2 {{ animation: p 2.4s ease-in-out .8s infinite; }}
  .l3 {{ animation: p 2.4s ease-in-out 1.6s infinite; }}
  @keyframes p {{ 0%,100% {{ opacity:.3 }} 50% {{ opacity:1 }} }}
  @media (prefers-reduced-motion: reduce) {{ .l1,.l2,.l3 {{ animation: none; }} }}
</style>
<rect width="1200" height="124" fill="{P['navy']}"/>
<rect x="0" y="0" width="1200" height="2" fill="{P['amber']}" opacity=".8"/>
<text x="34" y="52" font-family="{MONO}" font-size="20" letter-spacing="5" fill="{P['bone']}">DESIGNING. BUILDING. LEARNING. GROWING.</text>
<text x="34" y="74" font-family="{MONO}" font-size="12.5" letter-spacing="2.4" fill="{P['bone']}" opacity=".5">VR-2026-GH // BENGALURU, IN // github.com/Vaibhav-Reddy560</text>
{''.join(bars)}
<g>
  <circle class="l1" cx="1120" cy="46" r="5" fill="{P['phosphor']}"/>
  <circle class="l2" cx="1140" cy="46" r="5" fill="{P['amber']}"/>
  <circle class="l3" cx="1160" cy="46" r="5" fill="{P['rust']}"/>
</g>
<text x="1166" y="99" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{P['bone']}" opacity=".45" text-anchor="end">END OF LINE</text>
</svg>
'''


SECTIONS = [
    ("01", "IDENTITY"), ("02", "SELECTED WORK"), ("03", "DESIGN WORK"),
    ("04", "STACK"), ("05", "LEADERSHIP"), ("06", "EDUCATION"),
    ("07", "TELEMETRY"), ("08", "CONTACT"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    files = {
        "hero-dark.svg": hero(True),
        "hero-light.svg": hero(False),
        "ticker.svg": ticker(),
        "divider.svg": divider(),
        "footer.svg": footer(),
    }
    for num, label in SECTIONS:
        files[f"plate-{num}.svg"] = plate(num, label)

    for name, body in files.items():
        with open(os.path.join(OUT, name), "w") as f:
            f.write(body)
        print(f"{name:20s} {len(body.encode()):>7,d} bytes")
    total = sum(len(b.encode()) for b in files.values())
    print(f"{'TOTAL':20s} {total:>7,d} bytes")
