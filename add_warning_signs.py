#!/usr/bin/env python3
"""Add 'Signs Your Dryer Vent Needs Cleaning' section to all city pages, placed before the FAQ section."""

import re
import os

# City-specific localizations for the warning signs section
# Each city gets a unique intro line and one localized detail in each card
city_data = {
    "san-mateo": {
        "city": "San Mateo",
        "intro": "San Mateo homes built between the 1940s and 1970s in neighborhoods like Beresford, Baywood-Knolls, and Hillsdale often have longer vent runs that are more prone to blockage.",
        "card1_detail": "In older San Mateo homes with extended vent runs, restricted airflow traps moisture inside the drum — forcing two or three cycles per load.",
        "card2_detail": "San Mateo homeowners: if the top or sides of your dryer feel excessively hot during operation, heat is building up due to restricted exhaust airflow.",
        "card3_detail": "This is a serious fire hazard — the U.S. Fire Administration links overheated lint to approximately 2,900 home fires per year. Stop using the dryer and call immediately.",
        "card4_detail": "This counterintuitive sign is common in San Mateo homes with vent systems routed through walls and crawl spaces — lint bypasses the trap and collects in the duct instead.",
        "card5_detail": "A clogged vent pushes hot, moist air back into your laundry room instead of outside. In San Mateo's moderate climate, unexpected humidity indoors is a strong indicator of blockage.",
        "card6_detail": "Check the exterior vent flap on your San Mateo home — if lint is visible around the opening or the flap doesn't swing open during dryer operation, the vent is restricted.",
    },
    "burlingame": {
        "city": "Burlingame",
        "intro": "Many Burlingame homes in the Burlingame Hills, Easton Addition, and Ray Park neighborhoods were built in the 1920s–1950s with vintage vent configurations that restrict airflow over time.",
        "card1_detail": "In older Burlingame homes with extended or multi-bend vent runs, restricted airflow means moisture can't escape — your dryer runs two or three cycles per load.",
        "card2_detail": "Burlingame homeowners: if the top or sides of your dryer feel excessively hot during operation, heat is building up inside due to restricted exhaust.",
        "card3_detail": "This is a serious warning sign — the U.S. Fire Administration reports overheated lint causes approximately 2,900 home fires annually. Stop using the dryer and call immediately.",
        "card4_detail": "This is especially common in Burlingame's pre-war homes where vent ducts were routed through plaster walls — lint bypasses the trap and accumulates in the vent system.",
        "card5_detail": "A clogged vent pushes hot, moist air back into your laundry room. In Burlingame's older construction with limited laundry ventilation, this can also promote mold growth.",
        "card6_detail": "Walk around your Burlingame home and check the exterior vent flap — if lint is visible or the flap stays closed during dryer operation, the vent is restricted.",
    },
    "hillsborough": {
        "city": "Hillsborough",
        "intro": "Hillsborough's large estate homes — including properties in Carolands and Upper Hillsborough — often feature 30- to 50-foot vent runs and roof terminations that accumulate lint faster than standard installations.",
        "card1_detail": "In Hillsborough estates with long vent runs routed through multiple floors, restricted airflow traps moisture — forcing your dryer to run two or three cycles per load.",
        "card2_detail": "If the top or sides of your dryer feel excessively hot, heat is building up inside due to restricted exhaust — especially common in Hillsborough homes with long roof-exit vents.",
        "card3_detail": "This is a critical fire hazard — the U.S. Fire Administration links overheated lint to approximately 2,900 home fires per year. Stop using the dryer and call immediately.",
        "card4_detail": "In Hillsborough homes with extended vent systems, lint bypasses the trap and collects deep in the ductwork — sometimes 40+ feet from the dryer. Professional equipment is needed to clear it.",
        "card5_detail": "A clogged vent forces hot, moist air back into your laundry room. In Hillsborough's larger homes, this may go unnoticed initially but can lead to mold in interior walls.",
        "card6_detail": "Many Hillsborough homes have roof-exit vents that are difficult to inspect from the ground. If your dryer performance has declined, a professional inspection can verify the vent termination.",
    },
    "belmont": {
        "city": "Belmont",
        "intro": "Belmont homes built in the 1950s and 1960s — particularly in Belmont Village, Hallmark, and the Carlmont area — often have vent systems running through walls and under floors that accumulate lint over time.",
        "card1_detail": "In postwar Belmont homes with under-floor or through-wall vent runs, restricted airflow means moisture can't escape — your dryer runs two or three cycles per load.",
        "card2_detail": "Belmont homeowners: if the top or sides of your dryer feel excessively hot during operation, heat is building up inside due to restricted exhaust airflow.",
        "card3_detail": "This is a serious fire hazard — the U.S. Fire Administration links overheated lint to approximately 2,900 home fires per year. Stop using the dryer and call immediately.",
        "card4_detail": "In Belmont's mid-century homes, lint bypasses the trap and accumulates in older ductwork routed through crawl spaces — this is one of the most overlooked fire risks.",
        "card5_detail": "A clogged vent pushes hot, moist air back into your laundry room. In Belmont's hillside homes with limited natural ventilation, this can also promote mold growth.",
        "card6_detail": "Check the exterior vent flap on your Belmont home — if lint or debris is visible around the opening or the flap doesn't swing open during operation, the vent is restricted.",
    },
    "san-carlos": {
        "city": "San Carlos",
        "intro": "San Carlos homes in White Oaks, Devonshire, and the Crestview neighborhood — many with raised foundations and vent runs through crawl spaces — are especially susceptible to gradual lint buildup.",
        "card1_detail": "In San Carlos homes with raised foundations and under-floor vent routing, restricted airflow means moisture can't escape — your dryer runs two or three cycles per load.",
        "card2_detail": "San Carlos homeowners: if the top or sides of your dryer feel excessively hot during operation, heat is building up inside due to restricted exhaust.",
        "card3_detail": "This is a serious fire hazard — the U.S. Fire Administration links overheated lint to approximately 2,900 home fires per year. Stop using the dryer and call immediately.",
        "card4_detail": "In San Carlos homes with crawl-space vent runs, lint bypasses the trap and collects in hard-to-reach ductwork — making professional cleaning essential.",
        "card5_detail": "A clogged vent forces hot, moist air back into your laundry room. In San Carlos, this is especially common in homes along the Laurel Street corridor with older venting systems.",
        "card6_detail": "Walk around your San Carlos home and check the exterior vent flap — if lint is visible or the flap stays closed during dryer operation, your vent is restricted.",
    },
    "redwood-city": {
        "city": "Redwood City",
        "intro": "Redwood City homes in Woodside Plaza, Redwood Oaks, and Redwood Shores — spanning ranch-style single-family to modern condos — can develop blockages depending on vent length and configuration.",
        "card1_detail": "In Redwood City homes with long or multi-bend vent runs, restricted airflow traps moisture inside the drum — forcing two or three cycles per load.",
        "card2_detail": "Redwood City homeowners: if the top or sides of your dryer feel excessively hot during operation, heat is building up inside due to restricted exhaust.",
        "card3_detail": "This is a serious fire hazard — the Redwood City Fire Department recommends annual vent cleaning. The USFA links overheated lint to approximately 2,900 home fires per year.",
        "card4_detail": "In Redwood City's diverse housing stock — from 1950s ranches to newer Redwood Shores condos — lint bypasses the trap and collects in the ductwork over time.",
        "card5_detail": "A clogged vent pushes hot, moist air back into your laundry room. In Redwood City's warmer climate, this extra humidity can create uncomfortable conditions and promote mold.",
        "card6_detail": "Check the exterior vent flap on your Redwood City home — if lint is visible around the opening or the flap doesn't swing open during dryer operation, the vent is restricted.",
    },
    "menlo-park": {
        "city": "Menlo Park",
        "intro": "Menlo Park homes in The Willows, Allied Arts, Sharon Heights, and Belle Haven represent a wide range of construction eras — each with unique vent configurations that can accumulate lint.",
        "card1_detail": "In Menlo Park homes — from 1930s cottages in The Willows to modern builds in Sharon Heights — restricted airflow means moisture can't escape, forcing two or three cycles per load.",
        "card2_detail": "Menlo Park homeowners: if the top or sides of your dryer feel excessively hot during operation, heat is building up inside due to restricted exhaust airflow.",
        "card3_detail": "This is a serious fire hazard — the U.S. Fire Administration links overheated lint to approximately 2,900 home fires per year. Stop using the dryer and call immediately.",
        "card4_detail": "In Menlo Park's older homes, lint bypasses the trap and collects in ductwork routed through walls and under floors — professional equipment is needed to clear deep buildup.",
        "card5_detail": "A clogged vent pushes hot, moist air back into your laundry room. In Menlo Park, this can affect indoor air quality and contribute to mold in homes with limited ventilation.",
        "card6_detail": "Check the exterior vent flap on your Menlo Park home — if lint or debris is visible around the opening or the flap doesn't open during operation, the vent is restricted.",
    },
    "half-moon-bay": {
        "city": "Half Moon Bay",
        "intro": "Half Moon Bay's coastal environment — including Miramar, El Granada, Princeton-by-the-Sea, and Moss Beach — exposes dryer vents to salt air and humidity that accelerate lint buildup and corrosion.",
        "card1_detail": "In Half Moon Bay's humid coastal climate, restricted airflow compounds moisture problems — your dryer runs two or three cycles per load as damp air can't escape the drum.",
        "card2_detail": "Coastside homeowners: if the top or sides of your dryer feel excessively hot, heat is building up due to restricted exhaust — salt air corrosion on vent components makes this more common.",
        "card3_detail": "This is a serious fire hazard — the U.S. Fire Administration links overheated lint to approximately 2,900 home fires per year. Stop using the dryer and call immediately.",
        "card4_detail": "In Half Moon Bay's salt-air environment, lint combines with moisture and corrodes vent interiors — buildup becomes compacted and harder to clear than in inland communities.",
        "card5_detail": "A clogged vent pushes hot, moist air back into your laundry room. On the coast, where ambient humidity is already high, this significantly increases mold and mildew risk indoors.",
        "card6_detail": "Inspect the exterior vent on your Half Moon Bay home — salt air corrosion can cause the flap to seize shut, and coastal winds can push debris into unprotected vent openings.",
    },
    "san-francisco": {
        "city": "San Francisco",
        "intro": "San Francisco's Victorian and Edwardian row houses, TICs, and multi-unit buildings — particularly in the Sunset, Richmond, Noe Valley, and Mission districts — often have complex or aging vent systems.",
        "card1_detail": "In San Francisco row houses with vents routed through multiple floors or shared walls, restricted airflow means moisture can't escape — your dryer runs two or three cycles per load.",
        "card2_detail": "SF homeowners: if the top or sides of your dryer feel excessively hot, heat is building up due to restricted exhaust — especially common in Sunset and Richmond homes with long vent runs.",
        "card3_detail": "This is a serious fire hazard — the U.S. Fire Administration links overheated lint to approximately 2,900 home fires per year. Stop using the dryer and call immediately.",
        "card4_detail": "In San Francisco's dense housing — TICs, Victorians, and multi-unit buildings — lint bypasses the trap and collects in ductwork routed through shared walls and tight crawl spaces.",
        "card5_detail": "A clogged vent pushes hot, moist air back into your unit. In San Francisco's compact living spaces with limited ventilation, this can quickly lead to mold and poor indoor air quality.",
        "card6_detail": "Many SF homes have vents terminating through sidewalls or roofs that are difficult to inspect. If dryer performance has declined, a professional inspection can verify the vent outlet.",
    },
    "south-san-francisco": {
        "city": "South San Francisco",
        "intro": "South San Francisco homes in Westborough, Sunshine Gardens, and the Sign Hill area — many built during the mid-century housing boom — have vent systems that accumulate lint over decades of use.",
        "card1_detail": "In South San Francisco's mid-century homes with through-wall and under-floor vent runs, restricted airflow traps moisture — forcing two or three cycles per load.",
        "card2_detail": "South City homeowners: if the top or sides of your dryer feel excessively hot during operation, heat is building up inside due to restricted exhaust airflow.",
        "card3_detail": "This is a serious fire hazard — the U.S. Fire Administration links overheated lint to approximately 2,900 home fires per year. Stop using the dryer and call immediately.",
        "card4_detail": "In Westborough and Sunshine Gardens homes, lint bypasses the trap and accumulates in older ductwork — a fire risk that worsens with every load until professionally cleaned.",
        "card5_detail": "A clogged vent pushes hot, moist air back into your laundry room. In South San Francisco's fog-prone climate, adding indoor moisture can promote mold growth.",
        "card6_detail": "Check the exterior vent flap on your South San Francisco home — if lint is visible or the flap stays closed during dryer operation, the vent is restricted.",
    },
    "los-altos": {
        "city": "Los Altos",
        "intro": "Los Altos homes in Country Club, Loyola Corners, and North Los Altos — including many ranch-style properties built in the 1950s and 1960s — often have vent systems running through attics or crawl spaces.",
        "card1_detail": "In Los Altos ranch-style homes with attic or crawl-space vent runs, restricted airflow means moisture can't escape — your dryer runs two or three cycles per load.",
        "card2_detail": "Los Altos homeowners: if the top or sides of your dryer feel excessively hot during operation, heat is building up inside due to restricted exhaust airflow.",
        "card3_detail": "This is a serious fire hazard — the U.S. Fire Administration links overheated lint to approximately 2,900 home fires per year. Stop using the dryer and call immediately.",
        "card4_detail": "In Los Altos homes with attic-routed vents, lint bypasses the trap and collects where it's invisible — only professional inspection equipment can detect deep accumulation.",
        "card5_detail": "A clogged vent pushes hot, moist air back into your laundry room. In Los Altos and Los Altos Hills, this added moisture can damage finishes in premium home interiors.",
        "card6_detail": "Check the exterior vent on your Los Altos home — if lint or debris is visible or the flap doesn't swing open during dryer operation, the vent is restricted.",
    },
}


