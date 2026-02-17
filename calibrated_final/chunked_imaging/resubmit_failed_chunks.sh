#!/bin/bash
#
# Check for missing/failed chunks and resubmit only those
# Usage: ./resubmit_failed_chunks.sh <FIELD> <SPW>
#        ./resubmit_failed_chunks.sh all
#

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final"

# SPW channel counts
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

resubmit_missing_chunks() {
    local field=$1
    local spw=$2
    
    local totalchan=${SPW_CHANNELS[$spw]}
    local expected_chunks=$(( (totalchan + NCHAN_CHUNK - 1) / NCHAN_CHUNK ))
    
    # Construct work dir - match the naming from submit_chunked_jobs.sh
    local field_clean="${field//_/}"
    local work_dir="${BASE_DIR}/working_chunks/${field_clean}_spw${spw}"
    
    echo "================================================================"
    echo "Checking: FIELD=${field} SPW=${spw}"
    echo "  Total channels: ${totalchan}"
    echo "  Expected chunks: ${expected_chunks} (0-$(( expected_chunks - 1 )))"
    echo "  Work dir: ${work_dir}"
    
    # Check if merged cube already exists (chunks would have been cleaned up)
    local merged_cube="${work_dir}/oussid.SgrB2_${field_clean}_sci.spw${spw}.cube.I.residual"
    if [ -d "$merged_cube" ]; then
        echo "  Status: MERGED CUBE EXISTS - nothing to resubmit"
        echo "  Merged cube: $(basename $merged_cube)"
        echo "================================================================"
        echo ""
        return
    fi
    
    # Get list of completed chunks by parsing residual filenames
    # Format: oussid.SgrB2_<field>_sci.spw<spw>.<startchan>+<nch>.cube.I.residual
    local completed_chunks=()
    if [ -d "$work_dir" ]; then
        while IFS= read -r residual; do
            # Extract startchan from filename
            local basename=$(basename "$residual")
            # Pattern: oussid.SgrB2_DS9_sci.spw23.0000+032.cube.I.residual
            if [[ $basename =~ \.([0-9]{4})\+[0-9]{3}\.cube\.I\.residual$ ]]; then
                local startchan=${BASH_REMATCH[1]}
                # Remove leading zeros
                startchan=$((10#$startchan))
                # Calculate chunk ID
                local chunk_id=$(( startchan / NCHAN_CHUNK ))
                completed_chunks+=($chunk_id)
            fi
        done < <(find "$work_dir" -maxdepth 1 -name "*.residual" -type d 2>/dev/null)
    fi
    
    # Sort completed chunks
    if [ ${#completed_chunks[@]} -gt 0 ]; then
        IFS=$'\n' completed_chunks=($(sort -n <<<"${completed_chunks[*]}"))
        unset IFS
    fi
    
    # Find missing chunks
    local missing_chunks=()
    for (( chunk_id=0; chunk_id<expected_chunks; chunk_id++ )); do
        local found=0
        for completed in "${completed_chunks[@]}"; do
            if [ "$completed" -eq "$chunk_id" ]; then
                found=1
                break
            fi
        done
        if [ "$found" -eq 0 ]; then
            missing_chunks+=($chunk_id)
        fi
    done
    
    local completed_count=${#completed_chunks[@]}
    local missing_count=${#missing_chunks[@]}
    
    echo "  Completed: ${completed_count}/${expected_chunks}"
    if [ ${#completed_chunks[@]} -gt 0 ] && [ ${#completed_chunks[@]} -le 10 ]; then
        echo "    Chunks: ${completed_chunks[*]}"
    fi
    echo "  Missing: ${missing_count}/${expected_chunks}"
    
    if [ "$missing_count" -eq 0 ]; then
        echo "  Status: ALL COMPLETE - nothing to resubmit"
        echo "================================================================"
        echo ""
        return
    fi
    
    # Show missing chunks (up to 20)
    if [ "$missing_count" -le 20 ]; then
        echo "    Chunks: ${missing_chunks[*]}"
    else
        echo "    Chunks: ${missing_chunks[@]:0:10} ... ${missing_chunks[@]: -10}"
    fi
    
    # Build array specification for SLURM
    local array_spec=$(IFS=,; echo "${missing_chunks[*]}")
    
    echo "  Status: SUBMITTING ${missing_count} missing chunks"
    echo "  Array spec: ${array_spec}"
    
    # Submit array job for missing chunks only
    local chunk_job=$(sbatch \
        --array="${array_spec}%16" \
        --export=FIELD=${field},SPW=${spw},NCHAN_CHUNK=${NCHAN_CHUNK},WORK_DIR=${work_dir} \
        "${SCRIPT_DIR}/slurm_chunk_job.sh" | awk '{print $NF}')
    
    if [ -n "$chunk_job" ]; then
        echo "  Chunk array job: ${chunk_job}"
        
        # Don't submit merge job - use submit_merge_if_complete.sh after chunks finish
        echo "  Note: Run ./submit_merge_if_complete.sh after chunks complete"
    else
        echo "  ERROR: Failed to submit job"
    fi
    
    echo "================================================================"
    echo ""
}

# Main logic
if [ "$1" == "all" ]; then
    echo "Checking all field+SPW combinations for missing chunks..."
    echo ""
    
    submitted_count=0
    complete_count=0
    
    for field in "${FIELDS[@]}"; do
        for spw in "${SPWS[@]}"; do
            # Capture output to check if we submitted
            output=$(resubmit_missing_chunks "$field" "$spw")
            echo "$output"
            
            if echo "$output" | grep -q "SUBMITTING"; then
                ((submitted_count++))
            elif echo "$output" | grep -q "ALL COMPLETE"; then
                ((complete_count++))
            fi
        done
    done
    
    echo "================================================================"
    echo "Summary:"
    echo "  Complete: ${complete_count}/16"
    echo "  Resubmitted: ${submitted_count}/16"
    echo "  In progress: $(( 16 - complete_count - submitted_count ))/16"
    echo "================================================================"
    
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
    
    resubmit_missing_chunks "$FIELD" "$SPW"
fi
