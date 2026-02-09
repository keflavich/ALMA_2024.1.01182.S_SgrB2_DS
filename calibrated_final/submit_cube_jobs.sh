#!/bin/bash
#SBATCH --job-name=sgrb2_cubes
#SBATCH --output=/blue/adamginsburg/adamginsburg/logs/cube_%A_%a.out
#SBATCH --error=/blue/adamginsburg/adamginsburg/logs/cube_%A_%a.err
#SBATCH --array=0-15
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64gb
#SBATCH --time=96:00:00
#SBATCH --qos=astronomy-dept-b
#SBATCH --account=astronomy-dept

# SLURM array job script for imaging SgrB2 spectral cubes
# Each array task images one source+spw combination
#
# Job array indices:
#   0-3:   SgrB2S_DS1-5 (SPW 23, 25, 27, 29)
#   4-7:   SgrB2S_DS6   (SPW 23, 25, 27, 29)
#   8-11:  SgrB2S_DS7-8 (SPW 23, 25, 27, 29)
#   12-15: SgrB2S_DS9   (SPW 23, 25, 27, 29)
#
# Usage:
#   sbatch submit_cube_jobs.sh
#
# To submit only specific sources/spws, use:
#   sbatch --array=0-3 submit_cube_jobs.sh      # Only DS1-5
#   sbatch --array=0,4,8,12 submit_cube_jobs.sh  # Only SPW 23 for all sources

# Print job information
echo "========================================"
echo "SLURM Job Information"
echo "========================================"
echo "Job ID: $SLURM_JOB_ID"
echo "Array Job ID: $SLURM_ARRAY_JOB_ID"
echo "Array Task ID: $SLURM_ARRAY_TASK_ID"
echo "Node: $SLURMD_NODENAME"
echo "CPUs: $SLURM_CPUS_PER_TASK"
echo "Memory: $SLURM_MEM_PER_NODE MB"
echo "Working Directory: $SLURM_SUBMIT_DIR"
echo "========================================"
echo

# Ensure we're in the calibrated_final directory
# Handle both cases: submitted from parent or from calibrated_final
if [[ "$SLURM_SUBMIT_DIR" == */calibrated_final ]]; then
    cd $SLURM_SUBMIT_DIR
else
    cd $SLURM_SUBMIT_DIR/calibrated_final
fi

# Create logs directory in parent
mkdir -p ../logs

# Set CASA path (as specified in project documentation)
CASA_PATH="/orange/adamginsburg/casa/casa-6.6.6-17-pipeline-2025.1.0.35-py3.10.el8/bin/casa"

# Check if CASA exists
if [ ! -f "$CASA_PATH" ]; then
    echo "ERROR: CASA not found at $CASA_PATH"
    echo "Please update CASA_PATH in this script to point to your CASA installation"
    exit 1
fi

echo "Using CASA: $CASA_PATH"
echo

# Set cube ID from array task ID
CUBE_ID=$SLURM_ARRAY_TASK_ID

# Print cube information
echo "Imaging cube ID: $CUBE_ID"
case $CUBE_ID in
    0)  echo "  Source: SgrB2S_DS1-5, SPW: 23" ;;
    1)  echo "  Source: SgrB2S_DS1-5, SPW: 25" ;;
    2)  echo "  Source: SgrB2S_DS1-5, SPW: 27" ;;
    3)  echo "  Source: SgrB2S_DS1-5, SPW: 29" ;;
    4)  echo "  Source: DS6, SPW: 23" ;;
    5)  echo "  Source: DS6, SPW: 25" ;;
    6)  echo "  Source: DS6, SPW: 27" ;;
    7)  echo "  Source: DS6, SPW: 29" ;;
    8)  echo "  Source: DS7-DS8, SPW: 23" ;;
    9)  echo "  Source: DS7-DS8, SPW: 25" ;;
    10) echo "  Source: DS7-DS8, SPW: 27" ;;
    11) echo "  Source: DS7-DS8, SPW: 29" ;;
    12) echo "  Source: DS9, SPW: 23" ;;
    13) echo "  Source: DS9, SPW: 25" ;;
    14) echo "  Source: DS9, SPW: 27" ;;
    15) echo "  Source: DS9, SPW: 29" ;;
    *)  echo "  ERROR: Invalid cube ID"
        exit 1 ;;
esac
echo

# Set environment variables for CASA
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

# Start time
START_TIME=$(date +%s)
echo "Start time: $(date)"
echo

# Run CASA to image this cube
echo "Running CASA imaging for cube $CUBE_ID..."
echo "Command: $CASA_PATH --nologger --log2term -c image_cubes.py $CUBE_ID"
echo

$CASA_PATH --nologger --log2term -c image_cubes.py $CUBE_ID

# Check exit status
EXIT_STATUS=$?

# End time
END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))
HOURS=$((ELAPSED / 3600))
MINUTES=$(((ELAPSED % 3600) / 60))
SECONDS=$((ELAPSED % 60))

echo
echo "========================================"
echo "Job Summary"
echo "========================================"
echo "End time: $(date)"
echo "Elapsed time: ${HOURS}h ${MINUTES}m ${SECONDS}s"
echo "Exit status: $EXIT_STATUS"
echo "========================================"

# Exit with CASA's exit status
exit $EXIT_STATUS
