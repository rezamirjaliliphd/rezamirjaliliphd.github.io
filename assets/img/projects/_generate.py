"""Generate the project-card thumbnails as self-contained SVGs.

Each card gets an abstract motif drawn from the same palette as the site theme
and the Manim hero animation, so the projects page reads as one system rather
than a pile of stock photos.

    python assets/img/projects/_generate.py
"""

from __future__ import annotations

import math
import os
import random

W, H = 1200, 750
OUT = os.path.dirname(os.path.abspath(__file__))

BG_A = "#0b1220"
BG_B = "#132033"
TEAL = "#2dd4bf"
AMBER = "#fbbf24"
ROSE = "#fb7185"
SLATE = "#64748b"
SLATE_LIGHT = "#94a3b8"


def head(seed: int) -> list[str]:
    random.seed(seed)
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">',
        "<defs>",
        f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0%" stop-color="{BG_A}"/><stop offset="100%" stop-color="{BG_B}"/></linearGradient>',
        f'<radialGradient id="glow" cx="50%" cy="50%" r="50%">'
        f'<stop offset="0%" stop-color="{TEAL}" stop-opacity="0.20"/>'
        f'<stop offset="100%" stop-color="{TEAL}" stop-opacity="0"/></radialGradient>',
        "</defs>",
        f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
        f'<circle cx="{W*0.68}" cy="{H*0.3}" r="{H*0.62}" fill="url(#glow)"/>',
    ]


def tail() -> list[str]:
    return ["</svg>"]


def write(name: str, body: list[str], seed: int) -> None:
    svg = "\n".join(head(seed) + body + tail())
    path = os.path.join(OUT, f"{name}.svg")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(f"wrote {path}")


def dot(x, y, r=9, fill=SLATE, opacity=1.0):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" opacity="{opacity}"/>'


def line(x1, y1, x2, y2, stroke=SLATE, w=2.5, opacity=0.6, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{stroke}" stroke-width="{w}" opacity="{opacity}" stroke-linecap="round"{d}/>'
    )


def path(d, stroke=TEAL, w=4, opacity=1.0, fill="none", dash=None):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" '
        f'opacity="{opacity}" stroke-linecap="round" stroke-linejoin="round"{da}/>'
    )


# --- motifs ------------------------------------------------------------------


def mothership_routing() -> list[str]:
    """Support vehicle route with drone sorties fanning out."""
    body = []
    stops = [(210, 520), (430, 330), (660, 470), (900, 300)]
    depot = (110, 620)

    pts = [depot] + stops
    d = f"M {depot[0]} {depot[1]} " + " ".join(f"L {x} {y}" for x, y in stops)
    body.append(path(d, TEAL, 5))
    body.append(
        path(f"M {stops[-1][0]} {stops[-1][1]} L 1050 640 L {depot[0]} 660",
             TEAL, 4, opacity=0.35, dash="10 12")
    )

    customers = [
        [(140, 330), (300, 210), (170, 690)],
        [(380, 130), (560, 175), (455, 545)],
        [(640, 210), (790, 300), (700, 660)],
        [(880, 130), (1060, 165), (1030, 450)],
    ]
    for (sx, sy), group in zip(stops, customers):
        for cx, cy in group:
            mx, my = (sx + cx) / 2, (sy + cy) / 2
            nx, ny = -(cy - sy), (cx - sx)
            norm = max(1.0, math.hypot(nx, ny))
            k = 42
            body.append(
                path(f"M {sx} {sy} Q {mx + nx/norm*k:.0f} {my + ny/norm*k:.0f} {cx} {cy}",
                     AMBER, 2.4, opacity=0.55)
            )
            body.append(dot(cx, cy, 10, AMBER, 0.95))
        body.append(f'<circle cx="{sx}" cy="{sy}" r="20" fill="none" stroke="{TEAL}" stroke-width="3.5"/>')
        body.append(dot(sx, sy, 6, TEAL))

    body.append(
        f'<rect x="{depot[0]-17}" y="{depot[1]-17}" width="34" height="34" rx="4" '
        f'fill="{TEAL}" stroke="#f8fafc" stroke-width="3"/>'
    )
    return body


