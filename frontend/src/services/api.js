// API configuration
const API_CONFIG = {
    BASE_URL: 'http://localhost:5000/api',
    ENDPOINTS: {
        RECORDS: '/records',
        PREDICT: '/predict'
    }
};

// Generic API request function
async function apiRequest(endpoint, options = {}) {
    const url = `${API_CONFIG.BASE_URL}${endpoint}`;
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const config = { ...defaultOptions, ...options };

    try {
        const response = await fetch(url, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'API request failed');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// API methods - Read Only
const api = {
    // Get all records
    getAllRecords: () => apiRequest(API_CONFIG.ENDPOINTS.RECORDS),
    
    // Get record by customer ID
    getRecordById: (customerId) => apiRequest(`${API_CONFIG.ENDPOINTS.RECORDS}/${customerId}`),

    // Predict credit risk
    predict: (data) => apiRequest(API_CONFIG.ENDPOINTS.PREDICT, {
        method: 'POST',
        body: JSON.stringify(data)
    }),
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
}
