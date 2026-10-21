import random
import pandas as pd

random.seed(42)

reasons = ["damaged", "wrong_size", "changed_mind", "wrong_item", "not_as_expected"]
payments = ["card", "upi", "cod", "wallet"]
categories = ["dress", "jacket", "shoes", "jeans", "shirt", "handbag"]

rows = []
for i in range(1, 10001):
    orders = random.randint(1, 40)
    returns = random.randint(0, min(orders, 18))
    disputes = random.randint(0, min(returns, 5))
    days_to_return = random.randint(1, 30)
    amount = round(random.uniform(399, 15000), 2)
    returns_30d = random.randint(0, min(8, returns))
    category = random.choice(categories)
    reason = random.choice(reasons)
    payment = random.choice(payments)

    # Synthetic label: intentionally rule-based only for creating training data.
    risk = (
        0.18 * min(returns / max(orders, 1), 1) +
        0.18 * min(returns_30d / 8, 1) +
        0.16 * min(disputes / 5, 1) +
        0.12 * (1 if days_to_return <= 2 else 0) +
        0.10 * (1 if amount >= 8000 else 0) +
        0.10 * (1 if reason in ["wrong_item", "damaged"] else 0) +
        0.06 * (1 if payment == "cod" else 0) +
        random.uniform(-0.08, 0.08)
    )
    fraud = int(risk > 0.42)

    rows.append({
        "return_id": i,
        "orders": orders,
        "returns": returns,
        "disputes": disputes,
        "returns_30d": returns_30d,
        "days_to_return": days_to_return,
        "amount": amount,
        "category": category,
        "reason": reason,
        "payment": payment,
        "fraud": fraud,
    })

df = pd.DataFrame(rows)
df.to_csv("data/returns.csv", index=False)
print("Created data/returns.csv with", len(df), "rows")
