#!/usr/bin/env python3
"""Build the README diagrams as paired light and dark SVGs.

Run from anywhere:  python diagrams/build.py
Writes six files into the directory holding this script.

The diagrams are authored here rather than drawn by a layout engine, so the
geometry is deliberate and the two theme variants cannot drift apart. Text is
pre-wrapped in the data below; nothing is measured at runtime, which keeps the
output byte-stable across machines.
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent

# --------------------------------------------------------------------------
# Design system
# --------------------------------------------------------------------------

SANS = "ui-sans-serif,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

LIGHT = {
    "name": "light",
    "ink": "#111827",       # headings
    "body": "#4b5563",      # detail text
    "faint": "#9ca3af",     # eyebrows and meta
    "rule": "#e5e7eb",      # hairlines and panel edges
    "stroke": "#b6bec9",    # connectors
    "panel": "#f9fafb",     # enclosing wash
    "chip": "#ffffff",      # node fill
    "accent": "#b45309",    # single accent, amber
    "accentFill": "#fdf6e7",
    "bar": "#ccd3dc",
    "barAccent": "#c98a2e",
}

DARK = {
    "name": "dark",
    "ink": "#e6edf3",
    "body": "#a9b3bf",
    "faint": "#6e7781",
    "rule": "#2a3038",
    "stroke": "#48515c",
    "panel": "#13181f",
    "chip": "#0f141a",
    "accent": "#e0a53d",
    "accentFill": "#201a0e",
    "bar": "#343c46",
    "barAccent": "#a9802f",
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, fill, size=13.5, weight=400, family=SANS, anchor="start",
         spacing=None, opacity=None, style=None):
    bits = [
        f'x="{x}" y="{y}"',
        f'font-family="{family}"',
        f'font-size="{size}"',
        f'fill="{fill}"',
    ]
    if weight != 400:
        bits.append(f'font-weight="{weight}"')
    if anchor != "start":
        bits.append(f'text-anchor="{anchor}"')
    if spacing:
        bits.append(f'letter-spacing="{spacing}"')
    if opacity:
        bits.append(f'opacity="{opacity}"')
    if style:
        bits.append(f'font-style="{style}"')
    return f'<text {" ".join(bits)}>{esc(s)}</text>'


def eyebrow(x, y, s, t, anchor="start"):
    return text(x, y, s.upper(), t["faint"], size=9.5, weight=600,
                spacing="1.4", anchor=anchor)


def rect(x, y, w, h, fill, stroke=None, r=7, sw=1.0, dash=None):
    bits = [f'x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"', f'fill="{fill}"']
    if stroke:
        bits.append(f'stroke="{stroke}" stroke-width="{sw}"')
    if dash:
        bits.append(f'stroke-dasharray="{dash}"')
    return f'<rect {" ".join(bits)}/>'


def line(x1, y1, x2, y2, stroke, sw=1.0, dash=None, cap="round"):
    bits = [f'x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"',
            f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"']
    if dash:
        bits.append(f'stroke-dasharray="{dash}"')
    return f'<line {" ".join(bits)}/>'


def document(w, h, t, body, title, desc):
    """Wrap body elements in an SVG root. Background stays transparent so the
    page colour shows through in either GitHub theme."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" role="img" aria-labelledby="t d">'
        f'<title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>'
        f'<defs><marker id="ah" viewBox="0 0 8 8" refX="6.4" refY="4" '
        f'markerWidth="7" markerHeight="7" orient="auto">'
        f'<path d="M0.6 1.1 L6.6 4 L0.6 6.9" fill="none" stroke="{t["stroke"]}" '
        f'stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>'
        f'</marker>'
        f'<marker id="ahA" viewBox="0 0 8 8" refX="6.4" refY="4" '
        f'markerWidth="7" markerHeight="7" orient="auto">'
        f'<path d="M0.6 1.1 L6.6 4 L0.6 6.9" fill="none" stroke="{t["accent"]}" '
        f'stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>'
        f'</marker></defs>'
        + "".join(body) + "</svg>"
    )


# --------------------------------------------------------------------------
# Diagram 1: the run
# --------------------------------------------------------------------------

RUN_THINKING = [
    ("1", "classify", ["request type, session model, target model,",
                       "files named, steps with outside reach"]),
    ("2", "golden-rule pass", ["what a colleague with no context would ask,",
                               "answered from the repository first"]),
    ("3", "compose", ["fill the template in fixed tag order"]),
    ("4", "convert", ["rewrite the phrasing current models handle poorly"]),
]
RUN_VISIBLE = [
    ("5", "the prompt, on screen", ["with the target model, the assumptions made,",
                                    "and the wording that changed"], True),
    ("6", "execute", ["independent calls batched, files read before",
                      "claims about them, flagged steps wait for you"], False),
    ("7", "verify", ["run the checks it wrote, confirm the files",
                     "touched match the ones the task named"], False),
]


