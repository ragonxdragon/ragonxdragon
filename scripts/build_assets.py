"""Generate the light and dark SVG assets for the profile README.

Run from the repository root:  uv run --no-project python scripts/build_assets.py
Standard library only. Every number drawn here comes from the linked project's README.

Sizing: the banner and the twinflow figure render at full README width, so their text is
sized to stay readable when a phone scales them to about 45%. The three project tiles render
at their intrinsic 268 px width, which fits three to a row on desktop and wraps on a phone.
"""

import random
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "light": {
        "surface": "#f6f8fa",
        "node": "#ffffff",
        "border": "#d0d7de",
        "rule": "#d8dee4",
        "ink": "#1f2328",
        "muted": "#59636e",
        "accent": "#0f766e",
        "accent_fill": "#e3f2ef",
        "hatch": "#8c959f",
        "band": "#eef1f4",
    },
    "dark": {
        "surface": "#151b23",
        "node": "#0d1117",
        "border": "#3d444d",
        "rule": "#30363d",
        "ink": "#e6edf3",
        "muted": "#9198a1",
        "accent": "#2dd4bf",
        "accent_fill": "#0f2e2b",
        "hatch": "#656c76",
        "band": "#1b222c",
    },
}

SANS = '-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif'
MONO = 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace'
STYLE_FONTS = f".sans {{ font-family: {SANS}; }}\n    .mono {{ font-family: {MONO}; }}"


def svg_open(w: int, h: int, title: str, desc: str, extra_style: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-labelledby="t d">\n'
        f'  <title id="t">{title}</title>\n'
        f'  <desc id="d">{desc}</desc>\n'
        f"  <style>\n    {STYLE_FONTS}{extra_style}\n  </style>\n"
    )


def frame(t: dict, w: int, h: int) -> str:
    return f'  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="12" fill="{t["surface"]}" stroke="{t["border"]}"/>\n'


ARROW_DEFS = """  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 1 L9 5 L0 9" fill="none" stroke="{c}" stroke-width="1.6"/>
    </marker>
  </defs>
"""


# Banner ---------------------------------------------------------------------------------

# Readings on the control chart, in units of the limit distance from the center line (the
# limits sit at +1 and -1). Illustrative, not data: a fixed seed gives the same irregular trace
# on every build, every reading stays inside the limits, and one reading is set above the
# upper limit so the chart has something to flag.
TRACE_N, TRACE_SEED, TRACE_SD = 32, 20261013, 0.3
OUT_INDEX, OUT_VALUE = 20, 1.42


def _trace() -> list[float]:
    rng = random.Random(TRACE_SEED)
    values = [max(-0.88, min(0.88, rng.gauss(0.0, TRACE_SD))) for _ in range(TRACE_N)]
    values[OUT_INDEX] = OUT_VALUE
    return values


LOOP_S = 9.0
DRAW_START, DRAW_END = 0.04, 0.70  # fractions of the loop while the trace draws
HOLD_END, FADE_END = 0.90, 0.98  # finished trace holds, then fades before the loop resets


