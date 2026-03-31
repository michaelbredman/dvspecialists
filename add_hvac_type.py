#!/usr/bin/env python3
"""Add HVACBusiness to @type arrays across all HTML files."""
import re, glob

# Pattern 1: City pages with array format (already have ProfessionalService)
# ["LocalBusiness", "HomeAndConstructionBusiness", "ProfessionalService"]
# -> ["LocalBusiness", "HomeAndConstructionBusiness", "ProfessionalService", "HVACBusiness"]

# Pattern 2: index, services, contact, about with single string
# "@type": "LocalBusiness"
# -> "@type": ["LocalBusiness", "HomeAndConstructionBusiness", "ProfessionalService", "HVACBusiness"]

files = glob.glob('*.html') + glob.glob('resources/*.html')
updated = []

for f in files:
    with open(f, 'r') as fh:
        content = fh.read()

    original = content

    # Pattern 1: Array format missing HVACBusiness
    content = content.replace(
        '"@type": ["LocalBusiness", "HomeAndConstructionBusiness", "ProfessionalService"]',
        '"@type": ["LocalBusiness", "HomeAndConstructionBusiness", "ProfessionalService", "HVACBusiness"]'
    )

    # Pattern 2: Single "LocalBusiness" string (but NOT inside a provider block)
    # We need to be careful - only replace the main business @type, not nested provider references
    # Look for the pattern on its own line in a JSON-LD block
    content = re.sub(
        r'("@type":\s*)"LocalBusiness"(\s*,\s*\n\s*"@id":\s*"https://www\.dvspecialists\.com)',
        r'\1["LocalBusiness", "HomeAndConstructionBusiness", "ProfessionalService", "HVACBusiness"]\2',
        content
    )

    if content != original:
        with open(f, 'w') as fh:
            fh.write(content)
        updated.append(f)

print(f"Updated {len(updated)} files:")
for f in updated:
    print(f"  {f}")
