// GHOZTWOODS LLC - API Configuration
// Updated with live Render.com API URL

const API_CONFIG = {
    // Live Render.com API URL
    BACKEND_API_URL: 'https://ghoztwoods-llc-website.onrender.com',
    
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
