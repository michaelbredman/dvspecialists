/* ─────────────────────────────────────────────────────────────
   /api/reviews — Fetches Google reviews via Places API (New).
   Keeps the API key server-side. Cached at the edge for 24 hours.
   Required env var (set in Vercel dashboard):
     GOOGLE_PLACES_API_KEY — Places API key
───────────────────────────────────────────────────────────── */

const PLACE_ID = 'ChIJWf_sfsbhyWgR2xV2QE14BXU';

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 's-maxage=86400, stale-while-revalidate=3600');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  const API_KEY = process.env.GOOGLE_PLACES_API_KEY;
  if (!API_KEY) {
    return res.status(500).json({
      error: 'GOOGLE_PLACES_API_KEY not configured. Add it in the Vercel dashboard.',
    });
  }

  try {
    const url = `https://places.googleapis.com/v1/places/${PLACE_ID}`;

    const r = await fetch(url, {
      headers: {
        'X-Goog-Api-Key': API_KEY,
        'X-Goog-FieldMask': 'rating,userRatingCount,reviews',
      },
    });

    const data = await r.json();

    if (data.error) {
      throw new Error(data.error.message || `Places API error ${data.error.code}`);
    }

    return res.json({
      rating:       data.rating || null,
      totalReviews: data.userRatingCount || 0,
      reviews:      (data.reviews || []).map(rv => ({
        author:       rv.authorAttribution?.displayName || 'Anonymous',
        rating:       rv.rating,
        text:         rv.text?.text || '',
        relativeTime: rv.relativePublishTimeDescription || '',
        photoUrl:     rv.authorAttribution?.photoUri || null,
      })),
    });
  } catch (err) {
    console.error('[reviews]', err.message);
    return res.status(500).json({ error: err.message });
  }
};

module.exports.config = { maxDuration: 10 };
