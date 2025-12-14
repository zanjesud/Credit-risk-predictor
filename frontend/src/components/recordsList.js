// Records list component

class RecordsList {
    constructor(recordService) {
        this.recordService = recordService;
        this.records = [];
    }

    async loadRecords() {
        const recordsList = document.getElementById('records-list');
        recordsList.innerHTML = '<div class="loading">Loading records...</div>';

        try {
            this.records = await this.recordService.getAllRecords();
            this.render();
        } catch (error) {
            recordsList.innerHTML = `<div class="error">Error loading records: ${error.message}</div>`;
        }
    }

    render() {
        const recordsList = document.getElementById('records-list');
        
        if (this.records.length === 0) {
            recordsList.innerHTML = '<div class="loading">No records found</div>';
            return;
        }

        recordsList.innerHTML = this.records.map(record => {
            const formatted = this.recordService.formatRecordForDisplay(record);
            const riskClass = this.recordService.getRiskCategoryClass(formatted.riskCategory);
            const riskPercentage = formatted.riskScore ? (formatted.riskScore * 100).toFixed(1) : 0;
            const barClass = this.recordService.getRiskBarClass(formatted.riskCategory);
            
            return `
                <div class="record-card" data-id="${formatted.id}">
                    <h3>Customer ID: ${formatted.customerId || formatted.id}</h3>
                    <div class="record-info">
                        <strong>Age:</strong> ${formatted.personAge} | 
                        <strong>Grade:</strong> ${formatted.loanGrade || 'N/A'}
                    </div>
                    <div class="record-info">
                        <strong>Income:</strong> $${formatted.personIncome?.toLocaleString() || 'N/A'} | 
                        <strong>Loan:</strong> $${formatted.loanAmount?.toLocaleString() || 'N/A'}
                    </div>
                    ${formatted.riskScore !== undefined && formatted.riskScore !== null ? `
                        <div class="risk-bar-container">
                            <div class="risk-bar-label">
                                <span>Credit Risk</span>
                                <span class="risk-percentage">${riskPercentage}%</span>
                            </div>
                            <div class="risk-bar-wrapper">
                                <div class="risk-bar-fill ${barClass}" style="width: 0%">
                                    ${parseFloat(riskPercentage) > 10 ? `${riskPercentage}%` : ''}
                                </div>
                            </div>
                            <div class="risk-category-text">
                                Risk Level: <strong class="risk-badge ${riskClass}">${formatted.riskCategory || 'Unknown'}</strong>
                            </div>
                        </div>
                    ` : '<div class="risk-bar-container"><p>Risk assessment not available</p></div>'}
                </div>
            `;
        }).join('');

        // Animate bar charts and add click event listeners
        recordsList.querySelectorAll('.record-card').forEach((card, index) => {
            // Animate the bar chart
            const barFill = card.querySelector('.risk-bar-fill');
            if (barFill) {
                const width = barFill.style.width;
                const targetWidth = barFill.textContent.trim().replace('%', '') || 
                                   card.querySelector('.risk-percentage')?.textContent.replace('%', '') || '0';
                
                // Reset to 0 and animate
                barFill.style.width = '0%';
                setTimeout(() => {
                    barFill.style.width = `${targetWidth}%`;
                }, index * 50); // Stagger animations
            }
            
            // Add click event listener
            card.addEventListener('click', () => {
                const recordId = card.dataset.id;
                window.app.showRecordDetails(recordId);
            });
        });
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = RecordsList;
}

