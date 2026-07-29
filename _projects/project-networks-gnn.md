---
layout: page
title: project networks with graph neural networks
description: Predicting project duration and cost from activity–resource graphs, beyond CPM and PERT.
img: assets/img/projects/project-gnn.svg
importance: 5
category: research
related_publications: true
---

CPM and PERT have been the default tools for project scheduling for six decades. Both rest on
assumptions that are convenient rather than true: that task interdependencies are static, and
that a resource performs the same way regardless of what else it is assigned to. Real projects
violate both constantly.

### Modelling projects as graphs

We represent a project as a *heterogeneous* graph with two node types — activities and
resources — and edges carrying precedence, assignment, and contention relationships. This
lets the model see that two activities compete for the same crew even when there is no
precedence arc between them, which is exactly the structure a critical-path calculation
throws away.

Two architectures were evaluated:

- **GraphSAGE**, for the static case, aggregating over sampled neighbourhoods so the model
  scales to large project networks.
- **Temporal Graph Networks**, for the case where the graph itself evolves as the project
  progresses and resources are reassigned.

### Results

Against conventional statistical baselines, the learned models reduced mean absolute error on
duration and cost prediction by **23–31%**, with R² reaching approximately **0.91** on the
more complex project networks.

Just as usefully, the learned node embeddings turned out to be interpretable: resources whose
embeddings drifted furthest from their initial position were consistently the ones acting as
bottlenecks, and activity embeddings clustered around the genuine critical dependencies rather
than the nominal critical path.

The preprint {% cite mirjalili2025resource %} is on arXiv, joint work with Behrad Braghi and
Shahram Shadrokh Sikari.
