---
layout: single
title: "Muse Amazed Me Again — With One-Shot Imitation Learning"
description: "In reinforcement learning, one-shot imitation learning — mastering a new skill from a single demonstration — was a 2017 result about a robot stacking blocks. I gave Muse one video by a master explainer and the same instruction. It cloned his craft, rendered 8,235 frames of working simulations, and packaged the skill for reuse. The theory of imitation even predicts the ceiling — and it is the demonstrator."
---

For ten years, one of reinforcement learning's cleanest dreams has been a machine that learns a new skill from a *single* demonstration. This weekend I watched my Muse do exactly that — not on a robot task, but on a master's craft: explaining hard ideas on video. One demonstration was all it got. One was enough.

- **Watch the result (4¾ minutes):** [the side-by-side comparison](https://github.com/LiangGou/simulation-explainer-video/blob/main/examples/turing-machine-np/output/comparison-v1.mp4) — Manshi's original segment on top, Muse's imitation below, aligned shot by shot, playable right on its GitHub page; the imitation on its own is [here](https://github.com/LiangGou/simulation-explainer-video/blob/main/examples/turing-machine-np/output/turing-segment-v1.mp4)
- **Steal the skill pack:** [github.com/LiangGou/simulation-explainer-video](https://github.com/LiangGou/simulation-explainer-video) — the open-source project; drop it into your own agent (Muse, Claude Code, Codex) and make the same kind of video

<video controls preload="metadata" playsinline style="width:100%;height:auto;display:block;margin:1.2em 0 0.4em;" src="/assets/videos/comparison-v1.mp4"></video>
<p style="text-align:center;font-size:0.9em;color:#666;margin-top:0;">Play it right here: Manshi's original (top) vs Muse's imitation (bottom), aligned shot by shot.</p>

## The demonstration

The demonstration was a video by **Manshi （漫士沉思录）** — Lu Rui （卢睿）, a PhD student in Tsinghua's Yao Class — called [《这可能是人类提出最深刻的数学/计算机问题》](https://www.youtube.com/watch?v=v-jgX-aQ7KM) ("Possibly the deepest question humans have ever posed in mathematics and computer science"; also on [Bilibili](https://www.bilibili.com/video/BV1Ntxr6xE7Y)). [1] In seventy minutes he explains P vs NP, and his animations are not decoration: his Turing machine actually runs — the head moves, the tape rewrites itself, a counter ticks, the state table lights up in step. The diagram *is* the argument. Seventy minutes, and I watched like a student. By his own public account he spends up to three months on an episode, script first.

I asked Muse to figure out how he does it — and, before inventing anything of its own, to *imitate*: take just the five minutes where a Turing machine defines P and NP, **[24:35–29:40](https://www.youtube.com/watch?v=v-jgX-aQ7KM&t=1455s)**, and reproduce the craft. If that worked, we would generalize — to a Transformer explainer, say — and package the process so it could be reused.


## A short detour: what imitation learning is

Imitation learning is learning from demonstration instead of from reward and trial-and-error: watch an expert, then do what the expert does. Its founding example is as basic as robotics gets — in 1989, Dean Pomerleau's ALVINN was a small neural network that learned to steer a car by watching a human drive. [2] Treat the expert's every situation-and-action as training data, and you get *behavioral cloning*.

The field's most famous result explains why naive copying falls short. Ross and Bagnell summed it up in one inequality: [3] J(π̂) ≤ J(π*) + T²ε. Ignore the Greek letters — it says two simple things. One: **mistakes snowball**. Say a task takes T steps, and the copy gets each step right almost always, missing with some tiny rate ε. One wrong step still lands it in a situation the expert never showed it — and from there, the next mistake comes easier. So the total damage grows like T², the *square* of the task's length, not in a straight line. (Their fix, called DAgger, flattens the snowball back to a straight line. [4]) Two: look at the first term, J(π*) — that is the expert's own score, sitting right inside the copy's. The copy can approach the master, but **the master is the ceiling**. Imitation, the math says, cannot outrun its demonstration.

Then, in 2017, researchers at OpenAI and Berkeley (Duan, Andrychowicz, Sutskever, Abbeel, and colleagues) pushed the idea to its limit with a paper literally titled *One-Shot Imitation Learning*: [5] a robot trained so that a *single* demonstration of a new block-stacking task — one tower, shown once — is enough for it to perform new instances of that task. They closed with a hope: to build "a general system that can turn any demonstrations into robust policies." In 2017, that system was about stacking blocks in simulation.

## One demonstration, one copy

Muse worked the way a good student would. It took the transcript, extracted frames every five seconds across the segment — 62 frames — and reconstructed the *decomposition* before writing a line of code: how the five minutes split into small beats, each with a single job and one working visualization, what carries the viewer across the joins, definitions always arriving last, audio only at the very end. That decomposition, it turns out, is his real secret; the rendering is downstream of it.

Then it built its copy — not as slides, but by writing Python programs that rendered **8,235 frames**, one at a time. The key decision: every picture is drawn from a real simulation. The Turing machine on screen is an actual state machine Muse implemented; the balance scale shows sums the program computed; when the highlight on the rule table moves, it moves because the machine's state just changed. The animation cannot lie, because it is not an illustration of the computation — it is the computation, photographed 30 times a second. Narration was synthesized on top, and every spoken number was verified by transcribing the audio back with two independent speech recognizers.

One demonstration, no second example, no retraining — and the copy landed. So we did the step the 2017 paper dreamed about: we turned the demonstration into a *policy* others can run. The result is the open-source skill pack linked above, in three layers — an engine that never changes, a small set of reusable simulation archetypes (a tape machine, weighted mixing, a branching tree, an accumulating scale), and a fresh thin episode layer per topic — under one strict rule: a shape joins the archetypes only after it has recurred in real episodes. Grown, not collected. A Transformer episode, when we make it, is mostly the weighted-mixing archetype fed by a tiny model's real attention weights — computed, not hand-placed.

My honest rating of the copy: about **80%** of the original. The missing fifth is real — his props have true 3D weight, his pacing breathes — and, as the theorem would predict, the gap grows with the horizon: five minutes is not seventy.

## The takeaway

First, name what happened. An agent performed one-shot imitation learning on a complex creative skill — from one demonstration, in the wild, with no weight updates at all. The "learning" lives entirely in the decomposition it extracted and the skill it wrote down. That a general-purpose agent now ships with this capability built in is, to me, the real amazement — the 2017 result, except the task is no longer stacking blocks; it is any craft that can be demonstrated.

Second, the theory tells you where the ceiling is, and it is J(π*): the demonstrator. Everything that makes the copy good was already in Manshi's video — which problem deserved seventy minutes, how to cut it into climbable stages, which metaphor carries which abstraction, when to withhold the definition until the demonstration has earned it. A demonstration transmits behavior: the *what* and the *how*. It never transmits the reward function — the *why*. An entire subfield, inverse reinforcement learning, exists precisely because the intention is not in the data.

That is where the human value concentrates as generation gets cheap. Muse rendered eight thousand frames for almost nothing; the map those frames follow was drawn by a person, over months, out of taste. I have written before that taste is the new intelligence. Imitation learning's own mathematics now says the same thing in symbols: J(π̂) ≤ J(π*) + T²ε. The machine drew the frames. The human drew the map — and the map is the bound.

## Credit and sources

Everything imitated here belongs to **Lu Rui （卢睿） and his channel 漫士沉思录 (Manshi)** — go watch the original, it is better than the copy: [the video on YouTube](https://www.youtube.com/watch?v=v-jgX-aQ7KM) · [on Bilibili](https://www.bilibili.com/video/BV1Ntxr6xE7Y) · [the imitated segment, 24:35–29:40](https://www.youtube.com/watch?v=v-jgX-aQ7KM&t=1455s). Thank you, Manshi — this student learned a lot.

## References

[1] Lu Rui （卢睿） / 漫士沉思录 (Manshi). (2026). 《这可能是人类提出最深刻的数学/计算机问题》 [Possibly the deepest question humans have ever posed in mathematics and computer science]. Video, 70 min, finale of the series 图灵的沉思：理论计算机. [YouTube](https://www.youtube.com/watch?v=v-jgX-aQ7KM). [Bilibili](https://www.bilibili.com/video/BV1Ntxr6xE7Y).

[2] Pomerleau, D. (1989). ALVINN: An Autonomous Land Vehicle in a Neural Network. *Advances in Neural Information Processing Systems 1*.

[3] Ross, S., & Bagnell, D. (2010). Efficient Reductions for Imitation Learning. *Proceedings of AISTATS 2010*.

[4] Ross, S., Gordon, G. J., & Bagnell, D. (2011). A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning. *Proceedings of AISTATS 2011*. arXiv:1011.0686.

[5] Duan, Y., Andrychowicz, M., Stadie, B., Ho, J., Schneider, J., Sutskever, I., Abbeel, P., & Zaremba, W. (2017). One-Shot Imitation Learning. *Advances in Neural Information Processing Systems 30*. [arXiv:1703.07326](https://arxiv.org/abs/1703.07326).

P.S. The ideas and the story are mine; the craft is Muse's.
