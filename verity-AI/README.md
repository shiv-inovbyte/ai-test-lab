# Verity AI - Predictive Maintenance Assistant

Enhanced predictive maintenance system with machine-specific AI assistance powered by ML models and LLM integration.

## Features

- **ML Prediction**: RandomForest model trained on synthetic sensor data
- **LLM Integration**: OpenAI-powered maintenance advice generation  
- **Machine-specific Analysis**: Track and analyze individual machines by ID
- **REST API**: Easy integration with existing systems
- **Docker Support**: Containerized deployment

## API Endpoints

### 1. Health Check
```
GET /health
```
Returns server status and model loading state.

**Response:**
```json
{
  "status": "ok",
  "model_loaded": true
}
```

### 2. Basic Prediction
```
POST /predict
```
Get raw model predictions for sensor data.

**Request:**
```json
{
  "features": {
    "vibration": 25.5,
    "temperature": 75.2,
    "operating_hours": 1200,
    "temp_vibration_interaction": 1900.6,
    "vibration_rate_of_change": 2.1,
    "temp_rolling_avg": 74.8
  }
}
```

**Response:**
```json
{
  "predictions": [[0.85, 0.15]]
}
```

### 3. Maintenance Advice (NEW)
```
POST /maintenance-advice
```
Get AI-powered maintenance recommendations for a specific machine.

**Request:**
```json
{
  "machine_id": "M001",
  "features": {
    "vibration": 45.5,
    "temperature": 85.2,
    "operating_hours": 1200,
    "temp_vibration_interaction": 3850.6,
    "vibration_rate_of_change": 5.1,
    "temp_rolling_avg": 84.8
  }
}
```

**Response:**
```json
{
  "machine_id": "M001",
  "failure_probability": 78.5,
  "feature_values": {
    "vibration": 45.5,
    "temperature": 85.2,
    "operating_hours": 1200,
    "temp_vibration_interaction": 3850.6,
    "vibration_rate_of_change": 5.1,
    "temp_rolling_avg": 84.8
  },
  "maintenance_advice": "Given the high vibration levels (45.5) and elevated temperature (85.2°F), immediate action is recommended: 1) Stop machine operation immediately 2) Inspect bearings and alignment 3) Check cooling system 4) Schedule emergency maintenance within 4 hours",
  "status": "success"
}
```

## Required Features

The model expects these 6 features in the specified order:
- `vibration`: Vibration amplitude 
- `temperature`: Operating temperature
- `operating_hours`: Total machine runtime
- `temp_vibration_interaction`: Calculated interaction term
- `vibration_rate_of_change`: Rate of vibration change
- `temp_rolling_avg`: Rolling average temperature

## Setup

### Environment Variables
Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_api_key_here
MODEL_PATH=../verity-AI/model.joblib
PORT=6000
```

### Local Development
```bash
# Install dependencies
pip install -r deployment/requirements.txt

# Train the model (if not done)
python verity-AI/save_model.py

# Start the server
cd verity-AI/deployment
python app.py
```

### Docker Deployment
```bash
cd verity-AI/deployment
docker-compose up --build
```

## Testing

Run the test suite to verify all endpoints:
```bash
python verity-AI/test_api.py
```

## Architecture

```
verity-AI/
├── engineer_feature.py          # Feature engineering
├── generate_data.py             # Synthetic data generation  
├── save_model.py               # Model training & saving
├── verity_assistant_ai_llm.py  # LLM integration (enhanced)
├── model.joblib                # Trained model artifact
├── model_features.json         # Feature name ordering
├── test_api.py                 # API testing script
└── deployment/
    ├── app.py                  # Flask API server (enhanced)
    ├── requirements.txt        # Python dependencies
    ├── Dockerfile             # Container definition
    └── docker-compose.yml     # Multi-container setup
```

## Changes Made

### Enhanced LLM Integration
- Added `machine_id` parameter support to all LLM functions
- Created `get_maintenance_advice_api()` for structured API responses
- Improved error handling and response formatting
- Added detailed docstrings and type hints

### New API Endpoint
- `/maintenance-advice` endpoint for machine-specific AI recommendations
- Validates machine_id and feature inputs
- Returns structured JSON with failure probability and LLM advice
- Comprehensive error handling

### Updated Dependencies
- Maintained compatibility with existing requirements
- Added proper module imports and path handling
- Enhanced logging and debugging capabilities

## Security Notes

- Keep your OpenAI API key secure and never commit it to version control
- The model uses joblib (pickle-based) - only load trusted model files
- Use environment variables for sensitive configuration
- Consider rate limiting for production deployments