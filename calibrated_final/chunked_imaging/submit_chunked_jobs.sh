#!/bin/bash
#
# Master submitter for SgrB2 chunked cube imaging.
#
# Submits a SLURM array job for all chunks, then chains a merge+cleanup job
# with --dependency=afterok.
#
# Usage:
#   ./submit_chunked_jobs.sh <FIELD> <SPW>
#   ./submit_chunked_jobs.sh all           # submit all field+SPW combos
#
# Examples:
#   ./submit_chunked_jobs.sh DS9 23
#   ./submit_chunked_jobs.sh SgrB2S_DS1-5 25
#   ./submit_chunked_jobs.sh all

set -eu

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASEDIR="$(dirname "${SCRIPT_DIR}")"  # calibrated_final/

# ===========================
# Configuration
# ===========================
NCHAN_CHUNK=32
CHUNK_JOB="${SCRIPT_DIR}/slurm_chunk_job.sh"
MERGE_JOB="${SCRIPT_DIR}/slurm_merge_job.sh"
WORK_BASE="${BASEDIR}/working_chunks"

# Channel counts per SPW
declare -A TOTALNCHAN
TOTALNCHAN[23]=1916
TOTALNCHAN[25]=1920
TOTALNCHAN[27]=1920
TOTALNCHAN[29]=3840

# All fields and SPWs
ALL_FIELDS=("SgrB2S_DS1-5" "DS6" "DS7-DS8" "DS9")
ALL_SPWS=("23" "25" "27" "29")

# ===========================
# Functions
# ===========================

submit_field_spw() {
    local field="$1"
    local spw="$2"

    local total=${TOTALNCHAN[$spw]}
    local nchunks=$(( (total + NCHAN_CHUNK - 1) / NCHAN_CHUNK ))
    local max_array_idx=$(( nchunks - 1 ))

    # Clean field name for directory
    local field_clean="${field//_/}"
    local work_dir="${WORK_BASE}/${field_clean}_spw${spw}"

    echo "================================================================"
    echo "Submitting: FIELD=${field} SPW=${spw}"
    echo "  Total channels: ${total}"
    echo "  Chunks: ${nchunks} (${NCHAN_CHUNK} chan each)"
    echo "  Array range: 0-${max_array_idx}"
    echo "  Work dir: ${work_dir}"

    mkdir -p "${work_dir}"
    mkdir -p "${BASEDIR}/logs"

    # Submit chunk array job
    chunk_jobid=$(sbatch \
        --parsable \
        --array=0-${max_array_idx}%16 \
        --job-name="sgrb2_${field_clean}_spw${spw}_chunk" \
        --export=FIELD="${field}",SPW="${spw}",NCHAN_CHUNK="${NCHAN_CHUNK}",WORK_DIR="${work_dir}" \
        --output="${BASEDIR}/logs/chunk_${field_clean}_spw${spw}_%A_%a.log" \
        --error="${BASEDIR}/logs/chunk_${field_clean}_spw${spw}_%A_%a.err" \
        "${CHUNK_JOB}")

    echo "  Chunk array job: ${chunk_jobid}"

    # Submit merge job with dependency
    merge_jobid=$(sbatch \
        --parsable \
        --dependency=afterok:${chunk_jobid} \
        --job-name="sgrb2_${field_clean}_spw${spw}_merge" \
        --export=FIELD="${field}",SPW="${spw}",NCHAN_CHUNK="${NCHAN_CHUNK}",WORK_DIR="${work_dir}",CLEANUP_CHUNKS=1 \
        --output="${BASEDIR}/logs/merge_${field_clean}_spw${spw}_%j.log" \
        --error="${BASEDIR}/logs/merge_${field_clean}_spw${spw}_%j.err" \
        "${MERGE_JOB}")

    echo "  Merge job: ${merge_jobid} (depends on ${chunk_jobid})"
    echo "================================================================"
    echo ""
}

# ===========================
# Main
# ===========================

if [ $# -eq 0 ]; then
    echo "Usage: $0 <FIELD> <SPW>"
    echo "       $0 all"
    echo ""
    echo "Fields: ${ALL_FIELDS[*]}"
    echo "SPWs:   ${ALL_SPWS[*]}"
    echo ""
    echo "Examples:"
    echo "  $0 DS9 23"
    echo "  $0 all"
    exit 1
fi

if [ "$1" = "all" ]; then
    echo "Submitting ALL field+SPW combinations"
    echo ""
    for field in "${ALL_FIELDS[@]}"; do
        for spw in "${ALL_SPWS[@]}"; do
            submit_field_spw "$field" "$spw"
        done
    done
    echo "All jobs submitted!"
else
    if [ $# -ne 2 ]; then
        echo "ERROR: Need FIELD and SPW, or 'all'"
        exit 1
    fi
    submit_field_spw "$1" "$2"
fi
