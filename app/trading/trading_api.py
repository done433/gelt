import sqlite3

from flask import (
    Blueprint,
    jsonify,
    request,
    session
)

from trading.trading_engine import (
    buy_stock,
    sell_stock,
    get_balance,
    get_portfolio,
    get_history
)


trading_api = Blueprint(
    "trading_api",
    __name__
)



def get_user():

    if "username" not in session:
        return None

    return session["username"]



# =========================
# BALANCE
# =========================

@trading_api.route("/api/balance")
def balance():

    username = get_user()

    if not username:
        return jsonify({
            "error":"Unauthorized"
        }),401


    return jsonify({
        "balance": get_balance(username)
    })



# =========================
# BUY
# =========================

@trading_api.route(
    "/api/buy",
    methods=["POST"]
)
def buy():

    username = get_user()

    if not username:
        return jsonify({
            "error":"Unauthorized"
        }),401


    data = request.json


    try:

        symbol = data["symbol"]

        quantity = int(
            data["quantity"]
        )

        price = float(
            data["price"]
        )

    except Exception:

        return jsonify({
            "error":"Invalid trade data"
        }),400



    success,message = buy_stock(
        username,
        symbol,
        quantity,
        price
    )


    if not success:

        return jsonify({
            "error":message
        }),400


    return jsonify({
        "status":"bought",
        "message":message
    })




# =========================
# SELL
# =========================

@trading_api.route(
    "/api/sell",
    methods=["POST"]
)
def sell():

    username = get_user()


    if not username:

        return jsonify({
            "error":"Unauthorized"
        }),401



    data = request.json


    try:

        symbol = data["symbol"]

    except:

        return jsonify({
            "error":"Missing symbol"
        }),400



    success,message = sell_stock(
        username,
        symbol
    )


    if not success:

        return jsonify({
            "error":message
        }),400



    return jsonify({
        "status":"sold",
        "message":message
    })




# =========================
# SIMPLE PORTFOLIO
# =========================

@trading_api.route(
    "/api/portfolio"
)
def portfolio():

    username=get_user()


    if not username:

        return jsonify({
            "error":"Unauthorized"
        }),401



    stocks=get_portfolio(username)


    return jsonify([

        {
            "symbol":row[0],
            "quantity":row[1],
            "buy_price":row[2]
        }

        for row in stocks

    ])




# =========================
# PORTFOLIO DETAILS
# =========================

@trading_api.route(
    "/api/portfolio/details"
)
def portfolio_details():

    username=get_user()


    if not username:

        return jsonify({
            "error":"Unauthorized"
        }),401



    result=[]


    with sqlite3.connect(
        "/app/users.db"
    ) as userdb:


        stocks=userdb.execute(
            """
            SELECT symbol,quantity,buy_price
            FROM portfolio
            WHERE username=?
            """,
            (username,)
        ).fetchall()



        with sqlite3.connect(
            "/data/stocks.db"
        ) as market:


            for stock in stocks:


                symbol=stock[0]

                quantity=stock[1]

                buy_price=float(
                    stock[2]
                )



                trade=userdb.execute(
                    """
                    SELECT price,time
                    FROM transactions
                    WHERE username=?
                    AND symbol=?
                    AND action='BUY'
                    ORDER BY id ASC
                    LIMIT 1
                    """,
                    (
                        username,
                        symbol
                    )
                ).fetchone()



                if trade:

                    bought_price=float(
                        trade[0]
                    )

                    bought_time=trade[1]

                else:

                    bought_price=buy_price

                    bought_time=None



                current=market.execute(
                    """
                    SELECT close
                    FROM candles
                    WHERE symbol=?
                    ORDER BY timestamp DESC
                    LIMIT 1
                    """,
                    (symbol,)
                ).fetchone()



                current_price = (
                    float(current[0])
                    if current
                    else buy_price
                )



                buy_value = (
                    quantity *
                    bought_price
                )


                current_value = (
                    quantity *
                    current_price
                )


                profit = (
                    current_value -
                    buy_value
                )



                chart=market.execute(
                    """
                    SELECT close
                    FROM candles
                    WHERE symbol=?
                    ORDER BY timestamp ASC
                    """,
                    (symbol,)
                ).fetchall()



                result.append({

                    "symbol":symbol,

                    "quantity":quantity,

                    "bought_time":bought_time,

                    "buy_price":round(
                        bought_price,2
                    ),

                    "current_price":round(
                        current_price,2
                    ),

                    "current_value":round(
                        current_value,2
                    ),

                    "profit":round(
                        profit,2
                    ),

                    "profit_percent":round(
                        (profit / buy_value)*100,
                        2
                    ) if buy_value else 0,


                    "history":[
                        x[0]
                        for x in chart[-100:]
                    ]

                })


    return jsonify(result)




# =========================
# HISTORY
# =========================

@trading_api.route(
    "/api/history"
)
def history():

    username=get_user()


    if not username:

        return jsonify({
            "error":"Unauthorized"
        }),401



    rows=get_history(username)



    return jsonify([

        {
            "symbol":row[0],
            "action":row[1],
            "quantity":row[2],
            "price":row[3],
            "time":row[4]
        }

        for row in rows

    ])








