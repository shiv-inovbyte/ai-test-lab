#!/usr/bin/env python3
"""
Test script for the enhanced Verity AI API with machine ID support.

This script demonstrates how to:
1. Call the /health endpoint
2. Call the /predict endpoint  
3. Call the new /maintenance-advice endpoint with machine ID
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:6000"  # Adjust port as needed

def test_health():
    """Test the health endpoint."""
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_predict():
    """Test the basic prediction endpoint with dict format."""
    print("\nTesting /predict endpoint (dict format)...")
    
    # Sample feature values as dict
    payload = {
        "features": {
            "vibration": 25.5,
            "temperature": 75.2,
            "operating_hours": 1200,
            "temp_vibration_interaction": 1900.6,
            "vibration_rate_of_change": 2.1,
            "temp_rolling_avg": 74.8
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_predict_list():
    """Test the basic prediction endpoint with list format."""
    print("\nTesting /predict endpoint (list format)...")
    
    # Sample feature values as ordered list
    payload = {
        "features": [25.5, 75.2, 1200, 1900.6, 2.1, 74.8]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_maintenance_advice():
    """Test the new maintenance advice endpoint with machine ID."""
    print("\nTesting /maintenance-advice endpoint...")
    
    # Sample payload with machine ID and features
    payload = {
        "machine_id": 8,
        "features": {
            "vibration": 45.5,  # Higher vibration indicating potential issue
            "temperature": 85.2,  # Higher temperature
            "operating_hours": 1200,
            "temp_vibration_interaction": 3850.6,
            "vibration_rate_of_change": 5.1,  # Rapid change
            "temp_rolling_avg": 84.8
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/maintenance-advice",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("Verity AI API Test Suite")
    print("=" * 50)
    
    # Test each endpoint
    health_ok = test_health()
    predict_dict_ok = test_predict()
    predict_list_ok = test_predict_list()
    advice_ok = test_maintenance_advice()
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"Health endpoint: {'✓' if health_ok else '✗'}")
    print(f"Predict endpoint (dict): {'✓' if predict_dict_ok else '✗'}")
    print(f"Predict endpoint (list): {'✓' if predict_list_ok else '✗'}")
    print(f"Maintenance advice endpoint: {'✓' if advice_ok else '✗'}")
    
    if all([health_ok, predict_dict_ok, predict_list_ok, advice_ok]):
        print("\nAll tests passed! 🎉")
    else:
        print("\nSome tests failed. Check the server logs.")

if __name__ == "__main__":
    main()