/* ─────────────────────────────────────────────────────────────
   /api/work-page — SSR wrapper for the Our Work page.
   Reads work-template.html, fetches jobs from GitHub,
   pre-renders job card HTML, pagination, and JSON-LD schema
   so everything appears in View Source for crawlers.
   Supports ?page=N for pagination (12 jobs per page).
───────────────────────────────────────────────────────────── */

const fs   = require('fs');
const path = require('path');

const OWNER  = 'michaelbredman';
const REPO   = 'dvspecialists';
const BRANCH = 'main';
const GITHUB_RAW = `https://raw.githubusercontent.com/${OWNER}/${REPO}/${BRANCH}`;
const JOBS_PER_PAGE = 12;

const CITY_COORDS = {
  'San Mateo':            { lat: 37.5630, lng: -122.3255 },
  'San Francisco':        { lat: 37.7749, lng: -122.4194 },
  'South San Francisco':  { lat: 37.6547, lng: -122.4077 },
  'Burlingame':           { lat: 37.5841, lng: -122.3661 },
  'Hillsborough':         { lat: 37.5741, lng: -122.3794 },
  'Belmont':              { lat: 37.5202, lng: -122.2758 },
  'San Carlos':           { lat: 37.5072, lng: -122.2605 },
  'Redwood City':         { lat: 37.4852, lng: -122.2364 },
  'Menlo Park':           { lat: 37.4530, lng: -122.1817 },
  'Half Moon Bay':        { lat: 37.4636, lng: -122.4286 },
  'Los Altos':            { lat: 37.3852, lng: -122.1141 },
  'Palo Alto':            { lat: 37.4419, lng: -122.1430 },
  'Mountain View':        { lat: 37.3861, lng: -122.0839 },
  'Sunnyvale':            { lat: 37.3688, lng: -122.0363 },
  'Santa Clara':          { lat: 37.3541, lng: -121.9552 },
  'San Jose':             { lat: 37.3382, lng: -121.8863 },
};

function resolveImg(p) {
  if (!p) return p;
  return p.startsWith('http') ? p : GITHUB_RAW + '/' + p;
}

function esc(s) {
  return (s || '').replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;');
}

