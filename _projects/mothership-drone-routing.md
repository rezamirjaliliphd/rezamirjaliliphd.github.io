---
layout: page
title: mothership & drone routing
description: An exact branch-and-price-and-cut algorithm for coordinating a support vehicle with a fleet of delivery drones.
img: assets/img/projects/mothership-routing.svg
importance: 1
category: research
related_publications: true
---

A single ground vehicle — the *mothership* — carries a fleet of drones into a delivery
region, stops at a small number of launch points, and dispatches drones to serve the
surrounding customers. The vehicle and the drones have to agree on where and when they
meet, and the drones are constrained by flight endurance. Deciding the launch points, the
customer-to-drone assignment, and the timing all at once is what makes the problem hard.

An earlier decomposition of this problem, applied to diagnostic testing kit delivery during
the COVID-19 response, is described in {% cite park2022scheduling %}. The exact algorithm
below is the subject of {% cite mirjalili2026mothership %}.

<div class="row justify-content-sm-center">
  <div class="col-sm-12 mt-3 mt-md-0">
    {% include video.liquid path="assets/video/mothership-drone-routing.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=true muted=true loop=true %}
  </div>
</div>
<div class="caption">
  A truck-only tour compared against a coordinated mothership-and-drone schedule over the same
  twelve delivery points, followed by the column-generation loop that finds the schedule.
</div>

### Approach

The model is a set-partitioning formulation whose columns are feasible mothership-and-drone
routes. Because there are exponentially many of them, they are generated on demand:

- **Restricted master problem.** A linear relaxation over the routes generated so far, whose
  dual values price the customers and the vehicle's capacity.
- **Pricing subproblem.** An elementary shortest path problem with resource constraints
  (ESPPRC), solved with a bidirectional label-setting algorithm. Labels are extended forward
  from the depot and backward from the sink and joined in the middle, which keeps the label
  count manageable under tight endurance budgets.
- **Cutting planes.** Cover, Chvátal–Gomory, and conflict inequalities tighten the relaxation.
  A hybrid family combining all three closed roughly 8% more of the optimality gap than any
  one of them alone.
- **Branching.** Branching is done on the arc-flow variables implied by the columns, so that
  the pricing subproblem retains its structure at every node.

### Results

The valid inequalities improved LP bounds by 5–10%. A bound-inference strategy — using the
best known primal bound to prune label extensions before they are generated — reduced the
number of pricing calls and improved convergence by 18–50% depending on instance size.

The implementation is in Python with performance-critical labeling routines in Cython,
released from the GIL so that the forward and backward label sets can be extended in
parallel.
