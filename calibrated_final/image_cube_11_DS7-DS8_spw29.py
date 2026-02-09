#!/usr/bin/env python
"""
Image cube 11: DS7-DS8 SPW 29
Completely explicit script - all paths hardcoded and verified at generation time.
NO glob patterns, NO conditional logic, NO runtime path discovery.

Generated: Sat Feb  7 10:46:25 AM EST 2026
Data source: temp_line (field/SPW-specific)
MS count: 10 files
"""

import os

# Working directory (hardcoded absolute path)
WORKING_DIR = '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/working_cubes'
if not os.path.exists(WORKING_DIR):
    os.makedirs(WORKING_DIR)
os.chdir(WORKING_DIR)

# Output directory (hardcoded absolute path)
OUTPUT_DIR = '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/cube_images'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Input measurement sets (explicit list, verified at generation time)
VIS_LIST = [
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/temp_line/uid___A002_X12c4b14_X77b0_DS7DS8_spw29_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/temp_line/uid___A002_X12c7631_X2152_DS7DS8_spw29_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/temp_line/uid___A002_X12c99be_Xa92b_DS7DS8_spw29_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/temp_line/uid___A002_X12cdde9_Xb8e6_DS7DS8_spw29_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/temp_line/uid___A002_X12d0dd8_Xbca_DS7DS8_spw29_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/temp_line/uid___A002_X12d2ac0_X13ec_DS7DS8_spw29_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/temp_line/uid___A002_X12d2ac0_X72e2_DS7DS8_spw29_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/temp_line/uid___A002_X12d4098_X223c_DS7DS8_spw29_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/temp_line/uid___A002_X12de9a8_X8e3e_DS7DS8_spw29_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/temp_line/uid___A002_X12de9a8_X954b_DS7DS8_spw29_line.ms'
]

# Imaging parameters (all explicit, no variables)
FIELD = 'DS7-DS8'
SPW_SELECTION = ''
DATACOLUMN = 'data'
IMAGENAME = 'oussid.SgrB2_DS7-DS8_sci.spw29.cube.I'
PHASECENTER = 'ICRS 17:47:22.119692 -028.24.37.58403'

# Print configuration
print("="*80)
print(f"IMAGING: DS7-DS8 SPW 29")
print(f"  MS files: {len(VIS_LIST)}")
print(f"  datacolumn: data")
print(f"  spw: ''")
print(f"  output: {IMAGENAME}")
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
    nchan=-1,
    start='',
    width='',
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
print(f"\nMoving images to {OUTPUT_DIR}/")
os.system(f"mv {IMAGENAME}.* {OUTPUT_DIR}/ 2>/dev/null")

print(f"\nCompleted: DS7-DS8 SPW 29")
