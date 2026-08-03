import sqlite3
import json
import glob
from datetime import datetime, timezone


DB = "stocks.db"


db = sqlite3.connect(DB)
cur = db.cursor()


# טבלה קיימת - לא הורס נתונים
cur.execute("""
CREATE TABLE IF NOT EXISTS candles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    datetime TEXT,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER,
    UNIQUE(symbol, timestamp)
)
""")


# אינדקסים לחיפוש מהיר
cur.execute("""
CREATE INDEX IF NOT EXISTS idx_symbol_timestamp
ON candles(symbol, timestamp)
""")


cur.execute("""
CREATE INDEX IF NOT EXISTS idx_symbol
ON candles(symbol)
""")


files = glob.glob("output/*.json")

count = 0


for file in files:

    print("Loading:", file)

    try:
        with open(file) as f:
            data = json.load(f)

        result = data["chart"]["result"]

        if not result:
            print("SKIP:", file)
            continue

        result = result[0]


        symbol = result["meta"]["symbol"]

        timestamps = result.get("timestamp")

        if not timestamps:
            print("NO DATA:", symbol)
            continue


        quote = result["indicators"]["quote"][0]


        opens = quote.get("open", [])
        highs = quote.get("high", [])
        lows = quote.get("low", [])
        closes = quote.get("close", [])
        volumes = quote.get("volume", [])



        for i, ts in enumerate(timestamps):

            # אין מחיר = אין נר
            if closes[i] is None:
                continue


            dt = datetime.fromtimestamp(
                ts,
                timezone.utc
            ).strftime("%Y-%m-%d %H:%M:%S")


            cur.execute("""
            INSERT OR IGNORE INTO candles
            (
                symbol,
                timestamp,
                datetime,
                open,
                high,
                low,
                close,
                volume
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                symbol,
                ts,
                dt,
                opens[i],
                highs[i],
                lows[i],
                closes[i],
                volumes[i]
            ))


            count += 1


            # שמירה כל 5000 רשומות
            if count % 5000 == 0:
                db.commit()


    except Exception as e:
        print("ERROR:", file, e)



db.commit()
db.close()


print("DONE")
print("Inserted:", count)
