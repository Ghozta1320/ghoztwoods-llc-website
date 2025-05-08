// Matrix effect and authentication logic
document.addEventListener('DOMContentLoaded', function() {
    const initialsInput = document.getElementById('initials');
    const enterButton = document.getElementById('enter-button');
    const disclaimerModal = document.getElementById('disclaimer-modal');
    const content = document.getElementById('content');
    const overlay = document.getElementById('matrix-overlay');

    // Handle initials input
    initialsInput.addEventListener('input', function() {
        enterButton.disabled = this.value.length < 2;
    });

    // Handle enter button click
    enterButton.addEventListener('click', function() {
        // Hide disclaimer and show content
        disclaimerModal.style.display = 'none';
        content.classList.add('show-content');

        // Fade out matrix overlay
        overlay.classList.add('fade-out');
        setTimeout(() => {
            overlay.style.display = 'none';
        }, 1000);
    });
});

// Threat analysis function
function analyzeThreat() {
    const input = document.getElementById('target-input').value;
    const results = document.getElementById('scan-results');
    
    if (!input) {
        results.innerHTML = '<p style="color: #ff0000;">Please enter a target to analyze</p>';
        return;
    }

    results.innerHTML = '<p>Analyzing threat... Please wait.</p>';
    
    // Simulate analysis with a delay
    setTimeout(() => {
        const analysis = {
            target: input,
            riskLevel: Math.random() > 0.5 ? 'High' : 'Low',
            timestamp: new Date().toISOString(),
            details: 'Analysis complete. See results below.',
            recommendations: [
                'Monitor for suspicious activity',
                'Report to relevant authorities if needed',
                'Document all interactions'
            ]
        };

        results.innerHTML = `
            <h3>Analysis Results:</h3>
            <p><strong>Target:</strong> ${analysis.target}</p>
            <p><strong>Risk Level:</strong> ${analysis.riskLevel}</p>
            <p><strong>Timestamp:</strong> ${analysis.timestamp}</p>
            <p><strong>Details:</strong> ${analysis.details}</p>
            <h4>Recommendations:</h4>
            <ul>
                ${analysis.recommendations.map(rec => `<li>${rec}</li>`).join('')}
            </ul>
        `;
    }, 2000);
}
