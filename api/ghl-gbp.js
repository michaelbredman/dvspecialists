/* ─────────────────────────────────────────────────────────────
   /api/ghl-gbp — Posts job content to Google Business Profile
   via GoHighLevel's Social Planner API (v2).

   Credential resolution order:
     1. Vercel env vars (GHL_API_KEY, GHL_LOCATION_ID, etc.)
     2. Integration settings from Blob storage

   Required env vars OR integration settings:
     GHL_API_KEY        — Private Integration Token (pit-xxx)
     GHL_LOCATION_ID    — GHL sub-account Location ID
     GHL_GMB_ACCOUNT_ID — Connected GMB account ID
     GHL_USER_ID        — GHL user ID creating the post
───────────────────────────────────────────────────────────── */

const GHL_API = 'https://services.leadconnectorhq.com';
const getSettings = require('./_lib/get-settings');
const { generateContent, finalizeContentEvent } = require('./_lib/tradestack-generate');

const GBP_ACTION_MAP = {
  'Get a Quote': 'learn_more',
  'Call Now': 'call',
  'Learn More': 'learn_more',
  'Book Online': 'book',
};

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
    const ghl = settings.goHighLevel || {};

    // Resolve credentials: env vars first, then integration settings
    const API_KEY  = process.env.GHL_API_KEY || ghl.apiKey || '';
    const LOCATION = process.env.GHL_LOCATION_ID || ghl.locationId || '';
    const GMB_ACCT = process.env.GHL_GMB_ACCOUNT_ID || '';
    const USER_ID  = process.env.GHL_USER_ID || '';

    if (!API_KEY || !LOCATION) {
      return res.status(500).json({
        error: 'GoHighLevel not configured. Add credentials in Admin > Integrations or set env vars.',
      });
    }

    // AI-generated body + action button via tradestack-backend RAG,
    // with fallback to the legacy raw-fields build.
    const ai = await generateContent('gbp', {
      title: title || '',
      description: description || '',
      city: city || null,
      state: 'CA',
      propertyType: property || null,
      photos: (images || []).filter(Boolean).map((url) => ({ url })),
    });

    let summary;
    let actionType = 'learn_more';
    let eventId = null;
    if (ai && ai.body) {
      summary = ai.body;
      actionType = GBP_ACTION_MAP[ai.actionButton] || 'learn_more';
      eventId = ai.eventId || null;
    } else {
      const lines = [];
      if (title) lines.push(title);
      if (city) lines.push(`${city}, CA`);
      if (description) lines.push('', description);
      if (property) lines.push('', `Property type: ${property}`);
      lines.push('', 'View more of our work at dvspecialists.com/work');
      summary = lines.join('\n');
    }

    const jobImages = (images || []).filter(Boolean);
    const media = jobImages.map(url => ({ url, type: 'image/jpeg' }));

    // Determine GBP account IDs
    let accountIds = [];

    if (GMB_ACCT) {
      accountIds = [GMB_ACCT];
    } else {
      // Auto-discover GBP accounts from GHL
      const accountsRes = await fetch(
        `${GHL_API}/social-media-posting/${LOCATION}/accounts?type=google`,
        {
          headers: {
            'Authorization': `Bearer ${API_KEY}`,
            'Version': '2021-07-28',
            'Accept': 'application/json',
          },
        }
      );
      const accountsData = await accountsRes.json().catch(() => ({}));
      accountIds = (accountsData.accounts || accountsData.data || [])
        .map(a => a.id || a._id)
        .filter(Boolean);
    }

    if (!accountIds.length) {
      return res.status(500).json({
        error: 'No Google Business Profile accounts found in GoHighLevel. Connect GBP in your GHL account first.',
      });
    }

    const postBody = {
      accountIds,
      type: 'post',
      userId: USER_ID || undefined,
      summary,
      media,
      gmbPostDetails: {
        gmbEventType: 'STANDARD',
        actionType,
        url: 'https://www.dvspecialists.com/work',
      },
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

    if (!response.ok) {
      const msg = data.message || data.error || `GHL API error ${response.status}`;
      throw new Error(msg);
    }

    const postId = data.id || null;
    if (eventId) await finalizeContentEvent(eventId, summary, postId);
    return res.json({ ok: true, postId });

  } catch (err) {
    console.error('[ghl-gbp-post]', err.message);
    return res.status(500).json({ error: err.message });
  }
};

module.exports.config = { maxDuration: 60 };
