import sqlite3
import json
import glob
from datetime import datetime, timezone
import os
import time

DB = "stocks.db"

db = sqlite3.connect(DB)

# ביצועים
db.execute("PRAGMA journal_mode=WAL")
db.execute("PRAGMA synchronous=NORMAL")
db.execute("PRAGMA temp_store=MEMORY")
db.execute("PRAGMA cache_size=-100000")

cur = db.cursor()


# ==========================
# DATABASE STRUCTURE
# ==========================

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


# ==========================
# INDEXES
# ==========================

indexes = [

    """
    CREATE INDEX IF NOT EXISTS idx_symbol
    ON candles(symbol)
    """,

    """
    CREATE INDEX IF NOT EXISTS idx_timestamp
    ON candles(timestamp)
    """,

    """
    CREATE INDEX IF NOT EXISTS idx_symbol_timestamp
    ON candles(symbol, timestamp)
    """,

    """
    CREATE INDEX IF NOT EXISTS idx_datetime
    ON candles(datetime)
    """,

    """
    CREATE INDEX IF NOT EXISTS idx_close
    ON candles(close)
    """
]


for index in indexes:
    cur.execute(index)


db.commit()


# ==========================
# IMPORT
# ==========================

files = glob.glob("output/*.json")

total_files = len(files)
total_inserted = 0

start_time = time.time()


for file_number, file in enumerate(files, 1):

    print(
        f"\n[{file_number}/{total_files}] Loading: {file}"
    )

    try:

        with open(file, "r") as f:
            data = json.load(f)


        result = data.get("chart", {}).get("result")

        if not result:
            print("SKIP - no result")
            continue


        result = result[0]


        symbol = result["meta"]["symbol"]

        timestamps = result.get("timestamp")

        if not timestamps:
            print("SKIP - no timestamps")
            continue


        quote = result["indicators"]["quote"][0]


        opens = quote.get("open", [])
        highs = quote.get("high", [])
        lows = quote.get("low", [])
        closes = quote.get("close", [])
        volumes = quote.get("volume", [])


        rows = []


        total_points = len(timestamps)


        for i, ts in enumerate(timestamps):

            close = closes[i]

            # אין מחיר = אין נר
            if close is None:
                continue


            dt = datetime.fromtimestamp(
                ts,
                timezone.utc
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            )


            rows.append(
                (
                    symbol,
                    ts,
                    dt,
                    opens[i],
                    highs[i],
                    lows[i],
                    close,
                    volumes[i]
                )
            )


            if len(rows) >= 5000:

                cur.executemany(
                    """
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
                    rows
                )


                total_inserted += len(rows)

                rows.clear()


                db.commit()


        # שאריות אחרונות
        if rows:

            cur.executemany(
                """
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
                rows
            )


            total_inserted += len(rows)

            db.commit()


        elapsed = time.time() - start_time

        print(
            f"OK {symbol} | "
            f"Candles loaded: {total_points} | "
            f"Total inserted: {total_inserted} | "
            f"Time: {elapsed:.1f}s"
        )


    except Exception as e:

        print(
            "ERROR:",
            file,
            e
        )


db.close()


print("\n======================")
print("DONE")
print("Inserted:", total_inserted)
print(
    "Time:",
    round(time.time() - start_time, 2),
    "seconds"
)
print("======================")
