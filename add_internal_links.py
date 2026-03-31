#!/usr/bin/env python3
"""Add internal linking between city pages:
1. 'Nearby Service Areas' section between CTA and Footer
2. Contextual links in FAQ answers
"""
import re

# Geographic neighbor map: each city -> 5 nearest cities (ordered by proximity)
# Plus approximate driving minutes for display
NEIGHBORS = {
    'San Mateo': [
        ('Burlingame', 5), ('Belmont', 5), ('Hillsborough', 5),
        ('San Carlos', 8), ('South San Francisco', 10),
    ],
    'San Francisco': [
        ('South San Francisco', 10), ('Burlingame', 18),
        ('San Mateo', 20), ('Hillsborough', 20), ('Half Moon Bay', 35),
    ],
    'South San Francisco': [
        ('San Francisco', 10), ('Burlingame', 8), ('San Mateo', 12),
        ('Hillsborough', 10), ('Belmont', 15),
    ],
    'Burlingame': [
        ('San Mateo', 5), ('Hillsborough', 3), ('South San Francisco', 8),
        ('Belmont', 10), ('San Carlos', 12),
    ],
    'Hillsborough': [
        ('Burlingame', 3), ('San Mateo', 5), ('Belmont', 7),
        ('South San Francisco', 10), ('San Carlos', 10),
    ],
    'Belmont': [
        ('San Carlos', 5), ('San Mateo', 5), ('Hillsborough', 7),
        ('Redwood City', 8), ('Burlingame', 10),
    ],
    'San Carlos': [
        ('Belmont', 5), ('Redwood City', 5), ('San Mateo', 8),
        ('Menlo Park', 10), ('Hillsborough', 10),
    ],
    'Redwood City': [
        ('San Carlos', 5), ('Menlo Park', 8), ('Belmont', 8),
        ('Palo Alto', 12), ('Half Moon Bay', 20),
    ],
    'Menlo Park': [
        ('Redwood City', 8), ('Palo Alto', 5), ('San Carlos', 10),
        ('Los Altos', 12), ('Belmont', 15),
    ],
    'Palo Alto': [
        ('Menlo Park', 5), ('Los Altos', 5), ('Mountain View', 8),
        ('Redwood City', 12), ('Sunnyvale', 12),
    ],
    'Los Altos': [
        ('Palo Alto', 5), ('Mountain View', 5), ('Sunnyvale', 8),
        ('Menlo Park', 12), ('Santa Clara', 12),
    ],
    'Mountain View': [
        ('Los Altos', 5), ('Palo Alto', 8), ('Sunnyvale', 5),
        ('Santa Clara', 10), ('Menlo Park', 12),
    ],
    'Sunnyvale': [
        ('Mountain View', 5), ('Santa Clara', 5), ('Los Altos', 8),
        ('San Jose', 10), ('Palo Alto', 12),
    ],
    'Santa Clara': [
        ('Sunnyvale', 5), ('San Jose', 8), ('Mountain View', 10),
        ('Los Altos', 12), ('Palo Alto', 15),
    ],
    'San Jose': [
        ('Santa Clara', 8), ('Sunnyvale', 10), ('Mountain View', 15),
        ('Los Altos', 18), ('Palo Alto', 20),
    ],
    'Half Moon Bay': [
        ('San Mateo', 25), ('Belmont', 25), ('Redwood City', 20),
        ('San Carlos', 25), ('Burlingame', 28),
    ],
}

