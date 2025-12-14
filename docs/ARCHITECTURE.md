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

### 2. Backend (Python Flask)
- **Technology**: Flask, SQLite, scikit-learn, LightGBM
- **Purpose**: Unified backend handling API requests, database operations, and ML predictions
- **Responsibilities**:
  - RESTful API endpoints
  - CRUD operations on credit risk records
  - Database connection and queries
  - ML model loading and inference
  - Data validation and error handling

### 3. Database (SQLite)
- **Purpose**: Store credit risk records
- **Schema**: See `database/README.md`

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
