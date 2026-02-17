"""
Chunked cube imaging script for SgrB2.

This script images a single channel chunk of a cube for a given field+SPW.
It is meant to be called by a SLURM array job, with parameters passed via
environment variables:

    FIELD       - CASA field name (e.g., 'DS9', 'DS6', 'DS7-DS8', 'SgrB2S_DS1-5')
    SPW         - Spectral window number (23, 25, 27, 29)
    STARTCHAN   - Starting channel number for this chunk
    NCHAN_CHUNK - Number of channels per chunk
    WORK_DIR    - Working directory for output (absolute path)

Follows the pattern from brick-jwst-2221/alma/reduction/slurm_subjob_jwbrick.py
"""

import os
import sys
import shutil

def logprint(string, origin='sgrb2_chunk_imaging.py', priority='INFO', flush=True):
    print(string, flush=flush)
    casalog.post(string, origin=origin, priority=priority)

logprint(f"CASA log file: {casalog.logfile()}")

# ===========================
# Read environment variables
# ===========================

field = os.getenv('FIELD')
if field is None:
    raise ValueError("FIELD environment variable must be set")

spw = os.getenv('SPW')
if spw is None:
    raise ValueError("SPW environment variable must be set")

startchan = int(os.getenv('STARTCHAN', '0'))

nchan_chunk = int(os.getenv('NCHAN_CHUNK', '32'))

work_dir = os.getenv('WORK_DIR')
if work_dir is None:
    raise ValueError("WORK_DIR environment variable must be set")

domerge = os.getenv('DOMERGE', '0') == '1'

print(f"SgrB2 chunked imaging")
print(f"  FIELD={field}")
print(f"  SPW={spw}")
print(f"  STARTCHAN={startchan}")
print(f"  NCHAN_CHUNK={nchan_chunk}")
print(f"  WORK_DIR={work_dir}")
print(f"  DOMERGE={domerge}")

# ===========================
# Field configuration
# ===========================

BASE = '/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final'

# SgrB2S_DS1-5        17:47:20.026849 -28.23.46.89155 ICRS    4         950400
# DS6                 17:47:21.120900 -28.24.18.26700 ICRS    5         950400
# DS7-DS8             17:47:22.119692 -28.24.37.58403 ICRS    1         950400
# DS9                 17:47:23.456900 -28.25.52.09900 ICRS    6         950400

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

if field not in FIELD_CONFIG:
    raise ValueError(f"Unknown field '{field}'. Must be one of: {list(FIELD_CONFIG.keys())}")

cfg = FIELD_CONFIG[field]

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

# Build vis list
if cfg['use_temp_line']:
    vis_list = [f"{BASE}/temp_line/{uid}_{cfg['ms_key']}_spw{spw}_line.ms" for uid in MS_UIDS]
    datacolumn = 'data'
    # CRITICAL: temp_line MS files contain ALL SPWs (not split), so we MUST specify the SPW
    # The SPW numbers in temp_line MS are still 23, 25, 27, 29 (not renumbered)
    spw_selection = str(spw)
else:
    vis_list = [f"{BASE}/measurement_sets/{uid}_targets_line.ms" for uid in MS_UIDS]
    datacolumn = 'corrected'
    spw_selection = str(spw)

# Verify vis files exist
missing = [v for v in vis_list if not os.path.exists(v)]
if missing:
    raise FileNotFoundError(f"Missing MS files:\n" + "\n".join(missing))

# SPW-specific parameters
# SPW 23: pipeline specifies explicit start/width, 1916 total channels
# SPW 25,27: 1920 channels, use native gridding
# SPW 29: 3840 channels (highest resolution SPW), use native gridding
SPW_PARAMS = {
    '23': {'totalnchan': 1916, 'start': '', 'width': ''},
    '25': {'totalnchan': 1920, 'start': '', 'width': ''},
    '27': {'totalnchan': 1920, 'start': '', 'width': ''},
    '29': {'totalnchan': 3840, 'start': '', 'width': ''},
}

if spw not in SPW_PARAMS:
    raise ValueError(f"Unknown SPW '{spw}'. Must be one of: {list(SPW_PARAMS.keys())}")

spw_cfg = SPW_PARAMS[spw]
totalnchan = spw_cfg['totalnchan']

# ===========================
# Merge mode
# ===========================

