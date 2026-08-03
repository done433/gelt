import sqlite3
import pickle
from datetime import datetime

DB_FILE = "stocks.db"
MODEL_FILE = "models.pkl"

SYMBOL = "^IXIC"


# =========================
# טעינת מודל
# =========================

with open(MODEL_FILE, "rb") as f:
    models = pickle.load(f)


model = models[SYMBOL]


# =========================
# מסד נתונים
# =========================

db = sqlite3.connect(DB_FILE)
cur = db.cursor()


cur.execute("""
SELECT timestamp, close, volume
FROM candles
WHERE symbol=?
AND close IS NOT NULL
AND volume IS NOT NULL
ORDER BY timestamp ASC
""", (SYMBOL,))


rows = cur.fetchall()


print("=" * 40)
print("מודל:", SYMBOL)
print("=" * 40)


previous_price = None
previous_volume = None
previous_return = 0


total = 0
correct = 0

errors = []

start_correct = 0
start_total = 0

end_correct = 0
end_total = 0


for timestamp, price, volume in rows:


    if previous_price is None:
        previous_price = price
        previous_volume = volume
        continue


    if previous_price <= 0:
        continue


    # אמת
    actual = (
        (price - previous_price)
        /
        previous_price
    ) * 100


    volume_ratio = 1

    if previous_volume > 0:
        volume_ratio = volume / previous_volume


    x = {

        "previous_return": previous_return,

        "volume_ratio":
            min(max(volume_ratio,0.1),10),

        "hour":
            datetime.fromtimestamp(timestamp).hour,

        "minute":
            datetime.fromtimestamp(timestamp).minute
    }


    # תחזית לפני לימוד
    prediction = model.predict_one(x)


    if prediction is None:
        prediction = 0



    # בדיקת כיוון
    if (
        prediction >= 0 and actual >= 0
    ) or (
        prediction < 0 and actual < 0
    ):
        correct += 1


    total += 1


    error = abs(
        prediction - actual
    )

    errors.append(error)



    # 10% ראשונים
    if total <= len(rows) * 0.1:

        start_total += 1

        if (
            prediction >= 0 and actual >= 0
        ) or (
            prediction < 0 and actual < 0
        ):
            start_correct += 1



    # 10% אחרונים
    if total > len(rows) * 0.9:

        end_total += 1

        if (
            prediction >= 0 and actual >= 0
        ) or (
            prediction < 0 and actual < 0
        ):
            end_correct += 1



    # עכשיו לומד
    model.learn_one(
        x,
        actual
    )


    previous_price = price
    previous_volume = volume
    previous_return = actual



print()
print("=" * 40)
print("תוצאות")
print("=" * 40)


print(
    "בדיקות:",
    total
)


print(
    "דיוק כולל:",
    round(correct / total * 100,2),
    "%"
)


print(
    "שגיאה ממוצעת:",
    round(sum(errors)/len(errors),5),
    "%"
)


print()
print("התחלה:")
print(
    round(
        start_correct/start_total*100,
        2
    ),
    "%"
)


print("סוף:")
print(
    round(
        end_correct/end_total*100,
        2
    ),
    "%"
)


print()
print("שיפור:")
print(
    round(
        (end_correct/end_total*100)
        -
        (start_correct/start_total*100),
        2
    ),
    "%"
)


print("=" * 40)