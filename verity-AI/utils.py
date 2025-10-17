"""
Shared utility functions for the Verity AI system.

This module provides common functions used across different components,
particularly for loading feature names from the model_features.json file.
"""

import os
import json


def load_feature_names(file_path=None):
    """
    Load feature names from model_features.json file.
    
    Args:
        file_path (str, optional): Path to the JSON file. If None, uses default location.
    
    Returns:
        list: List of feature names in the correct order
    """
    if file_path is None:
        file_path = os.path.join(os.path.dirname(__file__), "model_features.json")
    
    # Default features (same as used throughout the codebase)
    default_features = [
        "vibration",
        "temperature",
        "operating_hours",
        "temp_vibration_interaction",
        "vibration_rate_of_change",
        "temp_rolling_avg"
    ]
    
    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as fh:
                features = json.load(fh)
            return features
        else:
            print(f"Warning: model_features.json not found at {file_path}, using default feature list")
            return default_features
    except Exception as e:
        print(f"Error loading features from JSON: {e}, using default feature list")
        return default_features


def get_feature_dict_ordered(feature_dict, feature_names=None):
    """
    Get feature values in the correct order from a feature dictionary.
    
    Args:
        feature_dict (dict): Dictionary mapping feature names to values
        feature_names (list, optional): Ordered list of feature names. If None, loads from JSON.
    
    Returns:
        list: Feature values in the correct order
    """
    if feature_names is None:
        feature_names = load_feature_names()
    
    return [feature_dict.get(f, 0.0) for f in feature_names]


def validate_feature_dict(feature_dict, feature_names=None):
    """
    Validate that a feature dictionary contains all required features.
    
    Args:
        feature_dict (dict): Dictionary mapping feature names to values
        feature_names (list, optional): Required feature names. If None, loads from JSON.
    
    Returns:
        tuple: (is_valid, missing_features)
    """
    if feature_names is None:
        feature_names = load_feature_names()
    
    missing_features = []
    for feature in feature_names:
        if feature not in feature_dict:
            missing_features.append(feature)
    
    return len(missing_features) == 0, missing_features