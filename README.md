# 🚀 Credit Risk Assessment Project

## Overview
This project leverages machine learning to predict credit risk, offering a comprehensive solution with a robust backend for model inference, an interactive frontend for user engagement, and a structured database for data management. Our goal is to provide an accurate and efficient tool for assessing creditworthiness.

## ✨ Features
- **Intelligent Backend**: A Python-based API designed for high-performance credit risk predictions using advanced machine learning models.
- **Intuitive Frontend**: A modern React-based user interface, providing a seamless and responsive experience for interacting with the credit risk assessment system.
- **Advanced Machine Learning**: Utilizes pre-trained, state-of-the-art models to deliver precise credit risk predictions.
- **Structured Data Management**: A well-organized database for securely storing credit risk data, model metadata, and historical predictions.

## 🛠️ Technologies Used
- **Backend**: Flask, Python, Scikit-learn, Pandas, NumPy, XGBoost, LightGBM, CatBoost
- **Frontend**: Vanilla JavaScript, HTML, CSS (served via http-server)
- **Database**: SQLite
- **Machine Learning**: Jupyter Notebooks, MLflow (for experiment tracking and model management)

## Project Structure
```
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
        credit_risk.db
    tests/
database/
    scripts/
        seed.py
    credit_risk_dataset.csv
    credit_risk.db
docs/
    ARCHITECTURE.md
    [various documentation files]
frontend/
    src/
        assets/
        components/
        pages/
        services/
        styles/
        utils/
        app.js
    index.html
    package.json
mlruns/
    models/
        [various ML model versions]
shared/
    constants/
    types/
catboost_info/
```

## Key Components
- **Backend**: Flask-based REST API with multiple ML model support (XGBoost, LightGBM, CatBoost, etc.)
- **Frontend**: Lightweight JavaScript-based user interface
- **Machine Learning**: Multiple pre-trained models with MLflow tracking and versioning
- **Database**: SQLite database for credit risk data and model metadata

## Setup
### Prerequisites
- Python 3.8+
- Node.js (for http-server)
- npm

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
2. Install http-server globally (if not already installed):
   ```bash
   npm install -g http-server
   ```
3. Start the development server:
   ```bash
   npm start
   ```

## Usage
- Access the frontend at `http://localhost:3001`.
- Use the backend API at `http://localhost:5000`.

## Machine Learning Models
- **Jupyter Notebook**: `credit-risk-assesment.ipynb` contains exploratory data analysis and model training
- **MLflow Integration**: Model versioning and experiment tracking in `mlruns/` directory
- **Supported Models**: AdaBoost, Bagging Classifier, Decision Tree, Extra Trees, Gradient Boosting, K-Neighbors, Logistic Regression, Random Forest, SVC, XGBoost

## Database Setup
Run the database seeding script to initialize the database:
```bash
cd database/scripts
python seed.py
```

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
