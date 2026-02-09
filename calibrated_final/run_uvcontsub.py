#!/usr/bin/env python
"""
Run continuum subtraction for fields that are missing from the line measurement sets.

This script processes DS6, DS7-DS8, and DS9 for all SPWs (23, 25, 27, 29) by:
1. Reading continuum ranges from cont.dat
2. Running uvcontsub on each MS/field/SPW combination
3. Creating *_targets_line.ms files with continuum subtracted

Usage:
    casa -c run_uvcontsub.py
"""

import os
import sys
import glob
import shutil
from casatasks import uvcontsub

# Field name mapping: cont.dat uses different names than MSs
FIELD_NAME_MAP = {
    'SgrB2S_DS6': 'DS6',
    'SgrB2S_DS7-8': 'DS7-DS8',
    'SgrB2S_DS9': 'DS9'
}

# Fields to process (exclude SgrB2S_DS1-5 which is already done)
FIELDS_TO_PROCESS = ['DS6', 'DS7-DS8', 'DS9']

# SPWs to process
SPWS = ['23', '25', '27', '29']


def parse_cont_dat(cont_dat_path):
    """
    Parse cont.dat file to extract continuum ranges for each field and SPW.
    
    Returns:
        dict: {field: {spw: 'freq_ranges'}}
    """
    continuum_ranges = {}
    current_field = None
    current_spw = None
    
    with open(cont_dat_path, 'r') as f:
        for line in f:
            line = line.strip()
            
            if line.startswith('Field:'):
                current_field = line.split('Field:')[1].strip()
                if current_field not in continuum_ranges:
                    continuum_ranges[current_field] = {}
                current_spw = None
                
            elif line.startswith('SpectralWindow:'):
                # Extract SPW number
                parts = line.split()
                current_spw = parts[1]
                
            elif '~' in line and 'GHz' in line and current_field and current_spw:
                # This is a frequency range line
                if current_spw not in continuum_ranges[current_field]:
                    continuum_ranges[current_field][current_spw] = []
                continuum_ranges[current_field][current_spw].append(line)
    
    # Convert lists of ranges to semicolon-separated strings
    for field in continuum_ranges:
        for spw in continuum_ranges[field]:
            continuum_ranges[field][spw] = ';'.join(continuum_ranges[field][spw])
    
    return continuum_ranges


def check_field_in_ms(vis, field):
    """Check if a field exists in a measurement set."""
    from casatools import msmetadata
    msmd = msmetadata()
    msmd.open(vis)
    fields = list(msmd.fieldnames())
    msmd.close()
    return field in fields


def run_contsub_for_field_spw(vis, field, spw, fitspec):
    """
    Run uvcontsub for a specific field and SPW.
    
    Creates a temporary output MS for each field/SPW combo, which will need
    to be combined later.
    
    Args:
        vis: Input measurement set (non-line version)
        field: Field name
        spw: SPW number as string
        fitspec: Continuum frequency ranges for fitting
    """
    # Check if field exists in this MS
    if not check_field_in_ms(vis, field):
        print(f"  ✗ Field '{field}' not found in {vis.split('/')[-1]}")
        return False
    
    # Create unique output name for this field/SPW combo
    ms_basename = os.path.basename(vis).replace('_targets.ms', '')
    outputvis = f"temp_line/{ms_basename}_{field.replace('-','')}_spw{spw}_line.ms"
    
    # Create temp directory if needed
    if not os.path.exists('temp_line'):
        os.makedirs('temp_line')
    
    # If output exists, remove it (uvcontsub won't overwrite)
    if os.path.exists(outputvis):
        print(f"  ! Removing existing {os.path.basename(outputvis)}")
        shutil.rmtree(outputvis)
    
    # Convert fitspec to include SPW number (format: "spw:freq~freq;freq~freq")
    # The fitspec from cont.dat is just "freq~freq;freq~freq"
    # Remove " LSRK" suffix if present (uvcontsub doesn't accept it)
    fitspec_clean = fitspec.replace(' LSRK', '')
    fitspec_with_spw = f"{spw}:{fitspec_clean}"
    
    print(f"\n{'='*80}")
    print(f"Running uvcontsub:")
    print(f"  Input:  {vis.split('/')[-1]}")
    print(f"  Output: {os.path.basename(outputvis)}")
    print(f"  Field:  {field}")
    print(f"  SPW:    {spw}")
    print(f"  Fitspec: {fitspec_with_spw[:70]}...")
    print(f"{'='*80}")
    
    try:
        uvcontsub(
            vis=vis,
            outputvis=outputvis,
            field=field,
            fitspec=fitspec_with_spw,
            fitmethod='gsl',
            fitorder=1,
            writemodel=False
        )
        print(f"  ✓ Successfully created {os.path.basename(outputvis)}")
        return True
        
    except Exception as e:
        print(f"  ✗ ERROR: {str(e)}")
        return False


