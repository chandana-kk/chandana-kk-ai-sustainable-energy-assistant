"""Train XGBoost model for optimization priority scoring."""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

SAVED_DIR = Path(__file__).parent / "saved_models"
SAVED_DIR.mkdir(exist_ok=True)


def main():
    np.random.seed(42)
    n = 2000
    df = pd.DataFrame({
        "power_kw": np.random.uniform(0.2, 3.5, n),
        "daily_kwh": np.random.uniform(5, 25, n),
        "monthly_kwh": np.random.uniform(150, 500, n),
        "estimated_bill": np.random.uniform(1200, 4500, n),
    })
    df["priority_score"] = (
        0.4 * df["power_kw"]
        + 0.003 * df["daily_kwh"]
        + 0.002 * df["monthly_kwh"]
        + 0.0003 * df["estimated_bill"]
        + np.random.normal(0, 0.1, n)
    )

    X = df[["power_kw", "daily_kwh", "monthly_kwh", "estimated_bill"]]
    y = df["priority_score"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.1)
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print(f"XGBoost R² on test: {score:.3f}")

    path = SAVED_DIR / "optimizer_model.joblib"
    joblib.dump(model, path)
    print(f"Optimizer model saved to {path}")


if __name__ == "__main__":
    main()
