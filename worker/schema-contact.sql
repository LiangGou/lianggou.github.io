-- Contact form backend tables for the Cloudflare Worker (blog-stats D1).
-- Run once in the D1 console (Workers & Pages -> D1 -> blog-stats -> Console).

-- Spam / filtered submissions. Never forwarded; sender sees a fake success.
CREATE TABLE IF NOT EXISTS contact_quarantine (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT NOT NULL DEFAULT '',
  message TEXT NOT NULL,
  reason TEXT NOT NULL DEFAULT '',
  agent_declared INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Legit messages that could NOT be forwarded to Formspree (form ID not set
-- yet, or the forward failed). Read these in the D1 console until forwarding
-- is wired up; nothing is ever silently dropped.
CREATE TABLE IF NOT EXISTS contact_inbox (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT NOT NULL DEFAULT '',
  message TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT '',
  agent_declared INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