def banner(t: dict) -> str:
    W, H, left = 800, 312, 44
    cx0, cx1 = 472, 756  # chart extent
    cl, sigma = 200, 58  # center line y, one limit's distance in px
    ucl, lcl = cl - sigma, cl + sigma

    trace = _trace()
    n = len(trace)
    pts = [(cx0 + 8 + i * (cx1 - cx0 - 16) / (n - 1), cl - v * sigma) for i, v in enumerate(trace)]
    # Straight segments between readings, as an individuals chart draws them.
    lengths = [((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5 for a, b in zip(pts, pts[1:])]
    total = sum(lengths)
    reach = [sum(lengths[:i]) / total for i in range(n)]  # fraction of the trace drawn at each point
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f} " + " ".join(f"L{x:.1f} {y:.1f}" for x, y in pts[1:])

    def at(frac):  # percent of the loop when the pen reaches a fraction of the trace
        return 100 * (DRAW_START + (DRAW_END - DRAW_START) * frac)

    hold, fade = 100 * HOLD_END, 100 * FADE_END
    L = total + 2
    css = [
        f"""
    .trace {{ stroke-dasharray: {L:.0f}; stroke-dashoffset: 0; animation: draw {LOOP_S}s infinite; }}
    @keyframes draw {{
      0% {{ stroke-dashoffset: {L:.0f}; opacity: 1; animation-timing-function: linear; }}
      {100 * DRAW_START:.1f}% {{ stroke-dashoffset: {L:.0f}; animation-timing-function: linear; }}
      {100 * DRAW_END:.1f}% {{ stroke-dashoffset: 0; opacity: 1; }}
      {hold:.1f}% {{ stroke-dashoffset: 0; opacity: 1; animation-timing-function: cubic-bezier(0.25, 1, 0.5, 1); }}
      {fade:.1f}%, 100% {{ stroke-dashoffset: 0; opacity: 0; }}
    }}
    .pt {{ transform-box: fill-box; transform-origin: center; }}
    .flag, .pulse {{ transform-box: fill-box; transform-origin: center; }}"""
    ]
    dots = []
    for i, (x, y) in enumerate(pts):
        if i == OUT_INDEX:
            continue
        a = at(reach[i])
        css.append(
            f"""
    .p{i} {{ animation: p{i} {LOOP_S}s infinite; }}
    @keyframes p{i} {{
      0%, {a:.1f}% {{ opacity: 0; transform: translateY(-5px); animation-timing-function: cubic-bezier(0.25, 1, 0.5, 1); }}
      {min(a + 4, hold):.1f}%, {hold:.1f}% {{ opacity: 1; transform: translateY(0); animation-timing-function: cubic-bezier(0.25, 1, 0.5, 1); }}
      {fade:.1f}%, 100% {{ opacity: 0; transform: translateY(0); }}
    }}"""
        )
        dots.append(f'<circle class="pt p{i}" cx="{x:.1f}" cy="{y:.1f}" r="2.3" fill="{t["accent"]}"/>')

    ox, oy = pts[OUT_INDEX]
    a = at(reach[OUT_INDEX])
    css.append(
        f"""
    .flag {{ animation: flag {LOOP_S}s infinite; }}
    @keyframes flag {{
      0%, {a:.1f}% {{ opacity: 0; transform: scale(0.4); animation-timing-function: cubic-bezier(0.25, 1, 0.5, 1); }}
      {a + 5:.1f}%, {hold:.1f}% {{ opacity: 1; transform: scale(1); animation-timing-function: cubic-bezier(0.25, 1, 0.5, 1); }}
      {fade:.1f}%, 100% {{ opacity: 0; transform: scale(1); }}
    }}
    .pulse {{ opacity: 0; animation: pulse {LOOP_S}s infinite; }}
    @keyframes pulse {{
      0%, {a + 1:.1f}% {{ opacity: 0; transform: scale(1); animation-timing-function: cubic-bezier(0.16, 1, 0.3, 1); }}
      {a + 2:.1f}% {{ opacity: 0.9; transform: scale(1); animation-timing-function: cubic-bezier(0.16, 1, 0.3, 1); }}
      {a + 16:.1f}%, 100% {{ opacity: 0; transform: scale(2.6); }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .trace, .pt, .flag {{ animation: none; }}
      .pulse {{ animation: none; opacity: 0; }}
    }}"""
    )
    band_fill = t["band"]
    return (
        svg_open(
            W,
            H,
            "Jack Hall",
            "Embedded systems, industrial data, applied AI, and process improvement. Firmware that stays "
            "connected, and the systems that read it. Open to contract and full-time roles. A signal "
            "trace runs inside a control band; one reading crosses the upper limit and is flagged.",
            "".join(css),
        )
        + frame(t, W, H)
        + f"""
  <text x="{left}" y="56" class="mono" font-size="14" letter-spacing="1.5" fill="{t["accent"]}">EMBEDDED  /  INDUSTRIAL DATA  /  APPLIED AI  /  PROCESS IMPROVEMENT</text>
  <text x="{left - 3}" y="128" class="sans" font-size="64" font-weight="700" letter-spacing="-1" fill="{t["ink"]}">Jack Hall</text>
  <text class="sans" font-size="26" fill="{t["muted"]}">
    <tspan x="{left}" y="174">Firmware that stays connected,</tspan>
    <tspan x="{left}" y="207">and the systems that read it.</tspan>
  </text>
  <circle cx="{left + 6}" cy="250" r="5" fill="{t["accent"]}"/>
  <text x="{left + 20}" y="256" class="sans" font-size="18" font-weight="600" fill="{t["ink"]}">Open to contract and full-time roles</text>

  <!-- control band: center line and limits -->
  <rect x="{cx0}" y="{ucl}" width="{cx1 - cx0}" height="{lcl - ucl}" fill="{band_fill}"/>
  <line x1="{cx0}" y1="{ucl}" x2="{cx1}" y2="{ucl}" stroke="{t["border"]}" stroke-width="1.25" stroke-dasharray="5 5"/>
  <line x1="{cx0}" y1="{cl}" x2="{cx1}" y2="{cl}" stroke="{t["border"]}" stroke-width="1"/>
  <line x1="{cx0}" y1="{lcl}" x2="{cx1}" y2="{lcl}" stroke="{t["border"]}" stroke-width="1.25" stroke-dasharray="5 5"/>

  <path class="trace" d="{d}" fill="none" stroke="{t["accent"]}" stroke-width="2.25" stroke-linecap="round" stroke-linejoin="round"/>
  {chr(10).join("  " + s for s in dots).lstrip()}

  <circle class="pulse" cx="{ox:.1f}" cy="{oy:.1f}" r="9" fill="none" stroke="{t["accent"]}" stroke-width="1.5"/>
  <g class="flag">
    <circle cx="{ox:.1f}" cy="{oy:.1f}" r="9" fill="none" stroke="{t["accent"]}" stroke-width="2"/>
    <circle cx="{ox:.1f}" cy="{oy:.1f}" r="4" fill="{t["accent"]}"/>
  </g>
</svg>
"""
    )


# twinflow feature -----------------------------------------------------------------------


def twinflow(t: dict) -> str:
    W, H = 720, 448

    def node(x, y, w, title, sub, accent=False):
        return (
            f'  <rect x="{x}" y="{y}" width="{w}" height="66" rx="8" fill="{t["node"]}" '
            f'stroke="{t["accent"] if accent else t["border"]}" stroke-width="{2 if accent else 1.5}"/>\n'
            f'  <text x="{x + 16}" y="{y + 29}" class="sans" font-size="18" font-weight="600" fill="{t["ink"]}">{title}</text>\n'
            f'  <text x="{x + 16}" y="{y + 51}" class="mono" font-size="14" fill="{t["muted"]}">{sub}</text>\n'
        )

    def arrow(x1, y1, x2, y2, color=None, sw=1.6):
        return (
            f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color or t["muted"]}" '
            f'stroke-width="{sw}" marker-end="url(#arrow)"/>\n'
        )

    zw, zy, zh = 262, 214, 206  # zone width, top, height
    ot_x, it_x = 24, W - 24 - zw
    nw = zw - 32
    top_y, bot_y = zy + 24, zy + zh - 24 - 66
    bridge_cy = bot_y + 33
    return (
        svg_open(
            W,
            H,
            "twinflow, a warehouse digital twin",
            "twinflow, version 0.1.0, phase 1 in progress. A warehouse digital twin that answers "
            "what-if questions with a statistical verdict. In the OT segment, Purdue levels 0 to 2, a "
            "discrete-event model of receiving and putaway drives a simulated MQTT device fleet. A broker "
            "bridge is the only path to the IT segment, Purdue levels 3 to 4, where a Lean Six Sigma "
            "engine judges the telemetry and a what-if agent returns a statistical verdict.",
        )
        + ARROW_DEFS.format(c=t["muted"])
        + frame(t, W, H)
        + f"""  <text x="32" y="46" class="mono" font-size="15" fill="{t["accent"]}">v0.1.0, phase 1 in progress</text>
  <text x="30" y="96" class="sans" font-size="42" font-weight="700" letter-spacing="-0.5" fill="{t["ink"]}">twinflow</text>
  <text class="sans" font-size="21" fill="{t["muted"]}">
    <tspan x="32" y="134">A warehouse digital twin that answers what-if</tspan>
    <tspan x="32" y="162">questions with a statistical verdict.</tspan>
  </text>

  <rect x="{ot_x}" y="{zy}" width="{zw}" height="{zh}" rx="10" fill="none" stroke="{t["border"]}" stroke-dasharray="5 5"/>
  <text x="{ot_x + 16}" y="{zy - 10}" class="mono" font-size="14" fill="{t["muted"]}">OT, Purdue L0 to L2</text>
{node(ot_x + 16, top_y, nw, "Discrete-event model", "receiving, putaway")}{node(ot_x + 16, bot_y, nw, "Device fleet", "simulated, MQTT")}{arrow(ot_x + 16 + nw // 2, top_y + 66, ot_x + 16 + nw // 2, bot_y - 3)}
  <rect x="{it_x}" y="{zy}" width="{zw}" height="{zh}" rx="10" fill="none" stroke="{t["border"]}" stroke-dasharray="5 5"/>
  <text x="{it_x + 16}" y="{zy - 10}" class="mono" font-size="14" fill="{t["muted"]}">IT, Purdue L3 to L4</text>
{node(it_x + 16, top_y, nw, "What-if agent", "statistical verdict")}{node(it_x + 16, bot_y, nw, "Lean Six Sigma engine", "judges telemetry", accent=True)}{arrow(it_x + 16 + nw // 2, bot_y, it_x + 16 + nw // 2, top_y + 69)}
{arrow(ot_x + 16 + nw, bridge_cy, it_x + 13, bridge_cy, t["accent"], 2)}  <rect x="{W // 2 - 66}" y="{bridge_cy - 17}" width="132" height="34" rx="17" fill="{t["accent_fill"]}" stroke="{t["accent"]}" stroke-width="1.5"/>
  <text x="{W // 2}" y="{bridge_cy + 5}" class="mono" font-size="13" text-anchor="middle" fill="{t["accent"]}">broker bridge</text>
  <text x="{W // 2}" y="{bridge_cy + 40}" class="sans" font-size="14" text-anchor="middle" fill="{t["muted"]}">only OT to IT path</text>
</svg>
"""
    )


