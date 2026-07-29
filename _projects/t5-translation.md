---
layout: page
title: English-to-French translation with T5
description: Fine-tuning T5-small on OPUS Books with mixed-precision training.
img: assets/img/projects/t5-translation.svg
importance: 8
category: applied ml
github: https://github.com/rezamirjaliliphd/t5-translation-opus
---

Google's T5-small fine-tuned on the OPUS Books English–French parallel corpus, built with
HuggingFace Transformers and the Trainer API.

### Setup

- Prompt-based tokenization in T5's text-to-text format
- FP16 mixed-precision training
- Custom BLEU metric computation via the `evaluate` library

### Results

- **BLEU improved by 61%**, from 0.038 to 0.061
- **Validation loss reduced from 2.14 to 1.47** over three epochs

Those BLEU numbers are low in absolute terms, which is the honest result for T5-small fine-tuned
briefly on a literary corpus — OPUS Books is stylistically far from the model's pretraining
distribution, and three epochs is not enough to close that gap. The relative improvement is
the meaningful signal.

[Code on GitHub](https://github.com/rezamirjaliliphd/t5-translation-opus)
