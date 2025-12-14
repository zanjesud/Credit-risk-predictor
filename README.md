# Credit Risk Assessment Project

## Overview
This project aims to predict credit risk using machine learning models. It includes a backend for model inference, a frontend for user interaction, and a structured database for data storage.

## Project Structure
```
chart.html
credit_risk_dataset.csv
credit-risk-assesment.ipynb
backend/
    app.py
    requirements.txt
    app/
        api/
        config/
        models/
        services/
        utils/
database/
    migrations/
    scripts/
docs/
frontend/
    src/
        components/
        pages/
        services/
        styles/
mlruns/
shared/
```

## Features
- **Backend**: Python-based API for predictions.
- **Frontend**: React-based user interface.
- **Machine Learning**: Pre-trained models for credit risk prediction.
- **Database**: Stores credit risk data and model metadata.

## Setup
### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend
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

### Frontend
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

## Usage
- Access the frontend at `http://localhost:3000`.
- Use the backend API at `http://localhost:5000`.

## Notebooks
- `credit-risk-assesment.ipynb`: Contains exploratory data analysis and model training steps.

## Contributing
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

## License
This project is licensed under the MIT License.