# Project tiles --------------------------------------------------------------------------

TW, TH, PAD = 268, 252, 20
X0, X1 = PAD, TW - PAD
SPAN = X1 - X0


def tile_head(t: dict, name: str, line1: str, line2: str) -> str:
    return (
        frame(t, TW, TH)
        + f"""  <text x="{PAD}" y="40" class="sans" font-size="20" font-weight="700" fill="{t["ink"]}">{name}</text>
  <text class="sans" font-size="14" fill="{t["muted"]}">
    <tspan x="{PAD}" y="64">{line1}</tspan>
    <tspan x="{PAD}" y="83">{line2}</tspan>
  </text>
"""
    )


def tile_pipeline(t: dict) -> str:
    runs = [3242, 4675, 3959, 4451]  # messages/s, sparkplug-pipeline README, Throughput
    median, lo, hi = 4205, 3000, 5000

    def sx(v):
        return X0 + (v - lo) / (hi - lo) * SPAN

    axis_y = 178
    dots = "".join(
        f'  <circle cx="{sx(v):.1f}" cy="{axis_y - 14}" r="6" fill="{t["accent"]}" fill-opacity="0.85"/>\n' for v in runs
    )
    ticks = "".join(
        f'  <line x1="{sx(v):.1f}" y1="{axis_y}" x2="{sx(v):.1f}" y2="{axis_y + 5}" stroke="{t["muted"]}"/>\n'
        f'  <text x="{sx(v):.1f}" y="{axis_y + 21}" class="mono" font-size="12" text-anchor="{a}" fill="{t["muted"]}">{v:,}</text>\n'
        for v, a in ((3000, "start"), (4000, "middle"), (5000, "end"))
    )
    m = sx(median)
    return (
        svg_open(
            TW,
            TH,
            "sparkplug-pipeline",
            "Sparkplug B over MQTT into TimescaleDB. Four ingest runs on a laptop at 3,242, 3,959, "
            "4,451 and 4,675 messages per second, median 4,205.",
        )
        + tile_head(t, "sparkplug-pipeline", "Sparkplug B over MQTT", "into TimescaleDB")
        + f"""  <line x1="{m:.1f}" y1="{axis_y - 52}" x2="{m:.1f}" y2="{axis_y}" stroke="{t["ink"]}" stroke-width="1.5"/>
  <text x="{m - 6:.1f}" y="{axis_y - 42}" class="mono" font-size="13" text-anchor="end" fill="{t["ink"]}">median 4,205</text>
  <line x1="{X0}" y1="{axis_y}" x2="{X1}" y2="{axis_y}" stroke="{t["border"]}"/>
{dots}{ticks}  <text x="{PAD}" y="{TH - 20}" class="mono" font-size="12.5" fill="{t["muted"]}">msg/s ingest, 4 runs, laptop</text>
</svg>
"""
    )


