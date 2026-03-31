/* ─────────────────────────────────────────────────────────────
   Shared helper: reads integration settings from Vercel Blob.
   Used by facebook.js, ghl-gbp.js, and other API endpoints
   to get credentials when env vars aren't set.
───────────────────────────────────────────────────────────── */

const { list } = require('@vercel/blob');

const SETTINGS_KEY = 'settings/integrations.json';
let _cache = null;
let _cacheTime = 0;
const CACHE_TTL = 30000; // 30 seconds

async function getSettings() {
  // Simple in-memory cache to avoid hitting Blob on every request
  if (_cache && Date.now() - _cacheTime < CACHE_TTL) return _cache;

  try {
    const blobs = await list({ prefix: 'settings/' });
    const settingsBlob = blobs.blobs.find(b => b.pathname === SETTINGS_KEY);
    if (!settingsBlob) return {};

    const response = await fetch(settingsBlob.url);
    const data = await response.json();
    _cache = data;
    _cacheTime = Date.now();
    return data;
  } catch (err) {
    console.error('[get-settings]', err.message);
    return {};
  }
}

module.exports = getSettings;
