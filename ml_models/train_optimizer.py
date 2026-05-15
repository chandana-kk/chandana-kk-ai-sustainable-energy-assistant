"""
Train XGBoost model for recommendation prioritization.
Run: python train_optimizer.py
"""

import numpy as np
from pathlib import Path
import joblib

MODEL_DIR = Path(__file__).parent / "saved_models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def train():
    try:
        import xgboost as xgb
    except ImportError:
        print("XGBoost not installed. pip install xgboost")
        return

    # Features: hour, monthly_kwh, is_peak
    np.random.seed(42)
    n = 1000
    X = np.column_stack([
        np.random.randint(0, 24, n),
        np.random.uniform(100, 600, n),
        np.random.randint(0, 2, n),
    ])
    # Target: optimization score (higher = more savings potential)
    y = X[:, 1] * 0.01 + X[:, 2] * 2 + (18 <= X[:, 0]) & (X[:, 0] <= 22) * 1.5
    y += np.random.normal(0, 0.3, n)

    model = xgb.XGBRegressor(n_estimators=50, max_depth=4, learning_rate=0.1)
    model.fit(X, y)
    path = MODEL_DIR / "optimizer_xgb.pkl"
    joblib.dump(model, path)
    print(f"Saved optimizer model to {path}")


if __name__ == "__main__":
    train()
