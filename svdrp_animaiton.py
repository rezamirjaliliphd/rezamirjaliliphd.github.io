"""
Truck-and-drone delivery: the optimal solution of instance C_nc50_nd3_ins19
(50 customers, 25 stations + depot, 1 truck, 3 drones), proven optimal by
branch-price-and-cut.

Written for 3b1b's manim (manimgl, https://github.com/3b1b/manim). Text is set in LaTeX
(needs a TeX install with dvisvgm). Truck and drone icons are Material Design Icons
(Pictogrammers, Apache 2.0) stored in assets/manim/icons/.

    pip install manimgl
    manimgl svdrp_animation.py SVDRPOptimal              # preview window
    manimgl svdrp_animation.py SVDRPOptimal -w --hd      # write a 1080p mp4
    manimgl svdrp_animation.py SVDRPOptimal -w --uhd     # write a 4K mp4

All times are minutes of the plan. The truck drives the station network; each
drone rides on the truck, is launched at a station, serves one or more customers,
and lands on the truck at the same or a later station. The timeline below is the
exact schedule of the optimal solution (cost = truck travel + drone flight +
truck waiting + drone hovering).
"""
from manimlib import *
import numpy as np
import shutil
import subprocess
import tempfile
from pathlib import Path

# ----------------------------------------------------------------------------
# LaTeX backend. manimgl normally needs `latex` + `dvisvgm`. If dvisvgm is not
# installed but `tectonic` and `pdftocairo` (poppler) are, compile with those
# instead: tectonic -> PDF -> SVG, with a lean preamble (Latin Modern).
# ----------------------------------------------------------------------------
TEX_PREAMBLE = r"""
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{xcolor}
"""

if shutil.which("dvisvgm") is None and shutil.which("tectonic") and shutil.which("pdftocairo"):
    import manimlib.utils.tex_file_writing as _tfw
    from manimlib.utils.cache import cache_on_disk

    @cache_on_disk
    def _tectonic_tex_to_svg(full_tex, compiler="latex", message=""):
        with tempfile.TemporaryDirectory() as tmp:
            tex = Path(tmp, "working.tex")
            tex.write_text(full_tex)
            r = subprocess.run(["tectonic", "-X", "compile", "--outdir", tmp, str(tex)],
                               capture_output=True, text=True)
            if r.returncode != 0:
                raise _tfw.LatexError((r.stdout + r.stderr)[-800:])
            svg = Path(tmp, "working.svg")
            subprocess.run(["pdftocairo", "-svg", str(Path(tmp, "working.pdf")), str(svg)], check=True)
            return svg.read_text()

    _tfw.full_tex_to_svg = _tectonic_tex_to_svg
    _tfw.get_tex_config = lambda template="": ("latex", TEX_PREAMBLE)

# ============================================================================
# Settings
# ============================================================================
SECONDS = 45.0                  # video seconds for the whole plan
BG_COLOR = "#0F1419"
EDGE_COLOR = "#3A4350"
STATION_COLOR = "#7D8794"
CUSTOMER_COLOR = "#AEB6BF"
TRUCK_COLOR = "#F5A623"
DRONE_COLORS = ["#4FC3F7", "#9CCC65", "#F06292"]
TEXT_COLOR = "#E6E9ED"
MUTED = "#8A94A0"

MAP_CENTER = np.array([1.75, -0.2, 0.0])
MAP_HEIGHT = 7.2
MAP_WIDTH = 9.4
PANEL_X = -6.75                 # left edge of the text panel
DOCK = 0.33                     # how far the drones sit from the truck centre
import os
ICON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "manim", "icons")
TRUCK_WIDTH = 0.62
DRONE_WIDTH = 0.27

