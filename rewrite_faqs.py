#!/usr/bin/env python3
"""Rewrite duplicate FAQs with unique, city-specific content for 8 cities."""
import re, json

# Each city gets 6 unique questions with localized answers.
# Questions vary in topic to avoid templated patterns.

CITY_FAQS = {
    'dryer-vent-cleaning-belmont-template.html': {
        'city': 'Belmont',
        'heading': 'Belmont Dryer Vent Cleaning FAQ',
        'faqs': [
            {
                'q': 'How often should Belmont homeowners schedule dryer vent cleaning?',
                'a': 'The NFPA recommends annual professional dryer vent cleaning. Many Belmont homes in Cipriani, Sterling Downs, and the Belmont Hills were built in the 1950s through 1970s with dryer vents routed through crawl spaces or up to rooftop exits. These longer runs collect lint faster than modern installations. If your household has four or more people, pets that shed, or a vent run exceeding 25 feet, every six months is safer.'
            },
            {
                'q': 'Why do hillside homes in Belmont have more dryer vent problems?',
                'a': 'Belmont sits along the eastern slopes of the Santa Cruz Mountains, and many homes in Belmont Hills, Plateau-Skymont, and Western Hills are built on steep grades. This means dryer vents often run at angles through foundations or upward to roof exits, creating extra bends where lint accumulates. Gravity also works against airflow in uphill vent runs. Our CDET-certified technicians use rotary brush systems designed for these complex configurations.'
            },
            {
                'q': 'What does dryer vent cleaning cost in Belmont?',
                'a': 'Residential dryer vent cleaning in Belmont ranges from $149 to $249 per vent. We use flat-rate pricing with no hidden fees. The final cost depends on vent length, number of bends, and whether your transition hose needs replacement with a UL 2158A-compliant duct. We include a post-cleaning airflow test and safety inspection with every service. Call (650) 484-4418 for your exact quote.'
            },
            {
                'q': 'Do you service dryer vents in Belmont condo complexes near Ralston Avenue?',
                'a': 'Yes. We clean dryer vents in single-family homes, townhomes, condos, and apartment buildings throughout Belmont, including multi-unit complexes along Ralston Avenue, near Carlmont Shopping Center, and in the Downtown Belmont area. Multi-unit properties often have shared or extended vent systems requiring specialized commercial equipment. HOAs and property managers with four or more units qualify for volume pricing.'
            },
            {
                'q': 'Can a clogged dryer vent cause mold in my Belmont home?',
                'a': 'Yes. When a dryer vent is blocked, hot, moisture-laden air is pushed back into your laundry area instead of being exhausted outside. In Belmont homes with limited ventilation, particularly older construction in Homeview and Belmont Woods, this trapped moisture can promote mold and mildew growth inside walls and around the dryer area. Professional vent cleaning restores proper airflow and eliminates this risk.'
            },
            {
                'q': 'Is same-day dryer vent cleaning available in Belmont?',
                'a': 'Yes. Belmont is minutes from our San Mateo headquarters, so same-day and next-day appointments are frequently available Monday through Saturday, 8 AM to 6 PM. Most residential cleanings take 45 to 60 minutes. Book at dvspecialists.com/book or call (650) 484-4418.'
            },
        ]
    },
    'dryer-vent-cleaning-palo-alto-template.html': {
        'city': 'Palo Alto',
        'heading': 'Palo Alto Dryer Vent Cleaning FAQ',
        'faqs': [
            {
                'q': 'How frequently should Palo Alto homes have dryer vents professionally cleaned?',
                'a': 'At least once per year, per NFPA guidelines. Palo Alto has a mix of housing stock, from pre-war Craftsman homes in Old Palo Alto and Crescent Park to mid-century ranches in Midtown and newer construction in Charleston Meadows. Older homes often have dryer vents routed through walls and attics with multiple elbows, which trap lint faster. Homes with four or more residents or pets should consider cleaning every six months.'
            },
            {
                'q': 'Are Palo Alto dryer vent configurations different from newer cities?',
                'a': 'Many are. Palo Alto was largely developed between the 1920s and 1960s, and neighborhoods like College Terrace, Evergreen Park, and Barron Park feature homes with dryer vents that were often retrofitted when gas and electric dryers replaced clotheslines. These retrofits frequently resulted in longer runs, extra bends, and non-standard terminations. Our technicians inspect the full vent path and recommend corrections to bring your system up to current safety standards.'
            },
            {
                'q': 'What is the cost of dryer vent cleaning in Palo Alto?',
                'a': 'Standard residential cleaning runs $149 to $249, depending on vent length, routing complexity, and whether the transition hose needs replacement. We use flat-rate pricing with no surprise charges. Every cleaning includes a rotary brush treatment, HEPA-filtered vacuum extraction, and a post-service airflow verification test. Call (650) 484-4418 for a quote specific to your Palo Alto home.'
            },
            {
                'q': 'Do you clean dryer vents in Palo Alto apartment buildings and multi-unit properties?',
                'a': 'Yes. We serve single-family homes, condos, townhomes, and apartment complexes across Palo Alto, including multi-unit buildings along El Camino Real, near California Avenue, and in the Downtown and University South areas. Shared vent systems in larger buildings require commercial-grade equipment and careful coordination. Property managers and HOAs with four or more units receive volume pricing.'
            },
            {
                'q': 'Why does my dryer take longer to dry clothes in my Palo Alto home?',
                'a': 'Extended drying times are the most common symptom of a clogged vent. In Palo Alto homes, especially those in Southgate and Gunn-Arastradero with longer vent runs through single-story slab construction, lint accumulates gradually and restricts airflow. A clogged vent forces the dryer to work harder, using up to 30% more energy per cycle. Professional cleaning restores airflow and typically cuts drying time in half.'
            },
            {
                'q': 'Can I book same-day dryer vent service in Palo Alto?',
                'a': 'Yes. We offer same-day and next-day appointments in Palo Alto, Monday through Saturday, 8 AM to 6 PM. Palo Alto is within our core Peninsula service area. Residential cleanings typically take 45 to 60 minutes. Schedule online at dvspecialists.com/book or call (650) 484-4418.'
            },
        ]
    },
    'dryer-vent-cleaning-san-jose-template.html': {
        'city': 'San Jose',
        'heading': 'San Jose Dryer Vent Cleaning FAQ',
        'faqs': [
            {
                'q': 'How often do San Jose homeowners need dryer vent cleaning?',
                'a': 'The NFPA recommends at least once per year. San Jose is a large city with diverse housing, from Victorian-era homes in Japantown and the Rose Garden to 1960s tract homes in Cambrian Park and modern developments in North San Jose. Older homes with longer vent runs or multiple bends should be cleaned more frequently. Households with heavy dryer usage, pets, or vent runs over 25 feet benefit from cleaning every six months.'
            },
            {
                'q': 'Does San Jose fire code require dryer vent cleaning?',
                'a': 'San Jose follows the California Fire Code, which requires property owners to maintain dryer exhaust systems in proper working condition. The San Jose Fire Department has specifically cited dryer lint buildup as a leading cause of residential fires. Multi-unit property owners and commercial laundry operators in San Jose are required to maintain documented cleaning schedules. For single-family homes, annual professional cleaning meets the standard of care.'
            },
            {
                'q': 'How much does dryer vent cleaning cost in San Jose?',
                'a': 'Residential dryer vent cleaning in San Jose costs $149 to $249 per vent. Price depends on vent length, number of elbows, and whether the flexible transition hose needs replacing with a UL 2158A-compliant duct. We offer flat-rate pricing with no hidden charges. Every service includes rotary brush cleaning, HEPA-filtered extraction, and a post-cleaning airflow test. Call (650) 484-4418 for your specific quote.'
            },
            {
                'q': 'Do you serve large apartment complexes in San Jose?',
                'a': 'Yes. We clean dryer vents in all property types across San Jose, from single-family homes in Willow Glen and Almaden Valley to high-density apartment and condo complexes in Downtown San Jose, Berryessa, and along the North First Street corridor. Multi-unit buildings with shared vent systems require commercial-grade equipment. We offer volume pricing and scheduled maintenance programs for property managers with four or more units.'
            },
            {
                'q': 'Why is dryer vent cleaning important in San Jose during fire season?',
                'a': 'San Jose and the greater Santa Clara Valley face elevated fire risk during the dry months from May through November. The San Jose Fire Department responds to dozens of dryer-related fires annually, many caused by lint buildup in exhaust systems. Homes in hillside areas like Silver Creek, Evergreen, and the East Foothills face compounded risk during red flag warnings. Professional vent cleaning removes the fuel source and is one of the simplest fire prevention steps a homeowner can take.'
            },
            {
                'q': 'Is same-day dryer vent cleaning available in San Jose?',
                'a': 'Yes. We offer same-day and next-day appointments throughout San Jose, Monday through Saturday, 8 AM to 6 PM. San Jose is within our expanded South Bay service area. Most residential cleanings take 45 to 60 minutes. Book online at dvspecialists.com/book or call (650) 484-4418.'
            },
        ]
    },
    'dryer-vent-cleaning-sunnyvale-template.html': {
        'city': 'Sunnyvale',
        'heading': 'Sunnyvale Dryer Vent Cleaning FAQ',
        'faqs': [
            {
                'q': 'How often should Sunnyvale residents clean their dryer vents?',
                'a': 'At minimum once per year, per NFPA recommendations. Sunnyvale has a large stock of 1950s and 1960s ranch-style homes in neighborhoods like Cherry Chase, Birdland, and Lakewood Village. These single-story homes typically have dryer vents running through crawl spaces or under slab foundations, where lint accumulates in hard-to-reach sections. Homes with four or more occupants or pets should schedule cleaning every six months.'
            },
            {
                'q': 'What makes Sunnyvale ranch homes prone to dryer vent issues?',
                'a': 'Sunnyvale was heavily developed during the post-war era, and the predominant single-story ranch homes in Ponderosa Park, Raynor Park, and Sunnyvale West often have dryer vents that run 15 to 30 feet through crawl spaces or slab-on-grade construction before reaching an exterior wall. These long horizontal runs with minimal slope create ideal conditions for lint accumulation. Our CDET-certified technicians use extended rotary brush systems specifically designed for these configurations.'
            },
            {
                'q': 'What does dryer vent cleaning cost in Sunnyvale?',
                'a': 'Standard residential cleaning in Sunnyvale runs $149 to $249 per vent. We use flat-rate pricing, so your quoted price is your final price. Cost varies by vent length, number of bends, and whether the transition hose needs replacement. Every cleaning includes a full rotary brush treatment, HEPA-filtered vacuum extraction, and airflow verification. Call (650) 484-4418 for a quote.'
            },
            {
                'q': 'Do you clean dryer vents in Sunnyvale townhome and condo developments?',
                'a': 'Yes. We service all property types across Sunnyvale, including single-family homes, townhomes, condos, and apartment complexes. Sunnyvale has significant multi-unit housing along Fair Oaks Avenue, El Camino Real, and in newer developments near the Heritage District and Downtown Sunnyvale. These properties often have stacked or shared vent systems that require commercial-grade cleaning equipment. Volume pricing is available for four or more units.'
            },
            {
                'q': 'Can a clogged dryer vent affect my home energy costs in Sunnyvale?',
                'a': 'Significantly. The U.S. Department of Energy estimates a restricted dryer vent can increase energy use by 30% or more per cycle. For a typical Sunnyvale household running four to five loads per week, that adds $15 to $25 monthly to your utility bill. With Sunnyvale electricity rates among the highest in the Bay Area, annual vent cleaning typically pays for itself in energy savings within a few months.'
            },
            {
                'q': 'How quickly can I get dryer vent cleaning in Sunnyvale?',
                'a': 'We offer same-day and next-day appointments in Sunnyvale, Monday through Saturday, 8 AM to 6 PM. Sunnyvale is a core part of our South Bay service area. Residential cleanings take 45 to 60 minutes. Schedule online at dvspecialists.com/book or call (650) 484-4418.'
            },
        ]
    },
    'dryer-vent-cleaning-santa-clara-template.html': {
        'city': 'Santa Clara',
        'heading': 'Santa Clara Dryer Vent Cleaning FAQ',
        'faqs': [
            {
                'q': 'How often should Santa Clara homeowners have dryer vents cleaned?',
                'a': 'The NFPA recommends annual professional cleaning. Santa Clara has a broad mix of housing, from early 20th-century bungalows in the Old Quad and Mission District neighborhoods to post-war tract homes in Central Park and newer construction in Rivermark and Montague. Older homes with longer vent runs through walls or attics need more frequent attention. Households with heavy usage or pets should consider every six months.'
            },
            {
                'q': 'Does the Santa Clara Fire Department recommend dryer vent cleaning?',
                'a': 'Yes. The Santa Clara Fire Department, like all California fire agencies, follows NFPA guidelines that identify dryer lint as a leading ignition source for residential fires. Santa Clara Fire has issued public advisories urging homeowners to have dryer exhaust systems professionally cleaned annually. Multi-unit property owners in Santa Clara are also required to maintain their dryer vent systems under the California Fire Code.'
            },
            {
                'q': 'How much does dryer vent cleaning cost in Santa Clara?',
                'a': 'Residential dryer vent cleaning in Santa Clara ranges from $149 to $249. We offer flat-rate pricing based on vent length, number of elbows, and whether your flexible transition duct needs replacement with a code-compliant UL 2158A duct. Every service includes rotary brush cleaning, HEPA-filtered vacuum extraction, airflow testing, and a written safety report. Call (650) 484-4418 for an exact quote.'
            },
            {
                'q': 'Do you clean dryer vents in Santa Clara apartment buildings near the university?',
                'a': 'Yes. We serve all property types in Santa Clara, including single-family homes, condos, townhomes, and apartment complexes. The University Neighborhood, Agnesi area, and Northside have significant multi-unit rental housing with shared or vertically stacked vent systems that require commercial-grade equipment. We work with property managers, HOAs, and landlords, and offer volume pricing for four or more units.'
            },
            {
                'q': 'What are common dryer vent problems in older Santa Clara neighborhoods?',
                'a': 'Homes in the Old Quad, Warburton, and Washington neighborhoods were built primarily in the 1940s through 1960s, often before modern dryer vent standards existed. Common issues include foil or vinyl flex duct (which is now prohibited by code), vents routed through walls with excessive bends, crushed ducts behind dryers pushed tight against walls, and missing or damaged exterior vent covers that allow pests to enter. Our inspection identifies and corrects all of these issues.'
            },
            {
                'q': 'Is same-day dryer vent cleaning available in Santa Clara?',
                'a': 'Yes. Santa Clara is within our core South Bay service area, and same-day and next-day appointments are frequently available Monday through Saturday, 8 AM to 6 PM. Most residential cleanings take 45 to 60 minutes. Book at dvspecialists.com/book or call (650) 484-4418.'
            },
        ]
    },
    'dryer-vent-cleaning-mountain-view-template.html': {
        'city': 'Mountain View',
        'heading': 'Mountain View Dryer Vent Cleaning FAQ',
        'faqs': [
            {
                'q': 'How often do Mountain View homes need dryer vent cleaning?',
                'a': 'At least annually, per NFPA guidelines. Mountain View has a wide range of housing stock, from 1940s bungalows in Old Mountain View and Rex Manor to 1960s ranch homes in Monta Loma and Waverly Park, plus newer townhome developments in North Whisman. Older homes with longer vent runs through attics or crawl spaces should be cleaned more frequently. Homes with pets or four or more occupants benefit from cleaning every six months.'
            },
            {
                'q': 'Why do homes near Shoreline in Mountain View have unique dryer vent challenges?',
                'a': 'Homes in Shoreline West, North Whisman, and the Gemello area are built on reclaimed marshland with slab-on-grade foundations. Dryer vents in these homes typically run horizontally under or through the slab to reach exterior walls, creating long runs with minimal slope. These horizontal configurations are especially prone to lint accumulation because gravity does not help move debris toward the exit. Our rotary brush system is designed to clear these long horizontal runs effectively.'
            },
            {
                'q': 'What is the price for dryer vent cleaning in Mountain View?',
                'a': 'Standard residential cleaning costs $149 to $249 per vent in Mountain View. We use flat-rate pricing with no hidden fees. Price depends on vent length, number of elbows, termination type (sidewall vs. roof), and whether the transition hose needs replacement. Every service includes rotary brush cleaning, HEPA-filtered vacuum, airflow testing, and a safety report. Call (650) 484-4418 for your quote.'
            },
            {
                'q': 'Do you serve the newer townhome developments in Mountain View?',
                'a': 'Yes. We clean dryer vents in all Mountain View property types, from single-family homes in Cuesta Park and Sylvan Park to newer high-density townhome and condo developments along El Camino Real, San Antonio Road, and in the North Bayshore area. Multi-story townhomes often have dryer vents routed vertically through upper floors or stacked with neighboring units, requiring specialized commercial equipment. Volume pricing is available for four or more units.'
            },
            {
                'q': 'How does lint buildup affect dryer performance and safety in Mountain View homes?',
                'a': 'Lint buildup restricts exhaust airflow, causing your dryer to run hotter and longer. This wastes energy (up to 30% more per cycle according to the DOE), puts excessive wear on dryer components, and creates a fire hazard. The U.S. Fire Administration attributes approximately 2,900 home fires annually to dryer lint ignition. In Mountain View, where many homes in Jackson Park and Monta Loma have aging dryer vent systems, regular cleaning is the most effective prevention measure.'
            },
            {
                'q': 'Can I get same-day dryer vent cleaning in Mountain View?',
                'a': 'Yes. Mountain View is in our core South Bay service area. Same-day and next-day appointments are available Monday through Saturday, 8 AM to 6 PM. Most residential cleanings take 45 to 60 minutes. Schedule at dvspecialists.com/book or call (650) 484-4418.'
            },
        ]
    },
    'dryer-vent-cleaning-burlingame-template.html': {
        'city': 'Burlingame',
        'heading': 'Burlingame Dryer Vent Cleaning FAQ',
        'faqs': [
            {
                'q': 'How often should Burlingame homeowners have their dryer vents cleaned?',
                'a': 'The NFPA recommends annual professional cleaning. Burlingame has a distinctive housing stock, with many homes in Burlingame Hills, Easton Addition, and Ray Park dating to the 1920s through 1940s. These older homes often have dryer vents that were added during remodels, resulting in longer runs through walls and tight spaces. If your household includes four or more people or pets, twice-yearly cleaning is recommended.'
            },
            {
                'q': 'Why are Burlingame Craftsman and Tudor homes at higher risk for dryer vent issues?',
                'a': 'Many of Burlingame\'s signature Craftsman and Tudor-style homes in Burlingame Park, Oak Grove, and Burlingame Terrace were built decades before modern dryer exhaust standards. When dryers were later installed, vents were often routed through existing wall cavities, basements, or attic spaces with multiple turns. These retrofitted vent paths are more prone to lint accumulation than purpose-built installations. Our CDET-certified technicians specialize in navigating these complex older configurations.'
            },
            {
                'q': 'What does dryer vent cleaning cost in Burlingame?',
                'a': 'Residential cleaning in Burlingame costs $149 to $249 per vent, depending on length, number of bends, and whether your transition hose needs replacing with a UL 2158A-compliant duct. We use flat-rate pricing with no hidden fees. Every service includes rotary brush cleaning, HEPA-filtered vacuum extraction, and a post-cleaning airflow test. Call (650) 484-4418 for an exact quote.'
            },
            {
                'q': 'Does Dryer Vent Specialists serve Burlingame apartment buildings along El Camino Real?',
                'a': 'Yes. We clean dryer vents in all Burlingame property types, from single-family homes in Mills Estate and Lyons Hoag to multi-unit apartment buildings along El Camino Real, near Broadway, and in the Burlingame Gardens area. Apartment buildings with shared or stacked vent systems require commercial-grade cleaning equipment. We offer volume pricing and scheduled maintenance for property managers with four or more units.'
            },
            {
                'q': 'What is CDET certification and why does it matter for Burlingame homeowners?',
                'a': 'CDET stands for Certified Dryer Exhaust Technician, a nationally recognized credential from the Chimney Safety Institute of America. CDET-certified technicians have passed testing on dryer exhaust system design, fire science, building codes, and proper cleaning techniques. In Burlingame, where many homes have complex vintage vent configurations, hiring a CDET-certified company ensures the work meets current safety standards and is not just a surface-level cleaning.'
            },
            {
                'q': 'Is same-day dryer vent service available in Burlingame?',
                'a': 'Yes. Burlingame is adjacent to our San Mateo headquarters, making same-day and next-day appointments frequently available Monday through Saturday, 8 AM to 6 PM. Most standard residential cleanings take 45 to 60 minutes. Book online at dvspecialists.com/book or call (650) 484-4418.'
            },
        ]
    },
    'dryer-vent-cleaning-menlo-park-template.html': {
        'city': 'Menlo Park',
        'heading': 'Menlo Park Dryer Vent Cleaning FAQ',
        'faqs': [
            {
                'q': 'How frequently should Menlo Park homeowners clean their dryer vents?',
                'a': 'The NFPA recommends professional dryer vent cleaning at least once per year. Menlo Park encompasses a range of housing, from mid-century homes in The Willows and Allied Arts to larger estates in Sharon Heights and West Menlo Park. Homes with longer vent runs, particularly those with roof-level terminations, need cleaning more frequently. Households running more than five loads per week or those with pets should schedule every six months.'
            },
            {
                'q': 'Are dryer vent problems common in Menlo Park\'s mid-century homes?',
                'a': 'Yes. Many homes in The Willows, Linfield Oaks, and Felton Gables were built in the 1950s and 1960s with dryer vents running through crawl spaces, interior walls, or up to second-story rooflines. These longer, more complex vent paths accumulate lint faster and are harder to clean with consumer-grade tools. We frequently find corrugated foil duct (now prohibited by code) and crushed transition hoses in these homes during inspections.'
            },
            {
                'q': 'What is the cost of dryer vent cleaning in Menlo Park?',
                'a': 'Standard residential cleaning ranges from $149 to $249 per vent in Menlo Park. Pricing is flat-rate based on vent length, number of elbows, and whether the transition hose needs replacement. There are no hidden charges. Every cleaning includes rotary brush treatment, HEPA-filtered vacuum extraction, airflow measurement, and a written safety report. Call (650) 484-4418 for a specific quote.'
            },
            {
                'q': 'Do you serve condos and multi-family buildings in Belle Haven and Menlo Oaks?',
                'a': 'Yes. We clean dryer vents in single-family homes, condos, townhomes, and apartment complexes across all Menlo Park neighborhoods, including Belle Haven, Menlo Oaks, University Heights, and multi-unit buildings near Downtown Menlo Park along Santa Cruz Avenue. Multi-unit properties with shared vent systems need commercial-grade equipment. Property managers and HOAs with four or more units qualify for volume pricing.'
            },
            {
                'q': 'How does a clogged dryer vent create a fire risk in Menlo Park homes?',
                'a': 'Lint is highly flammable and accumulates inside dryer exhaust ducts over time. When airflow is restricted, the dryer\'s heating element runs at higher temperatures, which can ignite trapped lint. The Menlo Park Fire Protection District, which also serves Atherton and parts of unincorporated San Mateo County, responds to dryer-related fire calls regularly. Annual professional cleaning removes the combustible material and is the single most effective step homeowners can take to prevent dryer fires.'
            },
            {
                'q': 'Can I get same-day dryer vent cleaning in Menlo Park?',
                'a': 'Yes. Menlo Park is within our core Peninsula service area, and same-day and next-day appointments are frequently available Monday through Saturday, 8 AM to 6 PM. Most residential cleanings take 45 to 60 minutes. Book at dvspecialists.com/book or call (650) 484-4418.'
            },
        ]
    },
}


