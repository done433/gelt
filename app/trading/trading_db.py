import sqlite3


USER_DB = "/app/users.db"



def get_db():

    return sqlite3.connect(USER_DB)



def create_trading_tables():

    with get_db() as conn:


        # בדיקה אם balance כבר קיים

        columns = conn.execute(
            "PRAGMA table_info(users)"
        ).fetchall()


        names = [
            column[1]
            for column in columns
        ]


        if "balance" not in names:

            conn.execute(
                """
                ALTER TABLE users
                ADD COLUMN balance REAL DEFAULT 100000
                """
            )



        conn.execute("""
        CREATE TABLE IF NOT EXISTS portfolio (

            id INTEGER PRIMARY KEY,

            username TEXT,

            symbol TEXT,

            quantity INTEGER,

            buy_price REAL

        )
        """)



        conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (

            id INTEGER PRIMARY KEY,

            username TEXT,

            symbol TEXT,

            action TEXT,

            quantity INTEGER,

            price REAL,

            time DATETIME DEFAULT CURRENT_TIMESTAMP

        )
        """)




def create_account(username):

    with get_db() as conn:

        conn.execute(
            """
            UPDATE users

            SET balance = 100000

            WHERE username=?
            """,
            (username,)
        )