# ============================================================================
# Data: the optimal solution (generated from the solver output)
# ============================================================================
INSTANCE = "C_nc50_nd3_ins19"
DEPOT = 0
STATIONS = list(range(0, 26))      # node 26 is the end-depot copy of node 0
CUSTOMERS = list(range(27, 77))
COORDS = {   # node: (x, y), from the instance file
    0: (35.7771, 44.7214),
    1: (11.4844, 12.3431),
    2: (30.5302, 13.8475),
    3: (51.6979, 12.3431),
    4: (71.8046, 12.3431),
    5: (91.9113, 12.3431),
    6: (11.4844, 29.8739),
    7: (37.1529, 27.2794),
    8: (53.0967, 29.4076),
    9: (70.3439, 29.3787),
    10: (91.9113, 29.8739),
    11: (11.4844, 47.4046),
    12: (31.5912, 47.4046),
    13: (49.226, 45.1575),
    14: (71.8046, 47.4046),
    15: (91.9113, 47.4046),
    16: (9.395, 62.6292),
    17: (31.8297, 67.6925),
    18: (53.8691, 68.2694),
    19: (71.8046, 64.9354),
    20: (91.9113, 64.9354),
    21: (11.4844, 82.4662),
    22: (31.5912, 82.4662),
    23: (51.6979, 82.4662),
    24: (71.8046, 82.4662),
    25: (91.9113, 82.4662),
    27: (59.0322, 49.1935),
    28: (12.522, 59.0322),
    29: (13.4164, 67.082),
    30: (69.7653, 35.7771),
    31: (31.305, 59.0322),
    32: (7.1554, 40.2492),
    33: (40.2492, 31.305),
    34: (37.5659, 51.8768),
    35: (33.9882, 8.9443),
    36: (42.0381, 31.305),
    37: (37.5659, 13.4164),
    38: (51.8768, 67.082),
    39: (22.3607, 76.0263),
    40: (37.5659, 58.1378),
    41: (31.305, 61.7155),
    42: (64.3988, 49.1935),
    43: (55.4545, 71.5542),
    44: (29.5161, 31.305),
    45: (8.9443, 35.7771),
    46: (3.5777, 49.1935),
    47: (49.1935, 76.0263),
    48: (33.9882, 4.4721),
    49: (17.8885, 49.1935),
    50: (80.4984, 31.305),
    51: (23.2551, 28.6217),
    52: (58.1378, 53.6656),
    53: (4.4721, 40.2492),
    54: (4.4721, 31.305),
    55: (20.5718, 46.5102),
    56: (50.0879, 57.2433),
    57: (7.1554, 35.7771),
    58: (46.5102, 67.082),
    59: (64.3988, 40.2492),
    60: (31.305, 4.4721),
    61: (62.6099, 51.8768),
    62: (1.7889, 35.7771),
    63: (31.305, 28.6217),
    64: (47.4046, 31.305),
    65: (13.4164, 71.5542),
    66: (22.3607, 26.8328),
    67: (51.8768, 62.6099),
    68: (53.6656, 49.1935),
    69: (55.4545, 61.7155),
    70: (22.3607, 44.7214),
    71: (76.0263, 31.305),
    72: (84.9706, 26.8328),
    73: (40.2492, 58.1378),
    74: (19.6774, 59.0322),
    75: (40.2492, 62.6099),
    76: (47.4046, 26.8328),
}
DEMAND = {27: 1, 28: 1, 29: 2, 30: 2, 31: 1, 32: 2, 33: 1, 34: 4, 35: 1, 36: 1, 37: 1, 38: 2, 39: 2, 40: 1, 41: 1, 42: 1, 43: 3, 44: 1, 45: 3, 46: 2, 47: 2, 48: 3, 49: 1, 50: 1, 51: 1, 52: 3, 53: 1, 54: 1, 55: 1, 56: 1, 57: 4, 58: 1, 59: 1, 60: 2, 61: 2, 62: 2, 63: 1, 64: 4, 65: 1, 66: 1, 67: 2, 68: 1, 69: 1, 70: 1, 71: 3, 72: 3, 73: 2, 74: 4, 75: 3, 76: 1}
TRUCK_EDGES = [  # road network between stations (undirected)
    (0, 7), (0, 8), (0, 11), (0, 12), (0, 13), (0, 17), (1, 2), (1, 6), (2, 3), (2, 6),
    (2, 7), (3, 4), (3, 7), (3, 8), (3, 9), (4, 5), (4, 8), (4, 9), (4, 10), (5, 10),
    (6, 7), (6, 11), (6, 12), (7, 8), (7, 12), (7, 13), (8, 9), (8, 13), (8, 14), (9, 10),
    (9, 13), (9, 14), (10, 14), (10, 15), (11, 12), (11, 16), (12, 13), (12, 16), (12, 17), (13, 14),
    (13, 18), (14, 15), (14, 19), (14, 20), (15, 19), (15, 20), (16, 17), (16, 21), (17, 18), (17, 21),
    (17, 22), (17, 23), (18, 19), (18, 22), (18, 23), (18, 24), (19, 20), (19, 23), (19, 24), (19, 25),
    (20, 24), (20, 25), (21, 22), (22, 23), (23, 24), (24, 25),
]
# truck route: (station, arrival, departure) in minutes
STOPS = [
    (0, 0, 0),
    (12, 4, 4),
    (17, 24, 25),
    (16, 47, 49),
    (11, 64, 66),
    (6, 83, 88),
    (2, 112, 128),
    (7, 142, 142),
    (8, 158, 158),
    (9, 175, 198),
    (14, 216, 216),
    (19, 233, 233),
    (18, 251, 266),
    (13, 289, 289),
    (0, 302, 302),
]
# per drone: sorties in order; nodes = launch station, customers..., retrieval station;
# legs = flight minutes of each arc; hover = minutes waiting at the retrieval station
SORTIES = [
    [
        dict(nodes=[12, 40, 73, 75, 17], legs=[9, 2, 3, 7], launch=4, hover=0, load=6),
        dict(nodes=[16, 28, 74, 11], legs=[3, 5, 11], launch=47, hover=0, load=5),
        dict(nodes=[11, 46, 53, 57, 6], legs=[6, 7, 4, 5], launch=66, hover=0, load=7),
        dict(nodes=[2, 66, 51, 44, 63, 7], legs=[12, 1, 5, 2, 4], launch=118, hover=0, load=4),
        dict(nodes=[9, 30, 59, 42, 14], legs=[5, 5, 7, 6], launch=193, hover=0, load=4),
        dict(nodes=[18, 69, 52, 61, 27, 68, 13], legs=[5, 6, 3, 3, 4, 4], launch=264, hover=0, load=8),
    ],
    [
        dict(nodes=[12, 34, 31, 41, 17], legs=[5, 7, 2, 4], launch=4, hover=2, load=6),
        dict(nodes=[17, 39, 65, 29, 16], legs=[10, 8, 3, 4], launch=24, hover=0, load=5),
        dict(nodes=[11, 49, 55, 70, 6], legs=[5, 3, 2, 14], launch=64, hover=0, load=3),
        dict(nodes=[2, 60, 48, 35, 2], legs=[7, 2, 3, 4], launch=112, hover=0, load=6),
        dict(nodes=[7, 33, 36, 64, 76, 8], legs=[4, 1, 4, 3, 4], launch=142, hover=0, load=7),
        dict(nodes=[18, 38, 58, 67, 56, 13], legs=[1, 4, 5, 4, 9], launch=266, hover=0, load=6),
    ],
    [
        dict(nodes=[11, 32, 45, 62, 54, 6], legs=[6, 3, 5, 4, 5], launch=64, hover=0, load=8),
        dict(nodes=[2, 37, 2], legs=[5, 5], launch=112, hover=0, load=1),
        dict(nodes=[9, 71, 50, 72, 9], legs=[4, 3, 5, 11], launch=175, hover=0, load=7),
        dict(nodes=[18, 47, 43, 18], legs=[7, 6, 2], launch=251, hover=0, load=5),
    ],
]
COST = dict(total=631, truck_travel=238, flight=327, truck_wait=64, hover=2)
Q_MAX, T_MAX, RUNTIME_S = 8, 26, 6691

