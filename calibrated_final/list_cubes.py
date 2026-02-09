#!/usr/bin/env python
"""
Helper script to list all cube configurations and check which have been completed.

Usage:
    python list_cubes.py [--check]
    
Options:
    --check    Check which cubes have already been imaged
"""

import os
import sys

# Source definitions - must match field names in measurement sets
SOURCES = ['SgrB2S_DS1-5', 'DS6', 'DS7-DS8', 'DS9']
SPWS = ['23', '25', '27', '29']

def list_cubes(check=False):
    """List all cube configurations."""
    
    print("="*80)
    print("SgrB2 Cube Imaging Configuration")
    print("="*80)
    print()
    print(f"Total cubes to image: {len(SOURCES) * len(SPWS)}")
    print(f"Sources: {len(SOURCES)}")
    print(f"SPWs per source: {len(SPWS)}")
    print()
    
    if check:
        print("{:>4s}  {:20s}  {:>6s}  {:10s}".format("ID", "Source", "SPW", "Status"))
        print("-"*80)
    else:
        print("{:>4s}  {:20s}  {:>6s}".format("ID", "Source", "SPW"))
        print("-"*80)
    
    cube_id = 0
    completed = 0
    
    for source in SOURCES:
        for spw in SPWS:
            # Check if cube exists
            status = ""
            if check:
                # Check in cube_images directory
                image_pattern = f"cube_images/oussid.SgrB2_{source}_sci.spw{spw}.cube.I.image"
                if os.path.exists(image_pattern):
                    status = "DONE"
                    completed += 1
                else:
                    status = "PENDING"
                
                print(f"{cube_id:4d}  {source:20s}  {spw:>6s}  {status:10s}")
            else:
                print(f"{cube_id:4d}  {source:20s}  {spw:>6s}")
            
            cube_id += 1
    
    print("="*80)
    
    if check:
        print()
        print(f"Completed: {completed}/{len(SOURCES) * len(SPWS)}")
        print(f"Remaining: {len(SOURCES) * len(SPWS) - completed}")
        print()


def print_source_info():
    """Print information about each source and its spatial properties."""
    
    print()
    print("="*80)
    print("Source Information")
    print("="*80)
    print()
    print("Based on cont.dat file and pipeline logs:")
    print()
    print("  SgrB2S_DS1-5:")
    print("    - Phase center: ICRS 17:47:20.0268 -028.23.46.892")
    print("    - Note: DS1-5 represents 5 separate dust sources observed as one field")
    print("    - All observed together, so spatial overlap is 100%")
    print()
    print("  SgrB2S_DS6:")
    print("    - Phase center: TBD (will be extracted from MS)")
    print("    - Separate observation")
    print()
    print("  SgrB2S_DS7-8:")
    print("    - Phase center: TBD (will be extracted from MS)")  
    print("    - Note: DS7 and DS8 observed together as one field")
    print()
    print("  SgrB2S_DS9:")
    print("    - Phase center: TBD (will be extracted from MS)")
    print("    - Separate observation")
    print()
    print("All sources use the same spectral window setup:")
    print("  SPW 23: ~133-134 GHz")
    print("  SPW 25: ~135-137 GHz")
    print("  SPW 27: ~145-146 GHz")
    print("  SPW 29: ~147 GHz")
    print()
    print("Imaging parameters (from pipeline):")
    print("  Image size: 11520 x 11520 pixels")
    print("  Cell size: 0.0063 arcsec")
    print("  Robust: 0.5")
    print("  Weighting: briggsbwtaper")
    print("="*80)
    print()


if __name__ == '__main__':
    check = '--check' in sys.argv
    list_cubes(check=check)
    
    if '--info' in sys.argv or '--help' in sys.argv:
        print_source_info()
