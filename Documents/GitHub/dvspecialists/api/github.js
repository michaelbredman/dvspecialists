/* ─────────────────────────────────────────────────────────────
   /api/github — Serverless proxy for all GitHub Content API calls.
   Keeps the GitHub PAT out of the browser entirely.
   Required env vars (set in Vercel dashboard):
     GITHUB_PAT      — Personal Access Token with repo write access
     ADMIN_PASSWORD  — Admin password (defaults to 'dvs2026')
───────────────────────────────────────────────────────────── */

const OWNER  = 'michaelbredman';
const REPO   = 'dvspecialists';
const BRANCH = 'main';

module.exports = async function handler(req, res) {
  // CORS preflight
  res.setHeader('Access-Control-Allow-Origin', req.headers.origin || '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const PAT           = process.env.GITHUB_PAT;
  const ADMIN_PASS    = process.env.ADMIN_PASSWORD || 'dvs2026';

  if (!PAT) {
    return res.status(500).json({
      error: 'GITHUB_PAT environment variable is not set. Add it in the Vercel dashboard.',
    });
  }

  const { password, action, ...data } = req.body || {};

  // read-jobs is public (jobs are already publicly visible on GitHub raw)
  if (action !== 'read-jobs' && password !== ADMIN_PASS) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  const gh = (path, method = 'GET', body = null) =>
    fetch(`https://api.github.com/repos/${OWNER}/${REPO}/contents/${path}`, {
      method,
      headers: {
        Authorization: `Bearer ${PAT}`,
        'Content-Type': 'application/json',
        Accept: 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
      },
      ...(body ? { body: JSON.stringify(body) } : {}),
    });

  try {
    switch (action) {

      case 'read-jobs': {
        const r = await gh('jobs.json');
        if (r.status === 404) return res.json({ jobs: [], sha: null });
        if (!r.ok) throw new Error(`GitHub ${r.status}`);
        const d = await r.json();
        const jobs = JSON.parse(Buffer.from(d.content.replace(/\n/g, ''), 'base64').toString('utf8'));
        return res.json({ jobs, sha: d.sha });
      }

      case 'write-jobs': {
        const { jobs, sha } = data;
        const content = Buffer.from(JSON.stringify(jobs, null, 2)).toString('base64');
        const body = { message: 'Update jobs.json', content, branch: BRANCH };
        if (sha) body.sha = sha;
        const r = await gh('jobs.json', 'PUT', body);
        if (!r.ok) {
          const e = await r.json().catch(() => ({}));
          throw new Error(e.message || `GitHub ${r.status}`);
        }
        return res.json({ ok: true });
      }

      case 'upload-image': {
        const { path, base64 } = data;
        const body = { message: `Add job photo: ${path}`, content: base64, branch: BRANCH };
        const r = await gh(path, 'PUT', body);
        if (!r.ok) {
          const e = await r.json().catch(() => ({}));
          throw new Error(e.message || `GitHub ${r.status}`);
        }
        return res.json({ ok: true });
      }

      case 'get-file-sha': {
        const { path } = data;
        const r = await gh(path);
        if (r.status === 404) return res.json({ sha: null });
        if (!r.ok) throw new Error(`GitHub ${r.status}`);
        const d = await r.json();
        return res.json({ sha: d.sha });
      }

      case 'delete-image': {
        const { path, sha } = data;
        const body = { message: `Delete job image: ${path}`, sha, branch: BRANCH };
        const r = await gh(path, 'DELETE', body);
        if (!r.ok) {
          const e = await r.json().catch(() => ({}));
          throw new Error(e.message || `GitHub ${r.status}`);
        }
        return res.json({ ok: true });
      }

      default:
        return res.status(400).json({ error: `Unknown action: ${action}` });
    }
  } catch (err) {
    console.error('[github-proxy]', err.message);
    return res.status(500).json({ error: err.message });
  }
};

module.exports.config = { maxDuration: 30 };