if domerge:
    os.chdir(work_dir)
    print(f"Merging in {os.getcwd()}")

    field_clean = field.replace('_', '')
    basename = f"oussid.SgrB2_{field_clean}_sci.spw{spw}"

    # Note: restoration=False means no .image file is produced;
    # the deconvolution products are .residual, .model, .mask, .psf, .pb, .sumwt
    for suffix in (".residual", ".model", ".mask", ".pb", ".psf", ".weight", ".sumwt"):
        infiles = [f'{basename}.{ii:04d}+{nchan_chunk:03d}.cube.I{suffix}'
                   for ii in range(0, totalnchan, nchan_chunk)]

        # Filter to only existing files (last chunk may be smaller)
        existing = [f for f in infiles if os.path.exists(f)]
        missing_files = [f for f in infiles if not os.path.exists(f)]

        if missing_files:
            print(f"WARNING: {len(missing_files)} chunk files missing for {suffix}:")
            for f in missing_files[:5]:
                print(f"  {f}")
            if len(missing_files) > 5:
                print(f"  ... and {len(missing_files)-5} more")

        if not existing:
            print(f"SKIPPING {suffix}: no chunk files found")
            continue

        outfile = f'{basename}.cube.I{suffix}'
        if os.path.exists(outfile):
            print(f"SKIPPING {suffix}: merged output already exists: {outfile}")
            continue

        print(f"Merging {len(existing)} files into {outfile}")
        ia.imageconcat(outfile=outfile, infiles=existing, mode='p', relax=True)

    # Create .image if it doesn't exist
    outimage = f'{basename}.cube.I.image'
    if not os.path.exists(outimage):
        print(f"\n.image does not exist, creating from model+residual with common beam...")
        
        # Determine common beam from merged .psf or first chunk
        merged_psf = f'{basename}.cube.I.psf'
        if os.path.exists(merged_psf):
            ia.open(merged_psf)
            beam_info = ia.restoringbeam()
            ia.close()
            if 'beams' in beam_info:
                # Multi-beam case: use median beam
                # Each channel has a beam stored as beams['*0']['*0'], beams['*1']['*0'], etc.
                major_list = []
                minor_list = []
                pa_list = []
                for chan_key in beam_info['beams']:
                    beam = beam_info['beams'][chan_key]['*0']  # Get the single beam for this channel
                    major_list.append(beam['major']['value'])
                    minor_list.append(beam['minor']['value'])
                    pa_list.append(beam['positionangle']['value'])
                
                import numpy as np
                major_unit = list(beam_info['beams'].values())[0]['*0']['major']['unit']
                minor_unit = list(beam_info['beams'].values())[0]['*0']['minor']['unit']
                pa_unit = list(beam_info['beams'].values())[0]['*0']['positionangle']['unit']
                
                common_beam = {
                    'major': {'value': np.median(major_list), 'unit': major_unit},
                    'minor': {'value': np.median(minor_list), 'unit': minor_unit},
                    'pa': {'value': np.median(pa_list), 'unit': pa_unit}
                }
            else:
                # Single beam case
                common_beam = {
                    'major': beam_info['major'],
                    'minor': beam_info['minor'],
                    'pa': beam_info.get('positionangle', beam_info.get('pa'))
                }
            print(f"  Common beam: {common_beam['major']['value']:.3f}{common_beam['major']['unit']} x {common_beam['minor']['value']:.3f}{common_beam['minor']['unit']}, PA={common_beam['pa']['value']:.1f}{common_beam['pa']['unit']}")
        else:
            raise FileNotFoundError(f"Cannot determine common beam: {merged_psf} not found")
        
        # Process each chunk: convolve model and add to residual
        chunk_images = []
        for ii in range(0, totalnchan, nchan_chunk):
            chunk_base = f'{basename}.{ii:04d}+{nchan_chunk:03d}.cube.I'
            chunk_model = f'{chunk_base}.model'
            chunk_residual = f'{chunk_base}.residual'
            chunk_image = f'{chunk_base}.image'
            
            if not os.path.exists(chunk_model) or not os.path.exists(chunk_residual):
                print(f"  SKIPPING chunk {ii:04d}: model or residual missing")
                continue
            
            if os.path.exists(chunk_image):
                print(f"  Chunk {ii:04d}: .image already exists")
                chunk_images.append(chunk_image)
                continue
            
            print(f"  Creating chunk {ii:04d} .image...")
            
            # Convolve model to common beam
            chunk_model_conv = f'{chunk_base}.model.conv'
            if os.path.exists(chunk_model_conv):
                shutil.rmtree(chunk_model_conv)
            
            imsmooth(
                imagename=chunk_model,
                kernel='gauss',
                major=f"{common_beam['major']['value']}{common_beam['major']['unit']}",
                minor=f"{common_beam['minor']['value']}{common_beam['minor']['unit']}",
                pa=f"{common_beam['pa']['value']}{common_beam['pa']['unit']}",
                targetres=True,
                outfile=chunk_model_conv
            )
            
            # Add convolved model to residual
            immath(
                imagename=[chunk_model_conv, chunk_residual],
                expr='IM0 + IM1',
                outfile=chunk_image
            )
            
            # Set proper restoring beam in header
            ia.open(chunk_image)
            ia.setrestoringbeam(
                major=f"{common_beam['major']['value']}{common_beam['major']['unit']}",
                minor=f"{common_beam['minor']['value']}{common_beam['minor']['unit']}",
                pa=f"{common_beam['pa']['value']}{common_beam['pa']['unit']}"
            )
            ia.close()
            
            # Clean up temporary convolved model
            shutil.rmtree(chunk_model_conv)
            
            chunk_images.append(chunk_image)
        
        # Concatenate chunk .image files
        if chunk_images:
            print(f"\n  Concatenating {len(chunk_images)} chunk .image files...")
            ia.imageconcat(outfile=outimage, infiles=chunk_images, mode='p', relax=True)
            print(f"  Created {outimage}")
        else:
            print("  ERROR: No chunk .image files to concatenate")
    else:
        print(f"\n.image already exists: {outimage}")

    # Cleanup: remove chunk files after successful merge
    cleanup = os.getenv('CLEANUP_CHUNKS', '1') == '1'
    if cleanup:
        print("\nCleaning up chunk files...")
        cleaned = 0
        for suffix in (".residual", ".model", ".mask", ".pb", ".psf", ".weight", ".sumwt", ".image"):
            merged = f'{basename}.cube.I{suffix}'
            if not os.path.exists(merged):
                print(f"  Skipping cleanup for {suffix}: merged file does not exist")
                continue
            for ii in range(0, totalnchan, nchan_chunk):
                chunk = f'{basename}.{ii:04d}+{nchan_chunk:03d}.cube.I{suffix}'
                if os.path.exists(chunk):
                    shutil.rmtree(chunk)
                    cleaned += 1
        print(f"  Removed {cleaned} chunk files")

    print("Merge complete!")
    sys.exit(0)

