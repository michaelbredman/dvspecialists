/* ─────────────────────────────────────────────────────────────
   /api/analyze-photos — Analyzes job photos via Claude Vision
   to auto-generate detailed job descriptions.
   Required env vars (set in Vercel dashboard):
     ANTHROPIC_API_KEY  — Anthropic API key
     ADMIN_PASSWORD     — Admin password (defaults to 'dvs2026')
───────────────────────────────────────────────────────────── */

const SYSTEM_PROMPT = `You are an expert dryer vent technician writing job descriptions for Dryer Vent Specialists, a professional dryer vent cleaning and repair company in the San Francisco Bay Area.

Analyze the provided job photo(s) and write a detailed, professional description of the work shown. Focus on:

1. **What you see**: Type of service (cleaning, repair, installation, reroute), condition of the vent/dryer, lint buildup severity, type of ductwork (rigid metal, semi-rigid, foil flex, etc.)
2. **Technical details**: Vent routing (wall, roof, ground level), approximate vent run length if visible, transition hose condition, exterior vent cap type/condition, any code violations
3. **Issues found**: Crushed/kinked ducts, bird nests, disconnected vents, improper materials, excessive lint accumulation, moisture/mold signs, pest intrusion
4. **Work performed**: What was cleaned, repaired, replaced, or installed based on before/after evidence

Rules:
- Write in past tense, third person (e.g., "Our technician cleaned...", "The dryer vent was...")
- Be specific and technical but readable (homeowners will see this)
- 2-5 sentences depending on complexity
- Do NOT invent details you cannot see in the photos
- Do NOT include pricing, promotional language, or calls to action
- Do NOT mention the photo itself (don't say "the photo shows...")
- If multiple photos show before/after, describe the transformation
- Output ONLY the description text, no quotes, no preamble`;

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

  const { password, images, context } = req.body || {};

  if (password !== ADMIN_PASS) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  if (!images || !images.length) {
    return res.status(400).json({ error: 'At least one image is required.' });
  }

  if (images.length > 10) {
    return res.status(400).json({ error: 'Maximum 10 images allowed.' });
  }

  try {
    // Build content array with images and optional context
    const content = [];

    for (const img of images) {
      // Accept base64 data URLs or raw base64
      let mediaType = 'image/jpeg';
      let data = img;

      if (img.startsWith('data:')) {
        const match = img.match(/^data:(image\/\w+);base64,(.+)$/);
        if (match) {
          mediaType = match[1];
          data = match[2];
        } else {
          data = img.split(',')[1] || img;
        }
      }

      content.push({
        type: 'image',
        source: {
          type: 'base64',
          media_type: mediaType,
          data: data,
        },
      });
    }

    // Add context prompt
    let userPrompt = 'Analyze these dryer vent job photos and write a detailed job description.';
    if (context) {
      userPrompt += `\n\nAdditional context from the technician: Job title: "${context.title || ''}", City: ${context.city || 'N/A'}, Property type: ${context.property || 'N/A'}`;
    }
    content.push({ type: 'text', text: userPrompt });

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
        messages: [{ role: 'user', content }],
      }),
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({}));
      throw new Error(err.error?.message || `Anthropic API ${response.status}`);
    }

    const data = await response.json();
    const description = data.content?.[0]?.text || '';

    if (!description) {
      throw new Error('No description returned from AI.');
    }

    return res.json({ description });
  } catch (err) {
    console.error('[analyze-photos]', err.message);
    return res.status(500).json({ error: err.message });
  }
};

module.exports.config = { maxDuration: 30 };
