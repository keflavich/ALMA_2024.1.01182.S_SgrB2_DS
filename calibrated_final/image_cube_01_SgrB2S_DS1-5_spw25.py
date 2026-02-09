#!/usr/bin/env python
"""
Image cube 1: SgrB2S_DS1-5 SPW 25
Standalone script with explicit paths and minimal abstraction.
"""

import os
import glob

# Change to working directory
working_dir = '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/working_cubes'
if not os.path.exists(working_dir):
    os.makedirs(working_dir)
os.chdir(working_dir)

# Input measurement sets - try temp_line first, then consolidated
temp_vis = sorted(glob.glob('/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/temp_line/uid*_DS15_spw25_line.ms'))
cons_vis = sorted(glob.glob('/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/measurement_sets/uid*targets_line.ms'))

if len(temp_vis) > 0:
    vis_list = temp_vis
    datacolumn = 'data'
    spw_selection = ''
    print(f"Using {len(vis_list)} temp_line MS files")
elif len(cons_vis) > 0:
    vis_list = cons_vis
    datacolumn = 'corrected'
    spw_selection = '25'
    print(f"Using {len(vis_list)} consolidated MS files")
else:
    raise RuntimeError("No measurement sets found!")

# Output directory and image name
output_dir = '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/cube_images'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

imagename = 'oussid.SgrB2_SgrB2S_DS1-5_sci.spw25.cube.I'

# Imaging parameters
print("="*80)
print(f"IMAGING: SgrB2S_DS1-5 SPW 25")
print(f"  vis: {len(vis_list)} MS files")
print(f"  datacolumn: {datacolumn}")
print(f"  spw: {spw_selection}")
print(f"  output: {imagename}")
print("="*80)

tclean(
    vis=vis_list,
    field='SgrB2S_DS1-5',
    spw=spw_selection,
    intent='OBSERVE_TARGET#ON_SOURCE',
    datacolumn=datacolumn,
    imagename=imagename,
    imsize=[2880, 2880],
    cell='0.025arcsec',
    phasecenter='ICRS 17:47:20.026849 -028.23.46.89155',
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

# Move images to output directory
print(f"\nMoving images to {output_dir}/")
os.system(f"mv {imagename}.* {output_dir}/ 2>/dev/null")

print(f"\nCompleted: SgrB2S_DS1-5 SPW 25")
