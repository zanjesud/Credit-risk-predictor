# Quick Start Guide

Follow these steps to get the Credit Risk Assessment System up and running.

## Prerequisites

1. **Python** (v3.8 or higher)
   - Download from: https://www.python.org/
   
2. **pip** (comes with Python)

3. **Node.js** (v16 or higher, for frontend development server)
   - Download from: https://nodejs.org/

## Step 1: Setup Backend (Python)

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The backend will run on `http://localhost:5000`

**Note:** Ensure the trained ML model is located at the path specified in `MODEL_PATH` in your `.env` file.

## Step 2: Setup Database

```bash
cd database/scripts
python seed.py
```

This will create the SQLite database file at `database/credit_risk.db`

## Step 3: Setup Frontend

```bash
cd frontend
npm install
npm start
```

The frontend will be available at `http://localhost:3000`.

## Step 4: Access the Application

Open your browser and navigate to:
```
http://localhost:3000
```

## Running the Application

You need to run the backend in a terminal:

### Terminal 1 - Backend
```bash
cd backend
python app.py
```

### Terminal 2 - Frontend (optional, can use any static server)
```bash
cd frontend
npm start
```

## Verifying Setup

1. **Backend Health Check:**
   ```bash
   curl http://localhost:5000/health
   ```

2. **Frontend:**
   - Open `http://localhost:3000` in your browser

## Common Issues

### Port Already in Use
If port 5000 is already in use, change it in `backend/.env`:
```
PORT=5001
```

### Model Not Found
Make sure you've trained the model using the Jupyter notebook and saved it to the path specified in `backend/.env`:
```
MODEL_PATH=../models/final_lgbm_model.joblib
```

### Database Connection Issues
Ensure the database path in `backend/.env` is correct:
```
DB_PATH=../database/credit_risk.db
```

### Python Dependencies
If you encounter import errors, make sure all dependencies are installed:
```bash
pip install -r backend/requirements.txt
```

## Next Steps

1. Import your CSV data into the database
2. Train your ML model using the Jupyter notebook
3. Test the API endpoints
4. Customize the frontend as needed

For detailed documentation, see:
- `README.md` - Main project overview
- `docs/ARCHITECTURE.md` - Architecture details
- `backend/README.md` - Backend documentation