def branch_tree() -> list[str]:
    """Branch-and-bound tree with a pruned subtree and an incumbent."""
    body = []
    levels = [[(600, 130)],
              [(380, 300), (820, 300)],
              [(260, 470), (500, 470), (720, 470), (950, 470)],
              [(200, 640), (320, 640), (560, 640), (880, 640), (1010, 640)]]
    edges = [
        (0, 0, 1, 0), (0, 0, 1, 1),
        (1, 0, 2, 0), (1, 0, 2, 1), (1, 1, 2, 2), (1, 1, 2, 3),
        (2, 0, 3, 0), (2, 0, 3, 1), (2, 1, 3, 2), (2, 3, 3, 3), (2, 3, 3, 4),
    ]
    active = {(1, 0), (2, 1), (3, 2)}
    pruned = {(2, 2), (3, 3), (3, 4)}

    for la, ia, lb, ib in edges:
        x1, y1 = levels[la][ia]
        x2, y2 = levels[lb][ib]
        on_path = (la, ia) in active or (lb, ib) in active or (la, ia) == (0, 0)
        col = TEAL if on_path else SLATE
        body.append(line(x1, y1, x2, y2, col, 3.5 if on_path else 2.2, 0.9 if on_path else 0.35))

    for li, row in enumerate(levels):
        for ii, (x, y) in enumerate(row):
            key = (li, ii)
            if key in pruned:
                body.append(dot(x, y, 13, ROSE, 0.5))
                body.append(line(x - 9, y - 9, x + 9, y + 9, ROSE, 3, 0.9))
                body.append(line(x - 9, y + 9, x + 9, y - 9, ROSE, 3, 0.9))
            elif key in active or key == (0, 0):
                body.append(dot(x, y, 15, TEAL))
            else:
                body.append(dot(x, y, 12, SLATE, 0.55))

    ix, iy = levels[3][2]
    body.append(f'<circle cx="{ix}" cy="{iy}" r="26" fill="none" stroke="{AMBER}" stroke-width="3.5"/>')
    return body


def cutting_planes() -> list[str]:
    """A relaxation polytope sliced by successive cutting planes."""
    body = []
    poly = "M 240 620 L 180 380 L 360 190 L 700 150 L 960 300 L 930 590 L 620 690 Z"
    body.append(path(poly, SLATE_LIGHT, 3, opacity=0.55, fill="rgba(45,212,191,0.10)"))

    cuts = [
        ("M 150 250 L 1050 430", AMBER, 0.9),
        ("M 300 700 L 1010 200", TEAL, 0.75),
        ("M 130 520 L 1020 620", SLATE_LIGHT, 0.45),
    ]
    for d, col, op in cuts:
        body.append(path(d, col, 3.2, opacity=op, dash="14 10"))

    lattice = []
    for gx in range(200, 1010, 78):
        for gy in range(170, 690, 74):
            lattice.append((gx, gy))
    for gx, gy in lattice:
        body.append(dot(gx, gy, 4.5, SLATE, 0.45))

    for x, y in [(430, 330), (586, 404), (664, 330), (508, 478)]:
        body.append(dot(x, y, 9, TEAL))
    body.append(dot(586, 404, 17, "none"))
    body.append(f'<circle cx="586" cy="404" r="19" fill="none" stroke="{AMBER}" stroke-width="3.5"/>')
    return body


