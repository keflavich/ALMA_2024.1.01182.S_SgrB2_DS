#!/usr/bin/env python3
"""
Generate 16 individual imaging scripts with completely explicit, hardcoded paths.
All file paths are verified to exist at generation time. No glob, no conditionals.
"""

import os

BASE = '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final'

# All paths verified to exist
CONSOLIDATED_MS = [
    f'{BASE}/measurement_sets/uid___A002_X12c4b14_X77b0_targets_line.ms',
    f'{BASE}/measurement_sets/uid___A002_X12c7631_X2152_targets_line.ms',
    f'{BASE}/measurement_sets/uid___A002_X12c99be_Xa92b_targets_line.ms',
    f'{BASE}/measurement_sets/uid___A002_X12cdde9_Xb8e6_targets_line.ms',
    f'{BASE}/measurement_sets/uid___A002_X12d0dd8_Xbca_targets_line.ms',
    f'{BASE}/measurement_sets/uid___A002_X12d2ac0_X13ec_targets_line.ms',
    f'{BASE}/measurement_sets/uid___A002_X12d2ac0_X72e2_targets_line.ms',
    f'{BASE}/measurement_sets/uid___A002_X12d4098_X223c_targets_line.ms',
    f'{BASE}/measurement_sets/uid___A002_X12de9a8_X8e3e_targets_line.ms',
    f'{BASE}/measurement_sets/uid___A002_X12de9a8_X954b_targets_line.ms',
]

# DS6 temp_line files (all verified to exist)
DS6_SPW23 = [f'{BASE}/temp_line/uid___A002_X12c4b14_X77b0_DS6_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12c7631_X2152_DS6_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12c99be_Xa92b_DS6_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12cdde9_Xb8e6_DS6_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12d0dd8_Xbca_DS6_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12d2ac0_X13ec_DS6_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12d2ac0_X72e2_DS6_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12d4098_X223c_DS6_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12de9a8_X8e3e_DS6_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12de9a8_X954b_DS6_spw23_line.ms']
DS6_SPW25 = [f'{BASE}/temp_line/uid___A002_X12c4b14_X77b0_DS6_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12c7631_X2152_DS6_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12c99be_Xa92b_DS6_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12cdde9_Xb8e6_DS6_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12d0dd8_Xbca_DS6_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12d2ac0_X13ec_DS6_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12d2ac0_X72e2_DS6_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12d4098_X223c_DS6_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12de9a8_X8e3e_DS6_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12de9a8_X954b_DS6_spw25_line.ms']
DS6_SPW27 = [f'{BASE}/temp_line/uid___A002_X12c4b14_X77b0_DS6_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12c7631_X2152_DS6_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12c99be_Xa92b_DS6_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12cdde9_Xb8e6_DS6_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12d0dd8_Xbca_DS6_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12d2ac0_X13ec_DS6_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12d2ac0_X72e2_DS6_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12d4098_X223c_DS6_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12de9a8_X8e3e_DS6_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12de9a8_X954b_DS6_spw27_line.ms']
DS6_SPW29 = [f'{BASE}/temp_line/uid___A002_X12c4b14_X77b0_DS6_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12c7631_X2152_DS6_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12c99be_Xa92b_DS6_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12cdde9_Xb8e6_DS6_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12d0dd8_Xbca_DS6_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12d2ac0_X13ec_DS6_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12d2ac0_X72e2_DS6_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12d4098_X223c_DS6_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12de9a8_X8e3e_DS6_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12de9a8_X954b_DS6_spw29_line.ms']

