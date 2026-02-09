#!/bin/bash
#SBATCH --job-name=sgrb2_merge
#SBATCH --output=/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/logs/merge_%x_%j.log
#SBATCH --error=/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/logs/merge_%x_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=64gb
#SBATCH --time=48:00:00
#SBATCH --qos=astronomy-dept-b
#SBATCH --account=astronomy-dept

# SgrB2 chunked cube imaging - merge + cleanup job
#
# This merges all chunk outputs into a single cube and optionally cleans up.
# Environment variables must be set:
#   FIELD          - field name
#   SPW            - spectral window
#   NCHAN_CHUNK    - channels per chunk (must match chunk jobs)
#   WORK_DIR       - directory containing chunk outputs
#   CLEANUP_CHUNKS - '1' to remove chunk files after merge (default: '1')
#
# This job should be submitted with --dependency=afterok:<chunk_array_jobid>

CASA_PATH="/orange/adamginsburg/casa/casa-6.6.6-17-pipeline-2025.1.0.35-py3.10.el8/bin/casa"
PYTHON_SCRIPT="/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/chunked_imaging/sgrb2_chunk_imaging.py"

if [ -z "$FIELD" ] || [ -z "$SPW" ] || [ -z "$NCHAN_CHUNK" ] || [ -z "$WORK_DIR" ]; then
    echo "ERROR: FIELD, SPW, NCHAN_CHUNK, and WORK_DIR must be set"
    exit 1
fi

echo "================================================================"
echo "SgrB2 chunked imaging - merge + cleanup job"
echo "  FIELD=${FIELD}"
echo "  SPW=${SPW}"
echo "  NCHAN_CHUNK=${NCHAN_CHUNK}"
echo "  WORK_DIR=${WORK_DIR}"
echo "  CLEANUP_CHUNKS=${CLEANUP_CHUNKS:-1}"
echo "  SLURM_JOB_ID=${SLURM_JOB_ID}"
echo "================================================================"

# Copy script to SLURM_TMPDIR so CASA can access it
cp "${PYTHON_SCRIPT}" "${SLURM_TMPDIR}/"
SCRIPT="${SLURM_TMPDIR}/sgrb2_chunk_imaging.py"

# Export variables for the CASA script
export FIELD SPW NCHAN_CHUNK WORK_DIR
export DOMERGE=1
export CLEANUP_CHUNKS=${CLEANUP_CHUNKS:-1}
# STARTCHAN is not used in merge mode but set it to avoid errors
export STARTCHAN=0

# Set up CASA environment
LOG_DIR="/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/logs"
LOGFILE="${LOG_DIR}/casa_merge_${SLURM_JOB_ID}.log"

# Run CASA using the working pattern from brick scripts
${CASA_PATH} --logfile=${LOGFILE} --nogui --nologger --cachedir=$SLURM_TMPDIR -c "execfile('${SCRIPT}')"
exit_code=$?

if [ $exit_code -ne 0 ]; then
    echo "CASA merge exited with code ${exit_code}"
    exit $exit_code
fi

echo "Merge + cleanup completed successfully"
