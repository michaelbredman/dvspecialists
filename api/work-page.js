/* ─────────────────────────────────────────────────────────────
   /api/work-page — SSR wrapper for the Our Work map page.
   Reads work-template.html, fetches jobs from GitHub,
   and injects JSON-LD schema so structured data appears
   in View Source for crawlers. The map renders client-side.
───────────────────────────────────────────────────────────── */

const fs   = require('fs');
const path = require('path');

const OWNER  = 'michaelbredman';
const REPO   = 'dvspecialists';
const BRANCH = 'main';
const GITHUB_RAW = `https://raw.githubusercontent.com/${OWNER}/${REPO}/${BRANCH}`;

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

module.exports = async (req, res) => {
  try {
    // Read template
    const tplPath = path.join(process.cwd(), 'work-template.html');
    let html = fs.readFileSync(tplPath, 'utf8');

    // Fetch jobs from GitHub
    let allJobs = [];
    try {
      const resp = await fetch(`https://api.github.com/repos/${OWNER}/${REPO}/contents/jobs.json?ref=${BRANCH}`, {
        headers: { 'Accept': 'application/vnd.github.v3+json', 'User-Agent': 'dvspecialists-ssr' }
      });
      if (resp.ok) {
        const data = await resp.json();
        allJobs = JSON.parse(Buffer.from(data.content.replace(/\n/g, ''), 'base64').toString('utf8'));
        allJobs.sort((a, b) => new Date(b.date) - new Date(a.date));
      }
    } catch (e) {
      console.error('[work-page] GitHub fetch error:', e.message);
    }

    // Inject JSON-LD into <head> for crawlers
    if (allJobs.length) {
      const schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Completed Dryer Vent Cleaning Jobs",
        "description": "Browse real completed dryer vent cleaning and repair jobs by Dryer Vent Specialists across the San Francisco Bay Area.",
        "numberOfItems": allJobs.length,
        "itemListElement": allJobs.map((job, i) => {
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

    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.setHeader('Cache-Control', 'public, s-maxage=300, stale-while-revalidate=60');
    return res.status(200).send(html);
  } catch (err) {
    console.error('[work-page] Error:', err.message);
    return res.status(500).send('Internal Server Error');
  }
};

module.exports.config = { maxDuration: 10 };
