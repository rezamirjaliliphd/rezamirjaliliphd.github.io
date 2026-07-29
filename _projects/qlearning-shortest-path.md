---
layout: page
title: Q-learning for shortest paths
description: Reinforcement learning on a constrained grid graph, as a bridge between RL and combinatorial optimization.
img: assets/img/projects/qlearning-path.svg
importance: 9
category: applied ml
github: https://github.com/rezamirjaliliphd/Q_learning_shortest_path
---

A tabular Q-learning agent that learns shortest paths on a grid world modelled as an
undirected graph $$G(N, A)$$, where some arcs are broken and impassable.

### Setup

- A 4×4 grid where each cell is a node and each legal move is an edge
- Selected arcs marked **broken**, carrying a reward of −100
- Arcs entering the target node rewarded +100; all other transitions neutral
- The agent starts at node 0 and must reach node 15
- ε-greedy action selection, with Q-values updated by the Bellman equation

The learned policy is visualised on the grid, with the start node, the goal, traversable
cells, and the broken arcs all rendered.

### Why this one matters to me

This is a small project, but it is the honest starting point for the line of work that became
my dissertation. The shortest path problem is exactly the pricing subproblem in
column generation, and asking whether an agent can learn to navigate a constrained graph is
the same question as asking whether an agent can learn to generate good columns. The
difference is only in scale: from a 16-node grid with hard-penalised arcs to an ESPPRC over
hundreds of nodes with resource windows.

[Code on GitHub](https://github.com/rezamirjaliliphd/Q_learning_shortest_path)
