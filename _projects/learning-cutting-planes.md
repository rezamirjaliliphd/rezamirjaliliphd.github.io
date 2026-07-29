---
layout: page
title: learning cutting planes
description: Deep Q-learning for generating Chvátal–Gomory cuts, plus a hybrid inequality family.
img: assets/img/projects/cutting-planes.svg
importance: 3
category: research
---

A Chvátal–Gomory cut is determined by a vector of multipliers applied to the constraint
rows. Choosing good multipliers is itself a hard problem — the separation problem for CG cuts
is NP-hard — so solvers fall back on heuristics that generate many weak cuts and rely on
cut management to discard them.

### Learning the multipliers

I framed multiplier selection as a reinforcement learning problem. The state is the current
LP relaxation: the fractional solution, the tableau rows most violated by it, and the slack
structure. The action selects a multiplier vector; the reward is the resulting bound
improvement per unit of separation time. Both Deep Q-learning and temporal-difference
learning were used, with TD learning proving more stable when the LP basis changes sharply
between rounds.

Predicting multipliers directly rather than searching for them reduced cut generation time by
roughly 25% at equal bound quality.

### A hybrid inequality

Separately from the learned separator, I developed a family of valid inequalities that
combines three structures already present in the mothership-and-drone formulation:

- **Cover inequalities** from the drone endurance budget,
- **Chvátal–Gomory rounding** on the assignment rows,
- **Conflict inequalities** from launch points that cannot both be used in a feasible schedule.

Combining them into a single inequality rather than adding all three separately closed about
8% more of the optimality gap, because the combined form dominates each individual cut on the
instances where they overlap.
