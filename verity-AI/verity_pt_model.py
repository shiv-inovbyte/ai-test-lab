
# Verity Pretrained Model Script

import os
import json
import engineer_feature as ef

# Building the predictive model using RandomForestClassifier for classification
# Random Forest classifier is a machine learning classifiation algorithm that uses multiple decision trees to make predictions usually via majority voting.
# For this program, we need a classifier and not a regressor because we are predicting a binary outcome (failure_imminent: 0 or 1) and not a continuous value.

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score


def load_feature_names():
    """
    Load feature names from model_features.json file.
    
    Returns:
        list: List of feature names in the correct order
    """
    try:
        features_path = os.path.join(os.path.dirname(__file__), "model_features.json")
        with open(features_path, "r") as fh:
            features = json.load(fh)
        return features
    except FileNotFoundError:
        # Fallback to hardcoded features if file not found
        print("Warning: model_features.json not found, using fallback feature list")
        return [
            "vibration",
            "temperature",
            "operating_hours",
            "temp_vibration_interaction",
            "vibration_rate_of_change",
            "temp_rolling_avg"
        ]
    except Exception as e:
        print(f"Error loading features from JSON: {e}")
        return [
            "vibration",
            "temperature",
            "operating_hours",
            "temp_vibration_interaction",
            "vibration_rate_of_change",
            "temp_rolling_avg"
        ]


# Prepare data for the model
features = load_feature_names()

target = "failure_imminent"

X = ef.df_engineered[features]
y = ef.df_engineered[target]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

rf_model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate the model
y_pred = rf_model.predict(X_test)
print("--- Model Evaluation ---")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))