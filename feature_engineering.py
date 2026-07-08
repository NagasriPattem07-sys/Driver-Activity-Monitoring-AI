import pandas as pd
import numpy as np


def create_windows(
    data,
    window_size=20,
    step_size=10,
    feature_cols=None,
    label_col="Class"
):

    if feature_cols is None:
        feature_cols = ['AccX','AccY','AccZ','GyroX','GyroY','GyroZ']

    data = data.sort_values("Timestamp").reset_index(drop=True)

    features_list = []
    labels_list = []

    for start in range(0, len(data)-window_size+1, step_size):

        window = data.iloc[start:start+window_size]

        if label_col in window.columns:
            if window[label_col].nunique() > 1:
                continue

        row = []

        for col in feature_cols:

            values = window[col].values

            row.extend([
                values.mean(),
                values.std(),
                values.min(),
                values.max(),
                values.max() - values.min()
            ])

        features_list.append(row)

        if label_col in window.columns:
            labels_list.append(window[label_col].iloc[0])

    feature_names = []

    for col in feature_cols:
        feature_names.extend([
            f"{col}_mean",
            f"{col}_std",
            f"{col}_min",
            f"{col}_max",
            f"{col}_range"
        ])

    X = pd.DataFrame(features_list, columns=feature_names)

    if label_col in data.columns:
        y = pd.Series(labels_list)
        return X, y

    return X