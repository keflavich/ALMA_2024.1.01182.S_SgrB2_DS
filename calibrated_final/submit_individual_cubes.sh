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
# Each array task runs an independent imaging script
#
# Job array indices:
#   0:   SgrB2S_DS1-5 SPW 23
#   1:   SgrB2S_DS1-5 SPW 25
#   2:   SgrB2S_DS1-5 SPW 27
#   3:   SgrB2S_DS1-5 SPW 29
#   4:   DS6 SPW 23
#   5:   DS6 SPW 25
#   6:   DS6 SPW 27
#   7:   DS6 SPW 29
#   8:   DS7-DS8 SPW 23
#   9:   DS7-DS8 SPW 25
#   10:  DS7-DS8 SPW 27
#   11:  DS7-DS8 SPW 29
#   12:  DS9 SPW 23
#   13:  DS9 SPW 25
#   14:  DS9 SPW 27
#   15:  DS9 SPW 29
#
# Usage:
#   sbatch submit_cube_jobs.sh                   # Submit all 16 jobs
#   sbatch --array=0-3 submit_cube_jobs.sh       # Only DS1-5
#   sbatch --array=4 submit_cube_jobs.sh         # Only DS6 SPW 23
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

# CASA path - MUST be set to your CASA installation
CASA_PATH="/orange/adamginsburg/casa/casa-6.6.6-17-pipeline-2025.1.0.35-py3.10.el8/bin/casa"

# Check if CASA exists
if [ ! -x "$CASA_PATH" ]; then
    echo "ERROR: CASA not found at $CASA_PATH"
    echo "Please set CASA_PATH to your CASA installation"
    exit 1
fi

# Map array task ID to script name
# Format: image_cube_XX_<source>_spw<spw>.py
case $SLURM_ARRAY_TASK_ID in
    0)  SCRIPT="image_cube_00_SgrB2S_DS1-5_spw23.py" ;;
    1)  SCRIPT="image_cube_01_SgrB2S_DS1-5_spw25.py" ;;
    2)  SCRIPT="image_cube_02_SgrB2S_DS1-5_spw27.py" ;;
    3)  SCRIPT="image_cube_03_SgrB2S_DS1-5_spw29.py" ;;
    4)  SCRIPT="image_cube_04_DS6_spw23.py" ;;
    5)  SCRIPT="image_cube_05_DS6_spw25.py" ;;
    6)  SCRIPT="image_cube_06_DS6_spw27.py" ;;
    7)  SCRIPT="image_cube_07_DS6_spw29.py" ;;
    8)  SCRIPT="image_cube_08_DS7-DS8_spw23.py" ;;
    9)  SCRIPT="image_cube_09_DS7-DS8_spw25.py" ;;
    10) SCRIPT="image_cube_10_DS7-DS8_spw27.py" ;;
    11) SCRIPT="image_cube_11_DS7-DS8_spw29.py" ;;
    12) SCRIPT="image_cube_12_DS9_spw23.py" ;;
    13) SCRIPT="image_cube_13_DS9_spw25.py" ;;
    14) SCRIPT="image_cube_14_DS9_spw27.py" ;;
    15) SCRIPT="image_cube_15_DS9_spw29.py" ;;
    *)
        echo "ERROR: Invalid array task ID: $SLURM_ARRAY_TASK_ID"
        exit 1
        ;;
esac

# Check if script exists
if [ ! -f "$SCRIPT" ]; then
    echo "ERROR: Script not found: $SCRIPT"
    exit 1
fi

# Print what we're running
echo "Running CASA script: $SCRIPT"
echo "CASA path: $CASA_PATH"
echo "Start time: $(date)"
echo

# Run CASA with the specific script
$CASA_PATH --pipeline --nogui --nologger --log2term -c "$SCRIPT"

# Capture exit code
EXIT_CODE=$?

echo
echo "End time: $(date)"
echo "Exit code: $EXIT_CODE"

if [ $EXIT_CODE -eq 0 ]; then
    echo "SUCCESS: Cube imaging completed"
else
    echo "ERROR: Cube imaging failed"
fi

exit $EXIT_CODE
