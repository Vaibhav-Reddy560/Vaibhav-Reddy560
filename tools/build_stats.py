"""Generate the telemetry panels from real GitHub API data.

Self-hosted on purpose: the usual third-party stat-card services were returning
503 and 402 at build time, which renders as a broken image in the README. These
are committed to the repo instead, so they cannot fail to load.
"""
import json
import os
from datetime import datetime

OUT = "assets"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono',monospace"

NAVY, BONE, AMBER, PHOSPHOR, RUST, BLUEPRINT = (
    "#14142a", "#ede6d6", "#e8a33c", "#f0a030", "#c1462f", "#3e6ca0")

# Brand spectrum, ordered so neighbouring segments never sit close in hue —
# the dominant language otherwise blends into the one beside it.
SPECTRUM = ["#e8a33c", "#5885b8", "#c1462f", "#f0a030", "#3e6ca0", "#dcd2bc", "#8a5e1e"]

LANGS = {
    "TypeScript": 301775 + 1589456 + 1334736 + 585626,
    "Python": 5640 + 477762,
    "HTML": 15455 + 309897,
    "JavaScript": 16095 + 2279 + 262805,
    "CSS": 12952 + 17810 + 19699 + 41571,
    "PLpgSQL": 16877,
    "Dockerfile": 473,
}
REPO_COUNT = 4   # repos that actually contain code


def languages() -> str:
    total = sum(LANGS.values())
    # Anything under a tenth of a percent renders as "0.0%", which reads as a
    # bug rather than a fact.
    rows = [kv for kv in sorted(LANGS.items(), key=lambda kv: -kv[1])
            if kv[1] / total * 100 >= 0.1]
    x0, x1, y = 34.0, 1166.0, 78.0
    bar_w, h = x1 - x0, 26.0

    segs, legend, cx = [], [], x0
    for i, (name, byte_count) in enumerate(rows):
        pct = byte_count / total * 100
        w = bar_w * byte_count / total
        segs.append(f'<rect x="{cx:.1f}" y="{y}" width="{max(w, 1.5):.1f}" height="{h}" fill="{SPECTRUM[i]}"/>')
        cx += w
    # Legend: one row, evenly distributed.
    step = bar_w / len(rows)
    for i, (name, byte_count) in enumerate(rows):
        pct = byte_count / total * 100
        lx = x0 + i * step
        legend.append(
            f'<circle cx="{lx + 5:.1f}" cy="146" r="5" fill="{SPECTRUM[i]}"/>'
            f'<text x="{lx + 18:.1f}" y="151" font-size="13.5" fill="{BONE}" opacity=".9">{name}</text>'
            f'<text x="{lx + 18:.1f}" y="172" font-size="13.5" fill="{BONE}" opacity=".45">{pct:.1f}%</text>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 200" width="1200" height="200" role="img" aria-label="Most used languages: {', '.join(f'{n} {v / total * 100:.1f}%' for n, v in rows)}">
<title>Most used languages</title>
<rect width="1200" height="200" fill="{NAVY}"/>
<rect x="0" y="0" width="1200" height="2" fill="{AMBER}" opacity=".8"/>
<g font-family="{MONO}" letter-spacing="2.4">
  <text x="34" y="46" font-size="16" fill="{AMBER}">MOST USED LANGUAGES</text>
  <text x="1166" y="46" font-size="12.5" fill="{BONE}" opacity=".45" text-anchor="end">BY BYTES · {REPO_COUNT} REPOS · PUBLIC + PRIVATE</text>
</g>
<g>{''.join(segs)}</g>
<g font-family="{MONO}" letter-spacing="1.2">{''.join(legend)}</g>
</svg>
'''


def activity() -> str:
    cal = json.load(open(os.path.join(os.path.dirname(__file__), "contrib.json")))["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = cal["weeks"]
    total = cal["totalContributions"]

    series = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in weeks]
    first_days = [w["contributionDays"][0]["date"] for w in weeks]

    x0, x1 = 60.0, 1160.0
    yb, yt = 282.0, 104.0
    peak = max(series) or 1
    n = len(series)
    step = (x1 - x0) / (n - 1)

    pts = [(x0 + i * step, yb - (v / peak) * (yb - yt)) for i, v in enumerate(series)]
    line = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f} {y:.1f}" for i, (x, y) in enumerate(pts))
    area = line + f" L{x1:.1f} {yb} L{x0:.1f} {yb} Z"

    # Gridlines at quarter steps of the peak.
    grid, labels = [], []
    for f in (0.25, 0.5, 0.75, 1.0):
        gy = yb - f * (yb - yt)
        grid.append(f'<line x1="{x0}" y1="{gy:.1f}" x2="{x1}" y2="{gy:.1f}" stroke="{BONE}" stroke-width="1" opacity=".08"/>')
        labels.append(f'<text x="{x0 - 12}" y="{gy + 4:.1f}" font-size="11" fill="{BONE}" opacity=".35" text-anchor="end">{round(peak * f)}</text>')

    # One label per month, at the first week that lands in it.
    months, seen = [], set()
    for i, d in enumerate(first_days):
        dt = datetime.strptime(d, "%Y-%m-%d")
        key = (dt.year, dt.month)
        if key not in seen:
            seen.add(key)
            months.append(f'<text x="{x0 + i * step:.1f}" y="306" font-size="11.5" fill="{BONE}" opacity=".45" text-anchor="middle">{dt.strftime("%b")}</text>')

    peak_i = series.index(peak)
    px, py = pts[peak_i]

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 340" width="1200" height="340" role="img" aria-label="Contribution activity: {total} contributions in the last year, peaking at {peak} in one week">
<title>Contribution activity — {total} contributions in the last year</title>
<defs>
  <linearGradient id="fillA" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{AMBER}" stop-opacity=".45"/>
    <stop offset="100%" stop-color="{AMBER}" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect width="1200" height="340" fill="{NAVY}"/>
<rect x="0" y="0" width="1200" height="2" fill="{AMBER}" opacity=".8"/>
<g font-family="{MONO}" letter-spacing="2.4">
  <text x="34" y="46" font-size="16" fill="{AMBER}">CONTRIBUTION ACTIVITY</text>
  <text x="34" y="72" font-size="12.5" fill="{BONE}" opacity=".5">{total} IN THE LAST YEAR · PUBLIC + PRIVATE · BY WEEK</text>
  <text x="1166" y="46" font-size="12.5" fill="{BONE}" opacity=".45" text-anchor="end">PEAK {peak}/WK</text>
</g>
<g font-family="{MONO}">{''.join(grid)}{''.join(labels)}</g>
<path d="{area}" fill="url(#fillA)"/>
<path d="{line}" fill="none" stroke="{AMBER}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>
<circle cx="{px:.1f}" cy="{py:.1f}" r="4.5" fill="{PHOSPHOR}"/>
<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{BONE}" stroke-width="1" opacity=".2"/>
<g font-family="{MONO}">{''.join(months)}</g>
</svg>
'''


if __name__ == "__main__":
    for name, body in [("stats-languages.svg", languages()), ("stats-activity.svg", activity())]:
        with open(f"{OUT}/{name}", "w") as f:
            f.write(body)
        print(f"{name:24s} {len(body.encode()):>7,d} bytes")
