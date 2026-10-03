---
layout: single
title: "Is Code the Universal Representation?"
description: "A provocative post claims coding models can generate anything — images, video, 3D worlds — and asks whether code is the optimal universal representation. I checked the claims and ran the experiments. Part 1: yes, code can render an image with no diffusion model at all."
---

*Inspired by "Coding Models之后" (After Coding Models) by Hokin的学术笔记 (Hokin's Academic Notes) — [original post](http://xhslink.com/o/9IpvfyZmy1Q). An [English translation of the original post](/after-coding-models-translation/) is available (translated by GPT-6). All credit for the ideas under examination goes to the original author; any mistakes in my checking are mine.*

I came across a thought-provoking post — "After Coding Models," eleven images, dense with claims. The core observation is hard to argue with: today's strongest coding models don't just write software. They generate images, animations, 3D scenes, and interactive environments by writing executable programs. Then comes the big question: **is code the optimal universal representation?** Can you express anything — a photograph, a video, a world — as a program?

The question the post poses stuck with me: if code can express images, video, 3D scenes — is it the optimal universal representation? It's a seductive idea. But there's a gap between expressing something and understanding it: a program that renders a room doesn't necessarily grasp the room the way a model trained on a million rooms might. I wanted to see how much of the claim survives contact with evidence. This is the first of a short series working through them one at a time — mostly to organize my own thinking, and in case it's useful to others.

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

## Control vs. photorealism

The more revealing test, to me, was a head-to-head: the same scene description, given two ways. Once as a coding brief — write a program that renders this scene. Once as a plain image prompt — just generate the picture. Then two follow-up edits applied to each: turn the small sphere blue, and move the camera to the other side.

![Left: scene rendered from model-written code across three steps. Right: direct image generation and edits from the same brief.](/assets/images/coding-image-comparison.png)
*Same brief, two routes, two edits. The third row is the telling one: after the camera move, the code route keeps the chrome sphere on the left; the generated image flips the scene.*

The base images tell one story: the generated one looks more photographic — textured floor tiles, an outdoor world reflected in the chrome — while the code output looks like simple CGI. The learned image model fills in rich appearance from its training; the program only knows what it was told.

The blue-sphere edit went fine on both sides. But the camera move is where it gets interesting. Moving the camera from one side to the other should keep the chrome sphere on the left and the glass on the right — I verified this by projecting the actual 3D coordinates through the new camera. The code route does exactly that: same world, new viewpoint, occlusion updates correctly. The generated image, meanwhile, produces a plausible-looking new picture with the spheres *reversed* — glass on the left, chrome on the right. It looks convincing. It's just wrong.

That's the tradeoff in one image: **pretty is not the same as correct.** Code gives you an inspectable scene — named parameters for every object, light, and camera angle that you can check and constrain. Direct generation gives you a beautiful picture with no guarantees about the world behind it. For anything where the geometry matters — and in the physical world, it always does — that inspectability is worth more than photorealism.

## What's next

Representability is established and control is real. But the harder questions remain: whether code is the *efficient* way for a model to learn spatial understanding, and whether it generalizes without shortcuts. The original author retracted his own earlier warning on exactly this point — next, I'll work through what that retraction does and doesn't settle.

*This is part 1 of a series examining the claims in "After Coding Models." Next: representability vs. learning efficiency.*
