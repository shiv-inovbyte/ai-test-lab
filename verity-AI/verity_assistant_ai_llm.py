import openai
import os
import dotenv
import numpy as np
import json

import engineer_feature as ef
import verity_pt_model as vpm

# Once the Pretrained Verity Model is built and evaluated, we can now use an LLM to simulate a 
# conversation around the model and provide "Intelligent" actionalbe insights
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Alternate way to pull the key from the .env file if needed
#dotenv.load_dotenv()

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

def get_llm_maintenance_advice(machine_id, failure_probability, feature_values):
    """
    Use OpenAI LLM to generate maintenance advice based on model prediction and features.
    
    Args:
        machine_id (str): Unique identifier for the machine
        failure_probability (float): Predicted failure probability (0-100)
        feature_values (dict): Dictionary of sensor readings/feature values
    
    Returns:
        str: LLM-generated maintenance advice
    """
    prompt = (
        f"Machine {machine_id} has a predicted failure probability of {failure_probability:.1f}%.\n"
        f"Sensor readings: {feature_values}\n"
        "What maintenance action should be taken? Respond in clear, actionable steps for a technician."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Changed to a more stable model
            messages=[
                {"role": "system", "content": "You are an expert maintenance assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating maintenance advice: {str(e)}"

def maintenance_assistance_response_llm(machine_id, ml_model, data_point):
    """
    Generate a conversational response using the Verity Pretrained Model and OpenAI LLM.
    
    Args:
        machine_id (str): Unique identifier for the machine
        ml_model: Trained ML model with predict_proba method
        data_point: DataFrame or array-like with feature values
    
    Returns:
        str: Formatted response with machine ID and LLM advice
    """
    try:
        failure_probability = ml_model.predict_proba(data_point.values)[0][1] * 100
        feature_values = data_point.iloc[0].to_dict()
        llm_response = get_llm_maintenance_advice(machine_id, failure_probability, feature_values)
        return f"Machine {machine_id}: {llm_response}"
    except Exception as e:
        return f"Machine {machine_id}: Error generating response: {str(e)}"


def get_maintenance_advice_api(machine_id, feature_dict, ml_model):
    """
    API-friendly function to get maintenance advice for a specific machine.
    
    Args:
        machine_id (str): Unique identifier for the machine
        feature_dict (dict): Dictionary of feature values
        ml_model: Trained ML model with predict_proba method
    
    Returns:
        dict: Response containing machine_id, failure_probability, and advice
    """
    try:
        # Load feature order from JSON file
        feature_order = load_feature_names()
        
        # Extract features in correct order
        feature_values = [feature_dict.get(f, 0.0) for f in feature_order]
        feature_array = np.array(feature_values).reshape(1, -1)
        
        # Get prediction
        failure_probability = ml_model.predict_proba(feature_array)[0][1] * 100
        
        # Get LLM advice
        advice = get_llm_maintenance_advice(machine_id, failure_probability, feature_dict)
        
        return {
            "machine_id": machine_id,
            "failure_probability": round(failure_probability, 2),
            "feature_values": feature_dict,
            "maintenance_advice": advice,
            "status": "success"
        }
    except Exception as e:
        return {
            "machine_id": machine_id,
            "error": str(e),
            "status": "error"
        }


# Required to specify all features to train the model [personally struggled with this as I presumed only certain features can be pulled out for suimulation]
# for thousands of features, better to use  config file like features.py
feature_cols = load_feature_names()

# Simulate a new data point for a specific machine showing signs of potential failure
machine_to_check = ef.df_engineered[ef.df_engineered['machine_id'] == 8].iloc[-1]  # Latest data point for machine_id 8
data_for_ai = machine_to_check.to_frame().T
data_for_ai = data_for_ai[feature_cols]
data_for_ai["vibration"] += 20 # Simulate a spike in vibration
data_for_ai["temperature"] += 10 # Simulate a spike in temperature
data_for_ai["temp_rolling_avg"] +=10 # Simulate a spike in temperature

# Example usage:
ai_response_llm = maintenance_assistance_response_llm(
    machine_id=8,
    ml_model=vpm.rf_model,
    data_point=data_for_ai
)
print("--- Verity Assistant AI LLM Response ---")
print(ai_response_llm)
