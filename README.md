# Fashion Return Risk

A real-world e-commerce risk analytics project that analyzes fashion return requests using customer behavior, transaction history, return patterns, and product/return images.

## What it does

A return request is scored from 0–100:

- **LOW**: generally safe for automated processing
- **MEDIUM**: additional checks recommended
- **HIGH**: manual review recommended

The system combines:
1. Customer/transaction behavior
2. Return frequency and previous disputes
3. Order value and time-to-return
4. Return reason
5. Image similarity between the original product image and returned-item image

## Stack

- Python
- Streamlit
- pandas
- scikit-learn
- Pillow
- imagehash
- SQLite-compatible CSV workflow

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt
python train_model.py
streamlit run app.py
```

The demo data is synthetic and is included only for development/testing.

## Important

This is a decision-support prototype, not a system that should automatically accuse customers of fraud. A high score should trigger human review, and production use would require validated data, privacy controls, fairness testing, audit logging, and domain review.

## Suggested GitHub description

> Real-time fashion e-commerce return-risk scoring using customer behavior, transaction patterns and computer-vision image similarity.

## Suggested resume title

**Fashion Return Fraud Detection & Risk Platform**
