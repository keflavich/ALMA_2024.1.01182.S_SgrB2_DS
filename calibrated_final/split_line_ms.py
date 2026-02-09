#!/usr/bin/env python
"""
Split continuum-subtracted data into separate *_targets_line.ms files.

This should be run AFTER run_uvcontsub.py has completed.
It extracts the CORRECTED_DATA column (which contains continuum-subtracted data)
from the original MSs into new *_targets_line.ms files for the specified fields.

Usage:
    casa -c split_line_ms.py
"""

import os
import sys
import glob
from casatasks import split

# Fields to process (those missing from line MSs)
FIELDS_TO_PROCESS = ['DS6', 'DS7-DS8', 'DS9']

# SPWs to process
SPWS = ['23', '25', '27', '29']


def check_field_in_ms(vis, field):
    """Check if a field exists in a measurement set."""
    from casatools import msmetadata
    msmd = msmetadata()
    msmd.open(vis)
    fields = list(msmd.fieldnames())
    msmd.close()
    return field in fields


def split_line_data(vis, output_dir='measurement_sets'):
    """
    Split continuum-subtracted data from CORRECTED_DATA column into a new MS.
    
    Args:
        vis: Input measurement set (with CORRECTED_DATA containing line data)
        output_dir: Directory for output line MS
    """
    # Construct output filename
    ms_basename = os.path.basename(vis)
    if ms_basename.endswith('_targets.ms'):
        output_basename = ms_basename.replace('_targets.ms', '_targets_line.ms')
    else:
        print(f"WARNING: Unexpected MS name format: {ms_basename}")
        output_basename = ms_basename.replace('.ms', '_line.ms')
    
    output_ms = os.path.join(output_dir, output_basename)
    
    # Check if output already exists
    if os.path.exists(output_ms):
        print(f"  ! Output MS already exists: {output_basename}")
        print(f"  Removing existing {output_basename}...")
        os.system(f"rm -rf {output_ms}")
    
    print(f"\n{'='*80}")
    print(f"Splitting line MS:")
    print(f"  Input:  {ms_basename}")
    print(f"  Output: {output_basename}")
    print(f"{'='*80}")
    
    try:
        split(
            vis=vis,
            outputvis=output_ms,
            datacolumn='corrected',  # CORRECTED_DATA contains the continuum-subtracted data
            keepflags=True
        )
        print(f"  ✓ Successfully created {output_basename}")
        return True
        
    except Exception as e:
        print(f"  ✗ ERROR: {str(e)}")
        return False


def main():
    """Main execution function."""
    
    # Get all measurement sets (non-line versions)
    ms_pattern = 'measurement_sets/uid*_targets.ms'
    all_ms = sorted(glob.glob(ms_pattern))
    
    # Filter to only non-line MSs
    all_ms = [ms for ms in all_ms if not ms.endswith('_targets_line.ms')]
    
    if len(all_ms) == 0:
        print(f"ERROR: No measurement sets found matching {ms_pattern}")
        sys.exit(1)
    
    print(f"Found {len(all_ms)} measurement sets")
    print(f"Will split out line data for fields: {', '.join(FIELDS_TO_PROCESS)}")
    print()
    
    # Check which MSs have the fields we're interested in
    ms_to_process = []
    for vis in all_ms:
        has_field = False
        for field in FIELDS_TO_PROCESS:
            if check_field_in_ms(vis, field):
                has_field = True
                break
        if has_field:
            ms_to_process.append(vis)
    
    print(f"Found {len(ms_to_process)} MSs containing target fields")
    print()
    
    # Track statistics
    total_processed = 0
    successful = 0
    
    # Process each MS
    for vis in ms_to_process:
        success = split_line_data(vis)
        total_processed += 1
        if success:
            successful += 1
    
    # Summary
    print(f"\n{'='*80}")
    print(f"SPLIT SUMMARY")
    print(f"{'='*80}")
    print(f"Total MSs processed:  {total_processed}")
    print(f"Successfully split:   {successful}")
    print(f"Failed:               {total_processed - successful}")
    print(f"{'='*80}")


if __name__ == '__main__':
    main()
