/* ─────────────────────────────────────────────────────────────
   /api/enhance — Enhances job descriptions via Anthropic Claude.
   Required env vars (set in Vercel dashboard):
     ANTHROPIC_API_KEY  — Anthropic API key
     ADMIN_PASSWORD     — Admin password (defaults to 'dvs2026')
───────────────────────────────────────────────────────────── */

const SYSTEM_PROMPT = `You are a professional copywriter for Dryer Vent Specialists, a dryer vent cleaning and repair company in the San Francisco Bay Area.

Your job is to rewrite the provided job description to be:
- Professional and clear
- Concise (2-4 sentences max)
- Written in past tense, third person (e.g., "Our technician cleaned..." or "The dryer vent was...")
- Informative about what was done and the outcome
- Free of spelling and grammar errors

Rules:
- Do NOT add facts, services, or details that were not in the original text
- Do NOT include pricing, promotional language, or calls to action
- Do NOT use marketing buzzwords or superlatives
- Keep technical details if the original included them (e.g., vent length, lint buildup severity, type of repair)
- Output ONLY the enhanced description text, no quotes, no preamble, no explanation`;

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', req.headers.origin || '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const API_KEY    = process.env.ANTHROPIC_API_KEY;
  const ADMIN_PASS = process.env.ADMIN_PASSWORD || 'dvs2026';

  if (!API_KEY) {
    return res.status(500).json({
      error: 'ANTHROPIC_API_KEY environment variable is not set. Add it in the Vercel dashboard.',
    });
  }

  const { password, description } = req.body || {};

  if (password !== ADMIN_PASS) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  if (!description || !description.trim()) {
    return res.status(400).json({ error: 'Description is required.' });
  }

  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-haiku-4-5-20251001',
        max_tokens: 1024,
        system: SYSTEM_PROMPT,
        messages: [{ role: 'user', content: description.trim() }],
      }),
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({}));
      throw new Error(err.error?.message || `Anthropic API ${response.status}`);
    }

    const data = await response.json();
    const enhanced = data.content?.[0]?.text || '';

    if (!enhanced) {
      throw new Error('No text returned from AI.');
    }

    return res.json({ enhanced });
  } catch (err) {
    console.error('[enhance]', err.message);
    return res.status(500).json({ error: err.message });
  }
};

module.exports.config = { maxDuration: 15 };
