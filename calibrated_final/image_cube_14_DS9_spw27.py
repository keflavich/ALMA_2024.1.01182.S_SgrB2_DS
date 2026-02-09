#!/usr/bin/env python
"""
Image cube 14: DS9 SPW 27
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
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/temp_line/uid___A002_X12c4b14_X77b0_DS9_spw27_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/temp_line/uid___A002_X12c7631_X2152_DS9_spw27_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/temp_line/uid___A002_X12c99be_Xa92b_DS9_spw27_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/temp_line/uid___A002_X12cdde9_Xb8e6_DS9_spw27_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/temp_line/uid___A002_X12d0dd8_Xbca_DS9_spw27_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/temp_line/uid___A002_X12d2ac0_X13ec_DS9_spw27_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/temp_line/uid___A002_X12d2ac0_X72e2_DS9_spw27_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/temp_line/uid___A002_X12d4098_X223c_DS9_spw27_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/temp_line/uid___A002_X12de9a8_X8e3e_DS9_spw27_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/temp_line/uid___A002_X12de9a8_X954b_DS9_spw27_line.ms'
]

# Imaging parameters (all explicit, no variables)
FIELD = 'DS9'
SPW_SELECTION = ''
DATACOLUMN = 'data'
IMAGENAME = 'oussid.SgrB2_DS9_sci.spw27.cube.I'
PHASECENTER = 'ICRS 17:47:23.456900 -028.25.52.09900'

# Print configuration
print("="*80)
print(f"IMAGING: DS9 SPW 27")
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

print(f"\nCompleted: DS9 SPW 27")
