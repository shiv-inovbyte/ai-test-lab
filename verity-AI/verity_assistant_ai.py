import engineer_feature as ef
import verity_pt_model as vpm

# Once the Pretrained Verity Model is built and evaluated, we can now use an LLM to simulate a conversation around the model and provide "Intelligent" actionalbe insights
# This is a simulation of how a larger LLM could use this trained ML model to provide a conversation response
# Note: This is a simplified simulation and does not involve actual LLM integration

def maintenance_assistance_response(machine_id, ml_model, data_point, knowledge_base):
    """
    Generate a conversational response using the Verity Pretrained Model and a knowledge base from a larger LLM.
    """
    failure_probability = ml_model.predict_proba(data_point.values)[0][1]*100  # Probability of failure_imminent being 1

    response = f"Machine {machine_id}: "

    if failure_probability > 70:
        response += (f"Predicted failure probability is **{failure_probability:.1f}%**. "
                     "Immediate maintenance is recommended to prevent downtime. "
                     "Please refer to the maintenance manual section 4.2 for urgent procedures.")
        action = knowledge_base.get("high_vibration_protocol")
        response += f" Urgent maintainnance is recommended. Protocal from maunala: '{action}'. "
    elif failure_probability > 30:
        response += (f"Predicted failure probability is **{failure_probability:.1f}%**. ")
        action = knowledge_base.get("medium_vibration_protocol")
        response += f" Monitor closely. Consider scheduled maintaince soon: '{action}'. "
    else:
        response += (f"THe machine is operating normally (failure probability {failure_probability:.1f}%). ")
        action = knowledge_base.get("normal_operation_protocol")
        response += f" Continue regular monitoring. Protocol: '{action}'. "

    return response
# Simulated knowledge base from a larger LLM
# RAG - Retrieval Augmented Generation simulated here with a simple dictionary. Vectory like DBs could be used for larger knowledge bases
knowledge_base_data = {
    'high_vibration_protocol': "Check motor mounts and bearing alignment immediately. Refer to manual M-456 for replacement parts.",
    'medium_vibration_protocol': "Perform a full system diagnostic check during the next scheduled downtime. Check for loose bolts.",
    'normal_operation_protocol': "No action required. All systems are within normal operating parameters."
}

# Required to specify all features to train the model [personally struggled with this as I presumed only certain features can be pulled out for suimulation]
# for thousands of features, better to use  config file like features.py
feature_cols = [
    "vibration",
    "temperature",
    "operating_hours",
    "temp_vibration_interaction",
    "vibration_rate_of_change",
    "temp_rolling_avg"
]

# Simulate a new data point for a specific machine showing signs of potential failure
machine_to_check = ef.df_engineered[ef.df_engineered['machine_id'] == 10].iloc[-1]  # Latest data point for machine_id 8
data_for_ai = machine_to_check.to_frame().T
data_for_ai = data_for_ai[feature_cols]
data_for_ai["vibration"] += 20 # Simulate a spike in vibration
data_for_ai["temperature"] += 10 # Simulate a spike in temperature
data_for_ai["temp_rolling_avg"] +=10 # Simulate a spike in temperature

ai_response = maintenance_assistance_response(
    machine_id=8,
    ml_model=vpm.rf_model,
    data_point=data_for_ai,
    knowledge_base=knowledge_base_data
)
print("--- Verity Assistant AI Response ---")
print(ai_response)
    