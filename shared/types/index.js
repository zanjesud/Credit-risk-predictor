// Shared type definitions (for JavaScript/Node.js)

/**
 * Credit Risk Record Type
 * @typedef {Object} CreditRiskRecord
 * @property {number} id
 * @property {number} person_age
 * @property {number} person_income
 * @property {string} person_home_ownership - RENT, MORTGAGE, OWN, OTHER
 * @property {number} person_emp_length
 * @property {string} loan_intent
 * @property {string} loan_grade - A, B, C, D, E, F, G
 * @property {number} loan_amnt
 * @property {number} loan_int_rate
 * @property {number} loan_status - 0 (no default) or 1 (default)
 * @property {number} loan_percent_income
 * @property {string} cb_person_default_on_file - Y or N
 * @property {number} cb_person_cred_hist_length
 * @property {number} risk_score - ML predicted risk score (0-1)
 * @property {string} risk_category - Low, Medium, High
 */

/**
 * Prediction Response Type
 * @typedef {Object} PredictionResponse
 * @property {number} prediction - 0 (no default) or 1 (default)
 * @property {number} risk_score - Probability of default (0-1)
 * @property {string} risk_category - Low, Medium, High
 * @property {number} probability_default
 * @property {number} probability_no_default
 */

module.exports = {};

