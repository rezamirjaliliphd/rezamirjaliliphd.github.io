---
layout: page
title: CNN hyperparameter search on CIFAR-10
description: Optuna-driven tuning of a convolutional network, optimising for search efficiency rather than raw accuracy.
img: assets/img/projects/cnn-optuna.svg
importance: 7
category: applied ml
github: https://github.com/rezamirjaliliphd/cnn-optuna-cifar10
---

Hyperparameter optimization for a convolutional network on CIFAR-10, using PyTorch and Optuna.

The constraint that shaped this project was deliberate: the model is trained on a _reduced_
dataset — 1,000 training images and 300 validation images — precisely so that the experiment
measures how efficiently the search finds good configurations, not how well a CNN can fit all
of CIFAR-10 given unlimited compute.

### Search space

- Dropout rate
- Optimizer choice across Adam, SGD, and RMSprop
- Learning rate range search
- Trial pruning for faster convergence

### Results

- **80%+ validation accuracy** in under 10 epochs
- **Over 40% reduction in training time** through Optuna's pruning mechanism

Pruning is what does the work here. Most trials in a random or TPE search are visibly hopeless
within two epochs, and killing them early is worth far more than any refinement of the search
distribution.

[Code on GitHub](https://github.com/rezamirjaliliphd/cnn-optuna-cifar10)
