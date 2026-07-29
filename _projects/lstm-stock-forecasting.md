---
layout: page
title: stock price forecasting with LSTM
description: An LSTM trained on eight years of AAPL data, judged on direction rather than on loss.
img: assets/img/projects/lstm-forecasting.svg
importance: 6
category: applied ml
github: https://github.com/rezamirjaliliphd/lstm-stock-prediction
---

A recurrent model trained on eight years of Apple daily closing prices, with data pulled from
the Yahoo Finance API.

### What it does

- Time-series windowing of daily closing prices into supervised sequences
- Normalization and sequence transformation
- A stacked LSTM with a dense output head, built in Keras

### Results

- **RMSE below 2.5** on held-out test data
- **96% directional accuracy** — the metric that actually matters for a trading signal
- **35% lower forecast error** than a moving-average baseline

The interesting part of this project was the gap between the two evaluation criteria. A model
tuned to minimise RMSE alone will happily lag the series by one step and score well, because
tomorrow's price is very close to today's. Scoring on direction instead forces the model to
commit to a call, and it is a much harder target.

[Code on GitHub](https://github.com/rezamirjaliliphd/lstm-stock-prediction)
