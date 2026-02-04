// GHOZTWOODS LLC - API Configuration
// This file will be updated after Render deployment

const API_CONFIG = {
    // IMPORTANT: After deploying to Render.com, replace this URL with your actual Render API URL
    // Example: 'https://ghoztwoods-scam-intel-api.onrender.com'
    BACKEND_API_URL: 'RENDER_API_URL_HERE',
    
    // Fallback to direct Hugging Face (will cause CORS errors on GitHub Pages)
    // Only works when testing locally
    USE_DIRECT_HF: false,
    
    // Health check endpoint
    HEALTH_CHECK: '/api/health',
    
    // Analysis endpoint
    ANALYZE_ENDPOINT: '/api/analyze'
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = API_CONFIG;
}
