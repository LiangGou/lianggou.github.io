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

## Notes

- Counts start at zero from the day the Worker goes live — no backfill.
- A reader can like a post once per browser (remembered locally, not tracked).
- The Worker only accepts requests from `https://lianggou.github.io` (see `CORS`
  in `worker.js`).
- To see raw numbers anytime: D1 → `blog-stats` → Console →
  `SELECT * FROM stats ORDER BY views DESC;`