# DS7-DS8 temp_line files
DS7DS8_SPW23 = [f'{BASE}/temp_line/uid___A002_X12c4b14_X77b0_DS7DS8_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12c7631_X2152_DS7DS8_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12c99be_Xa92b_DS7DS8_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12cdde9_Xb8e6_DS7DS8_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12d0dd8_Xbca_DS7DS8_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12d2ac0_X13ec_DS7DS8_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12d2ac0_X72e2_DS7DS8_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12d4098_X223c_DS7DS8_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12de9a8_X8e3e_DS7DS8_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12de9a8_X954b_DS7DS8_spw23_line.ms']
DS7DS8_SPW25 = [f'{BASE}/temp_line/uid___A002_X12c4b14_X77b0_DS7DS8_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12c7631_X2152_DS7DS8_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12c99be_Xa92b_DS7DS8_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12cdde9_Xb8e6_DS7DS8_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12d0dd8_Xbca_DS7DS8_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12d2ac0_X13ec_DS7DS8_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12d2ac0_X72e2_DS7DS8_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12d4098_X223c_DS7DS8_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12de9a8_X8e3e_DS7DS8_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12de9a8_X954b_DS7DS8_spw25_line.ms']
DS7DS8_SPW27 = [f'{BASE}/temp_line/uid___A002_X12c4b14_X77b0_DS7DS8_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12c7631_X2152_DS7DS8_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12c99be_Xa92b_DS7DS8_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12cdde9_Xb8e6_DS7DS8_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12d0dd8_Xbca_DS7DS8_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12d2ac0_X13ec_DS7DS8_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12d2ac0_X72e2_DS7DS8_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12d4098_X223c_DS7DS8_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12de9a8_X8e3e_DS7DS8_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12de9a8_X954b_DS7DS8_spw27_line.ms']
DS7DS8_SPW29 = [f'{BASE}/temp_line/uid___A002_X12c4b14_X77b0_DS7DS8_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12c7631_X2152_DS7DS8_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12c99be_Xa92b_DS7DS8_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12cdde9_Xb8e6_DS7DS8_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12d0dd8_Xbca_DS7DS8_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12d2ac0_X13ec_DS7DS8_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12d2ac0_X72e2_DS7DS8_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12d4098_X223c_DS7DS8_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12de9a8_X8e3e_DS7DS8_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12de9a8_X954b_DS7DS8_spw29_line.ms']

# DS9 temp_line files
DS9_SPW23 = [f'{BASE}/temp_line/uid___A002_X12c4b14_X77b0_DS9_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12c7631_X2152_DS9_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12c99be_Xa92b_DS9_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12cdde9_Xb8e6_DS9_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12d0dd8_Xbca_DS9_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12d2ac0_X13ec_DS9_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12d2ac0_X72e2_DS9_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12d4098_X223c_DS9_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12de9a8_X8e3e_DS9_spw23_line.ms', f'{BASE}/temp_line/uid___A002_X12de9a8_X954b_DS9_spw23_line.ms']
DS9_SPW25 = [f'{BASE}/temp_line/uid___A002_X12c4b14_X77b0_DS9_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12c7631_X2152_DS9_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12c99be_Xa92b_DS9_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12cdde9_Xb8e6_DS9_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12d0dd8_Xbca_DS9_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12d2ac0_X13ec_DS9_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12d2ac0_X72e2_DS9_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12d4098_X223c_DS9_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12de9a8_X8e3e_DS9_spw25_line.ms', f'{BASE}/temp_line/uid___A002_X12de9a8_X954b_DS9_spw25_line.ms']
DS9_SPW27 = [f'{BASE}/temp_line/uid___A002_X12c4b14_X77b0_DS9_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12c7631_X2152_DS9_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12c99be_Xa92b_DS9_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12cdde9_Xb8e6_DS9_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12d0dd8_Xbca_DS9_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12d2ac0_X13ec_DS9_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12d2ac0_X72e2_DS9_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12d4098_X223c_DS9_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12de9a8_X8e3e_DS9_spw27_line.ms', f'{BASE}/temp_line/uid___A002_X12de9a8_X954b_DS9_spw27_line.ms']
DS9_SPW29 = [f'{BASE}/temp_line/uid___A002_X12c4b14_X77b0_DS9_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12c7631_X2152_DS9_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12c99be_Xa92b_DS9_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12cdde9_Xb8e6_DS9_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12d0dd8_Xbca_DS9_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12d2ac0_X13ec_DS9_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12d2ac0_X72e2_DS9_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12d4098_X223c_DS9_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12de9a8_X8e3e_DS9_spw29_line.ms', f'{BASE}/temp_line/uid___A002_X12de9a8_X954b_DS9_spw29_line.ms']

