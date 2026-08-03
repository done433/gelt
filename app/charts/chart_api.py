import sqlite3
from flask import Blueprint, jsonify


chart_api = Blueprint(
    "chart_api",
    __name__
)


STOCK_DB = "/data/stocks.db"


def get_stock_db():
    return sqlite3.connect(STOCK_DB)



# =========================
# GET CHART DATA
# =========================

@chart_api.route("/api/chart/<symbol>")
def get_chart(symbol):

    with get_stock_db() as conn:

        rows = conn.execute("""
            SELECT
                timestamp,
                open,
                high,
                low,
                close,
                volume
            FROM candles
            WHERE symbol = ?
            ORDER BY timestamp
        """, (symbol,)).fetchall()


    candles = []

    for row in rows:

        candles.append({
            "time": row[0],
            "open": row[1],
            "high": row[2],
            "low": row[3],
            "close": row[4],
            "volume": row[5]
        })


    return jsonify(candles)



# =========================
# GET ALL SYMBOLS
# =========================

@chart_api.route("/api/stocks")
def get_stocks():

    with get_stock_db() as conn:

        rows = conn.execute("""
            SELECT DISTINCT symbol
            FROM candles
            ORDER BY symbol
        """).fetchall()


    symbols = []

    for row in rows:
        symbols.append(row[0])


    return jsonify(symbols)