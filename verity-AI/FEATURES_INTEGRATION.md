# Verity AI - Model Features JSON Integration

## Overview
This document outlines the comprehensive updates made to integrate consistent feature loading from the `model_features.json` file across the entire Verity AI codebase.

## Changes Made

### 1. Core Files Updated

#### `save_model.py`
- Added `load_or_create_features()` function to read from `model_features.json`
- Falls back to default feature list if JSON file doesn't exist
- Ensures model training uses the same features as inference

#### `verity_pt_model.py`
- Added `load_feature_names()` function
- Updated to use JSON-based feature loading instead of hardcoded list
- Maintains backward compatibility with fallback feature list

#### `verity_assistant_ai.py`
- Added `load_feature_names()` function
- Updated `feature_cols` to use JSON-based loading
- Ensures AI assistant uses consistent feature ordering

#### `verity_assistant_ai_llm.py`
- Already had JSON loading functionality
- Uses `load_feature_names()` for consistent feature ordering
- Enhanced with proper error handling and fallbacks

### 2. New Utility Module

#### `utils.py` (NEW)
- Centralized utility functions for feature management
- `load_feature_names()`: Load features from JSON with fallback
- `get_feature_dict_ordered()`: Convert feature dict to ordered list
- `validate_feature_dict()`: Validate required features are present

### 3. Enhanced API

#### `deployment/app.py`
- Integrated with utils module for feature validation
- Added validation for required features in `/maintenance-advice` endpoint
- Provides clear error messages for missing features
- Uses consistent feature ordering across all endpoints

## Feature Loading Strategy

### Primary Source: `model_features.json`
```json
[
  "vibration",
  "temperature", 
  "operating_hours",
  "temp_vibration_interaction",
  "vibration_rate_of_change",
  "temp_rolling_avg"
]
```

### Fallback Mechanism
If `model_features.json` is not found or corrupted, all modules fall back to the hardcoded feature list to ensure system stability.

### Load Order
1. Check for `model_features.json` in the script's directory
2. Load and parse JSON if file exists
3. Fall back to hardcoded list if file missing or parsing fails
4. Log appropriate warnings to help with debugging

## Benefits

### 1. Consistency
- All modules now use the same feature order
- Single source of truth for feature definitions
- Eliminates risk of mismatched features between training and inference

### 2. Maintainability
- Feature changes only need to be made in one place
- Easy to add/remove features without code changes
- Version control for feature sets

### 3. Robustness
- Graceful fallback if JSON file is missing
- Clear error messages for debugging
- Validation prevents runtime errors from missing features

### 4. API Enhancement
- Better error messages for invalid requests
- Feature validation at request time
- Clear documentation of required features

## File Structure
```
verity-AI/
├── model_features.json         # Single source of truth
├── utils.py                   # Shared utilities (NEW)
├── save_model.py              # Updated to use JSON
├── verity_pt_model.py         # Updated to use JSON  
├── verity_assistant_ai.py     # Updated to use JSON
├── verity_assistant_ai_llm.py # Already uses JSON
└── deployment/
    └── app.py                 # Enhanced with validation
```

## Usage Examples

### Loading Features in Python
```python
from utils import load_feature_names

# Load features from JSON with fallback
features = load_feature_names()

# Validate feature dictionary
is_valid, missing = validate_feature_dict(feature_dict)
```

### API Request Format
```bash
curl -X POST http://localhost:6000/maintenance-advice \
  -H "Content-Type: application/json" \
  -d '{
    "machine_id": "M001",
    "features": {
      "vibration": 25.5,
      "temperature": 75.2,
      "operating_hours": 1200,
      "temp_vibration_interaction": 1900.6,
      "vibration_rate_of_change": 2.1,
      "temp_rolling_avg": 74.8
    }
  }'
```

## Migration Notes

### Backward Compatibility
- All existing scripts continue to work
- Fallback mechanism ensures no breaking changes
- Hardcoded feature lists remain as backup

### Testing
- All modules compile successfully
- Syntax validation passed for all updated files
- Feature loading tested with and without JSON file

### Deployment
- No changes needed to existing deployment configurations
- JSON file is created automatically by `save_model.py`
- Docker containers will include the JSON file in the mounted volume

## Next Steps

1. **Test the complete pipeline**: Train model → Save features → Run API
2. **Validate API endpoints**: Test all three endpoints with real requests
3. **Monitor feature consistency**: Ensure all modules use the same features
4. **Consider feature versioning**: Add version tracking to JSON file for future updates

## Error Handling

### Common Issues and Solutions

1. **Missing JSON file**: Falls back to hardcoded features with warning
2. **Corrupted JSON**: Falls back to hardcoded features with error message
3. **Missing features in API request**: Returns 400 error with list of required features
4. **Feature count mismatch**: Model validation catches dimension mismatches

This comprehensive update ensures all components of the Verity AI system use consistent feature definitions while maintaining robustness and providing clear error messages for debugging.