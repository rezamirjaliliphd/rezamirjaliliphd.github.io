---
layout: page
title: network resilience after snow storms
description: Measuring and forecasting how New York City's transportation network recovers from winter storms.
img: assets/img/projects/network-resilience.svg
importance: 4
category: research
related_publications: true
---

When a snow storm hits a city, the transportation network does not fail uniformly and it does
not recover uniformly. Some corridors are cleared first, some boroughs lag, and the time to
return to normal varies by an order of magnitude across the network. Quantifying that
behaviour is the first step toward deciding where mitigation investment actually pays.

### Data and method

The study used public data from the New York City Department of Sanitation and from the
city's traffic speed detectors, across eight distinct snow events. Two questions had to be
answered:

1. **When has the network recovered?** Rather than pick an arbitrary speed threshold, we
   compared the distribution of observed speeds against the pre-storm distribution using
   Bhattacharyya distance and Kolmogorov–Smirnov tests. Recovery is declared when the
   post-storm distribution is no longer statistically distinguishable from the baseline.
2. **How much data do you actually need?** Detailed speed-detector coverage is expensive and
   not every city has it. We compared resilience estimates built from full speed data against
   estimates built from graph-theoretic metrics on the network topology alone.

### Finding

The less data-intensive graph theory metrics were sufficient to estimate transportation
network performance — meaning a city without dense sensor coverage can still produce useful
recovery forecasts. That makes it practical for officials and businesses to anticipate when
operations can resume after a storm.

This work was done in the Transportation and Logistics Lab at SUNY Stony Brook and published
in *Transportation Research Record* {% cite mirjalili2023resilience %}.