def build_warning_signs_section(data):
    """Build the warning signs HTML section for a city."""
    city = data["city"]
    return f'''
<!-- ── WARNING SIGNS ── -->
<section class="py-20 px-5" style="background:#faf6f1;">
  <div class="max-w-5xl mx-auto">
    <div class="mb-12 fade-in">
      <p class="font-display font-700 text-sm uppercase tracking-widest mb-2" style="color:var(--orange);">Warning Signs</p>
      <h2 class="font-display font-900 text-4xl mb-4" style="color:var(--teal-dark); letter-spacing:-.02em;">Signs Your Dryer Vent Needs Cleaning</h2>
      <p class="text-gray-500" style="line-height:1.7; max-width:48rem;">If you notice any of these symptoms, your vent is likely partially or fully clogged and should be professionally cleaned as soon as possible. {data["intro"]}</p>
    </div>
    <div class="grid md:grid-cols-3 gap-6 fade-in">

      <div style="background:var(--gray-lt); border-radius:14px; padding:1.75rem; border-left:4px solid var(--orange); position:relative;">
        <div style="font-size:1.5rem; margin-bottom:.75rem;">&#128168;</div>
        <h3 class="font-display font-800 text-lg mb-2" style="color:var(--teal-dark);">Clothes need multiple cycles to dry</h3>
        <p class="text-gray-500 text-sm" style="line-height:1.7;">{data["card1_detail"]}</p>
      </div>

      <div style="background:var(--gray-lt); border-radius:14px; padding:1.75rem; border-left:4px solid var(--orange); position:relative;">
        <div style="font-size:1.5rem; margin-bottom:.75rem;">&#9888;&#65039;</div>
        <h3 class="font-display font-800 text-lg mb-2" style="color:var(--teal-dark);">Dryer is very hot to the touch</h3>
        <p class="text-gray-500 text-sm" style="line-height:1.7;">{data["card2_detail"]}</p>
      </div>

      <div style="background:var(--gray-lt); border-radius:14px; padding:1.75rem; border-left:4px solid var(--orange); position:relative;">
        <div style="font-size:1.5rem; margin-bottom:.75rem;">&#128293;</div>
        <h3 class="font-display font-800 text-lg mb-2" style="color:var(--teal-dark);">Burning smell when dryer is running</h3>
        <p class="text-gray-500 text-sm" style="line-height:1.7;">{data["card3_detail"]}</p>
      </div>

      <div style="background:var(--gray-lt); border-radius:14px; padding:1.75rem; border-left:4px solid var(--orange); position:relative;">
        <div style="font-size:1.5rem; margin-bottom:.75rem;">&#129656;</div>
        <h3 class="font-display font-800 text-lg mb-2" style="color:var(--teal-dark);">Lint trap catches less lint than usual</h3>
        <p class="text-gray-500 text-sm" style="line-height:1.7;">{data["card4_detail"]}</p>
      </div>

      <div style="background:var(--gray-lt); border-radius:14px; padding:1.75rem; border-left:4px solid var(--orange); position:relative;">
        <div style="font-size:1.5rem; margin-bottom:.75rem;">&#128167;</div>
        <h3 class="font-display font-800 text-lg mb-2" style="color:var(--teal-dark);">Laundry room feels humid or warm</h3>
        <p class="text-gray-500 text-sm" style="line-height:1.7;">{data["card5_detail"]}</p>
      </div>

      <div style="background:var(--gray-lt); border-radius:14px; padding:1.75rem; border-left:4px solid var(--orange); position:relative;">
        <div style="font-size:1.5rem; margin-bottom:.75rem;">&#128065;</div>
        <h3 class="font-display font-800 text-lg mb-2" style="color:var(--teal-dark);">Visible lint around exterior vent</h3>
        <p class="text-gray-500 text-sm" style="line-height:1.7;">{data["card6_detail"]}</p>
      </div>

    </div>
  </div>
</section>
'''


def add_warning_signs_css(content):
    """Add responsive CSS for the warning signs cards if not already present."""
    # We don't need extra CSS - using inline styles and Tailwind grid classes
    return content


def process_file(filepath, city_slug):
    """Add warning signs section before the FAQ section in a city page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already added
    if '<!-- ── WARNING SIGNS ── -->' in content or 'Warning Signs' in content:
        print(f"  SKIP: {filepath} already has warning signs section")
        return False

    data = city_data[city_slug]
    section_html = build_warning_signs_section(data)

    # Find the FAQ section comment — both formats used across pages
    # Pattern 1 (full pages): <!-- ── FAQ ── -->
    # Pattern 2 (compact pages): <!-- FAQ -->
    faq_patterns = [
        '<!-- ── FAQ ── -->',
        '<!-- FAQ -->',
    ]

    inserted = False
    for pattern in faq_patterns:
        if pattern in content:
            content = content.replace(pattern, section_html + '\n' + pattern)
            inserted = True
            break

    if not inserted:
        print(f"  ERROR: Could not find FAQ section marker in {filepath}")
        return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  DONE: {filepath}")
    return True


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
