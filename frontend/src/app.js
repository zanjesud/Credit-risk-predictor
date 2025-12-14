// Main application file

// Initialize services
const recordService = new RecordService();

// Application object
const app = {
    init() {
        this.setupEventListeners();
    },

    setupEventListeners() {
        // Search form submission
        const searchForm = document.getElementById('search-form');
        searchForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.searchCustomer();
        });

        // Allow Enter key to submit
        const customerIdInput = document.getElementById('customer-id');
        customerIdInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                searchForm.dispatchEvent(new Event('submit'));
            }
        });
    },

    async searchCustomer() {
        const customerId = document.getElementById('customer-id').value.trim();
        const resultsSection = document.getElementById('results-section');
        const searchResults = document.getElementById('search-results');

        if (!customerId) {
            alert('Please enter a Customer ID');
            return;
        }

        // Show loading state
        resultsSection.style.display = 'block';
        searchResults.innerHTML = '<div class="loading">🔍 Searching for customer information...</div>';

        try {
            const record = await recordService.getRecordById(customerId);
            this.displaySearchResults(record);
        } catch (error) {
            searchResults.innerHTML = `
                <div class="error-message">
                    <h3>❌ Customer Not Found</h3>
                    <p>${error.message}</p>
                    <p class="error-hint">Please check the Customer ID and try again.</p>
                </div>
            `;
        }
    },

    displaySearchResults(record) {
        const searchResults = document.getElementById('search-results');
        const formatted = recordService.formatRecordForDisplay(record);
        const riskClass = recordService.getRiskCategoryClass(formatted.riskCategory);
        const riskPercentage = formatted.riskScore ? (formatted.riskScore * 100).toFixed(1) : 0;
        const barClass = recordService.getRiskBarClass(formatted.riskCategory);
        
        // Access raw record for additional fields
        const creditHistoryLength = record.cb_person_cred_hist_length || 'N/A';
        const previousDefault = record.cb_person_default_on_file || 'N/A';

        searchResults.innerHTML = `
            <div class="result-card">
                <div class="result-header">
                    <h2>📋 Customer Information</h2>
                    <span class="customer-id-badge">ID: ${formatted.customerId || formatted.id}</span>
                </div>

                <div class="result-content">
                    <!-- Personal Information Section -->
                    <div class="info-section">
                        <h3>👤 Personal Information</h3>
                        <div class="info-grid">
                            <div class="info-item">
                                <span class="info-label">Age</span>
                                <span class="info-value">${formatted.personAge}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Annual Income</span>
                                <span class="info-value">$${formatted.personIncome?.toLocaleString() || 'N/A'}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Home Ownership</span>
                                <span class="info-value">${formatted.homeOwnership || 'N/A'}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Employment Length</span>
                                <span class="info-value">${formatted.employmentLength || 'N/A'} years</span>
                            </div>
                        </div>
                    </div>

                    <!-- Loan Information Section -->
                    <div class="info-section">
                        <h3>💼 Loan Information</h3>
                        <div class="info-grid">
                            <div class="info-item">
                                <span class="info-label">Loan Intent</span>
                                <span class="info-value">${formatted.loanIntent || 'N/A'}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Loan Grade</span>
                                <span class="info-value grade-${formatted.loanGrade?.toLowerCase() || 'na'}">${formatted.loanGrade || 'N/A'}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Loan Amount</span>
                                <span class="info-value">$${formatted.loanAmount?.toLocaleString() || 'N/A'}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Interest Rate</span>
                                <span class="info-value">${formatted.loanInterestRate?.toFixed(2) || 'N/A'}%</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Loan Status</span>
                                <span class="info-value ${formatted.loanStatus === 0 ? 'status-good' : 'status-bad'}">
                                    ${formatted.loanStatus === 0 ? '✓ No Default' : '✗ Default'}
                                </span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Loan % of Income</span>
                                <span class="info-value">${record.loan_percent_income ? (record.loan_percent_income * 100).toFixed(1) : 'N/A'}%</span>
                            </div>
                        </div>
                    </div>

                    <!-- Credit History Section -->
                    <div class="info-section">
                        <h3>📊 Credit History</h3>
                        <div class="info-grid">
                            <div class="info-item">
                                <span class="info-label">Credit History Length</span>
                                <span class="info-value">${creditHistoryLength} ${typeof creditHistoryLength === 'number' ? 'years' : ''}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">Previous Default on File</span>
                                <span class="info-value ${previousDefault === 'Y' ? 'status-bad' : 'status-good'}">
                                    ${previousDefault === 'Y' ? '✗ Yes' : previousDefault === 'N' ? '✓ No' : 'N/A'}
                                </span>
                            </div>
                        </div>
                    </div>

                    <!-- Credit Risk Assessment Section -->
                    ${formatted.riskScore !== undefined && formatted.riskScore !== null ? `
                        <div class="info-section risk-section">
                            <h3>⚠️ Credit Risk Assessment</h3>
                            <div class="risk-bar-container-large">
                                <div class="risk-bar-label">
                                    <span>Default Probability</span>
                                    <span class="risk-percentage-large">${riskPercentage}%</span>
                                </div>
                                <div class="risk-bar-wrapper">
                                    <div class="risk-bar-fill ${barClass}" style="width: 0%">
                                        ${parseFloat(riskPercentage) > 10 ? `${riskPercentage}%` : ''}
                                    </div>
                                </div>
                                <div class="risk-category-text-large">
                                    Risk Level: <strong class="risk-badge-large ${riskClass}">${formatted.riskCategory || 'Unknown'}</strong>
                                </div>
                                <div class="risk-interpretation">
                                    ${this.getRiskInterpretation(formatted.riskCategory, riskPercentage)}
                                </div>
                            </div>
                        </div>
                    ` : ''}

                    <!-- Additional Information -->
                    <div class="info-section">
                        <h3>📅 Record Information</h3>
                        <div class="info-grid">
                            <div class="info-item">
                                <span class="info-label">Created At</span>
                                <span class="info-value">${new Date(formatted.createdAt).toLocaleString()}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Animate the bar chart
        setTimeout(() => {
            const barFill = searchResults.querySelector('.risk-bar-fill');
            if (barFill) {
                barFill.style.width = `${riskPercentage}%`;
            }
        }, 200);
    },

    getRiskInterpretation(category, percentage) {
        const interpretations = {
            'Low': `This customer has a low risk of default (${percentage}%). The loan appears to be relatively safe.`,
            'Medium': `This customer has a moderate risk of default (${percentage}%). Additional review may be recommended.`,
            'High': `This customer has a high risk of default (${percentage}%). Caution is advised before approving the loan.`
        };
        return `<p class="interpretation-text">${interpretations[category] || `Risk assessment: ${percentage}% default probability.`}</p>`;
    }
};

// Make app available globally
window.app = app;

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    app.init();
});

