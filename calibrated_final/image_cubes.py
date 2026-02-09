#!/usr/bin/env python
"""
Script to create spectral line image cubes for SgrB2 observations.
Uses pre-calibrated and continuum-subtracted measurement sets.

This script images each target source (DS1-5, DS6, DS7-8, DS9) in each 
spectral window (23, 25, 27, 29) using CASA's tclean.

Usage:
    casa -c image_cubes.py <cube_id>
    
Where cube_id is an integer from 0 to 15 identifying which cube to image.
"""

import sys
import os
import glob
from astropy.coordinates import SkyCoord
import astropy.units as u

# ===========================
# CONFIGURATION
# ===========================

# Source/field definitions with phase centers
# Field names MUST match those in the measurement sets
# Phase centers extracted from measurement sets (ICRS J2000):
# Order is important - must match cube_id mapping
SOURCE_ORDER = ['SgrB2S_DS1-5', 'DS6', 'DS7-DS8', 'DS9']
SOURCES = {
    'SgrB2S_DS1-5': 'ICRS 17:47:20.0268 -028.23.46.892',
    'DS6':          'ICRS 17:47:20.0222 -028.23.44.670',
    'DS7-DS8':      'ICRS 17:47:20.0260 -028.23.45.930',
    'DS9':          'ICRS 17:47:20.0302 -028.23.47.670',
}

# Spectral windows to image
SPWS = ['23', '25', '27', '29']

# SPW-specific parameters from pipeline
# Based on pipeline run pipeline-20251119T065601 and pipeline-20251217T191756
SPW_PARAMS = {
    '23': {
        'nchan': 1916,
        'start': '132.8931835956GHz',
        'width': '0.9766485MHz',
    },
    '25': {
        'nchan': -1,  # Use all channels
        'start': '',
        'width': '',
    },
    '27': {
        'nchan': -1,
        'start': '',
        'width': '',
    },
    '29': {
        'nchan': -1,
        'start': '',
        'width': '',
    },
}

# Imaging parameters (adapted from pipeline)
# Field of view: ~72 arcsec (2880 pixels × 0.025 arcsec/pixel)
# Note: Original pipeline used 11520 pixels × 0.0063 arcsec/pixel for same FOV
# Reduced pixel count with larger pixels for manageable cube sizes
IMSIZE = [2880, 2880]  # pixels
CELL = '0.025arcsec'   # pixel size - DO NOT change without adjusting IMSIZE
ROBUST = 0.5
WEIGHTING = 'briggsbwtaper'
OUTFRAME = 'LSRK'
PBLIMIT = 0.2
DECONVOLVER = 'hogbom'
NITER = 1000 
THRESHOLD = '1.5mJy' # expected RMS ~ 800uJy/beam
PERCHANWEIGHTDENSITY = True
GRIDDER = 'standard'
NTERMS = 2  # For MFS images; set to 1 for cube

# Mitigation parameters
MAXCUBESIZE = 1040.  # GB
MAXCUBELIMIT = 1060.  # GB

# ===========================
# FUNCTIONS
# ===========================

def get_cube_config(cube_id):
    """
    Get the configuration for a specific cube based on ID.
    
    Returns (source, spw)
    """
    # Create all combinations of sources and SPWs in specified order
    cube_configs = []
    for source in SOURCE_ORDER:
        for spw in SPWS:
            cube_configs.append((source, spw))
    
    if cube_id >= len(cube_configs):
        raise ValueError(f"cube_id {cube_id} is out of range (0-{len(cube_configs)-1})")
    
    source, spw = cube_configs[cube_id]
    return source, spw


def get_phasecenter(ms_list, field):
    """
    Extract phase center from measurement set for a given field.
    Uses astropy for proper coordinate conversion.
    """
    from casatools import msmetadata
    msmd = msmetadata()
    
    # Open first MS and get phase center
    msmd.open(ms_list[0])
    field_ids = msmd.fieldsforname(field)
    if len(field_ids) == 0:
        msmd.close()
        raise ValueError(f"Field {field} not found in {ms_list[0]}")
    
    direction = msmd.phasecenter(field_ids[0])
    msmd.close()
    
    # Convert to ICRS string format using astropy
    # CASA returns radians
    ra_rad = direction['m0']['value']
    dec_rad = direction['m1']['value']
    
    # Create SkyCoord object from radians
    coord = SkyCoord(ra=ra_rad*u.rad, dec=dec_rad*u.rad, frame='icrs')
    
    # Format as CASA-compatible string
    # CASA format: "ICRS HH:MM:SS.SSSS +DD.MM.SS.SSS"
    ra_str = coord.ra.to_string(unit=u.hour, sep=':', precision=4, pad=True)
    dec_str = coord.dec.to_string(unit=u.deg, sep='.', precision=3, 
                                   alwayssign=True, pad=True)
    
    phasecenter = f"ICRS {ra_str} {dec_str}"
    
    return phasecenter