def tile_conform(t: dict) -> str:
    total, exe = 299, 143  # spbconform README
    ew = SPAN * exe / total
    bar_y = 132
    return (
        svg_open(
            TW,
            TH,
            "spbconform",
            "Sparkplug B v3.0.0 conformance, clean-room. Of 299 testable assertions, 143 have "
            "executable checks and 156 have a recorded reason.",
        )
        + f"""  <defs>
    <pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="6" stroke="{t["hatch"]}" stroke-width="2"/>
    </pattern>
  </defs>
"""
        + tile_head(t, "spbconform", "Sparkplug B v3.0.0", "conformance, clean-room")
        + f"""  <text x="{X0}" y="{bar_y - 10}" class="mono" font-size="13" fill="{t["ink"]}">299 testable assertions</text>
  <rect x="{X0}" y="{bar_y}" width="{ew:.1f}" height="22" rx="3" fill="{t["accent"]}"/>
  <rect x="{X0 + ew + 3:.1f}" y="{bar_y + 0.5}" width="{SPAN - ew - 3.5:.1f}" height="21" rx="3" fill="url(#hatch)" stroke="{t["hatch"]}"/>
  <rect x="{X0}" y="{bar_y + 40}" width="12" height="12" rx="2" fill="{t["accent"]}"/>
  <text x="{X0 + 20}" y="{bar_y + 51}" class="mono" font-size="13" fill="{t["ink"]}">143 executable checks</text>
  <rect x="{X0 + 0.5}" y="{bar_y + 64.5}" width="11" height="11" rx="2" fill="url(#hatch)" stroke="{t["hatch"]}"/>
  <text x="{X0 + 20}" y="{bar_y + 75}" class="mono" font-size="13" fill="{t["ink"]}">156 with a recorded reason</text>
  <text x="{PAD}" y="{TH - 20}" class="mono" font-size="12.5" fill="{t["muted"]}">zero dependencies, MIT</text>
</svg>
"""
    )


