# Project Structure

Complete folder and file structure for the Credit Risk Assessment System.

```
credit-risk-project/
├── frontend/                          # Frontend Application
│   ├── src/
│   │   ├── components/               # UI Components
│   │   ├── pages/                    # Page components (if using SPA)
│   │   ├── services/                 # API Services
│   │   ├── utils/                    # Utility functions
│   │   ├── styles/                   # CSS Styles
│   │   └── assets/                   # Static assets (images, etc.)
│   ├── index.html                    # Main HTML file
│   ├── package.json                  # Frontend dependencies
├── backend/                          # Python Flask Backend
│   ├── app.py                        # Main Flask application entry point
│   ├── app/
│   │   ├── api/                      # API endpoints
│   │   ├── models/                   # Data models
│   │   ├── services/                 # Business logic
│   │   ├── config/                   # Configuration
├── database/                         # SQLite database scripts
│   ├── migrations/                   # Database migrations
│   ├── scripts/                      # Database initialization scripts
├── docs/                             # Documentation
├── shared/                           # Shared constants and utilities
├── mlruns/                           # Machine learning experiment tracking
├── README.md                         # Project documentation
```

## Key Files

### Backend (Python)
- `backend/app.py` - Flask application entry point
- `backend/app/config/database.py` - SQLite database connection
- `backend/app/api/routes.py` - API route registration
- `backend/app/api/records.py` - Records API endpoints
- `backend/app/api/predict.py` - Prediction API endpoints
- `backend/app/models/record_model.py` - Database model
- `backend/app/services/predict_service.py` - ML prediction service

### Frontend
- `frontend/index.html` - Main HTML
- `frontend/src/app.js` - Main application logic
- `frontend/src/services/api.js` - API client (configured for port 5000)

### Database
- `database/scripts/seed.py` - Database initialization (Python)

## Environment Files

Backend `.env` file:
```
PORT=5000
DEBUG=False
DB_PATH=../database/credit_risk.db
MODEL_PATH=../models/final_lgbm_model.joblib
```

## Model Files

Trained ML models should be placed in:
- `models/` directory (create if needed)
- Or update `MODEL_PATH` in `.env` to point to your model location