def build_faq_schema(faqs):
    """Build FAQPage JSON-LD."""
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq['q'],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq['a']
                }
            }
            for faq in faqs
        ]
    }, indent=4)


def build_faq_html(faqs):
    """Build visible FAQ accordion HTML."""
    items = []
    for faq in faqs:
        # Escape & for HTML display
        q_html = faq['q'].replace('&', '&amp;')
        a_html = faq['a'].replace('&', '&amp;')
        items.append(
            f'      <details class="faq-item"><summary>{q_html} <span class="faq-icon">+</span></summary>'
            f'<div class="faq-body">{a_html}</div></details>'
        )
    return '\n'.join(items)


for filename, data in CITY_FAQS.items():
    with open(filename, 'r') as f:
        content = f.read()

    city = data['city']
    faqs = data['faqs']
    heading = data['heading']

    # 1. Replace FAQPage JSON-LD schema
    faq_schema = build_faq_schema(faqs)
    # Match the existing FAQPage schema block
    schema_pattern = r'(<!-- FAQPage Schema -->\s*<script type="application/ld\+json">\s*)\{[^<]*"@type":\s*"FAQPage"[^<]*\}(\s*</script>)'
    match = re.search(schema_pattern, content, re.DOTALL)
    if match:
        content = content[:match.start(1)] + match.group(1) + faq_schema + match.group(2) + content[match.end():]
        print(f"  {filename}: Updated FAQPage schema")
    else:
        print(f"  {filename}: WARNING - FAQPage schema not found")

    # 2. Replace visible FAQ accordion HTML
    # Match from the FAQ heading to the closing </div> of the space-y-4 container
    faq_html_pattern = (
        r'(<h2 class="font-display font-900 text-4xl" style="color:var\(--teal-dark\);letter-spacing:-\.02em;">'
        r')[^<]*(</h2>\s*</div>\s*<div class="space-y-4 fade-in">\s*)'
        r'(.*?)'
        r'(</div>\s*</div>\s*</section>\s*\n\s*<!-- CTA)'
    )
    match2 = re.search(faq_html_pattern, content, re.DOTALL)
    if match2:
        new_faq_section = (
            match2.group(1) + heading + match2.group(2) +
            build_faq_html(faqs) + '\n' +
            match2.group(4)
        )
        content = content[:match2.start()] + new_faq_section + content[match2.end():]
        print(f"  {filename}: Updated visible FAQ HTML")
    else:
        print(f"  {filename}: WARNING - FAQ HTML section not found, trying alternate pattern")
        # Try a simpler pattern
        old_details = re.findall(r'<details class="faq-item">.*?</details>', content, re.DOTALL)
        if old_details:
            # Replace the first set of details elements
            first_detail_start = content.index(old_details[0])
            last_detail_end = content.index(old_details[-1]) + len(old_details[-1])
            content = content[:first_detail_start] + build_faq_html(faqs) + content[last_detail_end:]
            print(f"  {filename}: Updated FAQ HTML (alternate method)")

            # Also update the heading
            heading_pattern = rf'{re.escape(city)} Dryer Vent Cleaning FAQ'
            # Already correct in most cases

    with open(filename, 'w') as f:
        f.write(content)

print(f"\nDone! Updated {len(CITY_FAQS)} city pages with unique FAQs.")
