#!/bin/bash

mkdir -p output

TOTAL=$(grep -cv '^[[:space:]]*$' symbols.txt)
COUNT=0

while IFS= read -r SYMBOL; do
    [ -z "$SYMBOL" ] && continue

    COUNT=$((COUNT + 1))

    TIME=$(date +"%Y%m%d_%H%M%S")

    FILE="output/${SYMBOL}_${TIME}.json"

    echo "[$COUNT/$TOTAL] מוריד $SYMBOL -> $FILE"

    curl --socks5-hostname 127.0.0.1:9050 -s \
      -H "User-Agent: Mozilla/5.0" \
      "https://query1.finance.yahoo.com/v8/finance/chart/${SYMBOL}?range=60d&interval=5m" \
      -o "$FILE"

    echo "[$COUNT/$TOTAL] נשמר: $FILE"

    sleep 60

done < symbols.txt
