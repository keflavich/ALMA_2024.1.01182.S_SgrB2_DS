#!/usr/bin/env python
"""Quick script to get field coordinates from measurement sets"""

import sys
sys.path.append('/orange/adamginsburg/casa/casa-6.6.5-17-pipeline-2024.1.0.8/lib/py/lib/python3.8/site-packages/')

from casatools import msmetadata

msmd = msmetadata()

# Get one of the measurement sets
ms = 'measurement_sets/uid___A002_X12c4b14_X77b0_targets_line.ms'
msmd.open(ms)

# Get all fields
field_names = msmd.fieldnames()
field_ids = range(len(field_names))

print("Fields and their phase centers:")
for fid, fname in zip(field_ids, field_names):
    direction = msmd.phasecenter(fid)
    print(f"Field {fid}: {fname}")
    print(f"  Direction: {direction}")
    print()

msmd.close()
