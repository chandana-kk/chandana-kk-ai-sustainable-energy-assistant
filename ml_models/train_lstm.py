"""
Train LSTM model for energy consumption prediction.
Run: python train_lstm.py
"""

import numpy as np
from pathlib import Path

MODEL_DIR = Path(__file__).parent / "saved_models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def generate_synthetic_data(n_samples: int = 2000, seq_len: int = 24) -> tuple:
    """Synthetic hourly consumption patterns."""
    X, y = [], []
    for _ in range(n_samples):
        base = np.random.uniform(0.3, 1.2)
        seq = base + 0.2 * np.sin(np.linspace(0, 4 * np.pi, seq_len))
        seq += np.random.normal(0, 0.05, seq_len)
        if np.random.random() > 0.5:
            seq[18:22] *= 1.4  # peak hours
        X.append(seq)
        y.append(seq[-1] * np.random.uniform(0.9, 1.1))
    return np.array(X), np.array(y)


def train():
    try:
        from tensorflow.keras.layers import LSTM, Dense
        from tensorflow.keras.models import Sequential
    except ImportError:
        print("TensorFlow not installed. pip install tensorflow")
        return

    X, y = generate_synthetic_data()
    X = X.reshape((X.shape[0], X.shape[1], 1))
    model = Sequential([
        LSTM(32, input_shape=(24, 1)),
        Dense(16, activation="relu"),
        Dense(1),
    ])
    model.compile(optimizer="adam", loss="mse", metrics=["mae"])
    model.fit(X, y, epochs=10, batch_size=32, validation_split=0.2, verbose=1)
    path = MODEL_DIR / "lstm_energy.h5"
    model.save(path)
    print(f"Saved LSTM model to {path}")


if __name__ == "__main__":
    train()
