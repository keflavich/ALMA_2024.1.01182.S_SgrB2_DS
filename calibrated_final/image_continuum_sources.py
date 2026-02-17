"""
Image 2x2" cutouts around bright continuum sources DS1-DS9 with high resolution.

Cell size: 0.0125" (high resolution)
Image size: 160x160 pixels (2" / 0.0125" = 160)
Full spectral coverage for each SPW
"""

import os
import sys

def logprint(string, origin='image_continuum_sources.py', priority='INFO', flush=True):
    print(string, flush=flush)
    casalog.post(string, origin=origin, priority=priority)

logprint(f"CASA log file: {casalog.logfile()}")

# ===========================
# Configuration
# ===========================

BASE = '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final'
OUTPUT_DIR = f'{BASE}/continuum_source_cutouts'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Continuum source positions (from Jeff+ 2024)
SOURCES = {
    'DS1': {'ra': '17:47:19.58', 'dec': '-28:23:49.9', 'vsys': 56.2},
    'DS2': {'ra': '17:47:20.05', 'dec': '-28:23:46.7', 'vsys': 48.7},
    'DS3': {'ra': '17:47:19.99', 'dec': '-28:23:48.9', 'vsys': 52.8},
    'DS4': {'ra': '17:47:19.77', 'dec': '-28:23:43.5', 'vsys': 54.6},
    'DS5': {'ra': '17:47:19.71', 'dec': '-28:23:51.6', 'vsys': 55.1},
    'DS6': {'ra': '17:47:21.12', 'dec': '-28:24:18.3', 'vsys': 49.8},
    'DS7': {'ra': '17:47:22.23', 'dec': '-28:24:34.0', 'vsys': 48.7},
    'DS8': {'ra': '17:47:22.04', 'dec': '-28:24:42.6', 'vsys': 49.8},
    'DS9': {'ra': '17:47:23.46', 'dec': '-28:25:52.1', 'vsys': 47.3},
}

# Determine parent field for each source (needed to select correct MS)
SOURCE_TO_FIELD = {
    'DS1': 'SgrB2S_DS1-5',
    'DS2': 'SgrB2S_DS1-5',
    'DS3': 'SgrB2S_DS1-5',
    'DS4': 'SgrB2S_DS1-5',
    'DS5': 'SgrB2S_DS1-5',
    'DS6': 'DS6',
    'DS7': 'DS7-DS8',
    'DS8': 'DS7-DS8',
    'DS9': 'DS9',
}

# Field configuration (for MS selection)
FIELD_CONFIG = {
    'SgrB2S_DS1-5': {
        'ms_key': 'DS15',
        'use_temp_line': False,
    },
    'DS6': {
        'ms_key': 'DS6',
        'use_temp_line': True,
    },
    'DS7-DS8': {
        'ms_key': 'DS7DS8',
        'use_temp_line': True,
    },
    'DS9': {
        'ms_key': 'DS9',
        'use_temp_line': True,
    },
}

# MS UID stems
MS_UIDS = [
    'uid___A002_X12c4b14_X77b0',
    'uid___A002_X12c7631_X2152',
    'uid___A002_X12c99be_Xa92b',
    'uid___A002_X12cdde9_Xb8e6',
    'uid___A002_X12d0dd8_Xbca',
    'uid___A002_X12d2ac0_X13ec',
    'uid___A002_X12d2ac0_X72e2',
    'uid___A002_X12d4098_X223c',
    'uid___A002_X12de9a8_X8e3e',
    'uid___A002_X12de9a8_X954b',
]

# SPWs to image
SPWS = ['23', '25', '27', '29']

# ===========================
# Image each source and SPW
# ===========================

for source_name, source_info in SOURCES.items():
    parent_field = SOURCE_TO_FIELD[source_name]
    cfg = FIELD_CONFIG[parent_field]
    
    # Format phasecenter
    phasecenter = f"ICRS {source_info['ra']} {source_info['dec']}"
    
    print(f"\n{'='*70}")
    print(f"Source: {source_name} (in field {parent_field})")
    print(f"  Position: {phasecenter}")
    print(f"  Systemic velocity: {source_info['vsys']} km/s")
    print(f"{'='*70}")
    
    for spw in SPWS:
        print(f"\n--- SPW {spw} ---")
        
        # Build vis list
        if cfg['use_temp_line']:
            vis_list = [f"{BASE}/temp_line/{uid}_{cfg['ms_key']}_spw{spw}_line.ms" for uid in MS_UIDS]
            datacolumn = 'data'
            spw_selection = spw  # Must specify SPW for temp_line files
        else:
            vis_list = [f"{BASE}/measurement_sets/{uid}_targets_line.ms" for uid in MS_UIDS]
            datacolumn = 'corrected'
            spw_selection = spw
        
        # Verify vis files exist
        missing = [v for v in vis_list if not os.path.exists(v)]
        if missing:
            print(f"ERROR: Missing MS files for {source_name} SPW {spw}:")
            for m in missing[:3]:
                print(f"  {m}")
            if len(missing) > 3:
                print(f"  ... and {len(missing)-3} more")
            print("SKIPPING this SPW")
            continue
        
        # Output image name
        imagename = f"{OUTPUT_DIR}/{source_name}_spw{spw}_cutout"
        
        # Check if already exists
        if os.path.exists(f"{imagename}.image"):
            print(f"SKIPPING: {imagename}.image already exists")
            continue
        
        print(f"Imaging parameters:")
        print(f"  imagename: {imagename}")
        print(f"  field: {parent_field}")
        print(f"  phasecenter: {phasecenter}")
        print(f"  spw: {spw_selection}")
        print(f"  datacolumn: {datacolumn}")
        print(f"  imsize: 160x160 pixels (2 arcsec)")
        print(f"  cell: 0.0125 arcsec")
        print(f"  vis: {len(vis_list)} MS files")
        
        # Run tclean
        tclean(
            vis=vis_list,
            field=parent_field,
            spw=spw_selection,
            intent='OBSERVE_TARGET#ON_SOURCE',
            datacolumn=datacolumn,
            imagename=imagename,
            imsize=[160, 160],
            cell='0.0125arcsec',
            phasecenter=phasecenter,
            stokes='I',
            specmode='cube',
            nchan=-1,  # All channels in SPW
            start='',
            width='',
            outframe='LSRK',
            perchanweightdensity=True,
            gridder='standard',
            mosweight=False,
            usepointing=False,
            pblimit=0.2,
            deconvolver='hogbom',
            restoration=True,
            restoringbeam='common',
            pbcor=True,
            weighting='briggsbwtaper',
            robust=0.5,
            npixels=0,
            niter=10000,
            threshold='0.5mJy',
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
        
        print(f"Completed: {source_name} SPW {spw}")

print(f"\n{'='*70}")
print("All sources and SPWs imaged!")
print(f"{'='*70}")