# All 16 cube configurations with verified file paths
CUBES = [
    # 0-3: SgrB2S_DS1-5 uses consolidated (no temp_line files exist for DS15)
    {'id': 0, 'field': 'SgrB2S_DS1-5', 'spw': '23', 'vis': CONSOLIDATED_MS, 'datacolumn': 'corrected', 'spw_select': '23',
     'phasecenter': 'ICRS 17:47:20.0268 -028.23.46.892', 'nchan': 1916, 'start': '132.8931835956GHz', 'width': '0.9766485MHz'},
    {'id': 1, 'field': 'SgrB2S_DS1-5', 'spw': '25', 'vis': CONSOLIDATED_MS, 'datacolumn': 'corrected', 'spw_select': '25',
     'phasecenter': 'ICRS 17:47:20.0268 -028.23.46.892', 'nchan': -1, 'start': '', 'width': ''},
    {'id': 2, 'field': 'SgrB2S_DS1-5', 'spw': '27', 'vis': CONSOLIDATED_MS, 'datacolumn': 'corrected', 'spw_select': '27',
     'phasecenter': 'ICRS 17:47:20.0268 -028.23.46.892', 'nchan': -1, 'start': '', 'width': ''},
    {'id': 3, 'field': 'SgrB2S_DS1-5', 'spw': '29', 'vis': CONSOLIDATED_MS, 'datacolumn': 'corrected', 'spw_select': '29',
     'phasecenter': 'ICRS 17:47:20.0268 -028.23.46.892', 'nchan': -1, 'start': '', 'width': ''},
    
    # 4-7: DS6 uses temp_line
    {'id': 4, 'field': 'DS6', 'spw': '23', 'vis': DS6_SPW23, 'datacolumn': 'data', 'spw_select': '',
     'phasecenter': 'ICRS 17:47:20.0222 -028.23.44.670', 'nchan': 1916, 'start': '132.8931835956GHz', 'width': '0.9766485MHz'},
    {'id': 5, 'field': 'DS6', 'spw': '25', 'vis': DS6_SPW25, 'datacolumn': 'data', 'spw_select': '',
     'phasecenter': 'ICRS 17:47:20.0222 -028.23.44.670', 'nchan': -1, 'start': '', 'width': ''},
    {'id': 6, 'field': 'DS6', 'spw': '27', 'vis': DS6_SPW27, 'datacolumn': 'data', 'spw_select': '',
     'phasecenter': 'ICRS 17:47:20.0222 -028.23.44.670', 'nchan': -1, 'start': '', 'width': ''},
    {'id': 7, 'field': 'DS6', 'spw': '29', 'vis': DS6_SPW29, 'datacolumn': 'data', 'spw_select': '',
     'phasecenter': 'ICRS 17:47:20.0222 -028.23.44.670', 'nchan': -1, 'start': '', 'width': ''},
    
    # 8-11: DS7-DS8 uses temp_line
    {'id': 8, 'field': 'DS7-DS8', 'spw': '23', 'vis': DS7DS8_SPW23, 'datacolumn': 'data', 'spw_select': '',
     'phasecenter': 'ICRS 17:47:20.0260 -028.23.45.930', 'nchan': 1916, 'start': '132.8931835956GHz', 'width': '0.9766485MHz'},
    {'id': 9, 'field': 'DS7-DS8', 'spw': '25', 'vis': DS7DS8_SPW25, 'datacolumn': 'data', 'spw_select': '',
     'phasecenter': 'ICRS 17:47:20.0260 -028.23.45.930', 'nchan': -1, 'start': '', 'width': ''},
    {'id': 10, 'field': 'DS7-DS8', 'spw': '27', 'vis': DS7DS8_SPW27, 'datacolumn': 'data', 'spw_select': '',
     'phasecenter': 'ICRS 17:47:20.0260 -028.23.45.930', 'nchan': -1, 'start': '', 'width': ''},
    {'id': 11, 'field': 'DS7-DS8', 'spw': '29', 'vis': DS7DS8_SPW29, 'datacolumn': 'data', 'spw_select': '',
     'phasecenter': 'ICRS 17:47:20.0260 -028.23.45.930', 'nchan': -1, 'start': '', 'width': ''},
    
    # 12-15: DS9 uses temp_line
    {'id': 12, 'field': 'DS9', 'spw': '23', 'vis': DS9_SPW23, 'datacolumn': 'data', 'spw_select': '',
     'phasecenter': 'ICRS 17:47:20.0302 -028.23.47.670', 'nchan': 1916, 'start': '132.8931835956GHz', 'width': '0.9766485MHz'},
    {'id': 13, 'field': 'DS9', 'spw': '25', 'vis': DS9_SPW25, 'datacolumn': 'data', 'spw_select': '',
     'phasecenter': 'ICRS 17:47:20.0302 -028.23.47.670', 'nchan': -1, 'start': '', 'width': ''},
    {'id': 14, 'field': 'DS9', 'spw': '27', 'vis': DS9_SPW27, 'datacolumn': 'data', 'spw_select': '',
     'phasecenter': 'ICRS 17:47:20.0302 -028.23.47.670', 'nchan': -1, 'start': '', 'width': ''},
    {'id': 15, 'field': 'DS9', 'spw': '29', 'vis': DS9_SPW29, 'datacolumn': 'data', 'spw_select': '',
     'phasecenter': 'ICRS 17:47:20.0302 -028.23.47.670', 'nchan': -1, 'start': '', 'width': ''},
]