# ============================================================================
# Timeline (pure Python; no manim objects)
# ============================================================================
for _drone in SORTIES:
    for _s in _drone:
        _s["closed"] = _s["nodes"][0] == _s["nodes"][-1]
        _s["cum"] = list(np.cumsum([0] + _s["legs"]))
        _s["dur"] = _s["cum"][-1]
        _s["end"] = _s["launch"] + _s["dur"]

END_TIME = STOPS[-1][2]

# when each customer is served, and by which drone
VISIT = {}
for _d, _drone in enumerate(SORTIES):
    for _s in _drone:
        for _i, _c in enumerate(_s["nodes"][1:-1], start=1):
            VISIT[_c] = (_s["launch"] + _s["cum"][_i], _d)
assert sorted(VISIT) == CUSTOMERS


def _map():
    xs = [c[0] for c in COORDS.values()]
    ys = [c[1] for c in COORDS.values()]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    k = min(MAP_HEIGHT / (max(ys) - min(ys)), MAP_WIDTH / (max(xs) - min(xs)))
    return {n: MAP_CENTER + np.array([(x - cx) * k, (y - cy) * k, 0.0]) for n, (x, y) in COORDS.items()}


POS = _map()


def lerp(a, b, f):
    return a + (b - a) * f


def truck_progress(t):
    """(position, progress along the route in segments)."""
    if t <= STOPS[0][2]:
        return POS[STOPS[0][0]], 0.0
    for k, ((s0, a0, d0), (s1, a1, d1)) in enumerate(zip(STOPS, STOPS[1:])):
        if t < a1:
            f = (t - d0) / (a1 - d0)
            return lerp(POS[s0], POS[s1], f), k + f
        if t <= d1:
            return POS[s1], k + 1.0
    return POS[STOPS[-1][0]], float(len(STOPS) - 1)


