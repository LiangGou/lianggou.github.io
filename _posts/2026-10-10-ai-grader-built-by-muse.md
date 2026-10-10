---
layout: single
title: "My AI Employee Is Called Muse: Building an AI Grader with Zero Code"
description: "My wife spends 3–5 hours a week hand-grading 100+ math papers. I built her an AI grader — and wrote zero code doing it. Design, implementation, testing, deployment: all done by my AI employee. Here's the full story."
---

**Try it right now:**
- the app is live at [ai-grader-shwa.onrender.com](https://ai-grader-shwa.onrender.com)
  - public demo account — username `public`, password `public` — with its own isolated sandbox, so you can click through the whole thing without touching anyone's data
- the code is open source at [github.com/LiangGou/ai-grader](https://github.com/LiangGou/ai-grader)

## Background

My wife is a high school math teacher. Every week she gives a test, and every week she grades more than a hundred papers. The process is entirely manual: she writes the rubric, works through each paper against it, tallies the scores, then types every score into the school's system. One weekly test costs her three to five hours of grading.

The thought that kept nagging me: AI can already do every step of this. Vision models can read handwritten math. They are good at math. They can draft a rubric, verify a solution step by step, and assign partial credit consistently — arguably more consistently than a tired human at 11pm. So I decided to build her an AI grader, with my wife as customer zero.

And I gave myself one constraint, as an experiment: **I would not write any code.** No editor, no terminal commands typed by me, no "let me just fix this one line." From the first design conversation to the production deployment, everything would go through my AI assistant, Muse. I wanted to find out what that process actually feels like — where it shines, where it breaks, and what my job becomes when I'm not the one typing.

## The build

It started, as these things do, with a conversation. I described the problem and asked for a design doc. Back came a plan for a Flask web app: photograph or upload homework, generate a grading rubric two ways (reconstruct one from an already-graded example, or generate an AP-style rubric from scratch), grade each paper with a vision model against that rubric, then show class statistics and export a CSV for the school system. I read the doc, asked for changes, and approved it. That was the last "traditional" step of the whole project.

Then came the coding phase, and this is where my role changed completely. I stopped being a programmer and became something closer to a product manager with a very fast engineering team. The milestones, roughly:

**Day 1 — a working app.** From the approved design to a running app I could open on my phone the same day. Photograph a paper, get a rubric, get a grade. The core loop worked.

**The rubric engine.** This turned out to be the heart of the product. Teachers don't just want a score; they want a rubric they trust. So the app reconstructs a rubric from a teacher's graded example, or generates an AP-style one where the per-question point totals stay locked to the teacher's original total. Every question gets a "retry with AI" button when the first attempt fails, and everything auto-saves.

**The quality loop.** Here is where it got interesting. Instead of me judging output quality by vibes, I had the agent build an eval bank out of official AP Calculus AB free-response exams — real questions, real scoring guidelines. Then it iterated: fix the prompt, fix the workflow, re-run the exams, measure. Question detection went from flaky to reliable through a per-photo pipeline. The solver got a "generate then verify" discipline — ten attempts to solve, then an independent verification pass, never a shrug of "unsure." Diagrams get generated when a question needs one. Each fix came with a regression test, so nothing ever silently regressed.

**Two more agents as reviewers.** Before anything shipped, every code change was reviewed by two other models — GPT and Claude Opus — in parallel. They caught real bugs: authorization holes, race conditions, a token-budget bypass. Findings got fixed with their own regression tests, then re-reviewed until clean. AI reviewing AI, with me only reading the summary.

**Browser testing, like a human.** The agent drives a real Chromium browser: logs in, creates a class, uploads exam pages, generates a rubric, grades a paper, checks the results page, downloads the CSV. It catches what unit tests can't — the button that doesn't work on a phone screen, the flow that dead-ends. I did my own acceptance testing too, on my iPhone, sending back terse directives. My most-used instruction became "fix one by one": one bug, root cause, test, review, deploy, verify. No batching, no shortcuts.

**Deployment I never specified.** I deliberately never told it how to deploy. I just said: free tier, easy to set up. It evaluated the options and picked Render for hosting and Neon for Postgres, wired up persistence so uploads survive restarts, and put the OpenAI key behind a settings page. Then it added the public demo account — full data isolation, rate limits, a token budget, and a monitoring dashboard so I can watch what strangers do with my API key.

Five days after the first conversation, the app was in production, open-sourced under MIT, and my wife was looking at her first AI-graded class.

One number worth sharing: the whole thing took about a week, from the idea — which came up in a conversation with a couple of friends last week — to production. Every evening after work I spent roughly an hour talking to Muse: describing what I wanted, reviewing what came back, pointing at problems. That talking time added up to around five hours total. I never touched the code — not once.

## Lessons learned

**The agent is a project manager, not a code generator.** The popular image is "AI writes code fast." What actually happened: it managed the whole loop — broke work into steps, wrote the tests, ran them, got the reviews, deployed, verified in production, and reported back with a commit hash. Code was just one artifact among many.

**My job became specifying acceptance, not implementation.** The highest-leverage thing I did was define what "done" looks like: "every bug gets a regression test," "two-model review before shipping," "verify in production, then test in a browser." Once the quality gates were set, I mostly just pointed at problems and said "fix one by one."

**Evals turn arguments into measurements.** The single best decision was grounding quality in real AP exams. Without that, prompt iteration is vibes. With it, every change had a number attached.

**AI review works, but only as a gate, not a ritual.** The two-model review caught things I would never have found by reading diffs — including issues in code the agent itself had written and I had already "approved." The key was making it blocking: nothing ships until both reviewers are clean.

**The honest caveats.** It wasn't magic. Vague instructions produced vague results — "make grading better" went nowhere, while "question detection finds 4 of 6 questions on this exam page; fix it" got fixed. Long tasks needed supervision; I checked in, redirected, occasionally stopped it mid-flight. And I remained the only one who could say whether a rubric was actually good — taste, it turns out, is still the scarcest resource. The agent never got tired, but it also never knew which corners mattered until I told it.

The deeper surprise was how the work *felt*. I have spent years as the person who types. Letting go of the keyboard felt, at first, like giving up control. By the end it felt like the opposite: I operated at the level of decisions — what to build, what good looks like, what ships — and everything below that happened faster and more carefully than I would have done it myself.

My wife hasn't gotten her three to five hours back yet — customer zero is still evaluating. But for the first time, that feels like a matter of weeks, not years. And I never wrote a line of code.
