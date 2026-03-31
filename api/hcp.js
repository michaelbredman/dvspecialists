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
    if (action === 'customer-jobs') return await getCustomerJobs(API_KEY, req.body.customerId, res);
    if (action === 'job-detail') return await getJobDetail(API_KEY, req.body.jobId, res);
    if (action === 'upload-attachment') return await uploadAttachment(API_KEY, req.body.jobId, req.body.filename, req.body.base64, res);
    return res.status(400).json({ error: 'Invalid action. Use: employees, customers, customer-jobs, job-detail, upload-attachment' });
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

async function getCustomerJobs(apiKey, customerId, res) {
  if (!customerId) return res.status(400).json({ error: 'customerId required' });

  const r = await fetch(`${HCP_API}/jobs?customer_id=${customerId}&page_size=50`, {
    headers: { 'Authorization': `Token ${apiKey}`, 'Accept': 'application/json' },
  });
  if (!r.ok) return res.status(r.status).json({ error: `HCP API ${r.status}` });

  const data = await r.json();
  const jobs = (data.jobs || []).map(j => ({
    id: j.id,
    invoiceNumber: j.invoice_number,
    description: j.description,
    status: j.work_status,
    address: j.address ? [j.address.street, j.address.city, j.address.state].filter(Boolean).join(', ') : '',
    city: j.address?.city || '',
    scheduledStart: j.schedule?.scheduled_start,
    completedAt: j.work_timestamps?.completed_at,
    assignedTo: (j.assigned_employees || []).map(e => e.first_name + ' ' + e.last_name).join(', '),
    tags: j.tags || [],
    total: j.total_amount,
    balance: j.outstanding_balance,
  }));
  return res.json({ ok: true, jobs });
}

async function getJobDetail(apiKey, jobId, res) {
  if (!jobId) return res.status(400).json({ error: 'jobId required' });

  const r = await fetch(`${HCP_API}/jobs/${jobId}`, {
    headers: { 'Authorization': `Token ${apiKey}`, 'Accept': 'application/json' },
  });
  if (!r.ok) return res.status(r.status).json({ error: `HCP API ${r.status}` });

  const j = await r.json();
  return res.json({
    ok: true,
    job: {
      id: j.id,
      invoiceNumber: j.invoice_number,
      description: j.description,
      status: j.work_status,
      customer: j.customer ? { id: j.customer.id, name: [j.customer.first_name, j.customer.last_name].filter(Boolean).join(' ') } : null,
      address: j.address ? { street: j.address.street, city: j.address.city, state: j.address.state, zip: j.address.zip } : null,
      scheduledStart: j.schedule?.scheduled_start,
      completedAt: j.work_timestamps?.completed_at,
      assignedTo: (j.assigned_employees || []).map(e => ({ id: e.id, name: e.first_name + ' ' + e.last_name })),
      tags: j.tags || [],
      total: j.total_amount,
      notes: (j.notes || []).map(n => n.content),
    },
  });
}

async function uploadAttachment(apiKey, jobId, filename, base64, res) {
  if (!jobId || !base64) return res.status(400).json({ error: 'jobId and base64 required' });

  // Convert base64 to binary
  const buffer = Buffer.from(base64, 'base64');
  const boundary = '----HCPBoundary' + Date.now();

  const body = Buffer.concat([
    Buffer.from(`--${boundary}\r\nContent-Disposition: form-data; name="file"; filename="${filename || 'photo.jpg'}"\r\nContent-Type: image/jpeg\r\n\r\n`),
    buffer,
    Buffer.from(`\r\n--${boundary}--\r\n`),
  ]);

  const r = await fetch(`${HCP_API}/jobs/${jobId}/attachments`, {
    method: 'POST',
    headers: {
      'Authorization': `Token ${apiKey}`,
      'Content-Type': `multipart/form-data; boundary=${boundary}`,
    },
    body: body,
  });

  if (!r.ok) {
    const err = await r.text().catch(() => '');
    return res.json({ ok: false, error: `HCP attachment upload failed (${r.status}): ${err.substring(0, 200)}` });
  }

  const data = await r.json().catch(() => ({}));
  return res.json({ ok: true, attachment: data });
}

function formatAddress(c) {
  if (!c.addresses || !c.addresses.length) return '';
  const a = c.addresses[0];
  return [a.street, a.city, a.state, a.zip].filter(Boolean).join(', ');
}

module.exports.config = { maxDuration: 30 };
