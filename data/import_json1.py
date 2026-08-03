import sqlite3
import json
import glob
from datetime import datetime

db = sqlite3.connect("stocks.db")
cur = db.cursor()

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

# אינדקס נוסף לחיפושים לפי סימבול וזמן
cur.execute("""
CREATE INDEX IF NOT EXISTS idx_symbol_timestamp
ON candles(symbol, timestamp)
""")

files = glob.glob("output/*.json")

for file in files:
    print("Loading:", file)

    with open(file) as f:
        data = json.load(f)

    result = data["chart"]["result"][0]

    symbol = result["meta"]["symbol"]

    timestamps = result["timestamp"]

    quote = result["indicators"]["quote"][0]

    opens = quote["open"]
    highs = quote["high"]
    lows = quote["low"]
    closes = quote["close"]
    volumes = quote["volume"]

    for i, ts in enumerate(timestamps):

        dt = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

        cur.execute("""
        INSERT OR IGNORE INTO candles
        (symbol, timestamp, datetime, open, high, low, close, volume)
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

db.commit()
db.close()

print("DONE")
