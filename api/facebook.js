/* ─────────────────────────────────────────────────────────────
   /api/facebook — Posts job content to a Facebook Business Page.

   Credential resolution order:
     1. Vercel env vars (FB_PAGE_ID, FB_PAGE_TOKEN)
     2. Integration settings from Blob storage
     3. If GHL is connected and Facebook is not, routes through
        GHL Social Planner instead of direct Facebook API.

   Required env vars OR integration settings:
     FB_PAGE_ID       — Facebook Page ID
     FB_PAGE_TOKEN    — Long-lived Page Access Token
───────────────────────────────────────────────────────────── */

const FB_API = 'https://graph.facebook.com/v19.0';
const GHL_API = 'https://services.leadconnectorhq.com';
const getSettings = require('./_lib/get-settings');

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', req.headers.origin || '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const ADMIN_PASS = process.env.ADMIN_PASSWORD || 'dvs2026';
  const { password, title, city, description, property, images } = req.body || {};

  if (password !== ADMIN_PASS) return res.status(401).json({ error: 'Unauthorized' });

  try {
    const settings = await getSettings();

    // Resolve Facebook credentials: env vars first, then settings
    let PAGE_ID = process.env.FB_PAGE_ID || settings.facebook?.pageId || '';
    let PAGE_TOKEN = process.env.FB_PAGE_TOKEN || settings.facebook?.pageAccessToken || '';

    // If Facebook is not configured but GHL is, route through GHL Social Planner
    if ((!PAGE_ID || !PAGE_TOKEN) && settings.goHighLevel?.connected) {
      return await postViaGHL(settings, req.body, res);
    }

    if (!PAGE_ID || !PAGE_TOKEN) {
      return res.status(500).json({
        error: 'Facebook not configured. Add credentials in Admin > Integrations, or connect GoHighLevel.',
      });
    }

    // Build the post message
    const lines = [];
    if (title) lines.push(title);
    if (city) lines.push(`📍 ${city}`);
    if (description) lines.push('', description);
    if (property) lines.push('', `🏠 ${property}`);
    lines.push('', '🔗 https://www.dvspecialists.com/work');

    const message = lines.join('\n');
    const jobImages = (images || []).filter(Boolean);
    let result;

    if (jobImages.length > 0) {
      const photoIds = [];
      for (const imgUrl of jobImages.slice(0, 4)) {
        const uploaded = await fbPost(`${FB_API}/${PAGE_ID}/photos`, {
          url: imgUrl,
          published: 'false',
          access_token: PAGE_TOKEN,
        });
        if (uploaded.id) photoIds.push(uploaded.id);
      }

      const feedParams = { message, access_token: PAGE_TOKEN };
      photoIds.forEach((id, i) => {
        feedParams[`attached_media[${i}]`] = JSON.stringify({ media_fbid: id });
      });

      result = await fbPost(`${FB_API}/${PAGE_ID}/feed`, feedParams);
    } else {
      result = await fbPost(`${FB_API}/${PAGE_ID}/feed`, {
        message,
        link: 'https://www.dvspecialists.com/work',
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
  for (const [k, v] of Object.entries(params)) body.append(k, v);

  const r = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString(),
  });
  const data = await r.json();
  if (!r.ok || data.error) throw new Error(data.error?.message || `Facebook API ${r.status}`);
  return data;
}

// Route Facebook posting through GHL Social Planner
async function postViaGHL(settings, body, res) {
  const ghl = settings.goHighLevel;
  const API_KEY = process.env.GHL_API_KEY || ghl.apiKey;
  const LOCATION = process.env.GHL_LOCATION_ID || ghl.locationId;
  const USER_ID = process.env.GHL_USER_ID || '';

  if (!API_KEY || !LOCATION) {
    return res.status(500).json({ error: 'GoHighLevel not fully configured.' });
  }

  const { title, city, description, property, images } = body;
  const lines = [];
  if (title) lines.push(title);
  if (city) lines.push(`📍 ${city}`);
  if (description) lines.push('', description);
  if (property) lines.push('', `🏠 ${property}`);
  lines.push('', '🔗 https://www.dvspecialists.com/work');

  const summary = lines.join('\n');
  const jobImages = (images || []).filter(Boolean);
  const media = jobImages.slice(0, 4).map(url => ({ url, type: 'image/jpeg' }));

  // Get Facebook account IDs from GHL Social Planner
  const accountsRes = await fetch(
    `${GHL_API}/social-media-posting/${LOCATION}/accounts?type=facebook`,
    {
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Version': '2021-07-28',
        'Accept': 'application/json',
      },
    }
  );
  const accountsData = await accountsRes.json().catch(() => ({}));
  const fbAccounts = (accountsData.accounts || accountsData.data || []).map(a => a.id || a._id).filter(Boolean);

  if (!fbAccounts.length) {
    return res.status(500).json({ error: 'No Facebook accounts connected in GoHighLevel.' });
  }

  const postBody = {
    accountIds: fbAccounts,
    type: 'post',
    userId: USER_ID || undefined,
    summary,
    media,
  };

  const response = await fetch(
    `${GHL_API}/social-media-posting/${LOCATION}/posts`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Version': '2021-07-28',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(postBody),
    }
  );

  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.message || data.error || `GHL API error ${response.status}`);

  return res.json({ ok: true, postId: data.id || null, via: 'ghl' });
}

module.exports.config = { maxDuration: 60 };