def diagram_run(t):
    W = 880
    L = 64               # panel left
    R = W - 64           # panel right
    spine = L + 34
    tx = spine + 34      # text left edge
    out = []
    y = 56

    out.append(eyebrow(L, 26, "a run, start to finish", t))

    # ---- thinking panel ----
    panel_top = y - 18
    rows = []
    for num, head, detail in RUN_THINKING:
        rows.append((y, num, head, detail, False))
        y += 24 + 16 * len(detail) + 16
    panel_bot = y - 20
    out.insert(1, rect(L, panel_top, R - L, panel_bot - panel_top,
                       t["panel"], t["rule"], r=10, sw=1.0))
    out.append(eyebrow(R - 14, panel_top + 18, "in thinking, nothing on screen", t,
                       anchor="end"))

    # ---- divider ----
    dy = panel_bot + 30
    out.append(line(L, dy, R, dy, t["rule"], 1.0))
    label = "what you see"
    out.append(rect(L + 22, dy - 10, 104, 20, t["chip"], None, r=10))
    out.append(eyebrow(L + 32, dy + 4, label, t))

    # ---- visible rows ----
    y = dy + 34
    for num, head, detail, is_accent in RUN_VISIBLE:
        rows.append((y, num, head, detail, is_accent))
        y += 24 + 16 * len(detail) + 16

    # spine behind everything
    first_y = rows[0][0]
    last_y = rows[-1][0]
    out.insert(1, line(spine, first_y - 4, spine, last_y + 6, t["rule"], 1.2))

    # ---- rows ----
    for ry, num, head, detail, is_accent in rows:
        col = t["accent"] if is_accent else t["ink"]
        ring = t["accent"] if is_accent else t["stroke"]
        fill = t["accentFill"] if is_accent else t["chip"]
        out.append(f'<circle cx="{spine}" cy="{ry}" r="12.5" fill="{fill}" '
                   f'stroke="{ring}" stroke-width="1.1"/>')
        out.append(text(spine, ry + 4.2, num, col, size=11.5, weight=600,
                        family=MONO, anchor="middle"))
        out.append(text(tx, ry + 5, head, col, size=14.5, weight=600))
        for i, d in enumerate(detail):
            out.append(text(tx, ry + 25 + i * 16, d, t["body"], size=12.5))

    # ---- dry run annotation, attached beside the step 5 heading ----
    step5_y = rows[4][0]
    ax = tx + 196
    out.append(line(tx + 178, step5_y, ax - 6, step5_y, t["rule"], 1.0, dash="2 3"))
    out.append(rect(ax, step5_y - 12, 182, 25, t["chip"], t["rule"], r=12, dash="3 3"))
    out.append(text(ax + 14, step5_y + 5, "a dry run stops here", t["faint"], size=11.5))

    # ---- outcome ----
    oy = last_y + 22 + 16 * len(rows[-1][3]) + 10
    out.append(line(spine, last_y + 20, spine, oy - 10, t["stroke"], 1.1,
                    dash="2 4"))
    out.append(f'<path d="M{spine} {oy - 12} v6" stroke="{t["stroke"]}" '
               f'stroke-width="1.1" marker-end="url(#ah)" fill="none"/>')
    out.append(text(tx, oy + 2, "a recap that reads on its own", t["ink"],
                    size=13.5, weight=600))
    H = oy + 42

    return document(W, H, t, out, "How a run works",
                    "Seven numbered steps. Steps one to four happen in thinking: classify, "
                    "golden-rule pass, compose, convert. Step five puts the prompt on screen "
                    "with its assumptions, and a dry run stops there. Steps six and seven "
                    "execute and verify, ending in a recap that reads on its own.")


# --------------------------------------------------------------------------
# Diagram 2: how the target model is resolved
# --------------------------------------------------------------------------