def resilience_curve() -> list[str]:
    """Network performance dropping at a storm and recovering."""
    body = []
    body.append(line(140, 640, 1060, 640, SLATE, 2.5, 0.5))
    body.append(line(140, 640, 140, 150, SLATE, 2.5, 0.5))

    body.append(
        f'<rect x="330" y="150" width="150" height="490" fill="{SLATE_LIGHT}" opacity="0.10"/>'
    )
    baseline = "M 140 250 L 330 250"
    drop = "M 330 250 C 380 250 420 560 480 570"
    recover = "M 480 570 C 620 570 700 300 900 262 L 1060 258"
    body.append(path(baseline, SLATE_LIGHT, 4, opacity=0.6, dash="10 10"))
    body.append(path(drop, ROSE, 5))
    body.append(path(recover, TEAL, 5))

    body.append(
        f'<path d="M 140 250 L 330 250 C 380 250 420 560 480 570 '
        f'C 620 570 700 300 900 262 L 1060 258 L 1060 250 L 140 250 Z" '
        f'fill="{ROSE}" opacity="0.12"/>'
    )
    body.append(dot(480, 570, 12, ROSE))
    body.append(dot(900, 262, 12, TEAL))
    for x in (330, 480, 900):
        body.append(line(x, 640, x, 660, SLATE_LIGHT, 3, 0.7))
    return body


def gnn_layers() -> list[str]:
    """Message passing across a heterogeneous activity-resource graph."""
    body = []
    cols = [
        (250, [190, 330, 470, 610]),
        (600, [160, 300, 440, 580, 700]),
        (950, [250, 400, 550]),
    ]
    nodes = []
    for cx, ys in cols:
        nodes.append([(cx, y) for y in ys])

    for a, b in ((0, 1), (1, 2)):
        for i, (x1, y1) in enumerate(nodes[a]):
            for j, (x2, y2) in enumerate(nodes[b]):
                if (i + j) % 2 == 0:
                    body.append(line(x1, y1, x2, y2, TEAL, 2, 0.28))

    palette = [AMBER, TEAL, TEAL]
    for li, layer in enumerate(nodes):
        for x, y in layer:
            body.append(dot(x, y, 18, palette[li], 0.22))
            body.append(dot(x, y, 11, palette[li]))

    for x, y in nodes[1][:2]:
        body.append(f'<circle cx="{x}" cy="{y}" r="26" fill="none" stroke="{AMBER}" stroke-width="2.6" opacity="0.8"/>')
    return body


def timeseries() -> list[str]:
    """Observed series with a forecast fan."""
    body = []
    body.append(line(120, 660, 1080, 660, SLATE, 2.5, 0.45))

    xs = list(range(140, 700, 22))
    y = 430
    pts = []
    for x in xs:
        y += random.uniform(-38, 34)
        y = max(220, min(600, y))
        pts.append((x, y))
    d = "M " + " L ".join(f"{x} {y:.0f}" for x, y in pts)
    body.append(path(d, SLATE_LIGHT, 3.4, opacity=0.85))

    fx, fy = pts[-1]
    body.append(
        f'<path d="M {fx} {fy:.0f} L 1060 250 L 1060 470 Z" fill="{TEAL}" opacity="0.14"/>'
    )
    body.append(path(f"M {fx} {fy:.0f} C 800 {fy-40:.0f} 900 330 1060 300", TEAL, 4.5))
    body.append(line(fx, 180, fx, 660, AMBER, 2.6, 0.7, dash="10 10"))
    body.append(dot(fx, fy, 11, AMBER))
    for gy in (250, 350, 450, 550):
        body.append(line(120, gy, 1080, gy, SLATE, 1.4, 0.16))
    return body


def conv_stack() -> list[str]:
    """Convolutional feature maps shrinking, with a tuning sweep beneath."""
    body = []
    specs = [(150, 170, 300, 300), (400, 215, 210, 210), (650, 250, 140, 140), (840, 275, 90, 90)]
    for i, (x, y, w, h) in enumerate(specs):
        for k in range(3):
            off = k * 14
            body.append(
                f'<rect x="{x+off}" y="{y-off}" width="{w}" height="{h}" rx="6" '
                f'fill="{TEAL}" opacity="{0.10 + 0.05*k}" stroke="{TEAL}" '
                f'stroke-width="2" stroke-opacity="0.5"/>'
            )
    body.append(dot(1010, 320, 13, AMBER))
    body.append(dot(1010, 370, 13, AMBER, 0.55))
    body.append(dot(1010, 420, 13, AMBER, 0.3))

    bx, by, bw = 150, 640, 780
    for i in range(14):
        v = random.uniform(0.15, 1.0)
        h = 70 * v
        col = AMBER if v > 0.86 else SLATE
        body.append(
            f'<rect x="{bx + i*(bw/14):.0f}" y="{by - h:.0f}" width="{bw/14 - 12:.0f}" '
            f'height="{h:.0f}" rx="4" fill="{col}" opacity="{0.85 if v > 0.86 else 0.4}"/>'
        )
    return body


