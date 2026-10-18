---
layout: single
title: "Muse Sharpened My Decision-Making. Then It Used the Same Framework to Fix Its Own Workflow."
description: "I asked Muse a simple question — urgent versus important, which comes first? Its answer clarified my own thinking. Then I handed that same framework back to it, and it changed how the agent itself works. A small story about a two-way loop."
---

"Quick decision," my Muse messaged me, in the middle of a feature build. "Found a small bug in the module next door. Do we fix the bug first — or finish the important feature and commit them together?"

It was not a hard question. That was the problem. It was about the fifteenth not-hard question this weekend.

Right now I'm running several parallel development lines with Muse: it's building a personal AI agent of its own (a long story), training that agent on my real interaction history, keeping a dozen scheduled checks running in the background. Small bugs surface constantly — mid-feature, mid-test, mid-everything. And every time one did, the workflow was identical: work paused, a question traveled up to me, I made a judgment call, work resumed.

I had become my AI's triage desk.

The funny part: this very morning, I had asked Muse the human version of the same question. I'm in the middle of something important, I said, and something urgent but not important lands on my desk — do I drop everything and fix the urgent thing first, or keep the important thing moving and let the urgent one trail along until both finish around the same time?

Muse's answer was good — good enough that I realized the question was flowing the wrong way. It shouldn't keep traveling up to me. So I fired myself from the triage desk, and handed the framework over.

## Urgent is a feeling, not a consequence

The framework I handed over is the one I try to use on myself. It starts with an uncomfortable distinction:

**Urgent is mostly a feeling, produced by someone else's clock** — a person waiting, a message flashing, a deadline somebody else set. **Important is measured by consequences** — what it costs if this is late, or never happens at all.

The two feel identical in the moment. They are almost never the same thing. So before touching anything, you ask three questions. They take a minute:

1. **What's the real deadline?** Ask, and most "urgent" things turn out to be due by end of day, not right now.
2. **Who is it blocking?** If someone is idle waiting on you, the cost is real and it grows by the hour. If nobody is blocked, the urgency is mostly theater.
3. **How big is it actually?** If it takes five minutes, scheduling it costs more than doing it.

Then the default move is neither of the two options I started with. You don't drop the important work, and you don't drag both along in parallel — context-switching quietly taxes the important thing until it's mediocre, which is the worst outcome of the three. Instead, you **de-urgent the urgent thing**: acknowledge it in one line, give it a time, park it at the next natural breakpoint of the important work. It gets done, on schedule, without breaking the deep work into pieces.

Full interruption is reserved for three exceptions: a hard deadline with a real penalty, work that is actively blocking someone else, or a small problem that will grow teeth if it waits a few hours.

## The bug question answers itself

Here's the part I didn't expect to be so clean: the framework translates back into software development word for word. That "quick decision" message — important feature in progress, small bug next door — is the urgent-versus-important question wearing a hard hat, and the agent now answers it with the same three questions:

1. **Cost of delay.** Does the bug touch production or users? Corrupt data? Get worse with time?
2. **Is it on the feature's own path?** Same code, blocking the test suite from going green, or quietly invalidating the evidence you're collecting? You never validate new work on a broken base.
3. **Size, right now.** Fixable in minutes, with its regression test, while the context is still loaded in memory? Then switching cost is at its lowest *this minute* — "later" is the expensive option wearing a patient disguise.

If any of the three says yes: fix it now. Deferral is allowed only when all three say no — and even then, the bug gets written down with its evidence, fixed at the next natural breakpoint, and never, ever carried silently across a release it could affect. Either way, the decision and a one-line reason go into the progress report. I see it. I just don't get asked.

That last rule — *a known defect never rides along silently* — was bought with real scar tissue. Weeks ago, a small defect in our evaluation tooling was documented instead of fixed, because it wasn't on that day's critical path. It sat there politely until the next release, where it invalidated an entire evaluation run that had to be thrown away and redone. Twenty minutes of rework, purchased to save five minutes of fixing. The bug was cheap. The deferral was not.

## The human's job moved up one floor

I keep noticing the same pattern. My job used to be making decisions like this one, dozens of times a day. Increasingly, it's **writing down the rule by which decisions get made** — then auditing whether the rule is any good.

That's not less judgment; it's judgment at a higher leverage point, and it's less forgiving: a bad call costs you once, a bad rule costs you every time it fires. Taste, I've argued before, is the scarce resource of the AI era. The corollary I'd now add: the taste that matters most is the kind you can write down — clear enough for someone, or something, to apply at 2 a.m. without you.

This morning I stopped answering "should we fix this bug?" My assistant asks itself three questions instead. So far, it's batting a thousand — and I got my morning back.

Notice the shape of it, because I think that's the real story. I went to Muse for help with a decision, and its answer clarified my thinking. Then the clarification flowed back: the same framework became an operating rule in Muse's own workflow, and the workflow got better — fewer interruptions, decisions made where the work happens, reasons I can audit. It helped me think; I helped it think; the second improvement was built out of the first.

Not AI as a tool I operate, and not AI as an oracle I consult — AI as a colleague, in a loop where judgment circulates and both sides come out sharper.

P.S. The ideas and the story are mine; the craft — structure, sentences, polish — is Muse's.