def diagram_target(t):
    W, H = 880, 436
    L = 64
    out = []
    out.append(eyebrow(L, 26, "which profile writes the prompt", t))

    rows = [
        ("1", "a model flag is passed", "/rearticulate --model opus-5 …", "that profile", True),
        ("2", "a model is named for the deliverable", "\"write a system prompt for Sonnet 5\"", "that profile", False),
        ("3", "neither", "the ordinary case", "the model running the session", False),
    ]

    y = 62
    cond_x, cond_w = L, 392
    out_x = L + 470
    for num, cond, example, result, first in rows:
        out.append(rect(cond_x, y, cond_w, 54, t["chip"], t["rule"], r=8))
        out.append(text(cond_x + 18, y + 23, num, t["faint"], size=11, weight=600, family=MONO))
        out.append(text(cond_x + 38, y + 23, cond, t["ink"], size=13.5, weight=600))
        out.append(text(cond_x + 38, y + 41, example, t["faint"], size=11.5, family=MONO))

        col = t["accent"] if first else t["stroke"]
        mk = "url(#ahA)" if first else "url(#ah)"
        out.append(f'<path d="M{cond_x + cond_w + 10} {y + 27} H{out_x - 12}" '
                   f'stroke="{col}" stroke-width="1.1" fill="none" marker-end="{mk}"/>')
        rcol = t["accent"] if first else t["ink"]
        out.append(text(out_x, y + 31, result, rcol, size=13.5, weight=600 if first else 400))
        if first:
            out.append(text(out_x, y + 48, "first match wins", t["faint"], size=11))
        y += 70

    # ---- the split ----
    sy = y + 16
    out.append(line(L, sy, W - 64, sy, t["rule"], 1.0))
    out.append(eyebrow(L, sy + 26, "two dimensions, kept apart", t))

    pairs = [
        ("what the prompt says", "follows the target profile"),
        ("how the session behaves", "follows the model actually running it"),
    ]
    py = sy + 48
    for left, right in pairs:
        out.append(f'<circle cx="{L + 4}" cy="{py + 7}" r="2.6" fill="{t["stroke"]}"/>')
        out.append(text(L + 18, py + 11, left, t["ink"], size=13, weight=600))
        out.append(text(L + 218, py + 11, right, t["body"], size=13))
        py += 26

    out.append(line(L, py + 14, W - 64, py + 14, t["rule"], 1.0))
    out.append(text(L, py + 40, "A model mentioned in passing changes nothing.",
                    t["body"], size=13))

    return document(W, H, t, out, "How the target model is resolved",
                    "Three precedence rules, first match wins: a model flag, then a model "
                    "named for the deliverable, otherwise the session model. The prompt "
                    "content follows the target profile while narration, verification and "
                    "delegation follow the model actually running the session.")


# --------------------------------------------------------------------------
# Diagram 3: what is resident and what waits
# --------------------------------------------------------------------------

CONTEXT_ROWS = [
    ("templates/rearticulated-prompt.md", 370, "read on each run", True),
    ("references/models/ and model-notes.md", 5414, "a model is named, or a flag is passed", False),
    ("references/technique-catalog.md", 3610, "porting a prompt, or you ask why", False),
    ("references/snippet-library.md", 1303, "grafting a block not in the template", False),
    ("examples/rearticulations.md", 877, "no taxonomy row fits", False),
    ("references/request-taxonomy.md", 326, "two rows match, or an unusual signal", False),
]


def diagram_context(t):
    W = 880
    L = 64
    bar_x = 486
    bar_max = 300
    scale = bar_max / 5414.0
    out = []

    out.append(eyebrow(L, 26, "what sits in context, and what waits", t))

    # resident
    y = 58
    out.append(rect(L, y, 404, 56, t["accentFill"], t["accent"], r=8, sw=1.1))
    out.append(text(L + 18, y + 24, "SKILL.md", t["accent"], size=14, weight=600, family=MONO))
    out.append(text(L + 18, y + 43, "loaded when you invoke the skill", t["body"], size=12))
    w = max(3.0, 130 * scale)
    out.append(rect(bar_x, y + 20, w, 10, t["barAccent"], None, r=3))
    out.append(text(bar_x + w + 10, y + 29, "130 lines", t["accent"], size=12, weight=600, family=MONO))

    # on demand
    y += 86
    out.append(eyebrow(L, y, "opened on a stated trigger", t))
    y += 18

    for path, lines, trigger, solid in CONTEXT_ROWS:
        out.append(text(L + 18, y + 14, path, t["ink"], size=12.5, family=MONO))
        out.append(text(L + 18, y + 31, trigger, t["faint"], size=11.5))
        out.append(line(L + 4, y + 2, L + 4, y + 34, t["rule"] if not solid else t["stroke"],
                        1.6, dash=None if solid else "2 3"))
        w = max(3.0, lines * scale)
        out.append(rect(bar_x, y + 8, w, 10, t["bar"], None, r=3))
        out.append(text(bar_x + w + 10, y + 17, f"{lines:,} lines", t["body"],
                        size=12, family=MONO))
        y += 46

    y += 6
    out.append(line(L, y, W - 64, y, t["rule"], 1.0))
    out.append(text(L, y + 24, "130 lines resident. The other 11,900 stay on disk until a run reaches for them.",
                    t["body"], size=13))

    H = y + 48
    return document(W, H, t, out, "What sits in context, and what waits",
                    "SKILL.md is 130 lines and loads when the skill is invoked. Six reference "
                    "files totalling about 11,900 lines open only on stated triggers, shown "
                    "with bars proportional to their length.")


# --------------------------------------------------------------------------

BUILDS = [
    ("the-run", diagram_run),
    ("target-model", diagram_target),
    ("context", diagram_context),
]


def main():
    for stem, fn in BUILDS:
        for theme in (LIGHT, DARK):
            path = OUT / f"{stem}-{theme['name']}.svg"
            path.write_text(fn(theme), encoding="utf-8")
            print(f"{path.name:28} {path.stat().st_size:>6} bytes")


if __name__ == "__main__":
    main()
