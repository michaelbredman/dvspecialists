/* ─────────────────────────────────────────────────────────────
   /api/facebook — Posts job content to a Facebook Business Page.
   Uses the Facebook Graph API to create photo posts.

   Required env vars (set in Vercel dashboard):
     GITHUB_PAT       — (existing) GitHub PAT
     ADMIN_PASSWORD   — (existing) Admin password
     FB_PAGE_ID       — Facebook Page ID
     FB_PAGE_TOKEN    — Long-lived Page Access Token
                        (needs pages_manage_posts + pages_read_engagement)
───────────────────────────────────────────────────────────── */

const FB_API = 'https://graph.facebook.com/v19.0';

module.exports = async function handler(req, res) {
  // CORS preflight
  res.setHeader('Access-Control-Allow-Origin', req.headers.origin || '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const PAGE_ID    = process.env.FB_PAGE_ID;
  const PAGE_TOKEN = process.env.FB_PAGE_TOKEN;
  const ADMIN_PASS = process.env.ADMIN_PASSWORD || 'dvs2026';

  if (!PAGE_ID || !PAGE_TOKEN) {
    return res.status(500).json({
      error: 'Facebook env vars not set. Add FB_PAGE_ID and FB_PAGE_TOKEN in Vercel.',
    });
  }

  const { password, title, city, date, description, property, images } = req.body || {};

  if (password !== ADMIN_PASS) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  try {
    // Build the post message
    const lines = [];
    if (title) lines.push(title);
    if (city) lines.push(`📍 ${city}`);
    if (description) lines.push('', description);
    if (property) lines.push('', `🏠 ${property}`);
    lines.push('', '🔗 https://www.dvspecialists.com/work');

    const message = lines.join('\n');
    const firstImage = (images || []).filter(Boolean)[0];

    let result;

    if (!firstImage) {
      // ── Text/link post (no photo) ──
      result = await fbPost(`${FB_API}/${PAGE_ID}/feed`, {
        message,
        link: 'https://www.dvspecialists.com/work',
        access_token: PAGE_TOKEN,
      });

    } else {
      // ── Single photo post (first image only) ──
      result = await fbPost(`${FB_API}/${PAGE_ID}/photos`, {
        url: firstImage,
        message,
        access_token: PAGE_TOKEN,
      });
    }

    return res.json({ ok: true, postId: result.id || result.post_id || null });

  } catch (err) {
    console.error('[facebook-post]', err.message);
    return res.status(500).json({ error: err.message });
  }
};

async function fbPost(url, params) {
  const body = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    body.append(k, v);
  }

  const r = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString(),
  });

  const data = await r.json();

  if (!r.ok || data.error) {
    const msg = data.error?.message || `Facebook API ${r.status}`;
    throw new Error(msg);
  }

  return data;
}

module.exports.config = { maxDuration: 60 };
