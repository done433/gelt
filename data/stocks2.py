import sqlite3
import pickle
import os
from datetime import datetime

from river import linear_model
from river import preprocessing
from river import optim


DB_FILE = "stocks.db"
MODEL_FILE = "models.pkl"


# =========================
# טעינת מודלים
# =========================

if os.path.exists(MODEL_FILE):
    with open(MODEL_FILE, "rb") as f:
        models = pickle.load(f)
else:
    models = {}



# =========================
# התחברות למסד
# =========================

db = sqlite3.connect(DB_FILE)
cur = db.cursor()



cur.execute("""
SELECT DISTINCT symbol
FROM candles
ORDER BY symbol
""")


symbols = [
    row[0]
    for row in cur.fetchall()
]



# =========================
# יצירת מודל לכל סימול
# =========================

for symbol in symbols:

    if symbol not in models:

        models[symbol] = (
            preprocessing.StandardScaler()
            |
            linear_model.LinearRegression(
                optimizer=optim.SGD(0.001)
            )
        )



# =========================
# אימון היסטורי
# =========================

print("Starting training...")


for symbol in symbols:


    print("Training:", symbol)


    cur.execute("""
    SELECT timestamp, close, volume
    FROM candles
    WHERE symbol=?
      AND close IS NOT NULL
      AND volume IS NOT NULL
    ORDER BY timestamp ASC
    """, (symbol,))


    rows = cur.fetchall()


    previous_price = None
    previous_volume = None
    previous_return = 0



    for timestamp, price, volume in rows:



        if previous_price is None:

            previous_price = price
            previous_volume = volume
            continue



        if previous_price <= 0:

            previous_price = price
            previous_volume = volume
            continue



        # שינוי מחיר אמיתי
        current_return = (
            (price - previous_price)
            /
            previous_price
        ) * 100



        # הגבלת רעשים
        current_return = max(
            min(current_return, 5),
            -5
        )



        # יחס נפח
        volume_ratio = 1

        if previous_volume > 0:

            volume_ratio = (
                volume /
                previous_volume
            )


        volume_ratio = max(
            min(volume_ratio, 3),
            0.3
        )



        # מידע שהיה ידוע לפני המחיר הנוכחי
        x = {

            "previous_return":
                previous_return,

            "volume_ratio":
                volume_ratio,

            "hour":
                datetime.fromtimestamp(timestamp).hour / 24,

            "minute":
                datetime.fromtimestamp(timestamp).minute / 60
        }



        # תחזית לפני למידה
        prediction = models[symbol].predict_one(x)


        if prediction is None:
            prediction = 0



        
        
        # תחזית מחיר אמיתי
        predicted_price = price * (
            1 + prediction / 100
        )

        predicted_change_money = (
            predicted_price - price
        )


        print(
            f"{symbol:10} "
            f"מחיר:{price:.4f} | "
            f"צפי שינוי:{prediction:.4f}% | "
            f"מחיר חזוי:{predicted_price:.4f} | "
            f"הפרש:{predicted_change_money:.4f} | "
            f"אמת שינוי:{current_return:.4f}%"
        )
        

        # לימוד
        models[symbol].learn_one(
            x,
            current_return
        )



        previous_price = price
        previous_volume = volume
        previous_return = current_return



# =========================
# שמירה
# =========================

with open(MODEL_FILE, "wb") as f:

    pickle.dump(
        models,
        f
    )



print("=========================")
print("Training finished")
print("Models saved:", len(models))
print("=========================")