def tile_secom(t: dict) -> str:
    # Gradient boosting on the time-ordered test block, secom-spc README, result 4.
    noskill, auc, ci_lo, ci_hi, amax = 0.055, 0.085, 0.052, 0.167, 0.18

    def ax(v):
        return X0 + v / amax * SPAN

    axis_y, row_y = 178, 160
    ticks = "".join(
        f'  <line x1="{ax(v):.1f}" y1="{axis_y}" x2="{ax(v):.1f}" y2="{axis_y + 5}" stroke="{t["muted"]}"/>\n'
        f'  <text x="{ax(v):.1f}" y="{axis_y + 21}" class="mono" font-size="12" text-anchor="{a}" fill="{t["muted"]}">{v:.2f}</text>\n'
        for v, a in ((0.0, "start"), (0.05, "middle"), (0.10, "middle"), (0.15, "middle"))
    )
    ns = ax(noskill)
    return (
        svg_open(
            TW,
            TH,
            "secom-spc",
            "Statistical process control on UCI SECOM semiconductor data. The fail predictor's PR-AUC "
            "is 0.085 with a 95% interval of 0.052 to 0.167, which reaches below the 0.055 no-skill "
            "baseline, so it does not clearly beat chance.",
        )
        + tile_head(t, "secom-spc", "SPC on semiconductor fab", "data, UCI SECOM")
        + f"""  <line x1="{ns:.1f}" y1="{row_y - 40}" x2="{ns:.1f}" y2="{axis_y}" stroke="{t["muted"]}" stroke-width="1.5" stroke-dasharray="3 3"/>
  <text x="{ns - 6:.1f}" y="{row_y - 16}" class="mono" font-size="12.5" text-anchor="end" fill="{t["muted"]}">no skill</text>
  <line x1="{ax(ci_lo):.1f}" y1="{row_y}" x2="{ax(ci_hi):.1f}" y2="{row_y}" stroke="{t["accent"]}" stroke-width="2"/>
  <line x1="{ax(ci_lo):.1f}" y1="{row_y - 6}" x2="{ax(ci_lo):.1f}" y2="{row_y + 6}" stroke="{t["accent"]}" stroke-width="2"/>
  <line x1="{ax(ci_hi):.1f}" y1="{row_y - 6}" x2="{ax(ci_hi):.1f}" y2="{row_y + 6}" stroke="{t["accent"]}" stroke-width="2"/>
  <circle cx="{ax(auc):.1f}" cy="{row_y}" r="6" fill="{t["accent"]}"/>
  <text x="{ax(auc) + 2:.1f}" y="{row_y - 16}" class="mono" font-size="12.5" fill="{t["ink"]}">fail predictor</text>
  <line x1="{X0}" y1="{axis_y}" x2="{X1}" y2="{axis_y}" stroke="{t["border"]}"/>
{ticks}  <text x="{PAD}" y="{TH - 20}" class="mono" font-size="12.5" fill="{t["muted"]}">PR-AUC, 95% CI: no clear win</text>
</svg>
"""
    )


ASSET_BUILDERS = {
    "banner": banner,
    "twinflow": twinflow,
    "tile-sparkplug-pipeline": tile_pipeline,
    "tile-spbconform": tile_conform,
    "tile-secom-spc": tile_secom,
}


def main() -> None:
    for stem, build in ASSET_BUILDERS.items():
        for name, theme in THEMES.items():
            (ASSETS / f"{stem}-{name}.svg").write_text(build(theme), encoding="utf-8", newline="\n")
    print("wrote", sorted(p.name for p in ASSETS.glob("*.svg")))


if __name__ == "__main__":
    main()