def truck_point(t):
    return truck_progress(t)[0]


def flight_point(s, t):
    """Point of sortie s at time t (launch <= t <= end) and progress in legs."""
    x = t - s["launch"]
    for i, leg in enumerate(s["legs"]):
        if x <= s["cum"][i + 1] or i == len(s["legs"]) - 1:
            f = min(max((x - s["cum"][i]) / leg, 0.0), 1.0)
            return lerp(POS[s["nodes"][i]], POS[s["nodes"][i + 1]], f), i + f


DOCK_OFFSETS = [DOCK * np.array([np.cos(a), np.sin(a), 0.0])
                for a in (np.pi / 2, np.pi / 2 + 2 * np.pi / 3, np.pi / 2 + 4 * np.pi / 3)]


def drone_state(d, t):
    """(position, status text, active sortie or None)."""
    off = DOCK_OFFSETS[d]
    for s in SORTIES[d]:
        if s["launch"] <= t < s["end"]:
            p, _ = flight_point(s, t)
            ramp = min(t - s["launch"], s["end"] - t) / 1.5     # smooth undocking / docking
            w = 1.0 - min(max(ramp, 0.0), 1.0)
            return p + w * off, f"flying, load {s['load']}/{Q_MAX}", s
        if not s["closed"] and s["end"] <= t < s["end"] + s["hover"]:
            return POS[s["nodes"][-1]] + off, "hovering", s
    return truck_point(t) + off, "on truck", None


def sortie_progress(s, t):
    """Fraction of the sortie's polyline drawn at time t (0 before launch, 1 after)."""
    if t <= s["launch"]:
        return 0.0
    if t >= s["end"]:
        return 1.0
    _, k = flight_point(s, t)
    return k / len(s["legs"])


