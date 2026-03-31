/* ─────────────────────────────────────────────────────────────
   /api/hcp-customers — Fetches customers from HouseCall Pro API.

   Credential resolution:
     1. Vercel env var: HCP_API_KEY
     2. Integration settings from Blob storage (housecallPro.apiKey)
───────────────────────────────────────────────────────────── */

const getSettings = require('./_lib/get-settings');

const HCP_API = 'https://api.housecallpro.com';

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', req.headers.origin || '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const ADMIN_PASS = process.env.ADMIN_PASSWORD || 'dvs2026';
  const { password } = req.body || {};

  if (password !== ADMIN_PASS) return res.status(401).json({ error: 'Unauthorized' });

  try {
    const settings = await getSettings();
    const API_KEY = process.env.HCP_API_KEY || settings.housecallPro?.apiKey || '';

    if (!API_KEY) {
      return res.status(500).json({
        error: 'HouseCall Pro not configured. Add your API key in Admin > Integrations.',
      });
    }

    // Fetch customers (paginated — get first 200)
    const allCustomers = [];
    let page = 1;
    const pageSize = 200;

    while (page <= 5) { // max 1000 customers
      const custRes = await fetch(`${HCP_API}/customers?page=${page}&page_size=${pageSize}`, {
        headers: {
          'Authorization': `Token ${API_KEY}`,
          'Accept': 'application/json',
        },
      });

      if (!custRes.ok) {
        if (custRes.status === 401) {
          return res.status(401).json({ error: 'HouseCall Pro API key is invalid or expired.' });
        }
        throw new Error(`HCP API returned ${custRes.status}`);
      }

      const data = await custRes.json();
      const customers = data.customers || [];

      if (!customers.length) break;

      allCustomers.push(...customers);

      // If we got fewer than page_size, we've reached the end
      if (customers.length < pageSize) break;
      page++;
    }

    const mapped = allCustomers.map(c => ({
      id: c.id,
      firstName: c.first_name,
      lastName: c.last_name,
      name: [c.first_name, c.last_name].filter(Boolean).join(' ') || 'Unnamed',
      email: c.email || '',
      phone: c.mobile_number || c.home_number || '',
      address: formatAddress(c),
      company: c.company || '',
      tags: c.tags || [],
      notifications: c.notifications_enabled,
      createdAt: c.created_at,
    }));

    return res.json({ ok: true, customers: mapped });

  } catch (err) {
    console.error('[hcp-customers]', err.message);
    return res.status(500).json({ error: err.message });
  }
};

function formatAddress(c) {
  if (!c.addresses || !c.addresses.length) return '';
  const a = c.addresses[0];
  const parts = [a.street, a.city, a.state, a.zip].filter(Boolean);
  return parts.join(', ');
}

module.exports.config = { maxDuration: 30 };
