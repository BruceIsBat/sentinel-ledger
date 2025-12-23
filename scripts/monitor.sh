#!/bin/bash

# Sentinel-Ledger: System Resource Monitor
# Profiles CPU and Memory usage of the Flask application

echo "🔍 Starting Sentinel-Ledger Monitor..."
echo "Press [CTRL+C] to stop."
echo "-------------------------------------------"
echo "TIMESTAMP         CPU(%)  MEM(%)  PID"

# Loop to capture process stats every 2 seconds
while true; do
    # Find the PID of the run.py process
    PID=$(pgrep -f "python run.py" | head -n 1)

    if [ -z "$PID" ]; then
        echo "$(date '+%H:%M:%S') - Waiting for Sentinel-Ledger to start..."
    else
        # Use 'ps' to get CPU and Memory usage for the PID
        STATS=$(ps -p $PID -o %cpu,%mem --no-headers)
        echo "$(date '+%H:%M:%S')    $STATS    $PID"
    fi
    sleep 2
done