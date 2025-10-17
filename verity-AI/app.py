import os
import json
import sys
from typing import Any, Dict

from flask import Flask, request, jsonify
from dotenv import load_dotenv
import joblib
import numpy as np

# Add parent directory to Python path to import verity modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import verity_assistant_ai_llm as llm_assistant
    import utils
except ImportError as e:
    llm_assistant = None
    utils = None
    print(f"Warning: Could not import modules: {e}")

# Load environment variables from .env if present
load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH", "../verity-AI/model.joblib")

app = Flask(__name__)
model = None
model_feature_names = None


def load_model(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found at {path}")
    return joblib.load(path)


# Load the model at module import time (safer across Flask versions)
try:
    model = load_model(MODEL_PATH)
    app.logger.info(f"Loaded model from {MODEL_PATH}")
    # attempt to load a companion feature list
    try:
        feature_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model_features.json")
        if os.path.exists(feature_path):
            with open(feature_path, "r") as fh:
                model_feature_names = json.load(fh)
                app.logger.info(f"Loaded feature list from {feature_path}")
    except Exception:
        app.logger.exception("Failed to load feature list")
except Exception:
    app.logger.exception("Failed to load model")
    model = None


@app.route("/health", methods=["GET"])
def health() -> Any:
    return jsonify({"status": "ok", "model_loaded": model is not None})


@app.route("/predict", methods=["POST"])
def predict() -> Any:
    if model is None:
        return jsonify({"error": "model not loaded"}), 500

    payload: Dict[str, Any] = request.get_json(force=True)
    # Expect either {"features": [v1, v2, ...]} or {"features": {"feature_name": value, ...}}
    features = payload.get("features")
    if features is None:
        return jsonify({"error": "features key is required"}), 400

    try:
        # Handle both list and dict formats for features
        if isinstance(features, list):
            # Features provided as list - use directly
            feature_values = features
        elif isinstance(features, dict):
            # Features provided as dict - convert to ordered list
            feature_names = model_feature_names if model_feature_names is not None else getattr(model, "feature_names_in_", None)
            print(f"DEBUG: feature_names = {feature_names}")
            print(f"DEBUG: features dict = {features}")
            if feature_names is not None:
                feature_values = [features.get(k, 0.0) for k in feature_names]
                print(f"DEBUG: feature_values = {feature_values}")
            else:
                return jsonify({"error": "Model has no feature names - please provide features as a list"}), 400
        else:
            return jsonify({"error": "features must be a list or dict"}), 400

        # Convert to numpy array and make prediction
        arr = np.asarray(feature_values, dtype=float)
        if arr.ndim == 1:
            arr = arr.reshape(1, -1)
        preds = model.predict_proba(arr) if hasattr(model, "predict_proba") else model.predict(arr)
        # Convert numpy arrays to Python lists for JSON
        out = np.asarray(preds).tolist()
        return jsonify({"predictions": out})
    except Exception as e:
        app.logger.exception("Prediction failed")
        return jsonify({"error": str(e)}), 500


@app.route("/maintenance-advice", methods=["POST"])
def maintenance_advice() -> Any:
    """
    Get maintenance advice for a specific machine using ML prediction + LLM.
    
    Expected payload:
    {
        "machine_id": "M001",
        "features": {
            "vibration": 25.5,
            "temperature": 75.2,
            "operating_hours": 1200,
            "temp_vibration_interaction": 1900.6,
            "vibration_rate_of_change": 2.1,
            "temp_rolling_avg": 74.8
        }
    }
    """
    if model is None:
        return jsonify({"error": "model not loaded"}), 500
    
    if llm_assistant is None:
        return jsonify({"error": "LLM assistant not available"}), 500

    payload: Dict[str, Any] = request.get_json(force=True)
    
    # Validate required fields
    machine_id = payload.get("machine_id")
    features = payload.get("features")
    
    if not machine_id:
        return jsonify({"error": "machine_id is required"}), 400
    
    if not features or not isinstance(features, dict):
        return jsonify({"error": "features dict is required"}), 400

    # Validate features if utils is available
    if utils:
        is_valid, missing_features = utils.validate_feature_dict(features)
        if not is_valid:
            return jsonify({
                "error": f"Missing required features: {missing_features}",
                "required_features": utils.load_feature_names()
            }), 400

    try:
        # Use the API-friendly function from LLM assistant
        result = llm_assistant.get_maintenance_advice_api(
            machine_id=str(machine_id),
            feature_dict=features,
            ml_model=model
        )
        
        if result.get("status") == "error":
            return jsonify(result), 500
        
        return jsonify(result)
    except Exception as e:
        app.logger.exception("Maintenance advice failed")
        return jsonify({
            "machine_id": machine_id,
            "error": str(e),
            "status": "error"
        }), 500


if __name__ == "__main__":
    # Useful for local debugging; in production run via gunicorn
    port = int(os.getenv("PORT", 6000))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_DEBUG", "false").lower() in ("1", "true"))