def main():
    """Main execution function."""
    
    # Parse cont.dat
    cont_dat_path = 'caltables/cont.dat'
    if not os.path.exists(cont_dat_path):
        print(f"ERROR: cont.dat not found at {cont_dat_path}")
        sys.exit(1)
    
    print(f"Reading continuum ranges from {cont_dat_path}...")
    continuum_ranges = parse_cont_dat(cont_dat_path)
    print(f"Found continuum definitions for {len(continuum_ranges)} fields")
    
    # Get all measurement sets (non-line versions)
    ms_pattern = 'measurement_sets/uid*_targets.ms'
    all_ms = sorted(glob.glob(ms_pattern))
    
    # Filter to only non-line MSs (exclude *_line.ms)
    all_ms = [ms for ms in all_ms if not ms.endswith('_targets_line.ms')]
    
    if len(all_ms) == 0:
        print(f"ERROR: No measurement sets found matching {ms_pattern}")
        sys.exit(1)
    
    print(f"Found {len(all_ms)} measurement sets to process")
    
    # Track statistics
    total_tasks = 0
    completed_tasks = 0
    skipped_tasks = 0
    
    # Process each field
    for field in FIELDS_TO_PROCESS:
        print(f"\n{'#'*80}")
        print(f"# Processing field: {field}")
        print(f"{'#'*80}")
        
        # Map to cont.dat field name
        cont_field = None
        for cont_name, ms_name in FIELD_NAME_MAP.items():
            if ms_name == field:
                cont_field = cont_name
                break
        
        if cont_field not in continuum_ranges:
            print(f"WARNING: No continuum ranges found for {field} (looked for {cont_field})")
            continue
        
        # Process each SPW
        for spw in SPWS:
            if spw not in continuum_ranges[cont_field]:
                print(f"\nWARNING: No continuum ranges for {field} SPW {spw}")
                continue
            
            fitspec = continuum_ranges[cont_field][spw]
            
            # Process each MS
            for vis in all_ms:
                total_tasks += 1
                
                # Check if this field exists in this MS
                if not check_field_in_ms(vis, field):
                    skipped_tasks += 1
                    continue
                
                success = run_contsub_for_field_spw(vis, field, spw, fitspec)
                if success:
                    completed_tasks += 1
    
    # Summary
    print(f"\n{'='*80}")
    print(f"CONTINUUM SUBTRACTION SUMMARY")
    print(f"{'='*80}")
    print(f"Total combinations checked: {total_tasks}")
    print(f"Skipped (field not in MS):  {skipped_tasks}")
    print(f"Successfully processed:      {completed_tasks}")
    print(f"Failed:                      {total_tasks - skipped_tasks - completed_tasks}")
    print(f"{'='*80}")
    
    print("\nNOTE: uvcontsub created temporary field/SPW-specific line MSs in temp_line/")
    print("      These need to be concatenated with the existing *_targets_line.ms files")
    print("      Run the concat_line_ms.py script next to combine them.")


if __name__ == '__main__':
    main()
