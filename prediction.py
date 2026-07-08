import joblib

from feature_engineering import create_windows

# Load model artifacts
model = joblib.load("model/xgb_model.pkl")
label_encoder = joblib.load("model/label_encoder.pkl")
window_config = joblib.load("model/window_config.pkl")


def predict_driver(sensor_dataframe):

    result = create_windows(
        sensor_dataframe,
        window_size=window_config["window_size"],
        step_size=window_config["step_size"],
        feature_cols=window_config["feature_cols"]
    )

    if isinstance(result, tuple):
        X, _ = result
    else:
        X = result

    prediction = model.predict(X)

    behaviour = label_encoder.inverse_transform(prediction)

    return behaviour