# ===========================
# Imaging mode (single chunk)
# ===========================

os.makedirs(work_dir, exist_ok=True)
os.chdir(work_dir)
print(f"Working in {os.getcwd()}")

field_clean = field.replace('_', '')
imagename = f"oussid.SgrB2_{field_clean}_sci.spw{spw}.{startchan:04d}+{nchan_chunk:03d}.cube.I"

# Check if this chunk is already done (use .residual since restoration=False)
if os.path.exists(f"{imagename}.residual"):
    print(f"SKIPPING: {imagename}.residual already exists")
    sys.exit(0)
elif os.path.exists(f"{imagename}.psf"):
    print(f"SKIPPING: {imagename}.psf already exists (either it's in progress or broken)")
    sys.exit(1)

# Clamp nchan if we'd go past the end
actual_nchan = min(nchan_chunk, totalnchan - startchan)
if actual_nchan <= 0:
    print(f"SKIPPING: startchan={startchan} >= totalnchan={totalnchan}, nothing to image")
    # This is an error and should return a failure state
    sys.exit(1)

# For SPW 23 that has explicit start/width, we need to use channel-based start
# For other SPWs with start='', tclean uses native MS channels
if spw_cfg['start']:
    # SPW 23: start is a frequency, offset by startchan * width
    import numpy as np
    start_freq_ghz = float(spw_cfg['start'].replace('GHz', ''))
    width_mhz = float(spw_cfg['width'].replace('MHz', ''))
    chunk_start_freq = start_freq_ghz + (startchan * width_mhz / 1000.0)
    tclean_start = f'{chunk_start_freq:.10f}GHz'
    tclean_width = spw_cfg['width']
else:
    # SPW 25, 27, 29: use channel-based start
    tclean_start = startchan
    tclean_width = ''

print(f"\nImaging chunk:")
print(f"  imagename: {imagename}")
print(f"  field: {field}")
print(f"  spw_selection: '{spw_selection}'")
print(f"  datacolumn: {datacolumn}")
print(f"  nchan: {actual_nchan}")
print(f"  start: {tclean_start}")
print(f"  width: {tclean_width}")
print(f"  phasecenter: {cfg['phasecenter']}")
print(f"  vis: {len(vis_list)} MS files")

tclean(
    vis=vis_list,
    field=field,
    spw=spw_selection,
    intent='OBSERVE_TARGET#ON_SOURCE',
    datacolumn=datacolumn,
    imagename=imagename,
    imsize=[2880, 2880],
    cell='0.025arcsec',
    phasecenter=cfg['phasecenter'],
    stokes='I',
    specmode='cube',
    nchan=actual_nchan,
    start=tclean_start,
    width=tclean_width,
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

print(f"\nCompleted chunk: {imagename}")
