#!/usr/bin/env python
"""Search ALMA project 2024.1.01182.S for molecular lines"""

from astroquery.alma import Alma
from astroquery.splatalogue import Splatalogue, utils
import astropy.units as u
import re

# Query ALMA archive for the project
project = '2024.1.01182.S'
print(f"Querying ALMA archive for project {project}...")
result = Alma.query(payload={'project_code': project}, public=False)

if result is None or len(result) == 0:
    raise RuntimeError(f"No data found for project {project}")

# Parse frequency support to get actual covered ranges
freq_ranges = set()
for freq_support in result['frequency_support']:
    matches = re.findall(r'\[(\d+\.?\d*)\.\.(\d+\.?\d*)GHz', str(freq_support))
    freq_ranges.update([(float(lo), float(hi)) for lo, hi in matches])

freq_ranges = sorted(freq_ranges)
print(f"\nFound {len(result)} observations with {len(freq_ranges)} unique frequency ranges:")
for lo, hi in freq_ranges:
    print(f"  {lo:.2f} - {hi:.2f} GHz")

# Get overall min/max for initial query
freq_min = min(lo for lo, hi in freq_ranges)
freq_max = max(hi for lo, hi in freq_ranges)

# Molecules to search for
molecules = ['NaCl', 'KCl', 'H2O', 'AlO', 'AlF', 'SiS']

# Query Splatalogue for each molecule within the observed frequency range
print(f"\nSearching for molecular lines (including vibrationally excited)...")
for mol in molecules:
    lines = Splatalogue.query_lines(freq_min * u.GHz, freq_max * u.GHz, 
                                    chemical_name=f' {mol} ',
                                    line_lists=['CDMS', 'JPL'])
    if lines is not None and len(lines) > 0:
        clean_lines = utils.minimize_table(lines)
        # Filter lines to only those actually covered by ALMA frequency ranges
        covered_lines = []
        for line in clean_lines:
            line_freq_ghz = line['Freq'] / 1000.0  # Convert MHz to GHz
            if any(lo <= line_freq_ghz <= hi for lo, hi in freq_ranges):
                covered_lines.append(line)
        
        if covered_lines:
            print(f"\n{mol}: Found {len(covered_lines)} lines in covered ranges")
            for line in covered_lines:
                vib_state = line['name'] if line['name'] != line['chemical_name'] else 'v=0'
                print(f"  {line['Freq']/1000.0:.4f} GHz - {line['resolved_QNs']} ({vib_state})")
        else:
            print(f"\n{mol}: No lines in covered frequency ranges")
    else:
        print(f"\n{mol}: No lines found")