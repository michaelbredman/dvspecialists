/* ─────────────────────────────────────────────────────────────
   /api/ghl-contact — Creates or updates a contact in GoHighLevel
   CRM from the website contact form.

   Required env vars (set in Vercel dashboard):
     GHL_API_KEY      — Private Integration Token (pit-xxx)
     GHL_LOCATION_ID  — GHL sub-account Location ID
───────────────────────────────────────────────────────────── */

const GHL_API = 'https://services.leadconnectorhq.com';

module.exports = async function handler(req, res) {
  // CORS preflight
  res.setHeader('Access-Control-Allow-Origin', req.headers.origin || '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const API_KEY  = process.env.GHL_API_KEY;
  const LOCATION = process.env.GHL_LOCATION_ID;

  if (!API_KEY || !LOCATION) {
    return res.status(500).json({
      error: 'GoHighLevel env vars not set. Add GHL_API_KEY and GHL_LOCATION_ID in Vercel.',
    });
  }

  const { firstName, lastName, email, phone, message } = req.body || {};

  if (!firstName || !email) {
    return res.status(400).json({ error: 'First name and email are required.' });
  }

  try {
    const contactBody = {
      locationId: LOCATION,
      firstName,
      lastName: lastName || '',
      email,
      phone: phone || '',
      source: 'Website Contact Form',
    };

    // Add message to the contact.message custom field
    if (message) {
      contactBody.customFields = [
        { id: 'BuRMjUwh6AbxbJNX0ri5', value: message }
      ];
    }

    // Create or update contact
    const contactRes = await fetch(`${GHL_API}/contacts/upsert`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Version': '2021-07-28',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(contactBody),
    });

    const contactData = await contactRes.json().catch(() => ({}));

    if (!contactRes.ok) {
      const msg = contactData.message || contactData.error || `GHL API error ${contactRes.status}`;
      throw new Error(msg);
    }

    const contactId = contactData.contact?.id;

    // Add tag to contact (separate call — upsert doesn't support tags)
    if (contactId) {
      await fetch(`${GHL_API}/contacts/${contactId}/tags`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${API_KEY}`,
          'Version': '2021-07-28',
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tags: ['website-contact'] }),
      }).catch(err => {
        console.error('[ghl-contact] Tag addition failed:', err.message);
      });
    }


    return res.json({ ok: true, contactId });

  } catch (err) {
    console.error('[ghl-contact]', err.message);
    return res.status(500).json({ error: err.message });
  }
};

module.exports.config = { maxDuration: 30 };
