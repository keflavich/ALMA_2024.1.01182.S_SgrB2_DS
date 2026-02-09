#!/bin/bash
#SBATCH --job-name=sgrb2_chunk
#SBATCH --output=/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/logs/chunk_%x_%A_%a.log
#SBATCH --error=/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/logs/chunk_%x_%A_%a.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32gb
#SBATCH --time=48:00:00
#SBATCH --qos=astronomy-dept-b
#SBATCH --account=astronomy-dept

# SgrB2 chunked cube imaging - array job script
#
# This runs a single channel chunk. Environment variables must be set:
#   FIELD       - field name
#   SPW         - spectral window
#   NCHAN_CHUNK - channels per chunk
#   WORK_DIR    - output directory
#
# STARTCHAN is computed from SLURM_ARRAY_TASK_ID * NCHAN_CHUNK

CASA_PATH="/orange/adamginsburg/casa/casa-6.6.6-17-pipeline-2025.1.0.35-py3.10.el8/bin/casa"
PYTHON_SCRIPT="/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/chunked_imaging/sgrb2_chunk_imaging.py"

if [ -z "$FIELD" ] || [ -z "$SPW" ] || [ -z "$NCHAN_CHUNK" ] || [ -z "$WORK_DIR" ]; then
    echo "ERROR: FIELD, SPW, NCHAN_CHUNK, and WORK_DIR must be set"
    echo "  FIELD=${FIELD}"
    echo "  SPW=${SPW}"
    echo "  NCHAN_CHUNK=${NCHAN_CHUNK}"
    echo "  WORK_DIR=${WORK_DIR}"
    exit 1
fi

# Compute STARTCHAN from array task ID
export STARTCHAN=$(( SLURM_ARRAY_TASK_ID * NCHAN_CHUNK ))

echo "================================================================"
echo "SgrB2 chunked imaging - chunk job"
echo "  FIELD=${FIELD}"
echo "  SPW=${SPW}"
echo "  STARTCHAN=${STARTCHAN}"
echo "  NCHAN_CHUNK=${NCHAN_CHUNK}"
echo "  WORK_DIR=${WORK_DIR}"
echo "  SLURM_ARRAY_TASK_ID=${SLURM_ARRAY_TASK_ID}"
echo "  SLURM_JOB_ID=${SLURM_JOB_ID}"
echo "  Script: ${SCRIPT}"
echo "================================================================"

# Create output directories
mkdir -p "${WORK_DIR}"

# Copy script to SLURM_TMPDIR so CASA can access it
cp "${PYTHON_SCRIPT}" "${SLURM_TMPDIR}/"
SCRIPT="${SLURM_TMPDIR}/sgrb2_chunk_imaging.py"

echo "ls'ing SLURM_TMPDIR $SLURM_TMPDIR"
ls $SLURM_TMPDIR

[ ! -e $SCRIPT ] && echo "$SCRIPT does not exist"


# Export variables for the CASA script
export FIELD SPW STARTCHAN NCHAN_CHUNK WORK_DIR
export DOMERGE=0

# Set up CASA environment
LOG_DIR="/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/logs"
LOGFILE="${LOG_DIR}/casa_chunk_${SLURM_JOB_ID}.log"

# Run CASA using the working pattern from brick scripts
${CASA_PATH} --logfile=${LOGFILE} --nogui --nologger --cachedir=$SLURM_TMPDIR -c "execfile('${SCRIPT}')"
exit_code=$?

if [ $exit_code -ne 0 ]; then
    echo "CASA exited with code ${exit_code}"
    exit $exit_code
fi

echo "Chunk imaging completed successfully"
