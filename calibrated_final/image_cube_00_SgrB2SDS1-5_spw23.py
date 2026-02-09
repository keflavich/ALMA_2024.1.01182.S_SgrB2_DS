#!/usr/bin/env python
"""
Image cube 0: SgrB2S_DS1-5 SPW 23
Completely explicit script - all paths hardcoded and verified at generation time.
NO glob patterns, NO conditional logic, NO runtime path discovery.

Generated: Sat Feb  7 10:46:25 AM EST 2026
Data source: consolidated (all fields/SPWs)
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
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/measurement_sets/uid___A002_X12c4b14_X77b0_targets_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/measurement_sets/uid___A002_X12c7631_X2152_targets_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/measurement_sets/uid___A002_X12c99be_Xa92b_targets_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/measurement_sets/uid___A002_X12cdde9_Xb8e6_targets_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/measurement_sets/uid___A002_X12d0dd8_Xbca_targets_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/measurement_sets/uid___A002_X12d2ac0_X13ec_targets_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/measurement_sets/uid___A002_X12d2ac0_X72e2_targets_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/measurement_sets/uid___A002_X12d4098_X223c_targets_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/measurement_sets/uid___A002_X12de9a8_X8e3e_targets_line.ms',
    '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/measurement_sets/uid___A002_X12de9a8_X954b_targets_line.ms'
]

# Imaging parameters (all explicit, no variables)
FIELD = 'SgrB2S_DS1-5'
SPW_SELECTION = '23'
DATACOLUMN = 'corrected'
IMAGENAME = 'oussid.SgrB2_SgrB2SDS1-5_sci.spw23.cube.I'
PHASECENTER = 'ICRS 17:47:20.026849 -028.23.46.89155'

# Print configuration
print("="*80)
print(f"IMAGING: SgrB2S_DS1-5 SPW 23")
print(f"  MS files: {len(VIS_LIST)}")
print(f"  datacolumn: corrected")
print(f"  spw: '23'")
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
    nchan=1916,
    start='132.8931835956GHz',
    width='0.9766485MHz',
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

print(f"\nCompleted: SgrB2S_DS1-5 SPW 23")
