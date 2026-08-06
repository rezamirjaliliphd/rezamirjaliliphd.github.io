---
layout: about
title: about
permalink: /
subtitle: >
  Ph.D. in <a href='https://www.ie.uh.edu/'>Industrial &amp; Systems Engineering</a>,
  <a href='https://uh.edu/'>University of Houston</a>.
  <p>Operations Research Scientist — designing elegant solutions to messy problems.</p>

profile:
  align: right
  image: prof_pic.jpg
  image_circular: false # crops the image to make it circular
  more_info: >
    <p>Houston, Texas</p>
    <p>Open to research and industry roles</p>
    <p><a href="/assets/pdf/resume.pdf">Download CV (PDF)</a></p>

selected_papers: true # includes a list of papers marked as "selected={true}"
social: true # includes social icons at the bottom of the page

announcements:
  enabled: true # includes a list of news items
  scrollable: false # adds a vertical scroll bar if there are more than 3 news items
  limit: 4 # leave blank to include all the news in the `_news` folder

latest_posts:
  enabled: false
  scrollable: false # adds a vertical scroll bar if there are more than 3 new posts items
  limit: 3 # leave blank to include all the blog posts
---

I build algorithms that make large-scale logistics decisions tractable — and, increasingly,
algorithms that learn how to make themselves faster.

My doctoral work at the <a href='https://www.ie.uh.edu/research/centers-labs/socl'>Systems
Optimization and Computing Laboratory</a>, under <a href='https://www.ie.uh.edu/faculty/lim'>Prof.
Gino J. Lim</a>, produced exact methods for drone-assisted delivery: branch-and-price-and-cut
frameworks whose pricing subproblems are solved by bidirectional labeling, and whose search is
guided by reinforcement learning rather than by hand-tuned rules. The aim throughout is
provable optimality on instances that were previously out of reach.

<div class="hero-figure">
  <video
    class="hero-video"
    src="{{ '/assets/video/mothership-drone-routing.mp4' | relative_url }}"
    autoplay
    loop
    muted
    playsinline
    controls
    preload="metadata"
    title="Mothership and drone routing optimization, animated with Manim"
  ></video>
  <p class="hero-caption">
    The problem in one minute — a truck-only tour against a coordinated mothership-and-drone
    schedule, and the column-generation loop that finds it.
  </p>
</div>

---

## what I work on

<div class="pillars">
  <div class="pillar">
    <span class="pillar-icon"><i class="fa-solid fa-code-branch"></i></span>
    <h3>Exact methods at scale</h3>
    <p>
      Branch-and-price-and-cut for path-based routing formulations. Column generation where
      the pricing subproblem is an elementary shortest path problem with resource constraints,
      solved by bidirectional label setting.
    </p>
  </div>
  <div class="pillar">
    <span class="pillar-icon"><i class="fa-solid fa-scissors"></i></span>
    <h3>Cutting planes</h3>
    <p>
      Chvátal–Gomory, cover, conflict, and cycle-elimination inequalities — including a hybrid
      family that closed 8% more of the optimality gap than any of its components alone.
    </p>
  </div>
  <div class="pillar">
    <span class="pillar-icon"><i class="fa-solid fa-brain"></i></span>
    <h3>Learning inside the solver</h3>
    <p>
      Deep reinforcement learning for pricing, branching, and cut selection. Graph neural
      networks that prioritize subproblems, cutting column-generation convergence time by
      20–30%.
    </p>
  </div>
  <div class="pillar">
    <span class="pillar-icon"><i class="fa-solid fa-truck-fast"></i></span>
    <h3>Logistics applications</h3>
    <p>
      Drone-assisted and multi-echelon delivery networks, healthcare scheduling, and
      transportation network resilience under disruption.
    </p>
  </div>
</div>

<div class="cta-row">
  <a class="cta" href="{{ '/projects/' | relative_url }}">Browse projects</a>
  <a class="cta cta-quiet" href="{{ '/publications/' | relative_url }}">Publications</a>
  <a class="cta cta-quiet" href="{{ '/cv/' | relative_url }}">Full CV</a>
</div>

---

### toolbox

**Optimization** — Gurobi, CPLEX, SCIP, Pyomo, column generation, branch-and-price
&nbsp;·&nbsp; **AI/ML** — PyTorch, TensorFlow, deep RL, graph neural networks, CUDA
&nbsp;·&nbsp; **Languages** — Python, C, C++, Rust, Cython, MATLAB
&nbsp;·&nbsp; **Parallelism** — OpenMP, MPI, CUDA, Cython `nogil`
