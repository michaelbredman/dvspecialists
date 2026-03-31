/* ─────────────────────────────────────────────────────────────
   /api/city-page — SSR wrapper for city service area pages.
   Reads the city template HTML, fetches jobs filtered by city,
   pre-renders job card HTML, pagination, and JSON-LD schema
   so everything appears in View Source for crawlers.
   Supports ?page=N for pagination (9 jobs per page).
───────────────────────────────────────────────────────────── */

const fs   = require('fs');
const path = require('path');

const OWNER  = 'michaelbredman';
const REPO   = 'dvspecialists';
const BRANCH = 'main';
const GITHUB_RAW = `https://raw.githubusercontent.com/${OWNER}/${REPO}/${BRANCH}`;
const JOBS_PER_PAGE = 9;

const CITY_MAP = {
  'dryer-vent-cleaning-san-mateo':            { city: 'San Mateo',            lat: 37.5630, lng: -122.3255 },
  'dryer-vent-cleaning-san-francisco':        { city: 'San Francisco',        lat: 37.7749, lng: -122.4194 },
  'dryer-vent-cleaning-south-san-francisco':  { city: 'South San Francisco',  lat: 37.6547, lng: -122.4077 },
  'dryer-vent-cleaning-burlingame':           { city: 'Burlingame',           lat: 37.5841, lng: -122.3661 },
  'dryer-vent-cleaning-hillsborough':         { city: 'Hillsborough',        lat: 37.5741, lng: -122.3794 },
  'dryer-vent-cleaning-belmont':              { city: 'Belmont',             lat: 37.5202, lng: -122.2758 },
  'dryer-vent-cleaning-san-carlos':           { city: 'San Carlos',          lat: 37.5072, lng: -122.2605 },
  'dryer-vent-cleaning-redwood-city':         { city: 'Redwood City',        lat: 37.4852, lng: -122.2364 },
  'dryer-vent-cleaning-menlo-park':           { city: 'Menlo Park',          lat: 37.4530, lng: -122.1817 },
  'dryer-vent-cleaning-half-moon-bay':        { city: 'Half Moon Bay',       lat: 37.4636, lng: -122.4286 },
  'dryer-vent-cleaning-los-altos':            { city: 'Los Altos',           lat: 37.3852, lng: -122.1141 },
  'dryer-vent-cleaning-palo-alto':            { city: 'Palo Alto',           lat: 37.4419, lng: -122.1430 },
  'dryer-vent-cleaning-mountain-view':        { city: 'Mountain View',       lat: 37.3861, lng: -122.0839 },
  'dryer-vent-cleaning-sunnyvale':            { city: 'Sunnyvale',           lat: 37.3688, lng: -122.0363 },
  'dryer-vent-cleaning-santa-clara':          { city: 'Santa Clara',         lat: 37.3541, lng: -121.9552 },
  'dryer-vent-cleaning-san-jose':             { city: 'San Jose',            lat: 37.3382, lng: -121.8863 },
};

function resolveImg(p) {
  if (!p) return p;
  return p.startsWith('http') ? p : GITHUB_RAW + '/' + p;
}

function esc(s) {
  return (s || '').replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;');
}

