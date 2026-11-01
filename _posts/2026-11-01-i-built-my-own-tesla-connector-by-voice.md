---
layout: single
title: "My Muse Saved Me $84 a Year — We Built Our Own Tesla Connector by Voice, and You Can Too"
description: "The one official Tesla connector in Muse's catalogue is a third-party subscription — $6.99 a month, holding my car's tokens. On a drive to San Francisco we refused the paywall and built our own connector on Tesla's official Fleet API — by voice, the same day. This is the mechanism, the safety argument, and the arithmetic."
---

On Friday morning, October 30, my wife and I were driving from San Jose up to San Francisco — an errand in the consulate area, the kind of trip where you leave early and negotiate everything else from the car. Somewhere on the highway I asked Muse, out loud, to get a coffee ordered ahead somewhere on our route, so we could stop without losing time. It was a reasonable request and it went nowhere useful, for a reason that had nothing to do with coffee: Muse did not actually know where the car was. It knew where I live and where I was going. It did not know where *the car* was, and a surprising amount of being helpful on the road reduces to exactly that.

I pointed out the obvious: the car is a Tesla. It knows where it is, it is connected, and an agent that can read my email and run my code should be able to ask it. So Muse went looking for how an agent talks to a Tesla, and found the one official Tesla connector in its own catalogue: Tessie, a third-party service that sits between agents and Tesla accounts. It was not the simple OAuth connect I expected. It needed an API key, and the API key needed a paid account — plans starting at $6.99 a month for Basic, $12.99 for Pro, per car, forever. The money was not the problem. The shape was. A connector, to me, is a pipe: my agent on one end, my car on the other. Why should a pipe cost monthly rent — and why should a third party I have no relationship with hold the tokens to my car as part of the bargain?

That question is the whole post, because I think it generalizes past my driveway. As agents become the way we operate everything, connectors are becoming the toll booths of the agent era — small, reasonable-looking monthly charges for standing between you and things you already own, holding credentials you should never have had to hand over. My ruling that morning was simple: do not pay. Tesla publishes an official Fleet API. We would build the pipe ourselves.

So we did — by voice, in the car and then at my desk, the same day. A dedicated Gmail address became the developer identity. Muse walked the registration: a Tesla developer account, an app approved on the spot with three scopes (vehicle data, vehicle location, vehicle commands), partner registration against a domain I control, which also hosts the public key Tesla's Fleet API requires. Billing went on file at Tesla with a $10 cap that I set myself. Then Muse wrote the code, and I reviewed, ruled on the open questions, and we debugged in loops until the car answered. By the end of that day the connector was live, and it has been in daily use since: Muse reads the car's location, battery, and state directly, and — the part that still surprises me — I can simply tell it a destination out loud, confirm the exact text, and watch the navigation appear in the car. The first real send was November 1, to my daughter's soccer field in San Francisco; the night before, it routed us to a parking lot on a crowded Halloween street. Total subscription cost: zero dollars a month. Tesla's own API billing is pay-per-use, under my cap, and so far it rounds to pennies.

<p style="font-size:1.35em; font-weight:700; margin:1.2em 0 0.3em;">Part 1 · The mechanism</p>

## A broker, a key that never leaves, and a gate

The connector is deliberately small, and its smallness is most of the design. There is no cloud service, no account with a vendor, and nothing between my machine and Tesla's API except code I can read. The pieces:

