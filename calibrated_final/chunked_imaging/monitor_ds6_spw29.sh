#!/bin/bash
# Monitor DS6 SPW 29 imaging to verify correct SPW is being imaged

LOG_DIR="/orange/adamginsburg/sgrb2/2024.1.01182.S/calibrated_final/logs"
EXPECTED_FREQ_MIN=146.6  # SPW 29 should be ~146.6-147.6 GHz
EXPECTED_FREQ_MAX=147.6

echo "================================================================"
echo "Monitoring DS6 SPW 29 imaging (Job 24848843)"
echo "Expected frequency range: ${EXPECTED_FREQ_MIN}-${EXPECTED_FREQ_MAX} GHz"
echo "================================================================"
echo ""

# Check for job status
echo "Job status:"
squeue -j 24848843 -o "%.18i %.9P %.20j %.8u %.2t %.10M %.6D %R" 2>/dev/null || echo "  Job not found in queue (may be pending or finished)"
echo ""

# Find log files for this job
echo "Looking for log files..."
CASA_LOGS=$(find ${LOG_DIR} -name "casa_chunk_DS6_spw29_24848843.log" -o -name "casa_chunk_DS6_spw29_*.log" -newer ${LOG_DIR}/casa_chunk_DS6_spw29_24848843.log 2>/dev/null | head -5)
CHUNK_LOGS=$(ls ${LOG_DIR}/chunk_DS6_spw29_24848843_*.log 2>/dev/null | head -5)

if [ -z "$CASA_LOGS" ] && [ -z "$CHUNK_LOGS" ]; then
    echo "  No log files found yet. Jobs may still be pending."
    echo "  Run this script again in a few minutes."
    exit 0
fi

echo "Found log files, checking imaging parameters..."
echo ""

# Check CASA logs for frequency information
for logfile in $CASA_LOGS; do
    if [ -f "$logfile" ]; then
        echo "=== $(basename $logfile) ==="
        # Look for the imaging parameters printed by the script
        grep -A10 "Imaging chunk:" "$logfile" | head -15
        echo ""
        
        # Check for frequency in the log
        freq=$(grep "start:" "$logfile" | grep -oE '[0-9]+\.[0-9]+GHz' | grep -oE '[0-9]+\.[0-9]+')
        if [ -n "$freq" ]; then
            echo "  Detected frequency: ${freq} GHz"
            if (( $(echo "$freq >= $EXPECTED_FREQ_MIN && $freq <= $EXPECTED_FREQ_MAX" | bc -l) )); then
                echo "  ✓ CORRECT: Frequency is in SPW 29 range"
            else
                echo "  ✗ WRONG: Frequency is NOT in SPW 29 range!"
            fi
        fi
        echo ""
    fi
done

# Also check a couple chunk logs
for logfile in $CHUNK_LOGS; do
    if [ -f "$logfile" ]; then
        echo "=== $(basename $logfile) ==="
        grep -E "SPW=|start:|width:|spw_selection:" "$logfile" 2>/dev/null | head -5
        echo ""
    fi
done

echo "================================================================"
echo "Next check: run this script again in 20 minutes"
echo "  Or watch continuously: watch -n 1200 $0"
echo "================================================================"
