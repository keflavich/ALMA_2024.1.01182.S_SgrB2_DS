#!/bin/bash
#SBATCH --job-name=contsub
#SBATCH --output=/blue/adamginsburg/adamginsburg/logs/contsub_%j.out
#SBATCH --error=/blue/adamginsburg/adamginsburg/logs/contsub_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32gb
#SBATCH --time=24:00:00
#SBATCH --qos=astronomy-dept-b
#SBATCH --account=astronomy-dept

########################################
# Continuum Subtraction for Missing Fields
########################################
# This script runs uvcontsub for DS6, DS7-DS8, and DS9
# to create continuum-subtracted data needed for line imaging.
#
# Steps:
# 1. Run uvcontsub using cont.dat ranges
# 2. Split CORRECTED_DATA into *_targets_line.ms files
########################################

# CASA path - update this to your CASA installation
CASA_PATH="/orange/adamginsburg/casa/casa-6.6.6-17-pipeline-2025.1.0.35-py3.10.el8/bin/casa"

# Check CASA exists
if [ ! -f "$CASA_PATH" ]; then
    echo "ERROR: CASA not found at $CASA_PATH"
    echo "Please update CASA_PATH in this script"
    exit 1
fi

# Print job info
echo "========================================"
echo "SLURM Job Information"
echo "========================================"
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURM_NODELIST"
echo "CPUs: $SLURM_CPUS_PER_TASK"
echo "Memory: $SLURM_MEM_PER_NODE MB"
echo "Working Directory: $(pwd)"
echo "========================================"
echo ""

# Make sure we're in the right directory
cd /orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final

echo "Using CASA: $CASA_PATH"
echo "Start time: $(date)"
echo ""

########################################
# Step 1: Run uvcontsub
########################################
echo "========================================"
echo "STEP 1: Running uvcontsub"
echo "========================================"
echo ""

$CASA_PATH --nologger --log2term -c run_uvcontsub.py

CONTSUB_EXIT=$?

if [ $CONTSUB_EXIT -ne 0 ]; then
    echo ""
    echo "ERROR: uvcontsub failed with exit code $CONTSUB_EXIT"
    echo "Check logs for details"
    exit $CONTSUB_EXIT
fi

echo ""
echo "✓ uvcontsub completed successfully"
echo ""

########################################
# Step 2: Split line MSs
########################################
echo "========================================"
echo "STEP 2: Splitting line MSs"
echo "========================================"
echo ""

$CASA_PATH --nologger --log2term -c split_line_ms.py

SPLIT_EXIT=$?

if [ $SPLIT_EXIT -ne 0 ]; then
    echo ""
    echo "ERROR: split failed with exit code $SPLIT_EXIT"
    echo "Check logs for details"
    exit $SPLIT_EXIT
fi

echo ""
echo "✓ Split completed successfully"
echo ""

########################################
# Summary
########################################
echo "========================================"
echo "Job Summary"
echo "========================================"
echo "End time: $(date)"
echo "Exit status: 0"
echo "========================================"
echo ""
echo "Continuum subtraction complete!"
echo "You can now run imaging jobs for DS6, DS7-DS8, and DS9"