def seq2seq() -> list[str]:
    """Encoder-decoder with attention links between two token rows."""
    body = []
    src = [(180 + i * 130, 250) for i in range(7)]
    tgt = [(230 + i * 130, 560) for i in range(6)]

    for i, (x1, y1) in enumerate(src):
        for j, (x2, y2) in enumerate(tgt):
            weight = math.exp(-((i - j * 1.1) ** 2) / 3.0)
            if weight > 0.12:
                body.append(line(x1, y1 + 26, x2, y2 - 26, AMBER, 2.2, 0.55 * weight))

    for x, y in src:
        body.append(
            f'<rect x="{x-46}" y="{y-26}" width="92" height="52" rx="10" '
            f'fill="{TEAL}" opacity="0.16" stroke="{TEAL}" stroke-width="2.4"/>'
        )
    for x, y in tgt:
        body.append(
            f'<rect x="{x-46}" y="{y-26}" width="92" height="52" rx="10" '
            f'fill="{AMBER}" opacity="0.14" stroke="{AMBER}" stroke-width="2.4"/>'
        )
    return body


def grid_policy() -> list[str]:
    """Grid world with broken arcs and a learned optimal path."""
    body = []
    n, cell, ox, oy = 5, 108, 340, 110
    for r in range(n):
        for c in range(n):
            x, y = ox + c * cell, oy + r * cell
            body.append(
                f'<rect x="{x}" y="{y}" width="{cell-10}" height="{cell-10}" rx="8" '
                f'fill="{SLATE}" opacity="0.14" stroke="{SLATE}" stroke-width="1.6" stroke-opacity="0.4"/>'
            )

    def center(r, c):
        return ox + c * cell + (cell - 10) / 2, oy + r * cell + (cell - 10) / 2

    broken = [((1, 1), (1, 2)), ((2, 3), (3, 3)), ((3, 1), (3, 2))]
    for (r1, c1), (r2, c2) in broken:
        x1, y1 = center(r1, c1)
        x2, y2 = center(r2, c2)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        body.append(line(mx - 26, my - 26, mx + 26, my + 26, ROSE, 5, 0.9))
        body.append(line(mx - 26, my + 26, mx + 26, my - 26, ROSE, 5, 0.9))

    route = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (3, 2), (4, 2), (4, 3), (4, 4)]
    pts = [center(r, c) for r, c in route]
    d = "M " + " L ".join(f"{x:.0f} {y:.0f}" for x, y in pts)
    body.append(path(d, TEAL, 6))
    for x, y in pts:
        body.append(dot(x, y, 7, TEAL))

    sx, sy = center(0, 0)
    gx, gy = center(4, 4)
    body.append(f'<circle cx="{sx}" cy="{sy}" r="24" fill="none" stroke="{TEAL}" stroke-width="4"/>')
    body.append(f'<circle cx="{gx}" cy="{gy}" r="24" fill="{AMBER}" opacity="0.9"/>')
    return body


MOTIFS = {
    "mothership-routing": (mothership_routing, 7),
    "drl-pricing": (branch_tree, 11),
    "cutting-planes": (cutting_planes, 3),
    "network-resilience": (resilience_curve, 5),
    "project-gnn": (gnn_layers, 13),
    "lstm-forecasting": (timeseries, 17),
    "cnn-optuna": (conv_stack, 23),
    "t5-translation": (seq2seq, 29),
    "qlearning-path": (grid_policy, 31),
}

if __name__ == "__main__":
    for name, (fn, seed) in MOTIFS.items():
        random.seed(seed)
        write(name, fn(), seed)