def run_imaging(source, spw, output_dir='cube_images'):
    """
    Run tclean to create a spectral cube for the given source and spw.
    """
    print("="*80)
    print(f"IMAGING: Source={source}, SPW={spw}")
    print("="*80)
    
    # Get continuum-subtracted measurement sets
    # First try measurement_sets/*_targets_line.ms (consolidated)
    vis_pattern = '../measurement_sets/uid*targets_line.ms'
    all_vis_list = sorted(glob.glob(vis_pattern))
    
    # Also check temp_line/ for field/SPW-specific files
    # Map source name to MS field name (DS7-DS8 → DS7DS8)
    field_name = source.replace('SgrB2S_', '').replace('-', '')
    temp_pattern = '../temp_line/uid*_{field}_spw{spw}_line.ms'.format(field=field_name, spw=spw)
    temp_vis_list = sorted(glob.glob(temp_pattern))
    
    if len(temp_vis_list) > 0:
        # Use temp_line files for this specific field+SPW
        vis_list = temp_vis_list
        # uvcontsub output has continuum-subtracted data in DATA column
        datacolumn = 'data'
        # temp_line files are already filtered by SPW, so don't specify spw again
        spw_selection = ''
        print(f"Found {len(vis_list)} field/SPW-specific measurement sets in temp_line/")
        print(f"Using DATA column (uvcontsub output)")
        print(f"SPW selection: '' (pre-filtered by uvcontsub)")
    elif len(all_vis_list) > 0:
        # Use consolidated files (tclean will filter)
        vis_list = all_vis_list
        # Consolidated pipeline files use CORRECTED_DATA
        datacolumn = 'corrected'
        # Need to select SPW from the consolidated files
        spw_selection = spw
        print(f"Found {len(vis_list)} measurement sets total")
        print(f"Using CORRECTED_DATA column")
        print(f"SPW selection: {spw}")
    else:
        print(f"ERROR: No continuum-subtracted measurement sets found")
        print(f"  Tried: {vis_pattern}")
        print(f"  Tried: {temp_pattern}")
        print("Please run continuum subtraction first.")
        sys.exit(1)
    
    print(f"Using {len(vis_list)} measurement sets for {source} SPW {spw}")
    
    # Get phase center for this source
    
    # Get phase center for this source
    if SOURCES[source]:
        phasecenter = SOURCES[source]
    else:
        print(f"Determining phase center for {source}...")
        phasecenter = get_phasecenter(vis_list, source)
        print(f"Phase center: {phasecenter}")
    
    # Create output directory if needed
    if not os.path.exists(f"../{output_dir}"):
        os.makedirs(f"../{output_dir}")
    
    # Get SPW-specific parameters
    spw_params = SPW_PARAMS.get(spw, {})
    nchan = spw_params.get('nchan', -1)
    start = spw_params.get('start', '')
    width = spw_params.get('width', '')
    
    # Output image name
    imagename = f"oussid.SgrB2_{source}_sci.spw{spw}.cube.I"
    
    print(f"\nImaging parameters:")
    print(f"  imagename: {imagename}")
    print(f"  field: {source}")
    print(f"  spw: {spw}")
    print(f"  phasecenter: {phasecenter}")
    print(f"  imsize: {IMSIZE}")
    print(f"  cell: {CELL}")
    print(f"  nchan: {nchan}")
    print(f"  start: {start}")
    print(f"  width: {width}")
    print(f"  robust: {ROBUST}")
    print(f"  niter: {NITER}")
    print()
    
    # Run tclean to create spectral cube
    tclean(
        vis=vis_list,
        field=source,
        spw=spw_selection,
        intent='OBSERVE_TARGET#ON_SOURCE',
        datacolumn=datacolumn,
        imagename=imagename,
        imsize=IMSIZE,
        cell=CELL,
        phasecenter=phasecenter,
        stokes='I',
        specmode='cube',
        nchan=nchan,
        start=start,
        width=width,
        outframe=OUTFRAME,
        perchanweightdensity=PERCHANWEIGHTDENSITY,
        gridder=GRIDDER,
        mosweight=False,
        usepointing=False,
        pblimit=PBLIMIT,
        deconvolver=DECONVOLVER,
        restoration=False,
        restoringbeam='common',
        pbcor=False,
        weighting=WEIGHTING,
        robust=ROBUST,
        npixels=0,
        niter=NITER,
        threshold=THRESHOLD,
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
    os.system(f"mv {imagename}.* ../{output_dir}/ 2>/dev/null")
    
    print(f"\nCompleted imaging for {source} SPW {spw}")
    print("="*80)


# ===========================
# MAIN
# ===========================

if __name__ == '__main__':
    # Get cube ID from command line
    if len(sys.argv) < 2:
        print("ERROR: cube_id not provided")
        print("Usage: casa -c image_cubes.py <cube_id>")
        print()
        print("Available cube IDs:")
        cube_id = 0
        for source in SOURCE_ORDER:
            for spw in SPWS:
                print(f"  {cube_id:2d}: {source:15s} SPW {spw}")
                cube_id += 1
        sys.exit(1)
    
    cube_id = int(sys.argv[-1])
    
    # Get configuration for this cube
    source, spw = get_cube_config(cube_id)
    
    # Change to working directory
    if not os.path.exists('working_cubes'):
        os.makedirs('working_cubes')
    os.chdir('working_cubes')
    
    # Run imaging
    run_imaging(source, spw, output_dir='cube_images')
    
    # Move back
    os.chdir('..')
    
    print(f"\nSUCCESS: Cube {cube_id} ({source} SPW {spw}) completed")
