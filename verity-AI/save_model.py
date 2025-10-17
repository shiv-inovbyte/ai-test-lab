"""Train a simple RandomForest on the engineered synthetic data and save it as model.joblib

This script re-uses existing feature engineering code in `engineer_feature.py` which itself
generates synthetic data via `generate_data.py`.
"""
import os
import joblib
import warnings
import json

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

import engineer_feature as ef


def load_or_create_features():
    """
    Load features from JSON file if it exists, otherwise create the default feature list.
    
    Returns:
        list: List of feature names in the correct order
    """
    features_path = os.path.join(os.path.dirname(__file__), "model_features.json")
    
    # Default features (same as used throughout the codebase)
    default_features = [
        "vibration",
        "temperature",
        "operating_hours",
        "temp_vibration_interaction",
        "vibration_rate_of_change",
        "temp_rolling_avg",
    ]
    
    try:
        if os.path.exists(features_path):
            with open(features_path, "r") as fh:
                features = json.load(fh)
            print(f"Loaded features from {features_path}")
            return features
        else:
            print(f"model_features.json not found, using default feature list")
            return default_features
    except Exception as e:
        print(f"Error loading features from JSON: {e}, using default feature list")
        return default_features


def main():
    # Features expected by other code in the repo
    features = load_or_create_features()
    target = "failure_imminent"

    df = ef.df_engineered

    if df is None or df.empty:
        raise RuntimeError("Engineered dataframe is empty — ensure generate_synthetic_data runs correctly")

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print("--- Model Evaluation ---")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
    print(classification_report(y_test, y_pred))

    out_path = os.path.join(os.path.dirname(__file__), "model.joblib")
    joblib.dump(clf, out_path)
    print(f"Saved model to: {out_path}")
    # Save feature names alongside the model so inference code can preserve ordering
    features_path = os.path.join(os.path.dirname(__file__), "model_features.json")
    with open(features_path, "w") as fh:
        json.dump(features, fh)
    print(f"Saved feature names to: {features_path}")


if __name__ == "__main__":
    main()
