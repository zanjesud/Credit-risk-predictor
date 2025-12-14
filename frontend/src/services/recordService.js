// Record service for managing credit risk records

class RecordService {
    constructor() {
        this.api = window.api || api; // Use global api if available
    }

    async getAllRecords() {
        try {
            const records = await this.api.getAllRecords();
            return records;
        } catch (error) {
            console.error('Error fetching records:', error);
            throw error;
        }
    }

    async getRecordById(id) {
        try {
            const record = await this.api.getRecordById(id);
            return record;
        } catch (error) {
            console.error('Error fetching record:', error);
            throw error;
        }
    }


    formatRecordForDisplay(record) {
        return {
            customerId: record.customer_id || record.id,
            id: record.customer_id || record.id, // For backward compatibility
            personAge: record.person_age,
            personIncome: record.person_income,
            homeOwnership: record.person_home_ownership,
            employmentLength: record.person_emp_length,
            loanIntent: record.loan_intent,
            loanGrade: record.loan_grade,
            loanAmount: record.loan_amnt,
            loanInterestRate: record.loan_int_rate,
            loanStatus: record.loan_status,
            riskScore: record.risk_score || record.risk_prediction?.risk_score,
            riskCategory: record.risk_category || record.risk_prediction?.risk_category,
            createdAt: record.created_at
        };
    }

    getRiskCategoryClass(riskCategory) {
        if (!riskCategory) return 'risk-unknown';
        const category = riskCategory.toLowerCase();
        if (category === 'low') return 'risk-low';
        if (category === 'medium') return 'risk-medium';
        if (category === 'high') return 'risk-high';
        return 'risk-unknown';
    }

    getRiskBarClass(riskCategory) {
        if (!riskCategory) return 'risk-bar-medium';
        const category = riskCategory.toLowerCase();
        if (category === 'low') return 'risk-bar-low';
        if (category === 'medium') return 'risk-bar-medium';
        if (category === 'high') return 'risk-bar-high';
        return 'risk-bar-medium';
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = RecordService;
}

