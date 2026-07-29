---
layout: page
title: learning to price
description: Deep reinforcement learning for prioritizing pricing subproblems inside column generation.
img: assets/img/projects/drl-pricing.svg
importance: 2
category: research
---

Column generation spends most of its time in the pricing subproblem. When there are many
subproblems to solve per iteration — one per vehicle type, per depot, or per time window —
solving all of them to optimality every round is wasteful, because only a handful will
produce a column that actually enters the basis.

### The idea

Treat subproblem selection as a sequential decision problem. At each column-generation
iteration the agent observes the current dual vector, the recent history of reduced costs,
and structural features of each subproblem, and chooses which subproblems to solve and how
much effort to spend on each. The reward is shaped by how much the master objective improves
per unit of pricing time.

A graph neural network encodes the instance so that the policy transfers across instance
sizes rather than being retrained per instance: nodes carry customer and resource features,
edges carry reduced cost as the first channel and the remaining resource consumptions as the
rest, and message passing is edge-aware.

### What it bought

Prioritizing subproblems this way accelerated convergence by 20–30% relative to solving every
subproblem to optimality each round. The gain comes almost entirely from the early
iterations, where the dual vector is still far from optimal and most subproblems are not
worth solving exactly.

### Why the code is not public

This is the core of my dissertation and the underlying manuscripts are still in preparation,
so the implementation is not released. I am glad to discuss the method, the reward shaping,
or the transfer results directly.
