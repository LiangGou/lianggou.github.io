---
layout: single
title: "After Coding Models — English Translation"
description: "English translation of the original Chinese post by Hokin’s Academic Notes."
published: true
---

*Translated by GPT-6 from the original Chinese. This is a machine translation — the author’s claims and structure are preserved, but phrasing may be imperfect.*

*Original author: Hokin’s Academic Notes (Hokin的学术笔记) — [original post](http://xhslink.com/o/9IpvfyZmy1Q).*

---


Over the past few weeks, I have made dozens of phone calls and talked extensively with friends at frontier labs. I have reached an interim assessment of coding models, multimodality, and world models: toward a plurality of artificial minds.

First, I have to acknowledge that my judgment was wrong. Over the past three years, I have said quite vocally on many occasions that LLMs were a dead end: they could not solve multimodal intelligence, spatial intelligence, or embodied intelligence, and the VLM and VLA approaches would never work. It has now been shown that my judgment over those three years was mistaken. To put it very plainly, I think the capabilities GPT-6 and Fable 5.5 are showing have essentially solved all multimodal tasks in the VLM domain. Their 3D generation capabilities are already posing a major challenge to native 3D models such as World Labs. Instead of generating GS, NeRF, or a mesh end to end, coding models can actually build 3D scenes, and may offer better control over the details. Recently, we have also seen Fable create images and videos directly through coding, with results better than those of many native image and video models. This is a fact, and we need to acknowledge it.

Why do coding models work—not just for coding, but also for images, video, and 3D? I have always believed in scaling laws: as long as you have unlimited compute, you can do anything. So why did I previously think LLMs would not work for multimodal, spatial, and embodied intelligence? Because I thought an LLM’s language representation was one-dimensional, while images require two dimensions, video requires three, and the world requires four. Using a one-dimensional representation to express a four-dimensional world could only produce stochastic parrots and shortcuts.

Clearly, that judgment was wrong. But where did it go wrong? I think there were two points. First, I underestimated how quickly LLMs would scale. I always thought that you could use 1D to overfit 2D or 3D, but that this would be extremely inefficient. By the time an LLM successfully overfit those tasks, my 2D and 3D models would already have worked. Clearly, I misjudged the scaling part. Second, I overestimated how quickly reasoning would emerge in 2D and 3D models. In 2025, Veo and Sora had already shown some emergent capabilities, but we have not seen those capabilities amplified further. Of course, we have also not seen scaling practiced in multimodal models—whether image, video, or 3D—in the way it has been practiced in LLMs.

So just how powerful is LLM scaling? According to the information I have, GPT-6 was trained on 100,000 GPUs over two weeks, using more than a billion images, more than a million hours of video data, and more than a million hours of embodied data. A single pretraining run for a model like this costs $1.3–1.6 billion, and one training run for the next model, on 400,000 GPUs, would cost $5 billion. The cost of a single pretraining run exceeds the amount raised by AMI Labs, the largest world-model company.

Yet humanity’s resources are finite. Humanity as a whole does not currently have the confidence to give the world-model approach 400,000 GPUs and $5 billion for scaling. Even if you put $5 billion into it, it might not work. Put the same resources into a one-dimensional coding model, however, and it not only works for coding; it also works for many of the things that other technical approaches claim as their territory.

At this point, many people will wonder: will we only need GPT and Claude in the future? Will AI be reduced to OpenAI and Anthropic? A few days ago, Menlo Ventures’ Deedy Das wrote a piece saying that “neolab” is a false concept. The only window in which a neolab could become an OpenAI or Anthropic was the spring of 2024—the GPT-4 period—because only then could a venture funding round keep up with the spending required for model scaling. What remains are just two paths: verticalization and magic.

A few days ago, I had dinner with a VC friend in San Francisco and asked how things were going. He said, “What is there left to invest in? There’s nothing left. Just invest in OpenAI and Anthropic.” A friend sitting nearby asked, “But their valuations are already two trillion?” The reply was: “If you believe the future will contain only OpenAI and Anthropic, that’s where the money should go.”

Is this, then, our projection of the future? I think we need to make a fundamental judgment: is code the optimal universal representation? Essentially, you can use code to do anything. You can use code to write code, make images, make videos, create 3D, and build an interactive world model in which the world is written in code [the following comparison with diffusion is unclear in the supplied transcription; see Translator’s Note 1]. You can also use code to control robots.

This makes me marvel at how accurately Dario judged the situation. In his 2011 PhD thesis, he wrote: “intelligence will arise from the collective properties of large networks of relatively simple elements”. In 2016, he wrote in OpenAI’s Special projects: “A program that can write other programs would be, for obvious reasons, very powerful.” He got both bets right: scaling and coding.

But taking a step back, how can we make sense of this through our cognitive theories? How did coding come to work so well? How did it become the most important link on the road to AGI?

In 2024, I wrote a short essay about SayCan, discussing how Fodor’s Language of Thought could optimize long-horizon planning for embodied agents. Specifically, my argument was that all long-horizon task planning needs to be solved through LoT, rather than through internal model simulation, because LoT is obviously more efficient. After writing it, I forgot about the whole thing.

What is LoT? It is an idea from cognitive science and the philosophy of mind: thought itself is made up of structures that are language-like but are not language—in other words, formal languages. Coding is, of course, a formal language, and mathematics is also a formal language. In the philosophy of mind, this also forms a foundation of what is called Symbolism. Given how successful deep learning has been, I have always scoffed at this kind of symbolic thinking. But as some of its standard-bearers have switched sides, I have also begun to acknowledge that the reason LLM thinking is now so strong is that the models have begun using LoT and symbolic thinking.

According to Fodor, language of thought is all you need; symbolic representation is all you need for thinking. Anything visual does not count as thinking—it is merely low-level perception. In Liang Wenfeng’s words, “Multimodality is an accessory to intelligence.” Claude’s tone is essentially Fodor’s tone.

I think Anthropic already has a cohesive pathway toward solving thinking. And perhaps, to the Fodorians, it has already solved thinking. Because thinking is LoT, which is precisely the capability Fable is now demonstrating.

So what is left to do? Returning to Fodor’s own words, the mind has three distinct problems: (1) logical thought, (2) meaning, and (3) consciousness. I think the first has already been solved. The second—meaning, or how meaning is formed—is fundamentally an embodied problem. As Wittgenstein puts it, all meaning must in some form refer to things in the world in order to acquire meaning. As for the third problem, starting with Descartes, there must be an “inner theatre” for consciousness to be possible. Of course, Hinton disagrees; perhaps he has the historical stature to take on Descartes.

How does all this mystical pontificating actually guide what we do in the real world?

Anthropic has clearly already begun moving into problems (2) and (3). Its approach should be to add a great deal of multimodal and embodied data while retaining an LLM backbone. It should do this very well. So what should we do?

We need to establish how far coding intelligence can go. I think coding can, in fact, solve everything in the digital world: everything that runs on servers will become a subset of coding. Mathematics is obviously a subset of coding, and so is AI4Science. But when it comes to language-related work, Anthropic and OpenAI may not capture all of it. Harvey and Legora, for example, still have considerable room.

But that is as far as it goes.

Multimodality, on the other hand, needs to sneak in and take the home base. In the early days of computers, everyone wrote code in terminals, just as they do in Claude Code. But didn’t Microsoft ultimately rise because of the GUI? Why do we need a GUI? Because humans are visual animals. So, in the end, 100% of operating systems will become streaming audio-video models, perhaps with a Jev head to make API calls. This will rise alongside AI glasses and wipe out Apple and the iPhone, as well as OpenAI and Anthropic.

Second, the ultimate model for the physical world cannot be an LLM. In fact, the rapid improvement in GPT’s and Fable’s world-building capabilities is only good for world models, with no downside. A world model does not necessarily have to be a “large” model. There will be many small models and different kinds of models in the future. Previously, it was too hard for each small model to reach the threshold of usable intelligence: there was not enough data, and the results were poor. But Qwen3-0.6B is actually the most widely used model. In the future, there will certainly be many small models running at the edge, personalized models that are intelligent enough but not excessively intelligent, in everyone’s daily life. Suppose you have a 10T-parameter GPT, with 8T devoted to language representation and 2T to multimodal representation: perhaps it can do both fairly well. But if you have only 5B parameters, there is no reason to pack language representations into it—and you cannot fit them in anyway.

So, quite the opposite: world-model and multimodal approaches need to take an anti-LLM, anti-scaling-law path. These are currently the two biggest consensus positions in AI [see Translator’s Note 2]. Yet the future is shaped by people.

We need to demonstrate:

1. **Intelligence density.** At the same small parameter count, by continually improving our data and representations, our small models can outperform the so-called The Model in the domains people need. We do not need a Terminator in every home; we need an R2-D2.

2. **The diversity of artificial minds, just like the diversity of biological minds.** ElevenLabs initially had STT and TTS models, but now it has very good STS models that bypass text. With GPT and Fable enabling this, all kinds of strong specialist models can, in fact, emerge.

3. **Latency and local models are the most fundamental needs.** The recent Jev also shows people’s enthusiasm for small models, fast models, and models for specific purposes.

At its core, this opposes the so-called The Model, Model 101. In substance, it is anti-LLM and anti-scaling. These are all non-consensus positions, yet they are also the directions with the greatest potential.

## Translator notes

1. In the supplied transcription, the sentence about a code-written interactive world continues with “更由于diffusion出来的”. This wording does not establish a clear grammatical comparison with diffusion. It is marked in the translation rather than reconstructed as a definite claim.

2. The supplied text calls the anti-LLM and anti-scaling direction both one of AI’s biggest “consensus” positions and a “non-consensus” position. Both descriptions have been retained.

[Companion technical analysis](report.md)

