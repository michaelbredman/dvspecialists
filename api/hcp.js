/* ─────────────────────────────────────────────────────────────
   /api/hcp — Unified HouseCall Pro API endpoint.
   Actions: employees, customers

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
  const { password, action } = req.body || {};
  if (password !== ADMIN_PASS) return res.status(401).json({ error: 'Unauthorized' });

  try {
    const settings = await getSettings();
    const API_KEY = process.env.HCP_API_KEY || settings.housecallPro?.apiKey || '';
    if (!API_KEY) return res.status(500).json({ error: 'HouseCall Pro not configured. Add your API key in Admin > Integrations.' });

    if (action === 'employees') return await getEmployees(API_KEY, res);
    if (action === 'customers') return await getCustomers(API_KEY, res);
    return res.status(400).json({ error: 'Invalid action. Use: employees, customers' });
  } catch (err) {
    console.error('[hcp]', err.message);
    return res.status(500).json({ error: err.message });
  }
};

async function getEmployees(apiKey, res) {
  const r = await fetch(`${HCP_API}/employees`, {
    headers: { 'Authorization': `Token ${apiKey}`, 'Accept': 'application/json' },
  });
  if (!r.ok) return res.status(r.status).json({ error: r.status === 401 ? 'Invalid API key' : `HCP API ${r.status}` });

  const data = await r.json();
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
}

async function getCustomers(apiKey, res) {
  const all = [];
  let page = 1;
  const pageSize = 200;

  while (page <= 5) {
    const r = await fetch(`${HCP_API}/customers?page=${page}&page_size=${pageSize}`, {
      headers: { 'Authorization': `Token ${apiKey}`, 'Accept': 'application/json' },
    });
    if (!r.ok) return res.status(r.status).json({ error: r.status === 401 ? 'Invalid API key' : `HCP API ${r.status}` });

    const data = await r.json();
    const customers = data.customers || [];
    if (!customers.length) break;
    all.push(...customers);
    if (customers.length < pageSize) break;
    page++;
  }

  const mapped = all.map(c => ({
    id: c.id,
    firstName: c.first_name,
    lastName: c.last_name,
    name: [c.first_name, c.last_name].filter(Boolean).join(' ') || 'Unnamed',
    email: c.email || '',
    phone: c.mobile_number || c.home_number || '',
    address: formatAddress(c),
    company: c.company || '',
    tags: c.tags || [],
    createdAt: c.created_at,
  }));
  return res.json({ ok: true, customers: mapped });
}

function formatAddress(c) {
  if (!c.addresses || !c.addresses.length) return '';
  const a = c.addresses[0];
  return [a.street, a.city, a.state, a.zip].filter(Boolean).join(', ');
}

module.exports.config = { maxDuration: 30 };