# ============================================================================
# Scene
# ============================================================================
class SVDRPOptimal(Scene):

    def construct(self):
        self.t = ValueTracker(0.0)
        self.add(Rectangle(width=FRAME_WIDTH + 1, height=FRAME_HEIGHT + 1)
                 .set_fill(BG_COLOR, 1).set_stroke(width=0))

        network, stations, depot, customers = self.build_map()
        panel = self.build_panel()

        self.play(Write(panel["title"]), FadeIn(panel["subtitle"], shift=0.2 * DOWN), run_time=1.5)
        self.play(LaggedStartMap(ShowCreation, network, lag_ratio=0.02), run_time=2)
        self.play(FadeIn(stations, lag_ratio=0.05), FadeIn(depot), run_time=1.2)
        self.play(LaggedStartMap(GrowFromCenter, customers, lag_ratio=0.02), run_time=1.8)
        self.play(FadeIn(panel["legend"]), FadeIn(panel["live"]), run_time=1)

        movers = self.build_movers()
        self.play(FadeIn(movers, scale=0.5), run_time=0.8)
        self.wait(0.5)

        self.play(self.t.animate.set_value(END_TIME), run_time=SECONDS, rate_func=linear)
        self.wait(0.8)

        summary = self.build_summary()
        self.play(FadeOut(panel["live"]), FadeOut(panel["legend"]), run_time=0.6)
        self.play(FadeIn(summary, shift=0.2 * UP, lag_ratio=0.1), run_time=1.5)
        self.wait(5)

    # ------------------------------------------------------------------ helpers
    @staticmethod
    def text(s, size=22, color=TEXT_COLOR, weight=NORMAL):
        """LaTeX text; s is a LaTeX string. The vphantom keeps the line height constant."""
        body = r"\textbf{%s}" % s if weight == BOLD else s
        return TexText(r"\vphantom{Ag(}" + body, font_size=size).set_color(color)

    @staticmethod
    def icon(name, color, width, outline=None):
        m = SVGMobject(os.path.join(ICON_DIR, name + ".svg"))
        m.set_width(width)
        m.set_fill(color, 1)
        m.set_stroke(outline or BG_COLOR, 0.6 if outline else 0, opacity=1 if outline else 0)
        return m

    def live_text(self, func, size, color, anchor):
        """A Text that is rebuilt only when func(t) changes; left-aligned at anchor."""
        mob = self.text(func(0.0), size, color)
        mob.move_to(anchor, aligned_edge=LEFT)
        mob.last = func(0.0)

        def update(m):
            s = func(self.t.get_value())
            if s != m.last:
                m.become(self.text(s, size, color).move_to(anchor, aligned_edge=LEFT))
                m.last = s
        mob.add_updater(update)
        return mob

    # --------------------------------------------------------------------- map
    def build_map(self):
        network = VGroup(*[Line(POS[a], POS[b]).set_stroke(EDGE_COLOR, 1.5, opacity=0.8)
                           for a, b in TRUCK_EDGES])
        on_route = {s for s, _, _ in STOPS}
        stations = VGroup()
        for s in STATIONS:
            if s == DEPOT:
                continue
            sq = Square(side_length=0.14).move_to(POS[s])
            sq.set_fill(STATION_COLOR, 1 if s in on_route else 0.35).set_stroke(width=0)
            stations.add(sq)
        depot = VGroup(
            Square(side_length=0.26).move_to(POS[DEPOT]).set_fill(TEXT_COLOR, 1).set_stroke(width=0),
            self.text("Depot", 16, MUTED).next_to(POS[DEPOT], UP, buff=0.18),
        )

        customers = VGroup()
        for c in CUSTOMERS:
            served_at, d = VISIT[c]
            dot = Circle(radius=0.045 + 0.012 * DEMAND[c]).move_to(POS[c])
            dot.set_stroke(CUSTOMER_COLOR, 1.6).set_fill(DRONE_COLORS[d], 0)

            def upd(m, served_at=served_at, color=DRONE_COLORS[d]):
                if self.t.get_value() >= served_at:
                    m.set_fill(color, 1).set_stroke(color, 1.6)
                else:
                    m.set_fill(color, 0).set_stroke(CUSTOMER_COLOR, 1.6)
            dot.add_updater(upd)
            customers.add(dot)
        return network, stations, depot, customers

    # -------------------------------------------------------------- moving parts
    def build_movers(self):
        movers = VGroup()

        # trails (drawn underneath the vehicles)
        route = VMobject().set_points_as_corners([POS[s] for s, _, _ in STOPS])
        truck_trail = VMobject().set_stroke(TRUCK_COLOR, 4, opacity=0.9)
        segments = len(STOPS) - 1

        def upd_truck_trail(m):
            _, k = truck_progress(self.t.get_value())
            if k <= 0:
                m.set_stroke(opacity=0)
                return
            m.set_points(route.get_points())  # resize data so joint_angle copy matches (manimgl 1.7.2)
            m.pointwise_become_partial(route, 0, min(k / segments, 1.0))
            m.set_stroke(TRUCK_COLOR, 4, opacity=0.9)
        truck_trail.add_updater(upd_truck_trail)
        movers.add(truck_trail)

        for d, drone in enumerate(SORTIES):
            color = DRONE_COLORS[d]
            for s in drone:
                path = VMobject().set_points_as_corners([POS[n] for n in s["nodes"]])
                trail = VMobject().set_stroke(color, 2.2, opacity=0)

                def upd_trail(m, s=s, path=path, color=color):
                    t = self.t.get_value()
                    a = sortie_progress(s, t)
                    if a <= 0:
                        m.set_stroke(opacity=0)
                        return
                    m.set_points(path.get_points())  # resize data so joint_angle copy matches (manimgl 1.7.2)
                    m.pointwise_become_partial(path, 0, a)
                    m.set_stroke(color, 2.2, opacity=0.95 if t < s["end"] else 0.4)
                trail.add_updater(upd_trail)
                movers.add(trail)

        # pulses when a customer is served
        for c in CUSTOMERS:
            served_at, d = VISIT[c]
            ring = Circle(radius=0.1).move_to(POS[c]).set_stroke(DRONE_COLORS[d], 2.5, opacity=0)

            def upd_ring(m, served_at=served_at, c=c):
                x = self.t.get_value() - served_at
                if 0 <= x < 4:
                    m.set_width(0.12 + 0.35 * x / 4).move_to(POS[c])
                    m.set_stroke(opacity=1 - x / 4)
                else:
                    m.set_stroke(opacity=0)
            ring.add_updater(upd_ring)
            movers.add(ring)

        # truck and drones
        truck = self.icon("truck", TRUCK_COLOR, TRUCK_WIDTH, outline=BG_COLOR)
        truck.facing = 1                       # the icon points right; mirror it when driving left

        def upd_truck(m):
            t = self.t.get_value()
            dx = truck_point(t + 0.5)[0] - truck_point(t - 0.5)[0]
            if abs(dx) > 1e-6 and dx * m.facing < 0:
                m.flip(UP)
                m.facing *= -1
            m.move_to(truck_point(t))
        truck.add_updater(upd_truck)
        movers.add(truck)
        for d in range(len(SORTIES)):
            drone = VGroup(
                Circle(radius=0.2).set_fill(BG_COLOR, 0.75).set_stroke(DRONE_COLORS[d], 1.2, opacity=0.5),
                self.icon("quadcopter", DRONE_COLORS[d], DRONE_WIDTH),
            )
            drone.add_updater(lambda m, d=d: m.move_to(drone_state(d, self.t.get_value())[0]))
            movers.add(drone)

        movers.update()
        return movers

    # -------------------------------------------------------------------- panel
    def build_panel(self):
        title = self.text(r"Truck $+$ 3 drones", 34, TEXT_COLOR, BOLD)
        title.move_to(np.array([PANEL_X, 3.45, 0]), aligned_edge=LEFT)
        subtitle = VGroup(
            self.text(r"Optimal plan $\cdot$ 50 customers", 20, MUTED),
            self.text(r"25 stations $\cdot$ drone endurance %d min" % T_MAX, 20, MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.2)

        y = 1.55
        clock = self.live_text(lambda t: r"$t = %d$ min" % int(t), 30, TEXT_COLOR, np.array([PANEL_X, y, 0]))
        served = self.live_text(
            lambda t: r"Delivered \hspace{0.6em} $%d / %d$" % (sum(v[0] <= t for v in VISIT.values()), len(CUSTOMERS)),
            22, TEXT_COLOR, np.array([PANEL_X, y - 0.55, 0]))
        truck_line = self.live_text(
            lambda t: r"Truck \hspace{1.6em}" + ("driving" if self._truck_moving(t) else "at station"),
            20, TRUCK_COLOR, np.array([PANEL_X, y - 1.1, 0]))
        drones = VGroup(*[
            self.live_text(lambda t, d=d: r"Drone %d \hspace{1.2em} %s" % (d + 1, drone_state(d, t)[1]),
                           20, DRONE_COLORS[d], np.array([PANEL_X, y - 1.5 - 0.4 * d, 0]))
            for d in range(len(SORTIES))])
        live = VGroup(clock, served, truck_line, drones)

        legend = VGroup(
            self.legend_row(self.icon("truck", TRUCK_COLOR, 0.34), "truck route"),
            self.legend_row(self.icon("quadcopter", DRONE_COLORS[0], 0.24), "drone sortie"),
            self.legend_row(Square(side_length=0.13).set_fill(STATION_COLOR, 1).set_stroke(width=0), "station"),
            self.legend_row(Circle(radius=0.07).set_stroke(CUSTOMER_COLOR, 1.6), r"customer (size $\propto$ demand)"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        legend.move_to(np.array([PANEL_X, -3.0, 0]), aligned_edge=LEFT)
        return dict(title=title, subtitle=subtitle, live=live, legend=legend)

    def legend_row(self, icon, label):
        icon.move_to(ORIGIN)
        slot = Square(side_length=0.36).set_stroke(width=0).set_fill(opacity=0)   # fixed-width icon column
        row = VGroup(slot, self.text(label, 17, MUTED)).arrange(RIGHT, buff=0.15)
        icon.move_to(slot)
        return VGroup(icon, row)

    @staticmethod
    def _truck_moving(t):
        return any(d0 < t < a1 for (_, _, d0), (_, a1, _) in zip(STOPS, STOPS[1:]))

    def build_summary(self):
        rows = [
            ("Total cost", "%g min" % COST["total"], TEXT_COLOR),
            ("truck travel", "%g" % COST["truck_travel"], TRUCK_COLOR),
            ("drone flight", "%g" % COST["flight"], DRONE_COLORS[0]),
            ("truck waiting", "%g" % COST["truck_wait"], MUTED),
            ("drone hovering", "%g" % COST["hover"], MUTED),
        ]
        lines = VGroup()
        y = 0.9
        for i, (k, v, color) in enumerate(rows):
            size = 26 if i == 0 else 20
            weight = BOLD if i == 0 else NORMAL
            left = self.text(k, size, color, weight).move_to(np.array([PANEL_X, y, 0]), aligned_edge=LEFT)
            right = self.text(v, size, color, weight).move_to(np.array([PANEL_X + 3.6, y, 0]), aligned_edge=RIGHT)
            lines.add(VGroup(left, right))
            y -= 0.62 if i == 0 else 0.42
        note = VGroup(
            self.text("Proven optimal by", 18, MUTED),
            self.text("branch-price-and-cut", 18, MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        note.next_to(lines, DOWN, buff=0.4).align_to(lines, LEFT)
        return VGroup(lines, note)
