#!/bin/bash
#
# Check if all chunks for a field+SPW are complete, then submit merge job
# Usage: ./submit_merge_if_complete.sh <FIELD> <SPW>
#        ./submit_merge_if_complete.sh all
#

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final"

# SPW channel counts (from original submit script)
declare -A SPW_CHANNELS=(
    [23]=1916
    [25]=1920
    [27]=1920
    [29]=3840
)

NCHAN_CHUNK=32

# Field list
FIELDS=("SgrB2S_DS1-5" "DS6" "DS7-DS8" "DS9")
SPWS=("23" "25" "27" "29")

check_and_submit_merge() {
    local field=$1
    local spw=$2
    
    local totalchan=${SPW_CHANNELS[$spw]}
    local expected_chunks=$(( (totalchan + NCHAN_CHUNK - 1) / NCHAN_CHUNK ))
    
    # Construct work dir - match the naming from submit_chunked_jobs.sh
    local field_clean="${field//_/}"
    local work_dir="${BASE_DIR}/working_chunks/${field_clean}_spw${spw}"
    
    # Count existing residual files (exclude merged output files)
    local residual_count=0
    if [ -d "$work_dir" ]; then
        residual_count=$(find "$work_dir" -maxdepth 1 -name "*.[0-9][0-9][0-9][0-9]+[0-9][0-9][0-9].cube.I.residual" -type d 2>/dev/null | wc -l)
    fi
    
    echo "================================================================"
    echo "Checking: FIELD=${field} SPW=${spw}"
    echo "  Expected chunks: ${expected_chunks}"
    echo "  Found residuals: ${residual_count}"
    echo "  Work dir: ${work_dir}"
    
    if [ "$residual_count" -eq "$expected_chunks" ]; then
        echo "  Status: COMPLETE - submitting merge job"
        
        # Check if merge job is already running or pending
        local jobname="sgrb2_${field_clean}_spw${spw}_merge"
        local existing_jobs=$(squeue -u $USER -n "$jobname" -h | wc -l)
        
        if [ "$existing_jobs" -gt 0 ]; then
            echo "  WARNING: Merge job already in queue, skipping"
        else
            # Submit merge job without dependencies
            local merge_job=$(sbatch \
                --export=FIELD=${field},SPW=${spw},NCHAN_CHUNK=${NCHAN_CHUNK},WORK_DIR=${work_dir} \
                "${SCRIPT_DIR}/slurm_merge_job.sh" | awk '{print $NF}')
            
            echo "  Merge job submitted: ${merge_job}"
        fi
    elif [ "$residual_count" -eq 0 ]; then
        echo "  Status: NOT STARTED (no residuals found)"
    else
        echo "  Status: INCOMPLETE (${residual_count}/${expected_chunks})"
        echo "  Missing: $(( expected_chunks - residual_count )) chunks"
    fi
    echo "================================================================"
    echo ""
}

# Main logic
if [ "$1" == "all" ]; then
    echo "Checking all field+SPW combinations..."
    echo ""
    for field in "${FIELDS[@]}"; do
        for spw in "${SPWS[@]}"; do
            check_and_submit_merge "$field" "$spw"
        done
    done
else
    if [ -z "$1" ] || [ -z "$2" ]; then
        echo "Usage: $0 <FIELD> <SPW>"
        echo "       $0 all"
        echo ""
        echo "Available fields: ${FIELDS[@]}"
        echo "Available SPWs: ${SPWS[@]}"
        exit 1
    fi
    
    FIELD=$1
    SPW=$2
    
    if [ -z "${SPW_CHANNELS[$SPW]}" ]; then
        echo "ERROR: Invalid SPW '$SPW'. Must be one of: ${!SPW_CHANNELS[@]}"
        exit 1
    fi
    
    check_and_submit_merge "$FIELD" "$SPW"
fi
