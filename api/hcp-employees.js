/* ─────────────────────────────────────────────────────────────
   /api/hcp-employees — Fetches employees/technicians from
   HouseCall Pro API. Returns name, role, contact info, and avatar.

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

    // Fetch employees
    const empRes = await fetch(`${HCP_API}/employees`, {
      headers: {
        'Authorization': `Token ${API_KEY}`,
        'Accept': 'application/json',
      },
    });

    if (!empRes.ok) {
      if (empRes.status === 401) {
        return res.status(401).json({ error: 'HouseCall Pro API key is invalid or expired.' });
      }
      throw new Error(`HCP API returned ${empRes.status}`);
    }

    const data = await empRes.json();
    const employees = (data.employees || []).map(emp => ({
      id: emp.id,
      firstName: emp.first_name,
      lastName: emp.last_name,
      name: `${emp.first_name} ${emp.last_name}`,
      email: emp.email,
      phone: emp.mobile_number,
      role: emp.role,
      avatar: emp.avatar_url,
      color: emp.color_hex ? `#${emp.color_hex}` : null,
      tags: emp.tags || [],
      isAdmin: emp.permissions?.is_admin || false,
      canBeBooked: emp.permissions?.can_be_booked_online || false,
      companyName: emp.company_name,
      createdAt: emp.created_at,
    }));

    return res.json({ ok: true, employees, companyName: employees[0]?.companyName || '' });

  } catch (err) {
    console.error('[hcp-employees]', err.message);
    return res.status(500).json({ error: err.message });
  }
};

module.exports.config = { maxDuration: 15 };
