#!/bin/bash

mkdir -p output

while IFS= read -r SYMBOL; do
    [ -z "$SYMBOL" ] && continue

    TIME=$(date +"%Y%m%d_%H%M%S")

    FILE="output/${SYMBOL}_${TIME}.json"

    echo "מוריד $SYMBOL -> $FILE"

    curl -s \
      -H "User-Agent: Mozilla/5.0" \
      "https://query1.finance.yahoo.com/v8/finance/chart/${SYMBOL}?range=60d&interval=5m" \
      -o "$FILE"

    echo "נשמר: $FILE"

    sleep 2

done < symbols.txt