CITY_TO_SLUG = {
    'San Mateo': 'dryer-vent-cleaning-san-mateo',
    'San Francisco': 'dryer-vent-cleaning-san-francisco',
    'South San Francisco': 'dryer-vent-cleaning-south-san-francisco',
    'Burlingame': 'dryer-vent-cleaning-burlingame',
    'Hillsborough': 'dryer-vent-cleaning-hillsborough',
    'Belmont': 'dryer-vent-cleaning-belmont',
    'San Carlos': 'dryer-vent-cleaning-san-carlos',
    'Redwood City': 'dryer-vent-cleaning-redwood-city',
    'Menlo Park': 'dryer-vent-cleaning-menlo-park',
    'Palo Alto': 'dryer-vent-cleaning-palo-alto',
    'Los Altos': 'dryer-vent-cleaning-los-altos',
    'Mountain View': 'dryer-vent-cleaning-mountain-view',
    'Sunnyvale': 'dryer-vent-cleaning-sunnyvale',
    'Santa Clara': 'dryer-vent-cleaning-santa-clara',
    'San Jose': 'dryer-vent-cleaning-san-jose',
    'Half Moon Bay': 'dryer-vent-cleaning-half-moon-bay',
}

# Regional cluster labels
CLUSTERS = {
    'San Francisco': 'North Peninsula',
    'South San Francisco': 'North Peninsula',
    'Burlingame': 'North Peninsula',
    'Hillsborough': 'North Peninsula',
    'San Mateo': 'Central Peninsula',
    'Belmont': 'Central Peninsula',
    'San Carlos': 'Central Peninsula',
    'Redwood City': 'Central Peninsula',
    'Half Moon Bay': 'Coastside',
    'Menlo Park': 'South Peninsula',
    'Palo Alto': 'South Peninsula',
    'Los Altos': 'South Peninsula',
    'Mountain View': 'South Peninsula',
    'Sunnyvale': 'South Bay',
    'Santa Clara': 'South Bay',
    'San Jose': 'South Bay',
}


def build_nearby_section(city, neighbors):
    """Build the 'Nearby Service Areas' HTML section."""
    cards = []
    for neighbor_city, minutes in neighbors:
        slug = CITY_TO_SLUG[neighbor_city]
        cluster = CLUSTERS[neighbor_city]
        cards.append(f'''      <a href="/{slug}" class="block" style="background:#fff;border-radius:12px;padding:1.25rem 1.5rem;text-decoration:none;border:1px solid rgba(2,103,102,.1);transition:transform .2s,box-shadow .2s;" onmouseover="this.style.transform='translateY(-3px)';this.style.boxShadow='0 8px 24px rgba(2,103,102,.12)'" onmouseout="this.style.transform='';this.style.boxShadow=''">
        <div class="font-display font-800 text-lg" style="color:var(--teal-dark);margin-bottom:.25rem;">{neighbor_city}</div>
        <div style="font-size:.8rem;color:#888;">~{minutes} min from {city} &middot; {cluster}</div>
      </a>''')

    cards_html = '\n'.join(cards)

    return f'''
<!-- NEARBY SERVICE AREAS -->
<section class="py-16 px-5" style="background:var(--gray-lt);">
  <div class="max-w-5xl mx-auto">
    <div class="text-center mb-10 fade-in">
      <p class="font-display font-700 text-sm uppercase tracking-widest mb-2" style="color:var(--orange);">Also Serving Nearby</p>
      <h2 class="font-display font-900 text-4xl" style="color:var(--teal-dark);letter-spacing:-.02em;">Dryer Vent Cleaning Near {city}</h2>
      <p class="text-gray-500 mt-3" style="max-width:520px;margin:0 auto;line-height:1.7;">We provide the same CDET-certified service across the Bay Area Peninsula. Click a city to learn more about our service in your area.</p>
    </div>
    <div class="grid sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 fade-in">
{cards_html}
    </div>
    <div class="text-center mt-8">
      <a href="/dryer-vent-cleaning-san-mateo" class="font-display font-700 text-sm uppercase tracking-widest" style="color:var(--teal-dark);text-decoration:none;letter-spacing:.08em;">View All 16 Service Areas &rarr;</a>
    </div>
  </div>
</section>
'''


