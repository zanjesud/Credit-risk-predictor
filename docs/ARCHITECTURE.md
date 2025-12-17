# Architecture Overview

## System Architecture

```
┌─────────────┐
│   Frontend  │ (HTML/CSS/JS)
│   Port 3001 │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────┐
│   Backend   │ (Python/Flask)
│   Port 5000 │
│             │
│  ┌────────┐ │
│  │  API   │ │ - RESTful endpoints
│  └────────┘ │
│  ┌────────┐ │
│  │   ML   │ │ - Model loading
│  │Service │ │ - Predictions
│  └────────┘ │
└──────┬──────┘
       │
       └──► SQLite Database
            (credit_risk.db)
```

## Components

### 1. Frontend
- **Technology**: HTML/CSS/JavaScript
- **Purpose**: User interface for viewing and managing credit risk records
- **Features**:
  - Display all records
  - View record details with risk assessment
  - Add new records
  - Real-time risk prediction display
  - Organized structure:
    - `components/`: Reusable UI components
    - `pages/`: Page-level components
    - `services/`: API interaction logic
    - `utils/`: Helper functions
    - `styles/`: CSS styles

### 2. Backend (Python Flask)
- **Technology**: Flask, SQLite, scikit-learn, LightGBM
- **Purpose**: Unified backend handling API requests, database operations, and ML predictions
- **Responsibilities**:
  - RESTful API endpoints
  - CRUD operations on credit risk records
  - Database connection and queries
  - ML model loading and inference
  - Data validation and error handling
  - Organized structure:
    - `api/`: API endpoints
    - `models/`: Database models
    - `services/`: Business logic (ML service)
    - `config/`: Configuration files
    - `utils/`: Utility functions

### 3. Database (SQLite)
- **Purpose**: Store credit risk records
- **Schema**: See `database/scripts/seed.py` for initialization
- **Structure**:
  - `scripts/`: Database initialization scripts
  - `migrations/`: Database migration files

### 4. Shared
- **Purpose**: Shared constants and utilities
- **Structure**:
  - `constants/index.js`: Centralized constants for risk categories, loan grades, etc.

## Data Flow

1. **View Records**:
   - Frontend → Backend API → SQLite Database
   - Backend returns records to Frontend

2. **View Record with Risk Assessment**:
   - Frontend → Backend API → SQLite Database (get record)
   - Backend → ML Service (get prediction)
   - Backend → Frontend (return record + prediction)

3. **Add New Record**:
   - Frontend → Backend API
   - Backend → ML Service (get prediction)
   - Backend → SQLite Database (save record with prediction)
   - Backend → Frontend (return created record)

## Model Integration

The ML models are trained in the Jupyter notebook (`credit-risk-assesment.ipynb`) and saved as:
- Joblib files (`.joblib`)
- MLflow models

The backend's `PredictService` loads these models and applies the same preprocessing pipeline used during training.

## Backend Structure

```
backend/
├── app.py                    # Flask app factory
├── app/
│   ├── api/                 # API endpoints (Blueprints)
│   ├── models/              # Database models
│   ├── services/            # Business logic (ML service)
│   ├── config/              # Configuration
│   └── utils/               # Utilities
```

## Security Considerations

- Input validation on all endpoints
- SQL injection prevention (parameterized queries)
- CORS configuration for API access
- Environment variables for sensitive configuration

## Future Enhancements

- Authentication and authorization
- API rate limiting
- Caching for predictions
- WebSocket support for real-time updates
- Batch prediction endpoints
- Model versioning and A/B testing
- Convert to FastAPI for better async support
- Add database migrations framework (Alembic)
