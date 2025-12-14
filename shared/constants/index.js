// Shared constants

const RISK_CATEGORIES = {
    LOW: 'Low',
    MEDIUM: 'Medium',
    HIGH: 'High'
};

const LOAN_GRADES = ['A', 'B', 'C', 'D', 'E', 'F', 'G'];

const HOME_OWNERSHIP_TYPES = ['RENT', 'MORTGAGE', 'OWN', 'OTHER'];

const LOAN_INTENTS = [
    'PERSONAL',
    'EDUCATION',
    'MEDICAL',
    'VENTURE',
    'HOMEIMPROVEMENT',
    'DEBTCONSOLIDATION'
];

const DEFAULT_VALUES = {
    PORT_BACKEND: 3000,
    PORT_PYTHON_SERVICE: 5000,
    PORT_FRONTEND: 3001
};

module.exports = {
    RISK_CATEGORIES,
    LOAN_GRADES,
    HOME_OWNERSHIP_TYPES,
    LOAN_INTENTS,
    DEFAULT_VALUES
};

