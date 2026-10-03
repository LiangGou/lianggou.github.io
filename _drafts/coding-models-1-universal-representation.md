---
layout: single
title: "Is Code the Universal Representation?"
description: "A provocative post claims coding models can generate anything — images, video, 3D worlds — and asks whether code is the optimal universal representation. I checked the claims and ran the experiments. Part 1: yes, code can render an image with no diffusion model at all."
---

*Inspired by "Coding Models之后" (After Coding Models) by Hokin的学术笔记 (Hokin's Academic Notes) — [original post](http://xhslink.com/o/9IpvfyZmy1Q). All credit for the ideas under examination goes to the original author; any mistakes in my checking are mine.*

I came across a thought-provoking post — "After Coding Models," eleven images, dense with claims. The core observation is hard to argue with: today's strongest coding models don't just write software. They generate images, animations, 3D scenes, and interactive environments by writing executable programs. Then comes the big question: **is code the optimal universal representation?** Can you express anything — a photograph, a video, a world — as a program?

One camp says yes: code can do anything, so the future belongs to models that write code. The other camp says this confuses expressing something with understanding it — that a program rendering a scene doesn't mean the model grasps the world the way a native visual model might.

It got me curious, so I spent some time checking the claims that can be checked, and running small experiments where I could. This is the first of a short series working through them one at a time — mostly to organize my own thinking, and in case it's useful to others.

## Claim 1: code can produce an image with no diffusion model

The first claim held up better than I expected. Here's the idea, stripped down: a program describes a scene — where the objects are, what they're made of, where the light is, where the camera sits. A renderer then computes how light bounces around that scene and what the camera sees. Reflections, refraction through glass, soft shadows — all of it falls out of the math. No diffusion model, no training data, no image assets anywhere in the loop.

To make it concrete, I had a model write a small ray-tracer in Python and NumPy: three spheres on a checkerboard floor, a warm area light, a camera. Nothing else. It ran on CPU for about a minute and a half and produced this:

![Three spheres rendered by model-written Python code, no image model involved](/assets/images/coding-render-probe.png)
*Rendered entirely from code: analytic spheres, procedural checkerboard, area light, path tracing. No diffusion model, no textures, no assets.*

That's a real image, computed from a scene description. The reflections and the glass refraction aren't faked — they're the renderer solving light transport from the geometry the program specified.

## The honest caveats

I should be upfront about the limits here, because they matter. This image looks like simple CGI, not a photograph — you can see the sampling noise if you look closely. And notice where the intelligence actually lives in this pipeline: the *renderer* does the heavy lifting of turning geometry into pixels. The model's job was to write down the scene: sphere positions, materials, light, camera. Describing a scene precisely in code is genuinely useful work, but it's not the same as understanding what a room looks like from having seen a million rooms.

There's a deeper point the experiment makes visible: the renderer can't invent what the program doesn't specify. It won't recover the furniture of a real room from an incomplete description. Every detail in that image — the checkerboard, the cyan tint in the glass — came from the program or the renderer's math. A learned image model, by contrast, fills in rich appearance from its training: textures, environments, grime on the floor. It just can't tell you exactly where anything is.

So the first claim holds up, within its boundaries: **code can express a scene and render it without any learned image model.** Representability is established. But representability is the easy question. The hard ones — whether code is the *efficient* way for a model to learn spatial understanding, and whether it generalizes without shortcuts — need different evidence. To the original author's credit, he retracted his own earlier warning on exactly this point, and I'll take that up in a later installment.

## What's next

The most revealing experiment compared the two routes head-to-head: same scene brief, one rendered from model-written code, one generated directly as an image — then two edits applied to each. The image route looks more photographic. But when I asked both to move the camera, the generated image quietly *reversed* the left-right order of the objects, while the code route kept the geometry honest. Attractive synthesis versus controllable state — that's part 2.

*This is part 1 of a series examining the claims in "After Coding Models." Next: control vs. photorealism — what the camera experiment revealed.*
