#!/usr/bin/env python3
"""Replace 'How It Works' section on all city pages with card-based layout."""

import os
import re

city_data = {
    "san-mateo": "San Mateo",
    "burlingame": "Burlingame",
    "hillsborough": "Hillsborough",
    "belmont": "Belmont",
    "san-carlos": "San Carlos",
    "redwood-city": "Redwood City",
    "menlo-park": "Menlo Park",
    "half-moon-bay": "Half Moon Bay",
    "san-francisco": "San Francisco",
    "south-san-francisco": "South San Francisco",
    "los-altos": "Los Altos",
}


def build_how_it_works(city):
    return f'''<!-- ── HOW IT WORKS ── -->
<section id="how-it-works" class="py-20 px-5" style="background:#fff;">
  <div class="max-w-5xl mx-auto">
    <div class="mb-12 fade-in">
      <p class="font-display font-700 text-sm uppercase tracking-widest mb-2" style="color:var(--orange);">Simple Process</p>
      <h2 class="font-display font-900 text-4xl mb-4" style="color:var(--teal-dark); letter-spacing:-.02em;">How It Works</h2>
      <p class="text-gray-500" style="line-height:1.7; max-width:48rem;">From booking to completion, most {city} appointments take under an hour. Here&rsquo;s what to expect.</p>
    </div>
    <div class="grid md:grid-cols-3 gap-6 fade-in">

      <div style="background:var(--gray-lt); border-radius:14px; padding:1.75rem; border-left:4px solid var(--teal-light); position:relative;">
        <div class="font-display font-900 text-3xl mb-3" style="color:var(--teal-light); opacity:.5;">01</div>
        <h3 class="font-display font-800 text-lg mb-2" style="color:var(--teal-dark);">Book Online or Call</h3>
        <p class="text-gray-500 text-sm" style="line-height:1.7;">Pick a time at <a href="/book" style="color:var(--orange); text-decoration:none; font-weight:700;">dvspecialists.com/book</a> or call <a href="tel:+16504844418" style="color:var(--orange); text-decoration:none; font-weight:700;">(650) 484-4418</a>. Same-day and next-day appointments in {city} are often available, Monday through Saturday.</p>
      </div>

      <div style="background:var(--gray-lt); border-radius:14px; padding:1.75rem; border-left:4px solid var(--teal-light); position:relative;">
        <div class="font-display font-900 text-3xl mb-3" style="color:var(--teal-light); opacity:.5;">02</div>
        <h3 class="font-display font-800 text-lg mb-2" style="color:var(--teal-dark);">We Clean &amp; Inspect</h3>
        <p class="text-gray-500 text-sm" style="line-height:1.7;">A CDET-certified technician arrives on time with professional rotary brush and HEPA-filtered vacuum equipment. We clean the dryer, transition hose, and full vent run — then test airflow and inspect for damage or code violations.</p>
      </div>

      <div style="background:var(--gray-lt); border-radius:14px; padding:1.75rem; border-left:4px solid var(--teal-light); position:relative;">
        <div class="font-display font-900 text-3xl mb-3" style="color:var(--teal-light); opacity:.5;">03</div>
        <h3 class="font-display font-800 text-lg mb-2" style="color:var(--teal-dark);">Get Your Report</h3>
        <p class="text-gray-500 text-sm" style="line-height:1.7;">You receive a written condition report with before-and-after airflow measurements, photos, and any recommendations. Useful for HOA compliance, home sale disclosures, insurance records, and landlord documentation.</p>
      </div>

    </div>
  </div>
</section>'''


def process_file(filepath, slug):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    city = city_data[slug]
    new_section = build_how_it_works(city)

    # Match both comment formats and the full section up to the next section
    # Pattern 1: <!-- ── HOW IT WORKS ── -->
    # Pattern 2: <!-- HOW IT WORKS -->
    pattern = re.compile(
        r'<!-- (?:── )?HOW IT WORKS(?: ──)? -->\s*<section id="how-it-works".*?</section>',
        re.DOTALL
    )

    if pattern.search(content):
        content = pattern.sub(new_section, content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  DONE: {filepath}")
        return True
    else:
        print(f"  NO MATCH: {filepath}")
        return False


def main():
    base_dir = '/Users/michaelredman/Documents/GitHub/dvspecialists'
    for slug in city_data:
        filepath = os.path.join(base_dir, f'dryer-vent-cleaning-{slug}.html')
        if os.path.exists(filepath):
            process_file(filepath, slug)
        else:
            print(f"  NOT FOUND: {filepath}")


if __name__ == '__main__':
    main()