function buildJobCardHtml(job) {
  const imgs = (job.images || []).map(resolveImg);
  const id = job.id || Math.random().toString(36).slice(2);
  if (!imgs.length) return '';

  const imgJson = JSON.stringify(imgs).replace(/"/g, '&quot;');
  return `<div class="city-job-card"><div class="cjc-images" onclick="cjcOpenLb(${imgJson},cjcThumbs['${id}']||0)"><img id="cjc-t-${id}" src="${esc(imgs[0])}" alt="${esc(job.title)}" loading="lazy">${imgs.length > 1 ? `<div class="cjc-nav"><button onclick="event.stopPropagation();cjcCycle('${id}',${imgJson},-1)">&#8249;</button><button onclick="event.stopPropagation();cjcCycle('${id}',${imgJson},1)">&#8250;</button></div><div class="cjc-count" id="cjc-c-${id}">1 / ${imgs.length}</div>` : ''}</div><div class="city-job-card-body"><span class="cjc-badge">${esc(job.city)}</span><h3>${esc(job.title)}</h3>${job.description ? `<p>${esc(job.description)}</p><button class="cjc-toggle" onclick="(function(b){var p=b.previousElementSibling;p.classList.toggle('expanded');b.textContent=p.classList.contains('expanded')?'Show less':'Read more';})(this)">Read more</button>` : ''}</div></div>`;
}

function buildPaginationHtml(slug, currentPage, totalPages) {
  if (totalPages <= 1) return '';
  let html = '<div style="display:flex;justify-content:center;align-items:center;gap:.75rem;margin-top:2rem;">';

  if (currentPage > 1) {
    const prevUrl = currentPage === 2 ? `/${slug}` : `/${slug}?page=${currentPage - 1}`;
    html += `<a href="${prevUrl}" style="font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:.9rem;letter-spacing:.06em;text-transform:uppercase;padding:.6rem 1.25rem;border-radius:6px;border:2px solid #026766;color:#026766;text-decoration:none;transition:background .2s,color .2s;" onmouseover="this.style.background='#026766';this.style.color='#fff'" onmouseout="this.style.background='transparent';this.style.color='#026766'">&larr; Previous</a>`;
  }

  html += `<span style="font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:.85rem;color:#666;letter-spacing:.05em;">Page ${currentPage} of ${totalPages}</span>`;

  if (currentPage < totalPages) {
    html += `<a href="/${slug}?page=${currentPage + 1}" style="font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:.9rem;letter-spacing:.06em;text-transform:uppercase;padding:.6rem 1.25rem;border-radius:6px;border:2px solid #026766;color:#026766;text-decoration:none;transition:background .2s,color .2s;" onmouseover="this.style.background='#026766';this.style.color='#fff'" onmouseout="this.style.background='transparent';this.style.color='#026766'">Next &rarr;</a>`;
  }

  html += '</div>';
  return html;
}

function buildCityJobsJsonLd(cityJobs, cityName, cityCoords, page, totalPages) {
  if (!cityJobs.length) return '';

  const schema = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "name": `Dryer Vent Cleaning Jobs Completed in ${cityName}${page > 1 ? ` - Page ${page}` : ''}`,
    "description": `Recent dryer vent cleaning and repair jobs completed by Dryer Vent Specialists in ${cityName}, California.`,
    "numberOfItems": cityJobs.length,
    "itemListElement": cityJobs.map((job, i) => {
      const coords = (job.lat && job.lng)
        ? { lat: job.lat, lng: job.lng }
        : cityCoords;

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
          "areaServed": {
            "@type": "City",
            "name": cityName,
            "containedInPlace": { "@type": "State", "name": "California" }
          }
        }
      };

      if (coords) {
        item.item.serviceLocation = {
          "@type": "Place",
          "geo": { "@type": "GeoCoordinates", "latitude": coords.lat, "longitude": coords.lng },
          "address": { "@type": "PostalAddress", "addressLocality": cityName, "addressRegion": "CA", "addressCountry": "US" }
        };
      }
      if (job.images && job.images.length) item.item.image = job.images.map(resolveImg);
      if (job.date) item.item.serviceOutput = { "@type": "CreativeWork", "dateCreated": job.date };
      if (job.property) item.item.additionalType = job.property;

      return item;
    })
  };

  return `\n  <script type="application/ld+json" id="city-jobs-jsonld">\n  ${JSON.stringify(schema, null, 2).split('\n').join('\n  ')}\n  </script>`;
}

