
# Verity Pretrained Model Script

import engineer_feature as ef

# Building the predictive model using RandomForestClassifier for classification
# Random Forest classifier is a machine learning classifiation algorithm that uses multiple decision trees to make predictions usually via majority voting.
# For this program, we need a classifier and not a regressor because we are predicting a binary outcome (failure_imminent: 0 or 1) and not a continuous value.

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Prepare data for the model

features = ["vibration", "temperature", "operating_hours", "temp_vibration_interaction", "vibration_rate_of_change", "temp_rolling_avg"]

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