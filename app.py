import pickle
from pathlib import Path
import pandas as pd
import streamlit as st
from PIL import Image
import imagehash

st.set_page_config(page_title="Fashion Return Risk", page_icon="🛍️", layout="wide")

MODEL_PATH = Path("model.pkl")
DATA_PATH = Path("data/returns.csv")

st.title("🛍️ Fashion Return Risk")
st.caption("Decision-support prototype for e-commerce return review")

if not MODEL_PATH.exists():
    st.warning("Model not found. Run: python train_model.py")
    st.stop()

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

st.sidebar.header("Return request")

orders = st.sidebar.number_input("Customer total orders", 1, 100, 15)
returns = st.sidebar.number_input("Customer total returns", 0, 100, 4)
disputes = st.sidebar.number_input("Previous disputes", 0, 20, 1)
returns_30d = st.sidebar.number_input("Returns in last 30 days", 0, 20, 1)
days_to_return = st.sidebar.number_input("Days after purchase", 1, 60, 5)
amount = st.sidebar.number_input("Order value (₹)", 100.0, 100000.0, 3999.0)
category = st.sidebar.selectbox("Product category", ["dress", "jacket", "shoes", "jeans", "shirt", "handbag"])
reason = st.sidebar.selectbox("Return reason", ["damaged", "wrong_size", "changed_mind", "wrong_item", "not_as_expected"])
payment = st.sidebar.selectbox("Payment method", ["card", "upi", "cod", "wallet"])

st.subheader("1. Analyze return request")

row = pd.DataFrame([{
    "orders": orders,
    "returns": returns,
    "disputes": disputes,
    "returns_30d": returns_30d,
    "days_to_return": days_to_return,
    "amount": amount,
    "category": category,
    "reason": reason,
    "payment": payment
}])

if st.button("Analyze Risk", type="primary"):
    probability = float(model.predict_proba(row)[0, 1])
    score = round(probability * 100)

    if score >= 70:
        level = "HIGH"
        action = "Manual inspection recommended"
    elif score >= 35:
        level = "MEDIUM"
        action = "Additional verification recommended"
    else:
        level = "LOW"
        action = "Eligible for normal processing"

    c1, c2, c3 = st.columns(3)
    c1.metric("Risk score", f"{score}/100")
    c2.metric("Risk level", level)
    c3.metric("Recommended action", action)

    st.progress(score / 100)

    reasons = []
    if returns / max(orders, 1) > 0.35:
        reasons.append("High historical return rate")
    if returns_30d >= 3:
        reasons.append("Several returns in the last 30 days")
    if disputes >= 2:
        reasons.append("Previous return disputes")
    if days_to_return <= 2:
        reasons.append("Very short time between purchase and return")
    if amount >= 8000:
        reasons.append("High-value order")
    if reason in ["damaged", "wrong_item"]:
        reasons.append(f"Return reason: {reason}")

    st.subheader("Why this score?")
    if reasons:
        for r in reasons:
            st.write("⚠️", r)
    else:
        st.write("No strong behavioral risk signals were detected.")

st.divider()
st.subheader("2. Optional image comparison")

col1, col2 = st.columns(2)
with col1:
    original = st.file_uploader("Original product image", type=["jpg", "jpeg", "png"])
with col2:
    returned = st.file_uploader("Returned-item image", type=["jpg", "jpeg", "png"])

if original and returned:
    img1 = Image.open(original).convert("RGB")
    img2 = Image.open(returned).convert("RGB")
    h1 = imagehash.phash(img1)
    h2 = imagehash.phash(img2)
    distance = h1 - h2
    similarity = max(0.0, 1.0 - distance / 64.0)

    st.image([img1, img2], caption=["Original", "Returned item"], width=280)
    st.metric("Image similarity", f"{similarity:.0%}")

    if similarity < 0.65:
        st.warning("Low visual similarity — consider manual inspection.")
    else:
        st.success("Images have relatively high visual similarity.")

st.divider()
st.subheader("3. Historical return analytics")

if DATA_PATH.exists():
    df = pd.read_csv(DATA_PATH)
    a, b, c = st.columns(3)
    a.metric("Historical returns", f"{len(df):,}")
    b.metric("High-risk label rate", f"{df.fraud.mean():.1%}")
    c.metric("Average order value", f"₹{df.amount.mean():,.0f}")
    st.bar_chart(df.groupby("category")["fraud"].mean().sort_values(ascending=False))
else:
    st.info("Run synthetic_data.py to create demo analytics.")
