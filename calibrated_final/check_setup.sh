#!/bin/bash
# Test script to verify setup before running full array job
# This will perform basic checks without actually running imaging

echo "========================================"
echo "SgrB2 Cube Imaging - Setup Check"
echo "========================================"
echo

# Check 1: Measurement sets
echo "Checking for continuum-subtracted measurement sets..."
MS_COUNT=$(ls -d measurement_sets/uid*targets_line.ms 2>/dev/null | wc -l)
if [ $MS_COUNT -eq 0 ]; then
    echo "  ❌ ERROR: No continuum-subtracted measurement sets found!"
    echo "  Please run: casa --pipeline -c scriptForReprocessing.py --contsub"
    echo
    exit 1
else
    echo "  ✓ Found $MS_COUNT measurement sets"
    ls -1d measurement_sets/uid*targets_line.ms | head -3
    if [ $MS_COUNT -gt 3 ]; then
        echo "  ... and $((MS_COUNT - 3)) more"
    fi
fi
echo

# Check 2: CASA installation
echo "Checking CASA installation..."
# Extract CASA path from submit script
CASA_PATH=$(grep "^CASA_PATH=" submit_cube_jobs.sh | cut -d'"' -f2)
if [ -f "$CASA_PATH" ]; then
    echo "  ✓ CASA found at: $CASA_PATH"
    VERSION=$($CASA_PATH --version 2>/dev/null | head -1 || echo "Unknown version")
    echo "  Version: $VERSION"
else
    echo "  ❌ ERROR: CASA not found at: $CASA_PATH"
    echo "  Please update CASA_PATH in submit_cube_jobs.sh to point to your CASA installation"
    echo "  Example: CASA_PATH=\"/blue/adamginsburg/casa-6.6.5/bin/casa\""
    echo
    exit 1
fi
echo

# Check 3: Required scripts
echo "Checking required scripts..."
SCRIPTS=("image_cubes.py" "submit_cube_jobs.sh" "list_cubes.py")
for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        echo "  ✓ $script"
    else
        echo "  ❌ ERROR: Missing $script"
        exit 1
    fi
done
echo

# Check 4: Output directories
echo "Checking/creating output directories..."
mkdir -p logs
mkdir -p cube_images
mkdir -p working_cubes
echo "  ✓ logs/"
echo "  ✓ cube_images/"
echo "  ✓ working_cubes/"
echo

# Check 5: List cube configurations
echo "Listing cube configurations..."
python3 list_cubes.py
echo

# Check 6: Disk space
echo "Checking available disk space..."
DISK_AVAIL=$(df -h . | awk 'NR==2 {print $4}')
echo "  Available space: $DISK_AVAIL"
echo "  Note: Each cube requires ~100-500 GB"
echo "  Total required: ~2-8 TB for all 16 cubes"
echo

# Check 7: SLURM availability
echo "Checking SLURM..."
if command -v sbatch &> /dev/null; then
    echo "  ✓ SLURM available"
    echo "  QOS: adamginsburg-b"
    echo "  Account: adamginsburg"
    
    # Check queue status
    RUNNING=$(squeue -u $USER -t RUNNING | wc -l)
    PENDING=$(squeue -u $USER -t PENDING | wc -l)
    if [ $RUNNING -gt 1 ]; then
        echo "  Current jobs running: $((RUNNING - 1))"
    fi
    if [ $PENDING -gt 1 ]; then
        echo "  Current jobs pending: $((PENDING - 1))"
    fi
else
    echo "  ⚠ WARNING: sbatch command not found"
    echo "  You may need to load SLURM module"
fi
echo

# Check 8: Test dry run (optional)
echo "========================================"
echo "Setup Check Complete!"
echo "========================================"
echo
echo "To submit all cube imaging jobs:"
echo "  sbatch submit_cube_jobs.sh"
echo
echo "To test a single cube first (recommended):"
echo "  sbatch --array=0 submit_cube_jobs.sh"
echo
echo "To submit only specific sources:"
echo "  sbatch --array=0-3 submit_cube_jobs.sh    # Only DS1-5"
echo "  sbatch --array=4-7 submit_cube_jobs.sh    # Only DS6"
echo "  sbatch --array=8-11 submit_cube_jobs.sh   # Only DS7-8"
echo "  sbatch --array=12-15 submit_cube_jobs.sh  # Only DS9"
echo
echo "To check status after submission:"
echo "  squeue -u $USER"
echo "  python list_cubes.py --check"
echo
echo "Logs will be written to: logs/cube_<jobid>_<taskid>.{out,err}"
echo "Images will be written to: cube_images/"
echo
