"""Train LSTM model for hourly energy consumption prediction."""
import os
from pathlib import Path

import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers

SAVED_DIR = Path(__file__).parent / "saved_models"
SAVED_DIR.mkdir(exist_ok=True)


def generate_synthetic_data(n_days: int = 90) -> np.ndarray:
    """Synthetic hourly kWh series with daily seasonality."""
    hours = n_days * 24
    t = np.arange(hours)
    seasonal = 0.5 + 0.4 * np.sin(2 * np.pi * t / 24 - np.pi / 2)
    noise = np.random.normal(0, 0.08, hours)
    return np.maximum(0.1, seasonal + noise).astype(np.float32)


def build_sequences(data: np.ndarray, seq_len: int = 24):
    X, y = [], []
    for i in range(len(data) - seq_len):
        X.append(data[i : i + seq_len])
        y.append(data[i + seq_len])
    return np.array(X)[..., np.newaxis], np.array(y)


def main():
    print("Generating synthetic training data...")
    data = generate_synthetic_data(120)
    X, y = build_sequences(data)
    split = int(0.8 * len(X))
    X_train, X_val = X[:split], X[split:]
    y_train, y_val = y[:split], y[split:]

    model = keras.Sequential([
        layers.Input(shape=(24, 1)),
        layers.LSTM(64, return_sequences=True),
        layers.Dropout(0.2),
        layers.LSTM(32),
        layers.Dense(24),  # predict next 24 hours
    ])
    model.compile(optimizer="adam", loss="mse", metrics=["mae"])
    model.fit(
        X_train,
        np.tile(y_train[:, None], (1, 24)),
        validation_data=(X_val, np.tile(y_val[:, None], (1, 24))),
        epochs=15,
        batch_size=32,
        verbose=1,
    )

    path = SAVED_DIR / "lstm_model.h5"
    model.save(path)
    print(f"LSTM model saved to {path}")


if __name__ == "__main__":
    main()
