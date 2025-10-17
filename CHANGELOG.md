# Changelog

All notable changes to the AI Test Lab project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Machine ID Support for LLM Assistant** - Enhanced `verity_assistant_ai_llm.py` to accept machine ID as input parameter for personalized maintenance advice
- **New `/maintenance-advice` API Endpoint** - Added comprehensive API endpoint that combines ML predictions with LLM-powered maintenance recommendations
- **Centralized Feature Management** - Implemented consistent feature loading from `model_features.json` across all modules
- **Shared Utilities Module** - Created `utils.py` with common functions for feature validation and loading
- **Enhanced API Validation** - Added comprehensive input validation with helpful error messages
- **Test Suite** - Created `test_api.py` for automated testing of all API endpoints
- **Docker Support** - Added containerization with `Dockerfile` and `docker-compose.yml`
- **Comprehensive Documentation** - Added detailed README with API documentation and setup instructions

### Enhanced
- **LLM Integration** - Improved `get_llm_maintenance_advice()` function with better error handling and response formatting
- **Model Training Pipeline** - Updated `save_model.py` to use JSON-based feature management and save feature ordering
- **Deployment Architecture** - Enhanced Flask app with better module imports and error handling
- **Feature Consistency** - All modules now use `model_features.json` as single source of truth for feature definitions
- **API Robustness** - Added graceful fallbacks and detailed error messages for better debugging

### Technical Improvements
- **Code Organization** - Restructured project with proper deployment folder and separation of concerns
- **Error Handling** - Implemented comprehensive error handling across all modules
- **Type Safety** - Added type hints and better input validation
- **Logging** - Enhanced logging for better debugging and monitoring
- **Documentation** - Added inline documentation and comprehensive README files

## [1.0.0] - 2025-10-17

### Added
- **Initial Verity AI System** - Complete predictive maintenance system with ML models
- **Feature Engineering Pipeline** - Synthetic data generation and feature engineering capabilities
- **RandomForest Model** - Trained classification model for failure prediction
- **Basic AI Assistant** - Rule-based maintenance advice system
- **LLM Integration** - OpenAI GPT integration for intelligent maintenance recommendations
- **REST API** - Flask-based API for model predictions
- **Jupyter Notebooks** - Comprehensive notebooks for experimentation and learning

### Features
- **Synthetic Data Generation** - `generate_data.py` creates realistic sensor data
- **Feature Engineering** - `engineer_feature.py` creates interaction and derived features
- **Model Training** - `verity_pt_model.py` and `save_model.py` for model development
- **AI Assistance** - `verity_assistant_ai.py` and `verity_assistant_ai_llm.py` for intelligent recommendations
- **Web API** - RESTful endpoints for integration with external systems

### Technical Stack
- **Machine Learning**: scikit-learn, numpy, pandas
- **LLM Integration**: OpenAI API
- **Web Framework**: Flask
- **Deployment**: Docker, gunicorn
- **Development**: Jupyter, matplotlib, seaborn

## API Endpoints

### Current Endpoints
- `GET /health` - System health check
- `POST /predict` - Raw ML model predictions  
- `POST /maintenance-advice` - Machine-specific AI recommendations (NEW)

### Machine ID Integration
The new `/maintenance-advice` endpoint accepts:
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

And returns structured maintenance advice with failure probability and LLM-generated recommendations.

## Breaking Changes

### None
All changes maintain backward compatibility. Existing API endpoints continue to work as before.

## Migration Notes

### Feature Management
- All modules now read from `model_features.json` for consistent feature ordering
- Fallback mechanisms ensure stability if JSON file is missing
- No changes required for existing deployments

### New Dependencies
- Enhanced OpenAI integration requires `OPENAI_API_KEY` environment variable
- Docker deployment recommended for production use

## Security Considerations

### API Keys
- OpenAI API key should be set as environment variable
- Never commit API keys to version control
- Use `.env` files for local development

### Model Security
- joblib files use pickle - only load trusted model files
- Consider model signing for production deployments

## Future Roadmap

### Planned Features
- Real-time sensor data integration
- Advanced analytics dashboard
- Multi-model ensemble predictions
- Historical trend analysis
- Automated alert system

### Technical Improvements
- FastAPI migration for better performance
- Database integration for persistent storage
- Authentication and authorization
- Rate limiting and monitoring
- Automated testing pipeline

---

**Note**: This project is under active development. Features and APIs may evolve based on user feedback and requirements.