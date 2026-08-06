---
layout: about
title: about
permalink: /
subtitle: Operations Research Scientist

selected_papers: true
social: true

announcements:
  enabled: true
  scrollable: false
  limit: 4

latest_posts:
  enabled: false
  scrollable: false
  limit: 3
---

<section class="profile-intro">
  <div class="profile-portrait">
    {% include figure.liquid loading="eager" path="assets/img/prof_pic.jpg" class="img-fluid" alt="Portrait of Reza Mirjalili" cache_bust=true %}
    <p>Reza Mirjalili <span>Ph.D. &middot; Industrial &amp; Systems Engineering</span></p>
  </div>
  <div class="profile-copy">
    <p class="section-label">Profile / 2026</p>
    <h2>Turning mathematical structure into practical intelligence.</h2>
    <p>
      I build algorithms that make large-scale logistics decisions tractable&mdash;and,
      increasingly, algorithms that learn how to make themselves faster.
    </p>
    <p>
      My doctoral work at the <a href="https://www.ie.uh.edu/research/centers-labs/socl">Systems
      Optimization and Computing Laboratory</a>, under <a href="https://www.ie.uh.edu/faculty/lim">Prof.
      Gino J. Lim</a>, produced exact methods for drone-assisted delivery. The goal throughout is
      provable optimality on instances that were previously out of reach.
    </p>
    <div class="text-links">
      <a href="{{ '/assets/pdf/resume.pdf' | relative_url }}">Download CV <span aria-hidden="true">&#8599;</span></a>
      <a href="{{ '/publications/' | relative_url }}">View publications <span aria-hidden="true">&#8599;</span></a>
    </div>
  </div>
</section>

<section class="work-feature">
  <div class="section-heading">
    <p>Selected system</p>
    <h2>Routing, coordinated.</h2>
    <span>Exact optimization meets intelligent search.</span>
  </div>

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
      The problem in one minute &mdash; a truck-only tour against a coordinated mothership-and-drone
      schedule, and the column-generation loop that finds it.
    </p>
  </div>
</section>

<section class="capabilities">
  <div class="section-heading">
    <p>Capabilities</p>
    <h2>What I work on</h2>
    <span>Four connected ways to solve hard problems.</span>
  </div>

  <div class="pillars">
    <div class="pillar">
      <span class="pillar-index">01</span>
      <h3>Exact methods at scale</h3>
      <p>
        Branch-and-price-and-cut for path-based routing formulations, with resource-constrained
        shortest-path pricing solved by bidirectional label setting.
      </p>
    </div>
    <div class="pillar">
      <span class="pillar-index">02</span>
      <h3>Cutting planes</h3>
      <p>
        Chv&aacute;tal&ndash;Gomory, cover, conflict, and cycle-elimination inequalities, including a
        hybrid family that closed 8% more of the optimality gap.
      </p>
    </div>
    <div class="pillar">
      <span class="pillar-index">03</span>
      <h3>Learning inside the solver</h3>
      <p>
        Deep reinforcement learning for pricing, branching, and cut selection, plus graph neural
        networks that prioritize expensive subproblems.
      </p>
    </div>
    <div class="pillar">
      <span class="pillar-index">04</span>
      <h3>Logistics applications</h3>
      <p>
        Drone-assisted and multi-echelon delivery networks, healthcare scheduling, and
        transportation network resilience under disruption.
      </p>
    </div>
  </div>

  <div class="cta-row">
    <a class="cta" href="{{ '/projects/' | relative_url }}">Browse projects <span aria-hidden="true">&#8599;</span></a>
    <a class="cta" href="{{ '/publications/' | relative_url }}">Publications <span aria-hidden="true">&#8599;</span></a>
    <a class="cta" href="{{ '/cv/' | relative_url }}">Full CV <span aria-hidden="true">&#8599;</span></a>
  </div>
</section>

<section class="toolbox">
  <p class="section-label">Toolbox</p>
  <p><strong>Optimization</strong> Gurobi, CPLEX, SCIP, Pyomo, column generation, branch-and-price</p>
  <p><strong>AI / ML</strong> PyTorch, TensorFlow, deep RL, graph neural networks, CUDA</p>
  <p><strong>Languages</strong> Python, C, C++, Rust, Cython, MATLAB</p>
  <p><strong>Parallelism</strong> OpenMP, MPI, CUDA, Cython <code>nogil</code></p>
</section>