# Contextual FAQ links: for each city, define 2-3 links to weave into FAQ answers
# Format: (search_text, replacement_with_link)
FAQ_LINKS = {
    'San Mateo': [
        ('our San Mateo headquarters', 'our San Mateo headquarters'),  # already on SM page, skip
        ('Burlingame', '<a href="/dryer-vent-cleaning-burlingame" style="color:var(--teal-dark);text-decoration:underline;">Burlingame</a>'),
    ],
    'Belmont': [
        ('San Mateo headquarters', '<a href="/dryer-vent-cleaning-san-mateo" style="color:var(--teal-dark);text-decoration:underline;">San Mateo</a> headquarters'),
        ('San Carlos', '<a href="/dryer-vent-cleaning-san-carlos" style="color:var(--teal-dark);text-decoration:underline;">San Carlos</a>'),
    ],
    'San Carlos': [
        ('San Mateo', None),  # skip - too many references
        ('Redwood City', '<a href="/dryer-vent-cleaning-redwood-city" style="color:var(--teal-dark);text-decoration:underline;">Redwood City</a>'),
        ('Belmont', '<a href="/dryer-vent-cleaning-belmont" style="color:var(--teal-dark);text-decoration:underline;">Belmont</a>'),
    ],
    'Burlingame': [
        ('San Mateo headquarters', '<a href="/dryer-vent-cleaning-san-mateo" style="color:var(--teal-dark);text-decoration:underline;">San Mateo</a> headquarters'),
        ('Hillsborough', '<a href="/dryer-vent-cleaning-hillsborough" style="color:var(--teal-dark);text-decoration:underline;">Hillsborough</a>'),
    ],
    'Hillsborough': [
        ('San Mateo', '<a href="/dryer-vent-cleaning-san-mateo" style="color:var(--teal-dark);text-decoration:underline;">San Mateo</a>'),
        ('Burlingame', '<a href="/dryer-vent-cleaning-burlingame" style="color:var(--teal-dark);text-decoration:underline;">Burlingame</a>'),
    ],
    'Redwood City': [
        ('San Carlos', '<a href="/dryer-vent-cleaning-san-carlos" style="color:var(--teal-dark);text-decoration:underline;">San Carlos</a>'),
        ('Menlo Park', '<a href="/dryer-vent-cleaning-menlo-park" style="color:var(--teal-dark);text-decoration:underline;">Menlo Park</a>'),
    ],
    'Menlo Park': [
        ('Palo Alto', '<a href="/dryer-vent-cleaning-palo-alto" style="color:var(--teal-dark);text-decoration:underline;">Palo Alto</a>'),
        ('Redwood City', '<a href="/dryer-vent-cleaning-redwood-city" style="color:var(--teal-dark);text-decoration:underline;">Redwood City</a>'),
    ],
    'Palo Alto': [
        ('Menlo Park', '<a href="/dryer-vent-cleaning-menlo-park" style="color:var(--teal-dark);text-decoration:underline;">Menlo Park</a>'),
        ('Mountain View', '<a href="/dryer-vent-cleaning-mountain-view" style="color:var(--teal-dark);text-decoration:underline;">Mountain View</a>'),
    ],
    'Los Altos': [
        ('Palo Alto', '<a href="/dryer-vent-cleaning-palo-alto" style="color:var(--teal-dark);text-decoration:underline;">Palo Alto</a>'),
        ('Mountain View', '<a href="/dryer-vent-cleaning-mountain-view" style="color:var(--teal-dark);text-decoration:underline;">Mountain View</a>'),
    ],
    'Mountain View': [
        ('Sunnyvale', '<a href="/dryer-vent-cleaning-sunnyvale" style="color:var(--teal-dark);text-decoration:underline;">Sunnyvale</a>'),
        ('Palo Alto', '<a href="/dryer-vent-cleaning-palo-alto" style="color:var(--teal-dark);text-decoration:underline;">Palo Alto</a>'),
    ],
    'Sunnyvale': [
        ('Mountain View', '<a href="/dryer-vent-cleaning-mountain-view" style="color:var(--teal-dark);text-decoration:underline;">Mountain View</a>'),
        ('Santa Clara', '<a href="/dryer-vent-cleaning-santa-clara" style="color:var(--teal-dark);text-decoration:underline;">Santa Clara</a>'),
    ],
    'Santa Clara': [
        ('Sunnyvale', '<a href="/dryer-vent-cleaning-sunnyvale" style="color:var(--teal-dark);text-decoration:underline;">Sunnyvale</a>'),
        ('San Jose', '<a href="/dryer-vent-cleaning-san-jose" style="color:var(--teal-dark);text-decoration:underline;">San Jose</a>'),
    ],
    'San Jose': [
        ('Santa Clara', '<a href="/dryer-vent-cleaning-santa-clara" style="color:var(--teal-dark);text-decoration:underline;">Santa Clara</a>'),
        ('Sunnyvale', '<a href="/dryer-vent-cleaning-sunnyvale" style="color:var(--teal-dark);text-decoration:underline;">Sunnyvale</a>'),
    ],
    'San Francisco': [
        ('South San Francisco', '<a href="/dryer-vent-cleaning-south-san-francisco" style="color:var(--teal-dark);text-decoration:underline;">South San Francisco</a>'),
        ('San Mateo', '<a href="/dryer-vent-cleaning-san-mateo" style="color:var(--teal-dark);text-decoration:underline;">San Mateo</a>'),
    ],
    'South San Francisco': [
        ('San Francisco', '<a href="/dryer-vent-cleaning-san-francisco" style="color:var(--teal-dark);text-decoration:underline;">San Francisco</a>'),
        ('San Mateo headquarters', '<a href="/dryer-vent-cleaning-san-mateo" style="color:var(--teal-dark);text-decoration:underline;">San Mateo</a> headquarters'),
    ],
    'Half Moon Bay': [
        ('San Mateo', '<a href="/dryer-vent-cleaning-san-mateo" style="color:var(--teal-dark);text-decoration:underline;">San Mateo</a>'),
        ('Redwood City', '<a href="/dryer-vent-cleaning-redwood-city" style="color:var(--teal-dark);text-decoration:underline;">Redwood City</a>'),
    ],
}


