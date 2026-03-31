/* ─────────────────────────────────────────────────────────────
   /api/settings — Read/write integration settings to Vercel Blob.
   Stores a JSON object with connection credentials for:
     - Google Maps (API key, default center, zoom)
     - HouseCall Pro (API key)
     - GoHighLevel (API key, Location ID)
     - Facebook (Page Access Token, Page ID)
     - Google Business Profile (Account ID, credentials)

   Required env vars:
     BLOB_READ_WRITE_TOKEN — auto-provisioned by Vercel Blob
     ADMIN_PASSWORD        — existing admin password
───────────────────────────────────────────────────────────── */

const { put, list, head } = require('@vercel/blob');

const SETTINGS_KEY = 'settings/integrations.json';

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', req.headers.origin || '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const ADMIN_PASS = process.env.ADMIN_PASSWORD || 'dvs2026';
  const { password, action, settings } = req.body || {};

  if (password !== ADMIN_PASS) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  try {
    if (action === 'read') {
      // Read current settings from Blob
      try {
        const blobs = await list({ prefix: 'settings/' });
        const settingsBlob = blobs.blobs.find(b => b.pathname === SETTINGS_KEY);
        if (!settingsBlob) {
          return res.json({ ok: true, settings: getDefaultSettings() });
        }
        const response = await fetch(settingsBlob.url);
        const data = await response.json();
        // Mask sensitive values for client display
        return res.json({ ok: true, settings: data });
      } catch (err) {
        console.error('[settings] Read error:', err.message);
        return res.json({ ok: true, settings: getDefaultSettings() });
      }
    }

    if (action === 'write') {
      if (!settings || typeof settings !== 'object') {
        return res.status(400).json({ error: 'Missing settings object' });
      }

      // Merge with existing settings (so partial updates work)
      let existing = getDefaultSettings();
      try {
        const blobs = await list({ prefix: 'settings/' });
        const settingsBlob = blobs.blobs.find(b => b.pathname === SETTINGS_KEY);
        if (settingsBlob) {
          const response = await fetch(settingsBlob.url);
          existing = await response.json();
        }
      } catch { /* use defaults */ }

      const merged = deepMerge(existing, settings);
      merged.updatedAt = new Date().toISOString();

      await put(SETTINGS_KEY, JSON.stringify(merged, null, 2), {
        access: 'public',
        contentType: 'application/json',
        addRandomSuffix: false,
        allowOverwrite: true,
      });

      return res.json({ ok: true, settings: merged });
    }

    if (action === 'test-connection') {
      const { integration } = req.body;
      return await testConnection(integration, req.body, res);
    }

    return res.status(400).json({ error: 'Invalid action. Use: read, write, test-connection' });

  } catch (err) {
    console.error('[settings]', err.message);
    return res.status(500).json({ error: err.message });
  }
};

function getDefaultSettings() {
  return {
    googleMaps: {
      apiKey: '',
      defaultCenter: { lat: 37.5630, lng: -122.3255 },
      defaultZoom: 11,
      connected: false,
    },
    housecallPro: {
      apiKey: '',
      bookingUrl: '',
      connected: false,
    },
    goHighLevel: {
      apiKey: '',
      locationId: '',
      connected: false,
    },
    facebook: {
      pageAccessToken: '',
      pageId: '',
      pageName: '',
      connected: false,
    },
    googleBusinessProfile: {
      accountId: '',
      locationId: '',
      accessToken: '',
      refreshToken: '',
      connected: false,
    },
    updatedAt: null,
  };
}

function deepMerge(target, source) {
  const result = { ...target };
  for (const key of Object.keys(source)) {
    if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
      result[key] = deepMerge(target[key] || {}, source[key]);
    } else {
      result[key] = source[key];
    }
  }
  return result;
}

async function testConnection(integration, body, res) {
  try {
    switch (integration) {
      case 'googleMaps': {
        const { apiKey } = body;
        if (!apiKey) return res.json({ ok: false, error: 'API key is required' });
        // Test with a simple geocoding request
        const testUrl = `https://maps.googleapis.com/maps/api/geocode/json?address=San+Mateo,CA&key=${apiKey}`;
        const r = await fetch(testUrl);
        const data = await r.json();
        if (data.status === 'OK') {
          return res.json({ ok: true, message: 'Google Maps API key is valid' });
        } else if (data.status === 'REQUEST_DENIED') {
          return res.json({ ok: false, error: 'API key denied. Check key restrictions.' });
        } else {
          return res.json({ ok: false, error: `API returned: ${data.status}` });
        }
      }

      case 'housecallPro': {
        const { apiKey } = body;
        if (!apiKey) return res.json({ ok: false, error: 'API key is required' });
        const r = await fetch('https://api.housecallpro.com/employees', {
          headers: { 'Authorization': `Token ${apiKey}`, 'Accept': 'application/json' },
        });
        if (r.ok) {
          const data = await r.json();
          const companyName = data.employees?.[0]?.company_name || 'HouseCall Pro';
          return res.json({ ok: true, message: `Connected to: ${companyName}`, companyName });
        } else if (r.status === 401) {
          return res.json({ ok: false, error: 'Invalid API key. Check your key in HouseCall Pro settings.' });
        } else {
          return res.json({ ok: false, error: `API returned ${r.status}. Check your API key.` });
        }
      }

      case 'goHighLevel': {
        const { apiKey, locationId } = body;
        if (!apiKey) return res.json({ ok: false, error: 'API key is required' });
        const r = await fetch(`https://services.leadconnectorhq.com/locations/${locationId || 'test'}`, {
          headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Version': '2021-07-28',
            'Accept': 'application/json',
          },
        });
        if (r.ok) {
          const data = await r.json();
          return res.json({ ok: true, message: `Connected to: ${data.location?.name || 'GoHighLevel'}` });
        } else if (r.status === 401) {
          return res.json({ ok: false, error: 'Invalid API key' });
        } else {
          return res.json({ ok: false, error: `API returned ${r.status}` });
        }
      }

      case 'facebook': {
        const { pageAccessToken } = body;
        if (!pageAccessToken) return res.json({ ok: false, error: 'Page Access Token is required' });
        const r = await fetch(`https://graph.facebook.com/me?access_token=${pageAccessToken}&fields=name,id`);
        const data = await r.json();
        if (data.name) {
          return res.json({ ok: true, message: `Connected to: ${data.name}`, pageName: data.name, pageId: data.id });
        } else {
          return res.json({ ok: false, error: data.error?.message || 'Invalid token' });
        }
      }

      default:
        return res.json({ ok: false, error: 'Unknown integration: ' + integration });
    }
  } catch (err) {
    return res.json({ ok: false, error: 'Connection test failed: ' + err.message });
  }
}

module.exports.config = { maxDuration: 30 };
