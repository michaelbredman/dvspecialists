#!/usr/bin/env python3
"""Upgrade JSON-LD structured data on all 16 city pages."""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CITY_PAGES = {
    "dryer-vent-cleaning-san-mateo.html": ("San Mateo", "San_Mateo,_California"),
    "dryer-vent-cleaning-san-francisco.html": ("San Francisco", "San_Francisco"),
    "dryer-vent-cleaning-south-san-francisco.html": ("South San Francisco", "South_San_Francisco,_California"),
    "dryer-vent-cleaning-san-carlos.html": ("San Carlos", "San_Carlos,_California"),
    "dryer-vent-cleaning-burlingame.html": ("Burlingame", "Burlingame,_California"),
    "dryer-vent-cleaning-hillsborough.html": ("Hillsborough", "Hillsborough,_California"),
    "dryer-vent-cleaning-belmont.html": ("Belmont", "Belmont,_California"),
    "dryer-vent-cleaning-redwood-city.html": ("Redwood City", "Redwood_City,_California"),
    "dryer-vent-cleaning-menlo-park.html": ("Menlo Park", "Menlo_Park,_California"),
    "dryer-vent-cleaning-los-altos.html": ("Los Altos", "Los_Altos,_California"),
    "dryer-vent-cleaning-half-moon-bay.html": ("Half Moon Bay", "Half_Moon_Bay,_California"),
    "dryer-vent-cleaning-palo-alto.html": ("Palo Alto", "Palo_Alto,_California"),
    "dryer-vent-cleaning-mountain-view.html": ("Mountain View", "Mountain_View,_California"),
    "dryer-vent-cleaning-sunnyvale.html": ("Sunnyvale", "Sunnyvale,_California"),
    "dryer-vent-cleaning-santa-clara.html": ("Santa Clara", "Santa_Clara,_California"),
    "dryer-vent-cleaning-san-jose.html": ("San Jose", "San_Jose,_California"),
}


def make_howto_block(city_name):
    return f'''  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "HowTo",
    "name": "How to Get Your Dryer Vent Cleaned in {city_name}, CA",
    "description": "Step-by-step process for scheduling professional dryer vent cleaning in {city_name}, California.",
    "step": [
      {{
        "@type": "HowToStep",
        "position": 1,
        "name": "Recognize the Warning Signs",
        "text": "Look for clothes taking longer to dry, excessive heat from the dryer, burning smells, or the exterior vent flap not opening during cycles."
      }},
      {{
        "@type": "HowToStep",
        "position": 2,
        "name": "Schedule a Professional Cleaning",
        "text": "Contact Dryer Vent Specialists at (650) 484-4418 or book online. Same-day and next-day appointments are available in {city_name}."
      }},
      {{
        "@type": "HowToStep",
        "position": 3,
        "name": "Professional Inspection and Cleaning",
        "text": "A CDET-certified technician disconnects the dryer, uses commercial-grade rotary brush and vacuum equipment to clean the entire vent from dryer to exterior termination, and inspects for damage or code violations."
      }},
      {{
        "@type": "HowToStep",
        "position": 4,
        "name": "Verify Airflow and Review Results",
        "text": "The technician tests airflow to confirm the vent is fully clear, provides before-and-after photos, and recommends a maintenance schedule based on your household and vent configuration."
      }}
    ],
    "totalTime": "PT45M",
    "estimatedCost": {{
      "@type": "MonetaryAmount",
      "currency": "USD",
      "value": "149-249"
    }}
  }}
  </script>'''


