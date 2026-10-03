---
layout: single
title: "Encoding Isn't Understanding? Part Two"
description: "The original author once warned that squeezing a 4D world through a 1D representation could only produce stochastic parrots — then retracted it. He was right to retract, but the deeper question survives: encoding something is not the same as learning it efficiently."
---

*Part Two of a series inspired by "Coding Models之后" (After Coding Models) by Hokin的学术笔记 (Hokin's Academic Notes) — [original post](http://xhslink.com/o/9IpvfyZmy1Q). [1] [Part One](/2026/10/03/is-code-the-universal-representation.html) covered rendering and control.*

The most intellectually honest moment in the original post is a retraction. The author admits he used to argue, quite vocally, that expressing a four-dimensional world through a one-dimensional representation could only produce "stochastic parrots" and shortcuts — fluent mimics with no real understanding. He now says that judgment was wrong. I want to give him credit for that, because retracting in public is rare, and because the retraction itself opens the more interesting question: **what exactly was wrong with the original claim, and what survives of the worry behind it?**

## Why the worry felt reasonable

The intuition is easy to share. An image is two-dimensional; video adds time; the world adds depth. A language model sees all of it flattened into a one-dimensional sequence of tokens. It feels like something must be lost — like describing a sculpture over the phone and expecting the listener to sculpt it back. Surely a model built natively for 2D or 3D, with the right inductive biases, should learn spatial structure more naturally than a sequence model brute-forcing its way there.

That was the bet: 1D could overfit 2D or 3D tasks, but only inefficiently, and native models would win on learning speed. It turned out to be wrong in practice — but I think it's worth being precise about *which part* was wrong, because the useful version of the worry is still alive.

## Three questions, not one

Here's the distinction that cleared it up for me. There are three separate questions, and they need three separate kinds of evidence:

1. **Representability** — can the information be encoded at all?
2. **Learning efficiency** — how much data and training compute does it take to reach a given quality?
3. **Generalization** — does the learned capability survive new viewpoints, new layouts, new interventions, or does it lean on familiar shortcuts?

The original "stochastic parrots" claim blurred all three together. But they come apart cleanly.

On representability, the math is almost embarrassingly simple. Take an image of known width W: numbering each pixel row by row (`k = iW + j`) maps every 2D coordinate to a unique sequence position, reversibly. Nothing is lost — you can always reconstruct the image from the sequence. And a sequence index says nothing about the dimensionality of the model's internal states; a "1D" model can carry rich high-dimensional features at every position. So yes, a sequence can encode spatial information. That part of the old claim was simply mistaken, and the retraction is correct.

But — and this is the part I keep coming back to — **encodability says nothing about how efficiently a model discovers the spatial structure, or whether it generalizes.** A model can satisfy question 1 while failing questions 2 and 3 completely. Knowing that pixels *can* be numbered tells you nothing about whether training will find the geometry, how much data that takes, or whether the result transfers to a viewpoint it has never seen.

## What ViT does and doesn't prove

The best empirical datapoint here is the Vision Transformer: a transformer operating on sequences of image patches learned genuinely useful image classification. [3] That's real evidence that sequence models can do vision — I don't want to understate it.

What it doesn't establish is *equal* efficiency across architectures, or understanding of a dynamic 3D world. Maybe spatial inductive biases help on some tasks; maybe position encodings and scale compensate on others. Those are empirical comparisons, not deductions. And image classification is a long way from predicting what a scene looks like after you move the camera — which, as Part One showed, is exactly where today's models stumble.

## The worry, restated

So here's the humble version of the original warning, the one I'd defend: a successful render — like the one in Part One — proves representability, not learning efficiency and not robust generalization. Neither does the mere existence of an executable answer. The shortcuts concern isn't settled by showing that encoding works; it's settled by held-out tests: new viewpoints, compositional scene changes, action-dependent predictions, with task quality and training cost measured separately.

The author's retraction was right about the letter of his old claim. The spirit of it — *don't confuse "can be encoded" with "is efficiently learned"* — is a distinction the whole field could stand to keep.

## They don't have to compete

There's a framing I'd like to push back on gently — including my own from Part One: the idea that it's code *versus* native generators, with a winner. In practice, the interesting systems compose them, and the debate's vocabulary is blurrier than it looks.

First, the labels overlap. "Sequence model" describes how inputs are organized; "coding model" describes generating executable programs; "native generator" describes a learned model producing images or 3D content directly. A single system can be all three at once — the diffusion transformer (DiT) is a native image generator whose backbone is a transformer running over patches. [16] Sequence all the way down.

Second, when a coding model "builds a 3D scene," notice where the work actually happens. The model writes down geometry and material parameters; the *renderer* — an explicit algorithm — computes the intersections, shadows, and reflections. Much of the spatial calculation isn't learned at all; it's executed. So a compact program is no evidence that spatial understanding was learned cheaply. The cost of learning to write that code remains unknown, and the credit belongs to the whole pipeline, not to the program text alone.

And third, the combinations are where the real progress is. An LLM plans a scene layout in boxes, and a diffusion model fills it in following that layout. [17] A 2D image prior guides the optimization of a 3D scene. [18] Robot programs compose perception outputs with control APIs. [11] In each case the capability belongs to the complete system — no single component gets to claim the win.

So maybe the right question isn't which representation wins. It's which combination of representations, learned models, tools, and feedback delivers reliable performance under a task's constraints — and being honest about which component did which part of the work.

*Next in the series: what Fodor's Language of Thought actually supports — and what it doesn't.*

## References

[1] Hokin的学术笔记. (n.d.). Coding Models之后 [After Coding Models]. Eleven-image Chinese illustrated post. [Original post](http://xhslink.com/o/9IpvfyZmy1Q). [English translation](/after-coding-models-translation.html) (translated by GPT-6).

[3] Dosovitskiy, A., et al. (2021). An Image Is Worth 16×16 Words: Transformers for Image Recognition at Scale. ICLR. [arXiv:2010.11929](https://arxiv.org/abs/2010.11929).

[11] Liang, J., et al. (2023). Code as Policies: Language Model Programs for Embodied Control. ICRA. [arXiv:2209.07753](https://arxiv.org/abs/2209.07753).

[16] Peebles, W., & Xie, S. (2022). Scalable Diffusion Models with Transformers. [arXiv:2212.09748](https://arxiv.org/abs/2212.09748).

[17] Lian, L., Li, B., Yala, A., & Darrell, T. (2023). LLM-grounded Diffusion: Enhancing Prompt Understanding of Text-to-Image Models with Large Language Models. [arXiv:2305.13655](https://arxiv.org/abs/2305.13655).

[18] Poole, B., Jain, A., Barron, J. T., & Mildenhall, B. (2022). DreamFusion: Text-to-3D using 2D Diffusion. [arXiv:2209.14988](https://arxiv.org/abs/2209.14988).
