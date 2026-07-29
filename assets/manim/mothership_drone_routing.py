"""Mothership-and-drone routing, animated with Manim Community Edition.

Renders the hero animation used on the site's landing page: a single support
vehicle (the "mothership") carries a fleet of drones, stops at a small number of
launch points, and dispatches drones to serve the surrounding customers. The
animation contrasts a truck-only tour against the coordinated schedule, then
gestures at how the coordinated schedule is actually found -- by generating
routes as columns and keeping the ones with negative reduced cost.

Render with:

    python -m manim render -qh --format=mp4 \
        assets/manim/mothership_drone_routing.py MothershipDroneRouting
"""

from manim import *

# --- palette -----------------------------------------------------------------
BG = "#0b1220"
TEAL = "#2dd4bf"
TEAL_DIM = "#134e4a"
AMBER = "#fbbf24"
ROSE = "#fb7185"
SLATE = "#94a3b8"
SLATE_DIM = "#334155"
PAPER = "#f8fafc"

DEPOT = np.array([-5.9, -2.7, 0.0])

# Mothership launch points, left to right.
LAUNCH = [
    np.array([-3.6, -1.2, 0.0]),
    np.array([-0.9, 0.6, 0.0]),
    np.array([1.9, -0.9, 0.0]),
    np.array([4.6, 0.9, 0.0]),
]

# Customers grouped by the launch point that serves them.
CLUSTERS = [
    [np.array([-4.7, 0.7, 0.0]), np.array([-2.9, 1.7, 0.0]), np.array([-4.3, -2.3, 0.0])],
    [np.array([-1.7, 2.5, 0.0]), np.array([0.4, 2.1, 0.0]), np.array([-0.5, -1.5, 0.0])],
    [np.array([1.2, 1.7, 0.0]), np.array([3.0, 1.1, 0.0]), np.array([2.4, -2.5, 0.0])],
    [np.array([3.9, 2.4, 0.0]), np.array([5.7, 2.2, 0.0]), np.array([5.3, -1.5, 0.0])],
]
CUSTOMERS = [c for cluster in CLUSTERS for c in cluster]

# A deliberately zig-zagging truck-only tour through every customer.
TRUCK_ONLY_ORDER = [0, 2, 1, 5, 3, 4, 6, 7, 9, 10, 8, 11]


def make_drone(color=AMBER, scale=1.0):
    """A tiny quadcopter glyph."""
    arm = 0.13 * scale
    arms = VGroup(
        *[
            Line(ORIGIN, d * arm, stroke_width=2.2 * scale, color=color)
            for d in (UR, UL, DR, DL)
        ]
    )
    rotors = VGroup(
        *[
            Circle(radius=0.055 * scale, stroke_width=2.0 * scale, color=color).move_to(
                d * arm
            )
            for d in (UR, UL, DR, DL)
        ]
    )
    body = (
        Square(side_length=0.10 * scale)
        .set_fill(color, opacity=1.0)
        .set_stroke(width=0)
        .rotate(PI / 4)
    )
    return VGroup(arms, rotors, body)


def make_truck(color=TEAL):
    """A small side-on support vehicle."""
    box = (
        RoundedRectangle(corner_radius=0.04, width=0.46, height=0.24)
        .set_fill(color, opacity=1.0)
        .set_stroke(width=0)
    )
    cab = (
        RoundedRectangle(corner_radius=0.03, width=0.18, height=0.16)
        .set_fill(color, opacity=1.0)
        .set_stroke(width=0)
        .next_to(box, RIGHT, buff=0.02)
        .align_to(box, DOWN)
    )
    wheels = VGroup(
        Dot(radius=0.055, color=PAPER).move_to(box.get_corner(DL) + RIGHT * 0.11),
        Dot(radius=0.055, color=PAPER).move_to(box.get_corner(DR) + RIGHT * 0.06),
    )
    return VGroup(box, cab, wheels)


def corner_path(points, color, width=3.0, opacity=1.0):
    path = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity)
    path.set_points_as_corners([np.array(p) for p in points])
    return path


def tour_length(points):
    return float(sum(np.linalg.norm(b - a) for a, b in zip(points[:-1], points[1:])))


