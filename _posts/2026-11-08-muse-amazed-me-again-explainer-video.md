---
layout: single
title: "Muse Amazed Me Again: I Asked It to Clone a Master's Skill for Explaining Hard Concepts on Video"
description: "A YouTuber explains P vs NP beautifully. I asked Muse to study his video frame by frame, imitate one five-minute segment, and then package the whole craft as a reusable, open-source skill. It rendered 8,235 frames of working simulations to do it. The code was the cheap part — the takeaway is where the human value sits."
---

I gave Muse a master's explainer video and one instruction — *imitate it* — and it studied the video frame by frame, rebuilt the craft, rendered 8,235 frames of working simulations, and packaged the whole process as a reusable open-source skill.

- **Watch the result (4½ minutes):** [the imitation video](https://github.com/LiangGou/simulation-explainer-video/blob/main/examples/turing-machine-np/output/turing-segment-v1.mp4) — Muse's recreation of the Turing-machine segment, playable right on its GitHub page
- **Steal the skill pack:** [github.com/LiangGou/simulation-explainer-video](https://github.com/LiangGou/simulation-explainer-video) — the open-source project; drop it into your own agent (Muse, Claude Code, Codex) and make the same kind of video

## The video I couldn't stop watching

Recently I came across a YouTuber — Manshi (漫士沉思录), a mathematician and theoretical computer scientist — who explains very hard concepts unusually well. The video that hooked me is about P vs NP, the deepest open problem in computer science: what a Turing machine is, why some problems are easy to check but hard to solve, and why that asymmetry might be a law of the universe. Seventy minutes, and I watched like a student.

I make explainer notes myself, and I kept wondering how he does it. The animations are not decoration. His Turing machine actually runs — the head moves, the tape rewrites itself, a counter ticks, and the state table lights up in step. The diagram *is* the argument. I assumed a small studio, 3D tools, months of rendering. (He later turned out to spend up to three months per episode, script first. I learned this after what follows.)

So I asked Muse a question I half expected to fail: can you figure out how he makes this — and could you make one for a new concept, say, how a Transformer works? But first, imitation. Don't invent your own style. Take just the five minutes where he uses a Turing machine to define P and NP, and reproduce the craft.

## What Muse did with the video

Muse took the assignment literally, the way a student would. It got the full transcript, extracted frames every five seconds across that segment — 62 frames — and reconstructed his decomposition: how the segment is split into small beats, what each beat's single job is, and what carries the viewer across the joins. Only then did it write anything.

His secret, once you see the frames, is not the rendering. It is the decomposition. A hard idea is broken into a sequence of small stages; each stage gets one concrete, *working* visualization in a single consistent style; the definitions always arrive last, after you have watched the thing run. The script locks every beat's topic and its transition into the next before a single frame exists. Audio goes on at the end.

Then Muse built its version. Not slides — I asked afterward, because slides are how my earlier videos were made. For its 4 minutes 34 seconds, Muse wrote Python programs and rendered **8,235 frames**, one at a time. The core decision, and I think the right one: the pictures are drawn from a real simulation. The Turing machine in the video is an actual state machine Muse implemented — states, tape, transition table — and the renderer simply draws whatever the machine is doing at that second. The balance scale that checks the partition problem shows sums the program computed, not numbers someone typed. When the machine's highlight moves, it moves because the state changed. That is why it feels like his videos: the animation cannot lie, because it is not an illustration of the computation; it is the computation, photographed 30 times a second.

Narration was synthesized and laid over the frames, and — a detail I appreciated — every number spoken in the narration was cross-checked by transcribing the finished audio with two independent speech recognizers, so a mispronounced number could not ship quietly.

The finished video and the project it became are both linked at the top of this post. The project is the real subject of what follows.

## Then I asked it to package the skill

A one-off success is a demo. I wanted the *process* to survive: next time I hand Muse a topic, it should run the same play without rediscovering it. So we sat down and designed what generalizes — and, just as important, what does not.

The design that came out has three layers. An **engine** that never changes: frame loop, stage, glow, subtitles, assembly, audio and verification plumbing. A small set of **simulation archetypes** — a tape machine, weighted mixing, a branching tree, an accumulating scale, a containment stage — parameterized patterns that recur across topics; a Transformer episode, when we make it, is mostly the weighted-mixing archetype with real attention weights computed by a tiny model, not hand-placed numbers. And an **episode layer** written fresh each time: the decomposition, the script, and the one small state machine that is this topic's truth. In the Turing build, roughly 60% of the code was layers one and two, reusable as-is; the rest was cheap, topic-specific code.

One rule governs the growth of the library: a shape graduates into the archetypes only when it has appeared in real episodes — small and strict, grown, not collected. The project is open source; if you run an agent of your own (Muse, Claude Code, Codex), you can drop it in as a skill and have your agent make the same kind of video. The worked example is the Turing episode, complete.

My honest rating of the imitation: about **80%** of the original's quality. The missing 20% is real — his props have the weight of true 3D renders, his pacing breathes in places mine hurries, and five minutes is not seventy.

## The takeaway

But notice where that missing 20% sits — and, more importantly, where the present 80% came from. Generating the code was cheap. Rendering 8,235 frames was cheap. Computation is not the scarce resource anymore; it barely figures in the cost of the artifact.

The credit for everything that makes the video good belongs to the original creator, and it is not the rendering. It is knowing which problem is worth five minutes of your life; how to cut it into stages a mind can climb; which metaphor carries which abstraction; when to withhold the definition until the demonstration has earned it. That is taste. That is judgment. Muse cloned the execution faithfully and quickly — but the decomposition it imitated so well was a human's, designed over months, and the quality of my copy is capped by the quality of his original thinking.

I wrote a while ago that taste is the new intelligence. This experiment is the sharpest evidence I have yet: as generation gets cheaper, the human contribution concentrates into exactly the part that cannot be generated — deciding what is worth making, and how it ought to be explained. The machine drew eight thousand frames. The human drew the map.

P.S. The ideas and the story are mine; the craft is Muse's.