updated = []

for city, neighbors in NEIGHBORS.items():
    slug = CITY_TO_SLUG[city]
    filename = f'{slug}-template.html'

    try:
        with open(filename, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"  SKIP: {filename} not found")
        continue

    original = content

    # 1. Insert 'Nearby Service Areas' section between CTA and FOOTER
    nearby_html = build_nearby_section(city, neighbors)

    # Check if already added (idempotent)
    if '<!-- NEARBY SERVICE AREAS -->' not in content:
        # Insert before <!-- FOOTER -->
        footer_marker = '<!-- FOOTER -->'
        if footer_marker in content:
            content = content.replace(footer_marker, nearby_html + '\n' + footer_marker)
            print(f"  {filename}: Added Nearby Service Areas section")
        else:
            # Try alternate: before <footer
            footer_alt = '<footer'
            idx = content.find(footer_alt)
            if idx > 0:
                content = content[:idx] + nearby_html + '\n' + content[idx:]
                print(f"  {filename}: Added Nearby section (alt marker)")
            else:
                print(f"  {filename}: WARNING - no footer marker found")

    # 2. Add contextual links in FAQ answers (only within faq-body divs)
    if city in FAQ_LINKS:
        for search_text, replacement in FAQ_LINKS[city]:
            if replacement is None:
                continue
            # Only replace inside faq-body divs, and only first occurrence
            # to avoid over-linking
            faq_body_pattern = r'(<div class="faq-body">)(.*?)(</div></details>)'

            def replace_in_faq(match):
                prefix = match.group(1)
                body = match.group(2)
                suffix = match.group(3)
                # Only replace if the text exists and isn't already a link
                if search_text in body and f'>{search_text}</a>' not in body:
                    body = body.replace(search_text, replacement, 1)
                return prefix + body + suffix

            new_content = re.sub(faq_body_pattern, replace_in_faq, content, count=1, flags=re.DOTALL)
            if new_content != content:
                content = new_content

        if content != original:
            print(f"  {filename}: Added contextual FAQ links")

    if content != original:
        with open(filename, 'w') as f:
            f.write(content)
        updated.append(filename)

print(f"\nUpdated {len(updated)} of {len(NEIGHBORS)} city pages")