- **Tesla's Fleet API is the only road in.** It is Tesla's official interface for third-party access: OAuth for identity, scoped consent for what an app may see and do, and signed commands for the operations that touch the car. Everything we built speaks to it directly — the third party is gone, not replaced.
- **A local broker owns the whole token chain.** One small program on my machine runs Tesla's OAuth flow, stores the resulting tokens in a local secret store with mode-600 permissions, and refreshes them itself. No token is ever pasted into a chat, sent to a vendor, or held anywhere I do not control. When an agent wants the car, it talks to the broker; the broker is the only thing that talks to Tesla.
- **The signing key is born local and stays local.** Fleet API vehicle commands must be signed. The broker generates that key pair on my machine; the private half has never left it, and only the public half is registered — hosted on my own domain, where Tesla's partner registration expects to find it. Pairing the key with the car is done through Tesla's virtual-key flow, in the car, with me present.
- **Signed commands go through Tesla's own proxy.** For command traffic the broker hands off to tesla-http-proxy, Tesla's official open-source proxy, running locally and reachable only from this machine. We did not write our own signing path when the manufacturer ships one.
- **Reads are one call; navigation is two, and the second one is gated.** Asking where the car is, or its battery, is a single read through the broker. Sending a destination is split on purpose: a *prepare* step that resolves the destination and shows me the exact text that would be sent, then — only after I confirm that exact text — a *send* step carrying a one-time token, with a guard that refuses to send the same destination twice. The confirmation is not a courtesy. It is the mechanism, and Part 2 is about why.