module.exports = async function handler(req, res) {
  try {
    const urlPath = req.url.split('?')[0].replace(/^\//, '').replace(/\/$/, '');
    const cityInfo = CITY_MAP[urlPath];
    if (!cityInfo) return res.status(404).send('City page not found');

    // Parse page number
    const urlParams = new URL(req.url, 'https://x.com').searchParams;
    const page = Math.max(1, parseInt(urlParams.get('page') || '1', 10));

    const templateFile = urlPath + '-template.html';
    const templatePath = path.join(__dirname, '..', templateFile);
    if (!fs.existsSync(templatePath)) return res.status(404).send('Template not found');

    let html = fs.readFileSync(templatePath, 'utf8');

    // Fetch ALL jobs for this city (not paginated at fetch level)
    let allCityJobs = [];
    try {
      const PAT = process.env.GITHUB_PAT;
      const headers = { Accept: 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28' };
      if (PAT) headers.Authorization = `Bearer ${PAT}`;

      const ghRes = await fetch(`https://api.github.com/repos/${OWNER}/${REPO}/contents/jobs.json`, { headers });
      if (ghRes.ok) {
        const data = await ghRes.json();
        const allJobs = JSON.parse(Buffer.from(data.content.replace(/\n/g, ''), 'base64').toString('utf8'));
        allCityJobs = allJobs
          .filter(j => j.city === cityInfo.city && j.images && j.images.length)
          .sort((a, b) => new Date(b.createdAt || 0) - new Date(a.createdAt || 0));
      }
    } catch (e) {
      console.error('[city-page] Failed to fetch jobs:', e.message);
    }

    // Paginate
    const totalPages = Math.max(1, Math.ceil(allCityJobs.length / JOBS_PER_PAGE));
    const safePage = Math.min(page, totalPages);
    const startIdx = (safePage - 1) * JOBS_PER_PAGE;
    const pageJobs = allCityJobs.slice(startIdx, startIdx + JOBS_PER_PAGE);

    // 1. Inject JSON-LD into <head>
    if (pageJobs.length) {
      const jsonLd = buildCityJobsJsonLd(pageJobs, cityInfo.city, { lat: cityInfo.lat, lng: cityInfo.lng }, safePage, totalPages);
      html = html.replace('</head>', jsonLd + '\n</head>');
    }

    // 2. Pre-render job cards + pagination into the grid
    if (pageJobs.length) {
      const cardsHtml = pageJobs.map(buildJobCardHtml).join('');
      const paginationHtml = buildPaginationHtml(urlPath, safePage, totalPages);

      // Update the section heading to show total count
      const countLabel = allCityJobs.length > JOBS_PER_PAGE
        ? ` (${startIdx + 1}-${Math.min(startIdx + JOBS_PER_PAGE, allCityJobs.length)} of ${allCityJobs.length})`
        : '';

      html = html.replace(
        '<div id="city-work-grid" class="grid sm:grid-cols-2 md:grid-cols-3 gap-6 fade-in"></div>',
        `<div id="city-work-grid" class="grid sm:grid-cols-2 md:grid-cols-3 gap-6 fade-in">${cardsHtml}</div>${paginationHtml}`
      );

      html = html.replace(
        'id="city-recent-work" class="py-16 px-5" style="background:#fff; display:none;"',
        'id="city-recent-work" class="py-16 px-5" style="background:#fff;"'
      );

      // Show map section if there are GPS jobs
      const gpsJobs = allCityJobs.filter(j => j.lat && j.lng);
      if (gpsJobs.length) {
        html = html.replace(
          'id="city-job-map" class="py-16 px-5" style="background:var(--gray-lt); display:none;"',
          'id="city-job-map" class="py-16 px-5" style="background:var(--gray-lt);"'
        );
      }
    }

    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.setHeader('Cache-Control', 'public, s-maxage=300, stale-while-revalidate=60');
    return res.status(200).send(html);
  } catch (err) {
    console.error('[city-page] Error:', err.message);
    return res.status(500).send('Internal Server Error');
  }
};

module.exports.config = { maxDuration: 10 };