class MothershipDroneRouting(Scene):
    def construct(self):
        self.camera.background_color = BG

        depot_marker, depot_label, customer_dots, base_map = self.build_map()

        self.act_intro(depot_marker, depot_label, customer_dots)
        truck_cost = self.act_truck_only(base_map, customer_dots)
        hybrid_cost = self.act_mothership(base_map, customer_dots)
        self.act_column_generation()
        self.act_summary(truck_cost, hybrid_cost)

    # -- setup ----------------------------------------------------------------
    def build_map(self):
        depot_marker = (
            Square(side_length=0.30)
            .set_fill(TEAL, opacity=1.0)
            .set_stroke(PAPER, width=2)
            .move_to(DEPOT)
        )
        depot_label = (
            Text("depot", color=SLATE)
            .scale(0.32)
            .next_to(depot_marker, DOWN, buff=0.14)
        )
        customer_dots = VGroup(
            *[Dot(c, radius=0.075, color=SLATE) for c in CUSTOMERS]
        )
        base_map = VGroup(depot_marker, depot_label, customer_dots)
        return depot_marker, depot_label, customer_dots, base_map

    def panel_title(self, text, sub=None):
        title = Text(text, color=PAPER, weight=BOLD).scale(0.46)
        if sub is None:
            group = VGroup(title)
        else:
            subtitle = Text(sub, color=SLATE).scale(0.30)
            group = VGroup(title, subtitle).arrange(DOWN, buff=0.10, aligned_edge=LEFT)
        group.to_corner(UL, buff=0.45)
        return group

    def cost_readout(self, label, tracker, color):
        name = Text(label, color=SLATE).scale(0.28)
        number = DecimalNumber(
            0, num_decimal_places=1, color=color, font_size=34
        ).add_updater(lambda m: m.set_value(tracker.get_value()))
        unit = Text("min", color=SLATE).scale(0.26)
        row = VGroup(number, unit).arrange(RIGHT, buff=0.16, aligned_edge=DOWN)
        group = VGroup(name, row).arrange(DOWN, buff=0.08, aligned_edge=RIGHT)
        group.to_corner(UR, buff=0.45)
        return group, number

    # -- act 1 ----------------------------------------------------------------
    def act_intro(self, depot_marker, depot_label, customer_dots):
        title = Text("Mothership & Drone Routing", color=PAPER, weight=BOLD).scale(0.62)
        subtitle = Text(
            "one support vehicle, many drones, twelve delivery points",
            color=SLATE,
        ).scale(0.33)
        heading = VGroup(title, subtitle).arrange(DOWN, buff=0.22).move_to(ORIGIN)

        self.play(FadeIn(title, shift=UP * 0.25), run_time=1.0)
        self.play(FadeIn(subtitle, shift=UP * 0.15), run_time=0.7)
        self.wait(0.9)
        self.play(FadeOut(heading, shift=UP * 0.3), run_time=0.6)

        self.play(
            FadeIn(depot_marker, scale=0.6),
            FadeIn(depot_label),
            run_time=0.6,
        )
        self.play(
            LaggedStart(
                *[GrowFromCenter(d) for d in customer_dots],
                lag_ratio=0.06,
            ),
            run_time=1.3,
        )
        self.wait(0.4)

    # -- act 2 ----------------------------------------------------------------
    def act_truck_only(self, base_map, customer_dots):
        header = self.panel_title(
            "Baseline", "truck visits every customer"
        )
        self.play(FadeIn(header, shift=RIGHT * 0.2), run_time=0.5)

        points = [DEPOT] + [CUSTOMERS[i] for i in TRUCK_ONLY_ORDER] + [DEPOT]
        cost = tour_length(points) * 3.0

        tracker = ValueTracker(0.0)
        readout, number = self.cost_readout("truck-only schedule", tracker, ROSE)
        self.play(FadeIn(readout), run_time=0.4)

        route = corner_path(points, ROSE, width=3.0)
        truck = make_truck(ROSE).move_to(DEPOT)
        self.add(truck)

        self.play(
            Create(route),
            MoveAlongPath(truck, route),
            tracker.animate.set_value(cost),
            LaggedStart(
                *[
                    Succession(
                        Wait(0.0),
                        d.animate.set_color(ROSE).scale(1.25),
                    )
                    for d in [customer_dots[i] for i in TRUCK_ONLY_ORDER]
                ],
                lag_ratio=1.0,
            ),
            run_time=6.0,
            rate_func=linear,
        )
        number.clear_updaters()
        self.wait(0.7)

        self.play(
            FadeOut(route),
            FadeOut(truck),
            FadeOut(header),
            FadeOut(readout),
            *[d.animate.set_color(SLATE).scale(1 / 1.25) for d in customer_dots],
            run_time=0.7,
        )
        return cost

    # -- act 3 ----------------------------------------------------------------
    def act_mothership(self, base_map, customer_dots):
        header = self.panel_title(
            "Coordinated schedule",
            "truck stops at launch points, drones finish the job",
        )
        self.play(FadeIn(header, shift=RIGHT * 0.2), run_time=0.5)

        launch_markers = VGroup(
            *[
                VGroup(
                    Circle(radius=0.20, color=TEAL, stroke_width=2.5).move_to(p),
                    Dot(p, radius=0.05, color=TEAL),
                )
                for p in LAUNCH
            ]
        )
        self.play(
            LaggedStart(*[GrowFromCenter(m) for m in launch_markers], lag_ratio=0.15),
            run_time=0.9,
        )

        stops = [DEPOT] + LAUNCH + [DEPOT]
        truck_leg_cost = tour_length(stops) * 3.0
        drone_cost = 0.0
        for launch_point, cluster in zip(LAUNCH, CLUSTERS):
            drone_cost += max(
                np.linalg.norm(c - launch_point) for c in cluster
            ) * 2.0 * 1.15

        total = truck_leg_cost + drone_cost
        tracker = ValueTracker(0.0)
        readout, number = self.cost_readout("mothership + drones", tracker, TEAL)
        self.play(FadeIn(readout), run_time=0.4)

        truck = make_truck(TEAL).move_to(DEPOT)
        self.add(truck)

        travelled = 0.0
        for leg_index in range(len(LAUNCH)):
            start = DEPOT if leg_index == 0 else LAUNCH[leg_index - 1]
            end = LAUNCH[leg_index]
            leg = corner_path([start, end], TEAL, width=3.0)
            leg_cost = tour_length([start, end]) * 3.0

            self.play(
                Create(leg),
                MoveAlongPath(truck, leg),
                tracker.animate.set_value(travelled + leg_cost),
                run_time=1.1,
                rate_func=smooth,
            )
            travelled += leg_cost

            sortie_cost = (
                max(np.linalg.norm(c - end) for c in CLUSTERS[leg_index]) * 2.0 * 1.15
            )
            self.fly_sorties(
                end,
                CLUSTERS[leg_index],
                customer_dots,
                leg_index,
                tracker,
                travelled,
                sortie_cost,
            )
            travelled += sortie_cost

        return_leg = corner_path(
            [LAUNCH[-1], np.array([LAUNCH[-1][0], -3.3, 0.0]), np.array([DEPOT[0], -3.3, 0.0]), DEPOT],
            TEAL,
            width=3.0,
            opacity=0.45,
        )
        self.play(
            Create(return_leg),
            MoveAlongPath(truck, return_leg),
            tracker.animate.set_value(total),
            run_time=1.6,
            rate_func=smooth,
        )
        number.clear_updaters()
        self.wait(0.8)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        return total

    def fly_sorties(
        self, launch_point, cluster, customer_dots, leg_index, tracker, base, sortie_cost
    ):
        """Launch one drone per customer in the cluster, serve, and recover."""
        drones = []
        outbound = []
        for offset, target in enumerate(cluster):
            drone = make_drone(AMBER).move_to(launch_point)
            drones.append(drone)
            arc = ArcBetweenPoints(
                launch_point, target, angle=(-0.45 if offset % 2 else 0.45)
            ).set_stroke(AMBER, width=1.8, opacity=0.55)
            outbound.append((drone, arc))

        self.add(*drones)
        self.play(
            LaggedStart(
                *[
                    AnimationGroup(
                        Create(arc),
                        MoveAlongPath(drone, arc),
                    )
                    for drone, arc in outbound
                ],
                lag_ratio=0.18,
            ),
            tracker.animate.set_value(base + sortie_cost * 0.5),
            run_time=1.5,
            rate_func=smooth,
        )

        # CLUSTERS is flattened in order, so the global index is positional.
        first = sum(len(CLUSTERS[i]) for i in range(leg_index))
        served = [customer_dots[first + offset] for offset in range(len(cluster))]
        self.play(
            LaggedStart(
                *[
                    AnimationGroup(
                        Flash(d.get_center(), color=AMBER, line_length=0.14, num_lines=10,
                              flash_radius=0.22, run_time=0.5),
                        d.animate.set_color(TEAL).scale(1.3),
                    )
                    for d in served
                ],
                lag_ratio=0.12,
            ),
            run_time=0.8,
        )

        self.play(
            LaggedStart(
                *[
                    AnimationGroup(
                        MoveAlongPath(drone, arc.reverse_direction()),
                        FadeOut(arc, run_time=0.9),
                    )
                    for drone, arc in outbound
                ],
                lag_ratio=0.18,
            ),
            tracker.animate.set_value(base + sortie_cost),
            run_time=1.3,
            rate_func=smooth,
        )
        self.play(*[FadeOut(d, scale=0.4) for d in drones], run_time=0.35)

    # -- act 4 ----------------------------------------------------------------
    def act_column_generation(self):
        header = self.panel_title(
            "How the schedule is found",
            "price out candidate routes, keep the improving ones",
        )
        self.play(FadeIn(header, shift=RIGHT * 0.2), run_time=0.5)

        master = (
            RoundedRectangle(corner_radius=0.12, width=4.2, height=1.5)
            .set_stroke(TEAL, width=2.5)
            .set_fill(TEAL_DIM, opacity=0.25)
            .shift(LEFT * 3.4 + DOWN * 0.2)
        )
        master_label = VGroup(
            Text("Restricted master problem", color=PAPER).scale(0.32),
            Text("set partitioning over routes", color=SLATE).scale(0.25),
        ).arrange(DOWN, buff=0.12).move_to(master)

        pricing = (
            RoundedRectangle(corner_radius=0.12, width=4.2, height=1.5)
            .set_stroke(AMBER, width=2.5)
            .set_fill("#3f2d0a", opacity=0.35)
            .shift(RIGHT * 3.4 + DOWN * 0.2)
        )
        pricing_label = VGroup(
            Text("Pricing subproblem", color=PAPER).scale(0.32),
            Text("ESPPRC, bidirectional labeling", color=SLATE).scale(0.25),
        ).arrange(DOWN, buff=0.12).move_to(pricing)

        self.play(
            FadeIn(master, scale=0.9),
            FadeIn(master_label),
            FadeIn(pricing, scale=0.9),
            FadeIn(pricing_label),
            run_time=0.8,
        )

        duals = CurvedArrow(
            master.get_top() + UP * 0.05,
            pricing.get_top() + UP * 0.05,
            angle=-0.7,
            color=TEAL,
            stroke_width=2.5,
            tip_length=0.18,
        )
        duals_text = Text("duals", color=TEAL).scale(0.26).next_to(duals, UP, buff=0.06)

        columns = CurvedArrow(
            pricing.get_bottom() + DOWN * 0.05,
            master.get_bottom() + DOWN * 0.05,
            angle=-0.7,
            color=AMBER,
            stroke_width=2.5,
            tip_length=0.18,
        )
        columns_text = (
            Text("columns with negative reduced cost", color=AMBER)
            .scale(0.26)
            .next_to(columns, DOWN, buff=0.06)
        )

        self.play(Create(duals), FadeIn(duals_text), run_time=0.7)
        self.play(Create(columns), FadeIn(columns_text), run_time=0.7)

        candidates = VGroup(
            *[
                VGroup(
                    Text(name, color=SLATE).scale(0.28),
                    Text(value, color=color).scale(0.28),
                ).arrange(RIGHT, buff=0.35)
                for name, value, color in (
                    ("route a", "+1.84", SLATE),
                    ("route b", "-0.37", TEAL),
                    ("route c", "+0.52", SLATE),
                )
            ]
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(UP * 2.0)

        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in candidates], lag_ratio=0.2), run_time=1.0)
        self.play(
            Indicate(candidates[1], color=TEAL, scale_factor=1.18),
            run_time=0.9,
        )
        self.wait(0.6)
        self.play(
            FadeOut(VGroup(header, master, master_label, pricing, pricing_label,
                           duals, duals_text, columns, columns_text, candidates)),
            run_time=0.7,
        )

    # -- act 5 ----------------------------------------------------------------
    def act_summary(self, truck_cost, hybrid_cost):
        saving = (truck_cost - hybrid_cost) / truck_cost

        title = Text("Coordination pays", color=PAPER, weight=BOLD).scale(0.52).shift(UP * 2.3)

        bar_width_max = 6.4
        truck_bar = (
            RoundedRectangle(corner_radius=0.06, width=bar_width_max, height=0.52)
            .set_fill(ROSE, opacity=0.85)
            .set_stroke(width=0)
        )
        hybrid_bar = (
            RoundedRectangle(
                corner_radius=0.06,
                width=bar_width_max * hybrid_cost / truck_cost,
                height=0.52,
            )
            .set_fill(TEAL, opacity=0.9)
            .set_stroke(width=0)
        )

        rows = VGroup()
        for label, bar, value, color in (
            ("truck only", truck_bar, truck_cost, ROSE),
            ("mothership + drones", hybrid_bar, hybrid_cost, TEAL),
        ):
            name = Text(label, color=SLATE).scale(0.30)
            number = Text(f"{value:.0f} min", color=color).scale(0.30)
            bar_row = VGroup(bar, number).arrange(RIGHT, buff=0.22)
            row = VGroup(name, bar_row).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
            rows.add(row)
        rows.arrange(DOWN, buff=0.60, aligned_edge=LEFT).move_to(ORIGIN)

        footer = Text(
            f"{saving * 100:.0f}% less time to serve the same demand",
            color=PAPER,
        ).scale(0.36).next_to(rows, DOWN, buff=0.75)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.6)
        self.play(
            LaggedStart(
                *[FadeIn(r, shift=RIGHT * 0.3) for r in rows],
                lag_ratio=0.3,
            ),
            run_time=1.3,
        )
        self.play(Write(footer), run_time=1.0)
        self.wait(1.8)
        self.play(FadeOut(VGroup(title, rows, footer)), run_time=0.8)
