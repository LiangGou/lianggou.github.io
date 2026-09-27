# Post view + like counters — setup

The blog's read counts and like buttons are powered by a tiny Cloudflare Worker
backed by a D1 database. You own it end to end: free tier, no cookies, no IPs,
no personal data — just one counter row per post URL.

## One-time setup (~10 minutes, all in the Cloudflare dashboard)

1. **Create a free Cloudflare account** at https://dash.cloudflare.com/sign-up
   (skip if you already have one).

2. **Create the D1 database**
   - Go to Workers & Pages → D1 → Create database.
   - Name it `blog-stats` (any name works).
   - Open the database → Console tab → paste the contents of `schema.sql` → Execute.
     (Or: `npx wrangler d1 execute blog-stats --file schema.sql` if you use wrangler.)

3. **Create the Worker**
   - Go to Workers & Pages → Create → Create Worker → Deploy.
   - Click "Edit code", delete the template, paste the contents of `worker.js`, Deploy.
   - Go to the Worker's Settings → Bindings → Add binding → D1 database,
     set Variable name to `DB`, select the `blog-stats` database, Deploy again.

4. **Connect it to the site**
   - Copy the Worker's public URL (looks like
     `https://blog-stats.<your-name>.workers.dev`).
   - Send that URL to Astro (or put it in `_config.yml` under
     `stats: worker_url:`), and the read/like counters go live on every post.

## Contact form backend — LLM spam gate (three-layer defense)

The `/contact/` page posts to the Worker (`POST /api/contact`) instead of
directly to Formspree. Defenses, in order:

0. **Honeypot** — a hidden `_gotcha` field; naive bots fill it, humans never
   see it. Filled → quarantined, sender sees a fake success.
1. **reCAPTCHA v2** — widget on the form; the token is forwarded to Formspree,
   which verifies it against the secret key in the form's Settings → CAPTCHA →
   Custom reCAPTCHA. (Needs your keys — see below.)
2. **LLM quality gate** — an LLM (`gpt-4o-mini`) called through a Cloudflare
   AI Gateway classifies each message as LEGIT or SPAM, and also catches
   prompt injection ("ignore previous instructions", etc.). Spam is
   quarantined in D1, never forwarded, sender sees a fake success. Honest
   limit: this is a *quality* filter, not a human-vs-agent detector —
   declared agents are explicitly welcome (see
   `/.well-known/agent-contact.json`). History: the gate originally used
   Workers AI, but Cloudflare deprecated the chosen model (May 2026) and no
   replacement model ID worked on the account — so it now goes through the
   `blog-contact-gateway` AI Gateway to OpenAI (pennies per month; needs
   your API key — see below).
3. **Agent protocol** — well-behaved agents declare `name / operator / purpose`
   (see the contact page); the LLM gate lets declared agents through.

Legit messages are forwarded to the Formspree "Contact" form (email
notification to you). If the Formspree form ID isn't set yet, or a forward
fails, legit messages are stashed in the D1 `contact_inbox` table — read them
in the D1 console, nothing is silently dropped.

### Dashboard steps to activate (all in dash.cloudflare.com)

1. **Update the Worker code** — Workers & Pages → `blog-stats` → Edit code →
   replace everything with the contents of `worker.js` → Deploy.
2. **Create the AI Gateway** — left nav → AI Gateway → Create gateway → name
   it `blog-contact-gateway` (defaults are fine). The worker calls OpenAI
   through `https://gateway.ai.cloudflare.com/v1/<account-id>/blog-contact-gateway/openai`.
3. **Add the OpenAI key** — Worker → Settings → Variables and Secrets →
   Add → **Secret** → name `OPENAI_API_KEY` → paste your OpenAI API key →
   Save. (Never in chat, never in the repo.) Until this is set, the LLM gate
   fails open — messages still flow, they just skip AI filtering.
4. **Create the tables** — D1 → `blog-stats` → Console → paste the contents of
   `schema-contact.sql` → Execute.
5. **Set the Formspree form ID** — Worker → Settings → Variables and Secrets →
   add variable `FORMSPREE_FORM_ID` = your Formspree "Contact" form ID
   (e.g. `xgavprng`). Until this is set, legit messages pile up in
   `contact_inbox` instead of emailing you.
6. **reCAPTCHA keys** — register `lianggou.github.io` at
   https://www.google.com/recaptcha/admin (v2, Checkbox) → put the SITE key in
   the site's `_includes/contact-form.html` (`data-sitekey`) → put the SECRET
   key in the Formspree form's Settings → CAPTCHA → Custom reCAPTCHA.

To review quarantined spam anytime: D1 → `blog-stats` → Console →
`SELECT * FROM contact_quarantine ORDER BY id DESC LIMIT 20;`

## Notes (counters)

- Counts start at zero from the day the Worker goes live — no backfill.
- A reader can like a post once per browser (remembered locally, not tracked).
- The Worker only accepts requests from `https://lianggou.github.io` (see `CORS`
  in `worker.js`).
- To see raw numbers anytime: D1 → `blog-stats` → Console →
  `SELECT * FROM stats ORDER BY views DESC;`