function buildWorkCard(job) {
  const imgs = (job.images || []).map(resolveImg);
  const hasImg = imgs.length > 0;
  const id = job.id || Math.random().toString(36).slice(2);
  const imgJson = JSON.stringify(imgs).replace(/"/g, '&quot;');
  const titleJson = JSON.stringify(job.title || '').replace(/"/g, '&quot;');

  return `
      <article class="job-card" data-city="${esc(job.city)}">
        ${hasImg ? `
          <div class="card-images" onclick="openLightbox(${imgJson}, 0, ${titleJson})" data-imgs="${id}">
            <img id="thumb-${id}" src="${esc(imgs[0])}" alt="${esc(job.title || 'Job photo')}" loading="lazy" />
            ${imgs.length > 1 ? `
              <div class="img-nav">
                <button onclick="event.stopPropagation(); cycleThumb('${id}', ${imgJson}, -1)">&lsaquo;</button>
                <button onclick="event.stopPropagation(); cycleThumb('${id}', ${imgJson}, 1)">&rsaquo;</button>
              </div>
              <div class="img-count" id="count-${id}">1 / ${imgs.length}</div>
            ` : ''}
          </div>
        ` : `<div class="card-no-image">No Photos</div>`}
        <div class="card-body">
          <div class="card-meta">
            ${job.city ? `<span class="city-badge">${esc(job.city)}</span>` : ''}
          </div>
          ${job.title ? `<h3 class="card-title">${esc(job.title)}</h3>` : ''}
          ${job.description ? `<p class="card-desc" id="desc-${id}">${esc(job.description)}</p><button class="read-more-btn" id="rmb-${id}" onclick="toggleDesc('${id}')">Read more</button>` : ''}
          <a href="/book" class="card-cta">Book a Cleaning <span>&rarr;</span></a>
        </div>
      </article>`;
}

function buildPaginationHtml(currentPage, totalPages) {
  if (totalPages <= 1) return '';
  let html = `<div style="display:flex;justify-content:center;align-items:center;gap:.75rem;padding:2rem 1.5rem 0;">`;

  if (currentPage > 1) {
    const prevUrl = currentPage === 2 ? '/work' : `/work?page=${currentPage - 1}`;
    html += `<a href="${prevUrl}" style="font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:.9rem;letter-spacing:.06em;text-transform:uppercase;padding:.6rem 1.25rem;border-radius:6px;border:2px solid #026766;color:#026766;text-decoration:none;transition:background .2s,color .2s;" onmouseover="this.style.background='#026766';this.style.color='#fff'" onmouseout="this.style.background='transparent';this.style.color='#026766'">&larr; Previous</a>`;
  }

  html += `<span style="font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:.85rem;color:#666;letter-spacing:.05em;">Page ${currentPage} of ${totalPages}</span>`;

  if (currentPage < totalPages) {
    html += `<a href="/work?page=${currentPage + 1}" style="font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:.9rem;letter-spacing:.06em;text-transform:uppercase;padding:.6rem 1.25rem;border-radius:6px;border:2px solid #026766;color:#026766;text-decoration:none;transition:background .2s,color .2s;" onmouseover="this.style.background='#026766';this.style.color='#fff'" onmouseout="this.style.background='transparent';this.style.color='#026766'">Next &rarr;</a>`;
  }

  html += '</div>';
  return html;
}

function buildJobsJsonLd(jobs, page, totalPages) {
  if (!jobs.length) return '';

  const itemList = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "name": `Completed Dryer Vent Cleaning Jobs${page > 1 ? ` - Page ${page}` : ''}`,
    "description": "Browse real completed dryer vent cleaning and repair jobs by Dryer Vent Specialists across the San Francisco Bay Area.",
    "numberOfItems": jobs.length,
    "itemListElement": jobs.map((job, i) => {
      const coords = (job.lat && job.lng)
        ? { lat: job.lat, lng: job.lng }
        : (CITY_COORDS[job.city] || null);

      const item = {
        "@type": "ListItem",
        "position": i + 1,
        "item": {
          "@type": "Service",
          "serviceType": "Dryer Vent Cleaning",
          "category": "HVAC Maintenance",
          "name": job.title || "Dryer Vent Cleaning",
          "description": job.description || "",
          "provider": {
            "@type": ["LocalBusiness", "HomeAndConstructionBusiness", "ProfessionalService", "HVACBusiness"],
            "name": "Dryer Vent Specialists",
            "telephone": "+1-650-484-4418",
            "url": "https://www.dvspecialists.com"
          },
        }
      };

      if (job.city) {
        item.item.areaServed = {
          "@type": "City", "name": job.city,
          "containedInPlace": { "@type": "State", "name": "California" }
        };
      }
      if (coords) {
        item.item.serviceLocation = {
          "@type": "Place",
          "geo": { "@type": "GeoCoordinates", "latitude": coords.lat, "longitude": coords.lng },
          "address": { "@type": "PostalAddress", "addressLocality": job.city || "", "addressRegion": "CA", "addressCountry": "US" }
        };
      }
      if (job.images && job.images.length) item.item.image = job.images.map(resolveImg);
      if (job.date) item.item.serviceOutput = { "@type": "CreativeWork", "dateCreated": job.date };
      if (job.property) item.item.additionalType = job.property;

      return item;
    })
  };

  return `\n  <script type="application/ld+json" id="jobs-jsonld">\n  ${JSON.stringify(schema, null, 2).split('\n').join('\n  ')}\n  </script>`;
}

module.exports = async function handler(req, res) {
  try {
    const templatePath = path.join(__dirname, '..', 'work-template.html');
    let html = fs.readFileSync(templatePath, 'utf8');

    // Parse page number
    const urlParams = new URL(req.url, 'https://x.com').searchParams;
    const page = Math.max(1, parseInt(urlParams.get('page') || '1', 10));

    // Fetch all jobs
    let allJobs = [];
    try {
      const PAT = process.env.GITHUB_PAT;
      const headers = { Accept: 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28' };
      if (PAT) headers.Authorization = `Bearer ${PAT}`;

      const ghRes = await fetch(`https://api.github.com/repos/${OWNER}/${REPO}/contents/jobs.json`, { headers });
      if (ghRes.ok) {
        const data = await ghRes.json();
        allJobs = JSON.parse(Buffer.from(data.content.replace(/\n/g, ''), 'base64').toString('utf8'));
        // Normalize image paths
        allJobs = allJobs.map(j => ({ ...j, images: (j.images || []).map(resolveImg) }));
      }
    } catch (e) {
      console.error('[work-page] Failed to fetch jobs:', e.message);
    }

    // Paginate
    const totalPages = Math.max(1, Math.ceil(allJobs.length / JOBS_PER_PAGE));
    const safePage = Math.min(page, totalPages);
    const startIdx = (safePage - 1) * JOBS_PER_PAGE;
    const pageJobs = allJobs.slice(startIdx, startIdx + JOBS_PER_PAGE);

    // 1. Inject JSON-LD into <head>
    if (pageJobs.length) {
      const schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": `Completed Dryer Vent Cleaning Jobs${safePage > 1 ? ` - Page ${safePage}` : ''}`,
        "description": "Browse real completed dryer vent cleaning and repair jobs by Dryer Vent Specialists across the San Francisco Bay Area.",
        "numberOfItems": pageJobs.length,
        "itemListElement": pageJobs.map((job, i) => {
          const coords = (job.lat && job.lng)
            ? { lat: job.lat, lng: job.lng }
            : (CITY_COORDS[job.city] || null);

          const item = {
            "@type": "ListItem",
            "position": i + 1,
            "item": {
              "@type": "Service",
              "serviceType": "Dryer Vent Cleaning",
              "category": "HVAC Maintenance",
              "name": job.title || "Dryer Vent Cleaning",
              "description": job.description || "",
              "provider": {
                "@type": ["LocalBusiness", "HomeAndConstructionBusiness", "ProfessionalService", "HVACBusiness"],
                "name": "Dryer Vent Specialists",
                "telephone": "+1-650-484-4418",
                "url": "https://www.dvspecialists.com"
              },
            }
          };

          if (job.city) {
            item.item.areaServed = {
              "@type": "City", "name": job.city,
              "containedInPlace": { "@type": "State", "name": "California" }
            };
          }
          if (coords) {
            item.item.serviceLocation = {
              "@type": "Place",
              "geo": { "@type": "GeoCoordinates", "latitude": coords.lat, "longitude": coords.lng },
              "address": { "@type": "PostalAddress", "addressLocality": job.city || "", "addressRegion": "CA", "addressCountry": "US" }
            };
          }
          if (job.images && job.images.length) item.item.image = job.images;
          if (job.date) item.item.serviceOutput = { "@type": "CreativeWork", "dateCreated": job.date };
          if (job.property) item.item.additionalType = job.property;

          return item;
        })
      };

      const jsonLdScript = `\n  <script type="application/ld+json" id="jobs-jsonld">\n  ${JSON.stringify(schema, null, 2).split('\n').join('\n  ')}\n  </script>`;
      html = html.replace('</head>', jsonLdScript + '\n</head>');
    }

    // 2. Pre-render job cards into the grid (replace skeleton placeholders)
    if (pageJobs.length) {
      const cardsHtml = pageJobs.map(buildWorkCard).join('');
      const paginationHtml = buildPaginationHtml(safePage, totalPages);

      // Replace the skeleton placeholders with real cards
      const skeletonRegex = /(<div class="jobs-grid" id="jobs-grid">)[\s\S]*?(<\/div>\s*<\/section>)/;
      html = html.replace(skeletonRegex, `$1${cardsHtml}$2${paginationHtml}`);
    }

    // 3. Pass pagination info to client-side JS so it knows not to re-render SSR page
    html = html.replace(
      'let allJobs = [];',
      `let allJobs = [];\n  const SSR_PAGE = ${safePage};\n  const SSR_TOTAL_PAGES = ${totalPages};\n  const SSR_TOTAL_JOBS = ${allJobs.length};`
    );

    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.setHeader('Cache-Control', 'public, s-maxage=300, stale-while-revalidate=60');
    return res.status(200).send(html);
  } catch (err) {
    console.error('[work-page] Error:', err.message);
    return res.status(500).send('Internal Server Error');
  }
};

module.exports.config = { maxDuration: 10 };
