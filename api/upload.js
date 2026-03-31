/* ─────────────────────────────────────────────────────────────
   /api/upload — Upload job photos to Vercel Blob storage.
   Returns the public URL for each uploaded image.

   Required env vars (set automatically by Vercel Blob):
     BLOB_READ_WRITE_TOKEN — auto-provisioned by Vercel Blob
     ADMIN_PASSWORD        — existing admin password
───────────────────────────────────────────────────────────── */

const { put, del } = require('@vercel/blob');

module.exports = async function handler(req, res) {
  // CORS preflight
  res.setHeader('Access-Control-Allow-Origin', req.headers.origin || '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const ADMIN_PASS = process.env.ADMIN_PASSWORD || 'dvs2026';
  const { password, action, filename, base64, blobUrl } = req.body || {};

  if (password !== ADMIN_PASS) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  try {
    if (action === 'delete') {
      // Delete a blob by URL
      if (!blobUrl) return res.status(400).json({ error: 'Missing blobUrl' });
      await del(blobUrl);
      return res.json({ ok: true });
    }

    // Default action: upload
    if (!filename || !base64) {
      return res.status(400).json({ error: 'Missing filename or base64 data' });
    }

    // Convert base64 to Buffer
    const buffer = Buffer.from(base64, 'base64');

    // Upload to Vercel Blob
    const blob = await put(`work/${filename}`, buffer, {
      access: 'public',
      contentType: 'image/jpeg',
    });

    return res.json({ ok: true, url: blob.url });

  } catch (err) {
    console.error('[upload]', err.message);
    return res.status(500).json({ error: err.message });
  }
};

module.exports.config = { maxDuration: 30 };