def upgrade_file(filename, city_name, wiki_slug):
    filepath = os.path.join(BASE_DIR, filename)
    if not os.path.exists(filepath):
        print(f"  SKIP - file not found: {filename}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = []

    # 1. Add ProfessionalService to @type array
    old_type = '"@type": ["LocalBusiness", "HomeAndConstructionBusiness"]'
    new_type = '"@type": ["LocalBusiness", "HomeAndConstructionBusiness", "ProfessionalService"]'
    if old_type in content:
        content = content.replace(old_type, new_type)
        changes.append("Added ProfessionalService to @type")
    elif new_type in content:
        changes.append("ProfessionalService already present")
    else:
        print(f"  WARNING - @type pattern not found in {filename}")

    # 2. Upgrade areaServed to include containedInPlace
    # Handle both multi-line and single-line formats
    wiki_url = f"https://en.wikipedia.org/wiki/{wiki_slug}"

    # Single-line format
    old_area_single = f'"areaServed": {{ "@type": "City", "name": "{city_name}", "sameAs": "{wiki_url}" }}'
    new_area_single = (
        f'"areaServed": {{ "@type": "City", "name": "{city_name}", "sameAs": "{wiki_url}", '
        f'"containedInPlace": {{ "@type": "State", "name": "California", "sameAs": "https://en.wikipedia.org/wiki/California" }} }}'
    )

    # Multi-line format: find the sameAs line and closing brace
    old_area_multi = f'      "sameAs": "{wiki_url}"\n    }}'
    new_area_multi = (
        f'      "sameAs": "{wiki_url}",\n'
        f'      "containedInPlace": {{\n'
        f'        "@type": "State",\n'
        f'        "name": "California",\n'
        f'        "sameAs": "https://en.wikipedia.org/wiki/California"\n'
        f'      }}\n'
        f'    }}'
    )

    if old_area_single in content:
        content = content.replace(old_area_single, new_area_single)
        changes.append("Added containedInPlace to areaServed (single-line)")
    elif old_area_multi in content:
        content = content.replace(old_area_multi, new_area_multi)
        changes.append("Added containedInPlace to areaServed (multi-line)")
    elif "containedInPlace" in content:
        changes.append("containedInPlace already present")
    else:
        print(f"  WARNING - areaServed pattern not found in {filename}")

    # 3. Add availability and priceSpecification to Offer items
    # First offer (Dryer Vent Cleaning) - gets price info
    old_first_offer = '{ "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Dryer Vent Cleaning"'
    new_first_offer = '{ "@type": "Offer", "availability": "https://schema.org/InStock", "priceSpecification": { "@type": "PriceSpecification", "priceCurrency": "USD", "price": "149.00", "minPrice": "149.00", "maxPrice": "249.00", "description": "Flat-rate pricing, no hidden fees" }, "itemOffered": { "@type": "Service", "name": "Dryer Vent Cleaning"'

    if old_first_offer in content and '"availability"' not in content.split('"Dryer Vent Cleaning"')[0].split('"Offer"')[-1]:
        content = content.replace(old_first_offer, new_first_offer, 1)
        changes.append("Added availability + priceSpecification to first Offer")
    elif "priceSpecification" in content:
        changes.append("priceSpecification already present")
    else:
        print(f"  WARNING - first Offer pattern not found in {filename}")

    # Second offer (Repair & Replacement) - just availability
    old_second_offer = '{ "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Dryer Vent Repair & Replacement"'
    new_second_offer = '{ "@type": "Offer", "availability": "https://schema.org/InStock", "itemOffered": { "@type": "Service", "name": "Dryer Vent Repair & Replacement"'

    if old_second_offer in content:
        content = content.replace(old_second_offer, new_second_offer, 1)
        changes.append("Added availability to Repair offer")

    # Third offer (Installation) - just availability
    old_third_offer = '{ "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Dryer Vent Installation"'
    new_third_offer = '{ "@type": "Offer", "availability": "https://schema.org/InStock", "itemOffered": { "@type": "Service", "name": "Dryer Vent Installation"'

    if old_third_offer in content:
        content = content.replace(old_third_offer, new_third_offer, 1)
        changes.append("Added availability to Installation offer")

    # 4. Add HowTo JSON-LD block before </head>
    if '"@type": "HowTo"' not in content:
        howto_block = make_howto_block(city_name)
        content = content.replace('  </head>', howto_block + '\n  </head>')
        changes.append("Added HowTo JSON-LD block")
    else:
        changes.append("HowTo block already present")

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  OK - {filename}: {', '.join(changes)}")
        return True
    else:
        print(f"  NO CHANGES - {filename}: {', '.join(changes)}")
        return False


def main():
    print("Upgrading JSON-LD schemas on 16 city pages...\n")
    updated = 0
    for filename, (city_name, wiki_slug) in CITY_PAGES.items():
        if upgrade_file(filename, city_name, wiki_slug):
            updated += 1
    print(f"\nDone. Updated {updated} of {len(CITY_PAGES)} files.")


if __name__ == "__main__":
    main()
