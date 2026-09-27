// Cloudflare Worker: anonymous per-post view + like counters for lianggou.github.io
// Backed by a D1 database bound as `DB`. No cookies, no IPs, no personal data —
// just one counter row per post slug.
//
// Endpoints:
//   POST /hit   { slug }  -> increments views, returns { views, likes }
//   POST /like  { slug }  -> increments likes,  returns { views, likes }
//   GET  /stats?slug=... -> returns { views, likes } without incrementing

const CORS = {
  'Access-Control-Allow-Origin': 'https://lianggou.github.io',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS },
  });
}

async function getRow(db, slug) {
  return db.prepare('SELECT views, likes FROM stats WHERE slug = ?').bind(slug).first();
}

async function bump(db, slug, col) {
  // col is one of the two hardcoded column names below — never user input.
  // Seed the new row with 1 in the bumped column so the very first
  // hit/like on a new slug counts as one, not zero.
  const viewsVal = col === 'views' ? 1 : 0;
  const likesVal = col === 'likes' ? 1 : 0;
  await db
    .prepare(
      `INSERT INTO stats (slug, views, likes) VALUES (?, ${viewsVal}, ${likesVal})
       ON CONFLICT(slug) DO UPDATE SET ${col} = ${col} + 1`
    )
    .bind(slug)
    .run();
  return getRow(db, slug);
}

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') return new Response(null, { headers: CORS });

    const url = new URL(request.url);
    let slug = url.searchParams.get('slug') || '/';
    if (request.method === 'POST') {
      try {
        const body = await request.json();
        if (body && typeof body.slug === 'string' && body.slug.startsWith('/')) {
          slug = body.slug;
        }
      } catch (e) {
        /* malformed body -> fall back to query/default slug */
      }
    }
    if (slug.length > 200) slug = slug.slice(0, 200);

    try {
      if (url.pathname === '/hit' && request.method === 'POST') {
        const row = await bump(env.DB, slug, 'views');
        return json({ views: row.views, likes: row.likes });
      }
      if (url.pathname === '/like' && request.method === 'POST') {
        const row = await bump(env.DB, slug, 'likes');
        return json({ views: row.views, likes: row.likes });
      }
      if (url.pathname === '/stats') {
        const row = (await getRow(env.DB, slug)) || { views: 0, likes: 0 };
        return json({ views: row.views, likes: row.likes });
      }
      return json({ error: 'not found' }, 404);
    } catch (err) {
      return json({ error: 'database unavailable' }, 500);
    }
  },
};