# Verify all paths exist NOW (at generation time)
print("Verifying all MS files exist...")
all_ms = set()
for cube in CUBES:
    for ms in cube['vis']:
        all_ms.add(ms)

missing = []
for ms in sorted(all_ms):
    if not os.path.exists(ms):
        missing.append(ms)
        print(f"  MISSING: {ms}")
    
if missing:
    print(f"\nERROR: {len(missing)} MS files are missing!")
    print("Cannot generate scripts with missing data.")
    exit(1)
else:
    print(f"  ✓ All {len(all_ms)} unique MS files verified to exist")

# Generate all 16 scripts
print("\nGenerating 16 explicit imaging scripts...")
for cube in CUBES:
    field_clean = cube['field'].replace('_', '')
    filename = f"image_cube_{cube['id']:02d}_{field_clean}_spw{cube['spw']}.py"
    
    # Format vis list for script
    vis_lines = ',\n    '.join([f"'{v}'" for v in cube['vis']])
    
    script_content = f'''#!/usr/bin/env python
"""
Image cube {cube['id']}: {cube['field']} SPW {cube['spw']}
Completely explicit script - all paths hardcoded and verified at generation time.
NO glob patterns, NO conditional logic, NO runtime path discovery.

Generated: {os.popen("date").read().strip()}
Data source: {'temp_line (field/SPW-specific)' if cube['datacolumn'] == 'data' else 'consolidated (all fields/SPWs)'}
MS count: {len(cube['vis'])} files
"""

import os

# Working directory (hardcoded absolute path)
WORKING_DIR = '{BASE}/working_cubes'
if not os.path.exists(WORKING_DIR):
    os.makedirs(WORKING_DIR)
os.chdir(WORKING_DIR)

# Output directory (hardcoded absolute path)
OUTPUT_DIR = '{BASE}/cube_images'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Input measurement sets (explicit list, verified at generation time)
VIS_LIST = [
    {vis_lines}
]

# Imaging parameters (all explicit, no variables)
FIELD = '{cube['field']}'
SPW_SELECTION = '{cube['spw_select']}'
DATACOLUMN = '{cube['datacolumn']}'
IMAGENAME = 'oussid.SgrB2_{field_clean}_sci.spw{cube['spw']}.cube.I'
PHASECENTER = '{cube['phasecenter']}'

# Print configuration
print("="*80)
print(f"IMAGING: {cube['field']} SPW {cube['spw']}")
print(f"  MS files: {{len(VIS_LIST)}}")
print(f"  datacolumn: {cube['datacolumn']}")
print(f"  spw: '{cube['spw_select']}'")
print(f"  output: {{IMAGENAME}}")
print("="*80)

# Run tclean with all parameters explicitly specified
tclean(
    vis=VIS_LIST,
    field=FIELD,
    spw=SPW_SELECTION,
    intent='OBSERVE_TARGET#ON_SOURCE',
    datacolumn=DATACOLUMN,
    imagename=IMAGENAME,
    imsize=[2880, 2880],
    cell='0.025arcsec',
    phasecenter=PHASECENTER,
    stokes='I',
    specmode='cube',
    nchan={cube['nchan']},
    start='{cube['start']}',
    width='{cube['width']}',
    outframe='LSRK',
    perchanweightdensity=True,
    gridder='standard',
    mosweight=False,
    usepointing=False,
    pblimit=0.2,
    deconvolver='hogbom',
    restoration=False,
    restoringbeam='common',
    pbcor=False,
    weighting='briggsbwtaper',
    robust=0.5,
    npixels=0,
    niter=1000,
    threshold='1.5mJy',
    nsigma=0.0,
    interactive=False,
    fullsummary=False,
    usemask='auto-multithresh',
    sidelobethreshold=2.5,
    noisethreshold=5.0,
    lownoisethreshold=1.5,
    negativethreshold=0.0,
    minbeamfrac=0.3,
    growiterations=75,
    restart=True,
    calcres=True,
    calcpsf=True,
    parallel=False,
)

# Move output to final location
print(f"\\nMoving images to {{OUTPUT_DIR}}/")
os.system(f"mv {{IMAGENAME}}.* {{OUTPUT_DIR}}/ 2>/dev/null")

print(f"\\nCompleted: {cube['field']} SPW {cube['spw']}")
'''
    
    with open(filename, 'w') as f:
        f.write(script_content)
    
    print(f"  Created: {filename}")

print("\n✓ All 16 scripts generated successfully!")
print("Each script contains:")
print("  - Hardcoded, absolute paths to all MS files")
print("  - No glob, no search, no conditional logic")
print("  - All paths verified to exist at generation time")
