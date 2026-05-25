/* ─────────────────────────────────────────────────────────────
   tradestack-generate — calls tradestack-backend's
   POST /v1/content/generate to produce platform-tuned, RAG-grounded
   copy for a job before we post to Facebook / GBP / website.

   Failure semantics: returns null on any error (missing config,
   network failure, AI 5xx, malformed response). Callers fall back
   to the legacy "post raw jobs.json fields" path so a transient AI
   problem never blocks an actual post going out.
───────────────────────────────────────────────────────────── */

const DEFAULT_API_URL = "https://tradestack-backend.vercel.app/v1";

/**
 * @param {"facebook"|"gbp"|"website"} kind
 * @param {{
 *   title:string, description:string, city?:string, state?:string,
 *   propertyType?:string, date?:string,
 *   photos?:Array<{url:string, caption?:string}>
 * }} job
 * @returns {Promise<null | {
 *   kind:"facebook", body:string, hashtags:string[],
 *     recommendedImageUrls:string[],
 *     citedProblemIds:string[], citedStandardIds:string[], model:string
 * } | {
 *   kind:"gbp", body:string,
 *     actionButton:"Get a Quote"|"Call Now"|"Learn More"|"Book Online",
 *     citedProblemIds:string[], citedStandardIds:string[], model:string
 * } | {
 *   kind:"website", title:string, summary:string, body:string,
 *     photoAlts:string[], slug:string,
 *     citedProblemIds:string[], citedStandardIds:string[], model:string
 * }>}
 */
async function generateContent(kind, job) {
  const apiUrl = (process.env.TRADESTACK_API_URL || DEFAULT_API_URL).replace(/\/+$/, "");
  const token = process.env.TRADESTACK_SERVICE_TOKEN;
  if (!token) {
    console.warn("[tradestack-generate] TRADESTACK_SERVICE_TOKEN not set; skipping AI generation");
    return null;
  }

  // 25s timeout — endpoint typical p95 is ~6-10s; bail well before
  // any upstream serverless function timeout (Vercel default 60s for the caller).
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 25_000);

  try {
    const res = await fetch(`${apiUrl}/content/generate`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ kind, job }),
      signal: controller.signal,
    });
    if (!res.ok) {
      const text = await res.text().catch(() => "");
      console.warn(`[tradestack-generate] ${kind} failed: ${res.status} ${text.slice(0, 200)}`);
      return null;
    }
    const data = await res.json();
    if (!data || typeof data !== "object" || data.kind !== kind) {
      console.warn(`[tradestack-generate] ${kind} returned unexpected shape`);
      return null;
    }
    return data;
  } catch (err) {
    const msg = err && err.name === "AbortError" ? "timeout after 25s" : err && err.message;
    console.warn(`[tradestack-generate] ${kind} request failed:`, msg);
    return null;
  } finally {
    clearTimeout(timer);
  }
}

module.exports = { generateContent };
