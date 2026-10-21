from pathlib import Path
import pickle
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score

DATA = Path("data/returns.csv")
MODEL = Path("model.pkl")

if not DATA.exists():
    import synthetic_data  # creates the dataset

df = pd.read_csv(DATA)

features = [
    "orders", "returns", "disputes", "returns_30d",
    "days_to_return", "amount", "category", "reason", "payment"
]
X = df[features]
y = df["fraud"]

numeric = ["orders", "returns", "disputes", "returns_30d", "days_to_return", "amount"]
categorical = ["category", "reason", "payment"]

preprocess = ColumnTransformer([
    ("num", "passthrough", numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
])

model = Pipeline([
    ("preprocess", preprocess),
    ("classifier", RandomForestClassifier(
        n_estimators=250,
        max_depth=10,
        random_state=42,
        class_weight="balanced"
    ))
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model.fit(X_train, y_train)
prob = model.predict_proba(X_test)[:, 1]

print(classification_report(y_test, (prob >= 0.5).astype(int)))
print("ROC-AUC:", round(roc_auc_score(y_test, prob), 4))

with open(MODEL, "wb") as f:
    pickle.dump(model, f)

print("Saved model to", MODEL)
