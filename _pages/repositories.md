---
layout: page
permalink: /repositories/
title: code
description: Open-source work I can share publicly — applied machine learning, reinforcement learning, and this site. Research code from my dissertation is kept private.
nav: true
nav_order: 4
---

{% if site.data.repositories.github_users %}

<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% for user in site.data.repositories.github_users %}
    {% include repository/repo_user.liquid username=user %}
  {% endfor %}
</div>

{% if site.repo_trophies.enabled %}
{% for user in site.data.repositories.github_users %}
{% if site.data.repositories.github_users.size > 1 %}

  <h4>{{ user }}</h4>
  {% endif %}
  <div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% include repository/repo_trophies.liquid username=user %}
  </div>

{% endfor %}
{% endif %}
{% endif %}

{% if site.data.repositories.github_repos %}

## Public repositories

<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% for repo in site.data.repositories.github_repos %}
    {% include repository/repo.liquid repository=repo %}
  {% endfor %}
</div>
{% endif %}

---

### A note on what is not here

My dissertation work — the branch-and-price-and-cut framework, the DRL-assisted pricing
subproblem, and the learned cut-generation heuristics — is not released as open source
while the underlying papers are still in preparation. If you would like to discuss the
methods or see the implementation, please [get in touch](mailto:{{ site.data.socials.email }}).
