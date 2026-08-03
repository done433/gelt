import sqlite3

from trading.trading_db import get_db


# =========================
# BALANCE
# =========================

def get_balance(username):

    with get_db() as conn:

        row = conn.execute(
            """
            SELECT balance
            FROM users
            WHERE username=?
            """,
            (username,)
        ).fetchone()

    return row[0] if row else None



# =========================
# BUY STOCK
# =========================

def buy_stock(username, symbol, quantity, price):

    cost = quantity * price


    with get_db() as conn:


        user = conn.execute(
            """
            SELECT balance
            FROM users
            WHERE username=?
            """,
            (username,)
        ).fetchone()


        if not user:

            return False, "User not found"



        balance = user[0]


        if balance < cost:

            return False, "Not enough money"



        conn.execute(
            """
            UPDATE users
            SET balance = balance - ?
            WHERE username=?
            """,
            (
                cost,
                username
            )
        )



        existing = conn.execute(
            """
            SELECT quantity,buy_price
            FROM portfolio
            WHERE username=?
            AND symbol=?
            """,
            (
                username,
                symbol
            )
        ).fetchone()



        if existing:


            old_quantity = existing[0]

            old_price = existing[1]


            new_quantity = old_quantity + quantity


            new_price = (
                (old_quantity * old_price)
                +
                (quantity * price)
            ) / new_quantity



            conn.execute(
                """
                UPDATE portfolio
                SET quantity=?,
                    buy_price=?
                WHERE username=?
                AND symbol=?
                """,
                (
                    new_quantity,
                    new_price,
                    username,
                    symbol
                )
            )


        else:


            conn.execute(
                """
                INSERT INTO portfolio
                (
                    username,
                    symbol,
                    quantity,
                    buy_price
                )
                VALUES (?,?,?,?)
                """,
                (
                    username,
                    symbol,
                    quantity,
                    price
                )
            )



        conn.execute(
            """
            INSERT INTO transactions
            (
                username,
                symbol,
                action,
                quantity,
                price
            )
            VALUES (?,?,?,?,?)
            """,
            (
                username,
                symbol,
                "BUY",
                quantity,
                price
            )
        )



    return True, "Bought successfully"




# =========================
# SELL STOCK
# =========================

def sell_stock(username, symbol):


    with get_db() as conn:


        position = conn.execute(
            """
            SELECT quantity,buy_price
            FROM portfolio
            WHERE username=?
            AND symbol=?
            """,
            (
                username,
                symbol
            )
        ).fetchone()



        if not position:

            return False, "Position not found"



        quantity = position[0]

        buy_price = position[1]



        market = sqlite3.connect(
            "/data/stocks.db"
        )


        current = market.execute(
            """
            SELECT close
            FROM candles
            WHERE symbol=?
            ORDER BY timestamp DESC
            LIMIT 1
            """,
            (symbol,)
        ).fetchone()


        market.close()



        if current:

            sell_price = float(current[0])

        else:

            sell_price = buy_price



        total = quantity * sell_price



        conn.execute(
            """
            UPDATE users
            SET balance = balance + ?
            WHERE username=?
            """,
            (
                total,
                username
            )
        )



        conn.execute(
            """
            DELETE FROM portfolio
            WHERE username=?
            AND symbol=?
            """,
            (
                username,
                symbol
            )
        )



        conn.execute(
            """
            INSERT INTO transactions
            (
                username,
                symbol,
                action,
                quantity,
                price
            )
            VALUES (?,?,?,?,?)
            """,
            (
                username,
                symbol,
                "SELL",
                quantity,
                sell_price
            )
        )



    return True, f"Sold {symbol} for ${sell_price:.2f}"





# =========================
# PORTFOLIO
# =========================

def get_portfolio(username):

    with get_db() as conn:

        rows = conn.execute(
            """
            SELECT symbol,quantity,buy_price
            FROM portfolio
            WHERE username=?
            """,
            (username,)
        ).fetchall()


    return rows





# =========================
# HISTORY
# =========================

def get_history(username):

    with get_db() as conn:

        rows = conn.execute(
            """
            SELECT symbol,action,quantity,price,time
            FROM transactions
            WHERE username=?
            ORDER BY time DESC
            """,
            (username,)
        ).fetchall()


    return rows
