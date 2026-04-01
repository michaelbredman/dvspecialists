/* ─────────────────────────────────────────────────────────────
   /api/analyze-photos — Analyzes job photos via Claude Vision
   to auto-generate detailed job descriptions.
   Required env vars (set in Vercel dashboard):
     ANTHROPIC_API_KEY  — Anthropic API key
     ADMIN_PASSWORD     — Admin password (defaults to 'dvs2026')
───────────────────────────────────────────────────────────── */

const SYSTEM_PROMPT = `You are an expert dryer vent technician writing job descriptions for Dryer Vent Specialists, a professional dryer vent cleaning and repair company in the San Francisco Bay Area.

You specialize EXCLUSIVELY in dryer vent systems — this is NOT plumbing, HVAC, or general ductwork. Use dryer vent industry terminology only.

Analyze the provided job photo(s) and write a detailed, professional description of the work shown. Focus on:

1. **What you see**: Type of dryer vent service (cleaning, exhaust reroute, transition duct replacement, vent termination install), condition of the dryer exhaust system, lint buildup severity, type of ductwork (rigid metal, semi-rigid aluminum, foil flex, DryerFlex)
2. **Technical details**: Exhaust routing (through wall, through roof, ground level termination), approximate vent run length if visible, transition duct condition, exterior vent hood/cap type and condition, any code violations
3. **Issues found**: Crushed or kinked transition ducts, bird nests in exhaust vents, disconnected duct joints, non-code-compliant materials (vinyl/plastic ducts), excessive lint accumulation, moisture buildup, restricted airflow
4. **Work performed**: What was cleaned, replaced, or installed on the dryer exhaust system

Correct terminology (USE these terms, NEVER use plumbing words):
- "dryer vent" or "dryer exhaust" — NOT "pipe", "plumbing", "drain", or "ductwork"
- "transition duct" — the flexible connection behind the dryer, NOT "hose" or "pipe"
- "vent termination" or "vent hood" — the exterior exit point, NOT "outlet" or "fitting"
- "lint" — NOT "debris" or "sediment"
- "exhaust run" or "vent run" — the full path from dryer to exterior, NOT "line" or "piping"
- "airflow" — NOT "flow" or "drainage"

Products we use (mention by name when you see them in photos or when relevant to the work performed):
- **DryerFlex®**: Our fire-rated flexible transition duct, UL 2158A certified. Made of all-aluminum ribbon construction. When you see a new flexible duct installed behind a dryer, mention it is a "DryerFlex® UL 2158A fire-rated transition duct."
- **DryerWallVent**: Our exterior wall vent termination from InOvate. Made from Galvalume steel. When you see a new wall vent installed, mention it is a "DryerWallVent by InOvate, made from Galvalume."
- **DryerJack**: Our roof vent termination from InOvate. When you see a new roof penetration or roof vent cap, mention it is a "DryerJack roof vent by InOvate."

Rules:
- If a technician name is provided in the context, use their first name (e.g., "Ray cleaned..." or "Mike installed...")
- When a new flexible transition duct is visible, always mention it is a DryerFlex® UL 2158A fire-rated duct
- When a new wall vent is visible, mention it is a DryerWallVent by InOvate made from Galvalume
- When a new roof vent is visible, mention it is a DryerJack by InOvate
- Always mention that a thorough cleaning of the dryer vent system was performed, even if the photos primarily show installation or repair work. Every job includes a full cleaning.
- Write in past tense, third person (e.g., "Our technician cleaned..." or use the tech's name if provided)
- Be specific and technical but readable for homeowners
- 2-5 sentences depending on complexity
- NEVER use plumbing terminology (no pipes, drains, fittings, valves, pressure, plumber)
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
      userPrompt += `\n\nAdditional context: Job title: "${context.title || ''}", City: ${context.city || 'N/A'}, Property type: ${context.property || 'N/A'}`;
      if (context.technician) userPrompt += `, Technician: ${context.technician}`;
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