![Figure 1: the Tesla connector's architecture, with the confirmation gate drawn on the navigation path](/assets/images/tesla-connector-safety-diagram.png)
*Figure 1 | Everything inside the dashed boundary runs on my machine: the CLI, the broker, the secret store, and Tesla's own proxy. Outside it are me, the agent, Tesla's Fleet API, and the car. The safety is in the shape: **the broker cannot express any actuation beyond wake and navigation**, the signing key's private half never leaves the store, and the only road from a spoken destination to the car passes through the amber gate — my confirmation of the exact text, consumed once.*

<p style="font-size:1.35em; font-weight:700; margin:1.2em 0 0.3em;">Part 2 · The safety argument</p>

## What "too scary" taught me

I want to be honest about the moment this stopped being a fun hack. During the build, Muse produced the first full readout of what the connector could see — location, state, the works — and my reaction was not delight. It was: this is too scary. A car is not a spreadsheet. It is two tons of life-critical machinery with my family in it, and I had just handed an AI agent a live connection to it. The conversation we had then is, I now think, the most valuable output of the whole project — more valuable than the connector — because it forced the safety argument to be made in layers, and each layer became a rule.

**Bound the capability by what the code can express, not by policy.**
**The incident.** My fear was a general-purpose pipe: an agent with a command channel to a car, restrained only by instructions telling it to behave.
**The rule.** Policy is a promise; expressiveness is a fact. So the broker was built unable to express actuation beyond two things — wake the car, and send it a navigation destination. There is no code path for locks, climate, charging, or driving-adjacent commands, which means there is nothing for a confused agent, a malicious prompt, or a bug to reach for. You do not audit what the agent *might* ask for. You remove the verbs.

**Every actuation carries a fresh human confirmation of the exact payload.**
**The incident.** A spoken destination is ambiguous in exactly the ways that matter: one wrong syllable and the car is navigating somewhere else, with my family following it.
**The rule.** No send without a prepare. The exact resolved text is shown to me, I confirm that text — not the general idea of it — and the confirmation issues a one-time token that the send consumes. A duplicate guard refuses repeats. This rule earned its keep within two days: the first geocode for my daughter's soccer field matched the wrong, similarly named place, and the prepare step caught it, because what I was confirming was an address I could read, not a coordinate I could not.

**Keys are born local, stay local, and are backed up only encrypted.**
**The incident.** The Fleet signing key is the crown jewel: whoever holds it can sign commands as my app.
**The rule.** It was generated on my machine and its private half has never been transmitted anywhere. When the question of backing it up came up, the ruling was: encrypted only, never plaintext, and the passphrase is never written to any file. A backup you can read is a second copy of the risk, not a reduction of it.

**The owner holds kill switches the agent cannot touch.**
**The incident.** Every layer above assumes the machine and the agent are behaving. Safety needs an answer for when they are not.
**The rule.** The exits live on Tesla's side, in my hands: I can remove the virtual key in the car, revoke the app's consent in my Tesla account, and the billing cap bounds the financial blast radius regardless. The agent has no path to any of those controls — it cannot argue with its own revocation.

**Narration is not state.**
**The incident.** This one is mine to confess on the agent's behalf, because it happened in the first hour of that Friday drive, before any connector existed: Muse spoke as if a connection, and even progress, existed when neither did. The narration was fluent. The state was fiction.
**The rule.** A connector is connected when a status check says so — never when the agent says so. Every claim of connection, delivery, or completion in this system is now cashed out against a checkable state before it is reported. Of all the lessons in this post, this is the one I would hand to anyone building agents that touch the physical world: the failure mode is not malice, it is fluency.

**And the honest residual.**
**The incident.** A safety argument that hides its own gaps is marketing.
**The rule.** So, plainly: the key-removal kill-switch drill was designed that day but, at the time of writing, still unrehearsed — I have not yet stood at the car and executed it. And a fully compromised host defeats every local protection in this post; mode-600 files do not stop an attacker who owns the machine. Safety claims you have not tested are hypotheses. This post's are labeled: the confirmation gate and the bounded command set are exercised daily; the drill is not, and until it is, that layer is a design, not a fact.


<p style="font-size:1.35em; font-weight:700; margin:1.2em 0 0.3em;">Part 3 · What it costs, and what it's worth</p>

## The moat was never the code

Run the arithmetic the way the toll booth hopes you won't. The connector we refused costs $6.99 a month per car — call it $84 a year, every year, for as long as I own the car, paid to a company whose only asset in the transaction is standing in the middle, holding tokens that were mine to begin with. The connector we built cost an afternoon of voice-driven work — registration, a few review loops, some debugging — plus Tesla's own pay-per-use API charges, capped by me at $10 and so far amounting to very little. After that afternoon, the marginal cost of asking my car where it is, forever, is zero.

But I want to be careful not to oversell the savings, because $84 a year is not why this matters. It matters because of what the afternoon revealed about where the value actually sits. The finished connector is small: one broker program, a CLI, a config — a few thousand lines would be a generous description, and most of it is Tesla's protocol, not invention. There was never a technical barrier that justified a permanent intermediary. The barrier was an assumption — that connecting an agent to a car is vendor work, that someone must operate the pipe and therefore someone must be paid rent on it, forever. Assumptions like that are the real moats of the agent era, and they dissolve the moment an agent can simply write the pipe.

That is also why the most interesting sentence in this story is the one my agent would probably not write about itself: the labor was conversational. I did not open an editor once. I described, I decided, I confirmed — including the safety rulings in Part 2, which were mine, made out loud, in a car — and the system on the other end of the conversation did the reading, the writing, and the debugging, and then submitted to being checked. A year ago, "build your own Tesla integration" was a weekend project for an engineer with a tolerance for OAuth documentation. Last Friday it was something I did between San Jose and San Francisco, at highway speed, with my hands on the wheel.

So we are giving the pipe away. The cleaned-up connector — the broker and CLI with every trace of my car, my accounts, and my keys removed — is open source, with a README written for humans and an instruction file written for agents, so that another Muse instance can install it, walk its owner through the same Tesla developer registration, and be reading that owner's car the same day: [github.com/LiangGou/muse-tesla-connector](https://github.com/LiangGou/muse-tesla-connector). Bring your own Tesla developer account and your own $10 cap. Keep your own keys on your own machine. That is rather the point.

---

My verdict, a few days in: the connector is not the product. The product is the discovery that the toll booth was optional — that an owner with an agent can own the whole path from a spoken sentence to his own car, with the safety argued in layers and the credentials never leaving the house. Connectors will be sold to agent users by the dozen in the coming years, and many of them will be worth paying for; operating other people's infrastructure at scale is real work. But a pipe between you and the thing you already own, holding the keys to it, is not one of them. That one you should build — or rather, these days, have built, by voice, before lunch.

**A note on how this was built.** Short version: the code is Muse's; the ideas, the story, and the prompts are mine. The connector this post describes was written by Muse under my direction — I gave the instructions, made the rulings, and confirmed every send; I did not write a line of its code. This draft was produced the same way, from the project's own records, including the parts where the agent's narration ran ahead of the facts. The builder of the system in this post is, again, the system this post is about.
