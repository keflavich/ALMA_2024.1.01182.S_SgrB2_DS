"""
Image CH3OH 9(0,9)-8(1,8) line at 146.618697 GHz for all 4 fields.

Velocity range: -25 to +125 km/s
Cell size: 0.0125" (2x higher resolution)
Image size: 5760x5760 pixels (2x larger)
"""

import os
import sys
from astropy import constants as const
from astropy import units as u

def logprint(string, origin='image_ch3oh_line.py', priority='INFO', flush=True):
    print(string, flush=flush)
    casalog.post(string, origin=origin, priority=priority)

logprint(f"CASA log file: {casalog.logfile()}")

# ===========================
# Configuration
# ===========================

BASE = '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final'
OUTPUT_DIR = f'{BASE}/ch3oh_line_images'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Line parameters
REST_FREQ_GHZ = 146.618697  # CH3OH 9(0,9)-8(1,8)
VMIN_KMS = -25.0
VMAX_KMS = 125.0

# Convert velocity range to frequency range (radio definition)
c_kms = const.c.to(u.km/u.s).value
# ν = ν_0 * (1 - v/c)
freq_at_vmax = REST_FREQ_GHZ * (1 - VMAX_KMS / c_kms)  # Low freq (high velocity)
freq_at_vmin = REST_FREQ_GHZ * (1 - VMIN_KMS / c_kms)  # High freq (low velocity)

print(f"\nCH3OH line imaging setup:")
print(f"  Rest frequency: {REST_FREQ_GHZ:.6f} GHz")
print(f"  Velocity range: {VMIN_KMS} to {VMAX_KMS} km/s")
print(f"  Frequency range: {freq_at_vmax:.6f} to {freq_at_vmin:.6f} GHz")
print(f"  Bandwidth: {(freq_at_vmin - freq_at_vmax)*1000:.3f} MHz")

# Field configuration
FIELD_CONFIG = {
    'SgrB2S_DS1-5': {
        'phasecenter': 'ICRS 17:47:20.026849 -028.23.46.89155',
        'ms_key': 'DS15',
        'use_temp_line': False,
    },
    'DS6': {
        'phasecenter': 'ICRS 17:47:21.120900 -028.24.18.26700',
        'ms_key': 'DS6',
        'use_temp_line': True,
    },
    'DS7-DS8': {
        'phasecenter': 'ICRS 17:47:22.119692 -028.24.37.58403',
        'ms_key': 'DS7DS8',
        'use_temp_line': True,
    },
    'DS9': {
        'phasecenter': 'ICRS 17:47:23.456900 -028.25.52.09900',
        'ms_key': 'DS9',
        'use_temp_line': True,
    },
}

# MS UID stems (common to all fields)
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

# SPW 27 contains the CH3OH line at 146.618697 GHz
# SPW 27 range: 144.836 - 146.710 GHz
SPW = '27'

# ===========================
# Image each field
# ===========================

for field, cfg in FIELD_CONFIG.items():
    print(f"\n{'='*70}")
    print(f"Imaging field: {field}")
    print(f"{'='*70}")
    
    # Build vis list
    if cfg['use_temp_line']:
        vis_list = [f"{BASE}/temp_line/{uid}_{cfg['ms_key']}_spw{SPW}_line.ms" for uid in MS_UIDS]
        datacolumn = 'data'
        spw_selection = SPW  # Must specify SPW for temp_line files
    else:
        vis_list = [f"{BASE}/measurement_sets/{uid}_targets_line.ms" for uid in MS_UIDS]
        datacolumn = 'corrected'
        spw_selection = SPW
    
    # Verify vis files exist
    missing = [v for v in vis_list if not os.path.exists(v)]
    if missing:
        print(f"ERROR: Missing MS files for {field}:")
        for m in missing[:3]:
            print(f"  {m}")
        if len(missing) > 3:
            print(f"  ... and {len(missing)-3} more")
        print("SKIPPING this field")
        continue
    
    # Output image name
    field_clean = field.replace('_', '')
    imagename = f"{OUTPUT_DIR}/ch3oh_146.619GHz_{field_clean}"
    
    # Check if already exists
    if os.path.exists(f"{imagename}.image"):
        print(f"SKIPPING: {imagename}.image already exists")
        continue
    
    print(f"\nImaging parameters:")
    print(f"  imagename: {imagename}")
    print(f"  field: {field}")
    print(f"  spw: {spw_selection}")
    print(f"  datacolumn: {datacolumn}")
    print(f"  phasecenter: {cfg['phasecenter']}")
    print(f"  imsize: 5760x5760 pixels")
    print(f"  cell: 0.0125 arcsec")
    print(f"  start: {freq_at_vmax:.6f}GHz")
    print(f"  width: (native channel width)")
    print(f"  vis: {len(vis_list)} MS files")
    
    # Run tclean
    tclean(
        vis=vis_list,
        field=field,
        spw=spw_selection,
        intent='OBSERVE_TARGET#ON_SOURCE',
        datacolumn=datacolumn,
        imagename=imagename,
        imsize=[5760, 5760],
        cell='0.0125arcsec',
        phasecenter=cfg['phasecenter'],
        stokes='I',
        specmode='cube',
        nchan=-1,  # Use all channels in frequency range
        start=f'{freq_at_vmax:.10f}GHz',
        width='',  # Native channel width
        outframe='LSRK',
        restfreq=f'{REST_FREQ_GHZ}GHz',
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
        threshold='1.0mJy',
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
    
    print(f"\nCompleted: {field}")

print(f"\n{'='*70}")
print("All fields imaged!")
print(f"{'='*70}")
