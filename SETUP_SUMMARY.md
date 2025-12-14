# Project Setup Summary

## Overview
The Credit Risk Assessment System has been restructured to use a unified Python backend and React frontend. This document summarizes the setup process and changes made.

### Directory Structure
```
credit-risk-project/
├── frontend/              # React-based frontend
├── backend/               # Python Flask backend (API + ML service)
├── database/              # SQLite database scripts
├── shared/                # Shared constants and utilities
├── docs/                  # Documentation
├── mlruns/                # ML experiment tracking
├── README.md              # Project documentation
```

### Changes Made
- **Removed**: Node.js backend and separate Python ML service.
- **Added**: Unified Python Flask backend with integrated ML service.
- **Updated**: Frontend API configuration to use port 5000.
- **Updated**: Documentation to reflect the new structure.

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the backend server:
   ```bash
   python app.py
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```

### Database Setup
1. Navigate to the database scripts directory:
   ```bash
   cd database/scripts
   ```
2. Initialize the database:
   ```bash
   python seed.py
   ```
