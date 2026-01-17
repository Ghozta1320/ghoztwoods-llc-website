/* ============================================
   TECHNICIAN TRACKER - JAVASCRIPT
   Real-time tracking better than Uber/DoorDash
   ============================================ */

// Global variables
let map;
let technicianMarker;
let customerMarker;
let routeLine;
let updateInterval;

// Demo data - In production, this would come from your backend API
const demoData = {
    'DEMO-001': {
        technician: {
            name: 'Avery Delpit',
            title: 'Lead Technician',
            location: { lat: 35.0527, lng: -78.8784 }, // Fayetteville, NC
            credentials: [
                { icon: 'shield-check', text: '94F Veteran', color: 'green' },
                { icon: 'award', text: 'Secret Clearance', color: 'blue' },
                { icon: 'graduation-cap', text: 'CompTIA Security+', color: 'green' },
                { icon: 'cpu', text: 'Network+', color: 'blue' },
                { icon: 'lock', text: 'CMMC Certified', color: 'green' }
            ]
        },
        customer: {
            location: { lat: 35.0827, lng: -78.9184 }
        },
        service: {
            type: 'Network Security Setup',
            scheduledTime: '2:00 PM',
            status: 'En Route',
            serviceId: 'GHZ-2025-001'
        }
    }
};

/* ============================================
   INITIALIZATION
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    initializeMap();
    
    // Auto-load demo if service ID is in URL
    const urlParams = new URLSearchParams(window.location.search);
    const serviceId = urlParams.get('service');
    if (serviceId) {
        document.getElementById('service-id').value = serviceId;
        trackService();
    }
});

/* ============================================
   MAP INITIALIZATION
   ============================================ */

function initializeMap() {
    // Initialize Leaflet map centered on Fayetteville, NC
    map = L.map('map').setView([35.0527, -78.8784], 13);

    // Add dark theme tile layer
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);

    // Custom marker icons
    const techIcon = L.divIcon({
        className: 'custom-marker',
        html: `
            <div style="
                width: 40px;
                height: 40px;
                background: linear-gradient(135deg, #00ff00, #00d4ff);
                border: 3px solid #0a0a0a;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
                animation: pulse 2s ease-in-out infinite;
            ">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0a0a0a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"></path>
                    <circle cx="12" cy="10" r="3"></circle>
                </svg>
            </div>
        `,
        iconSize: [40, 40],
        iconAnchor: [20, 40]
    });

    const customerIcon = L.divIcon({
        className: 'custom-marker',
        html: `
            <div style="
                width: 40px;
                height: 40px;
                background: #00d4ff;
                border: 3px solid #0a0a0a;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
            ">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0a0a0a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                    <polyline points="9 22 9 12 15 12 15 22"></polyline>
                </svg>
            </div>
        `,
        iconSize: [40, 40],
        iconAnchor: [20, 40]
    });

    // Store icons for later use
    window.techIcon = techIcon;
    window.customerIcon = customerIcon;
}

/* ============================================
   SERVICE TRACKING
   ============================================ */

function trackService() {
    const serviceId = document.getElementById('service-id').value.trim();
    
    if (!serviceId) {
        alert('Please enter a service ID');
        return;
    }

    // Check if service exists (in demo, only DEMO-001 works)
    if (!demoData[serviceId]) {
        alert('Service ID not found. Try: DEMO-001');
        return;
    }

    // Load service data
    const serviceData = demoData[serviceId];
    
    // Show technician profile
    document.getElementById('tech-profile').style.display = 'block';
    
    // Update profile information
    document.getElementById('tech-name').textContent = serviceData.technician.name;
    document.getElementById('tech-title').textContent = serviceData.technician.title;
    document.getElementById('service-type').textContent = serviceData.service.type;
    document.getElementById('scheduled-time').textContent = serviceData.service.scheduledTime;
    document.getElementById('display-service-id').textContent = serviceData.service.serviceId;
    document.getElementById('service-status').textContent = serviceData.service.status;

    // Add markers to map
    addMarkersToMap(serviceData);
    
    // Start real-time updates
    startRealTimeUpdates(serviceData);
    
    // Calculate and display route
    calculateRoute(serviceData);
}

/* ============================================
   MAP MARKERS
   ============================================ */

function addMarkersToMap(serviceData) {
    // Remove existing markers
    if (technicianMarker) map.removeLayer(technicianMarker);
    if (customerMarker) map.removeLayer(customerMarker);
    if (routeLine) map.removeLayer(routeLine);

    // Add technician marker
    technicianMarker = L.marker(
        [serviceData.technician.location.lat, serviceData.technician.location.lng],
        { icon: window.techIcon }
    ).addTo(map);

    technicianMarker.bindPopup(`
        <div style="font-family: 'JetBrains Mono', monospace; color: #0a0a0a;">
            <strong style="color: #00ff00;">Technician Location</strong><br>
            ${serviceData.technician.name}<br>
            <small>Last updated: ${new Date().toLocaleTimeString()}</small>
        </div>
    `);

    // Add customer marker
    customerMarker = L.marker(
        [serviceData.customer.location.lat, serviceData.customer.location.lng],
        { icon: window.customerIcon }
    ).addTo(map);

    customerMarker.bindPopup(`
        <div style="font-family: 'JetBrains Mono', monospace; color: #0a0a0a;">
            <strong style="color: #00d4ff;">Your Location</strong><br>
            Service destination
        </div>
    `);

    // Fit map to show both markers
    const bounds = L.latLngBounds([
        [serviceData.technician.location.lat, serviceData.technician.location.lng],
        [serviceData.customer.location.lat, serviceData.customer.location.lng]
    ]);
    map.fitBounds(bounds, { padding: [50, 50] });
}

/* ============================================
   ROUTE CALCULATION
   ============================================ */

function calculateRoute(serviceData) {
    // Draw a simple line between technician and customer
    // In production, you'd use a routing API like OSRM or Mapbox
    const latlngs = [
        [serviceData.technician.location.lat, serviceData.technician.location.lng],
        [serviceData.customer.location.lat, serviceData.customer.location.lng]
    ];

    if (routeLine) map.removeLayer(routeLine);

    routeLine = L.polyline(latlngs, {
        color: '#00ff00',
        weight: 3,
        opacity: 0.7,
        dashArray: '10, 10'
    }).addTo(map);

    // Calculate distance and ETA
    const distance = calculateDistance(
        serviceData.technician.location.lat,
        serviceData.technician.location.lng,
        serviceData.customer.location.lat,
        serviceData.customer.location.lng
    );

    // Update UI
    document.getElementById('distance').textContent = distance.toFixed(1) + ' mi';
    
    // Estimate ETA (assuming 30 mph average speed)
    const etaMinutes = Math.round((distance / 30) * 60);
    document.getElementById('eta-time').textContent = etaMinutes + ' min';
}

/* ============================================
   REAL-TIME UPDATES
   ============================================ */

function startRealTimeUpdates(serviceData) {
    // Clear existing interval
    if (updateInterval) clearInterval(updateInterval);

    // Simulate real-time movement (in production, this would poll your API)
    updateInterval = setInterval(() => {
        // Simulate technician moving closer to customer
        const currentLat = serviceData.technician.location.lat;
        const currentLng = serviceData.technician.location.lng;
        const targetLat = serviceData.customer.location.lat;
        const targetLng = serviceData.customer.location.lng;

        // Move 10% closer each update
        const newLat = currentLat + (targetLat - currentLat) * 0.1;
        const newLng = currentLng + (targetLng - currentLng) * 0.1;

        serviceData.technician.location.lat = newLat;
        serviceData.technician.location.lng = newLng;

        // Update marker position
        if (technicianMarker) {
            technicianMarker.setLatLng([newLat, newLng]);
        }

        // Recalculate route
        calculateRoute(serviceData);

        // Check if arrived
        const distance = calculateDistance(newLat, newLng, targetLat, targetLng);
        if (distance < 0.1) {
            document.getElementById('service-status').textContent = 'Arrived';
            document.getElementById('eta-time').textContent = '0 min';
            clearInterval(updateInterval);
        }
    }, 3000); // Update every 3 seconds
}

/* ============================================
   UTILITY FUNCTIONS
   ============================================ */

function calculateDistance(lat1, lon1, lat2, lon2) {
    // Haversine formula
    const R = 3959; // Earth's radius in miles
    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);
    const a = 
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
}

function toRad(degrees) {
    return degrees * (Math.PI / 180);
}

/* ============================================
   MAP CONTROLS
   ============================================ */

function centerOnTechnician() {
    if (technicianMarker) {
        map.setView(technicianMarker.getLatLng(), 15);
        technicianMarker.openPopup();
    }
}

function toggleTraffic() {
    alert('Traffic layer feature coming soon!');
}

function refreshLocation() {
    const serviceId = document.getElementById('service-id').value.trim();
    if (serviceId && demoData[serviceId]) {
        // In production, this would fetch fresh data from API
        alert('Location refreshed!');
        technicianMarker.openPopup();
    }
}

/* ============================================
   COMMUNICATION FUNCTIONS
   ============================================ */

function callTechnician() {
    // In production, this would initiate a call
    window.location.href = 'tel:+19346670073';
}

function openChat() {
    document.getElementById('chat-modal').style.display = 'block';
    lucide.createIcons();
}

function closeChat() {
    document.getElementById('chat-modal').style.display = 'none';
}

function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;

    // Add user message to chat
    const messagesContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'chat-message user-message';
    messageDiv.innerHTML = `
        <strong>You</strong>
        <p>${message}</p>
        <span class="chat-time">${new Date().toLocaleTimeString()}</span>
    `;
    messagesContainer.appendChild(messageDiv);

    // Clear input
    input.value = '';

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    // Simulate technician response (in production, this would be real-time)
    setTimeout(() => {
        const responseDiv = document.createElement('div');
        responseDiv.className = 'chat-message tech-message';
        responseDiv.innerHTML = `
            <strong>Avery (Technician)</strong>
            <p>Got it! I'll take care of that when I arrive.</p>
            <span class="chat-time">${new Date().toLocaleTimeString()}</span>
        `;
        messagesContainer.appendChild(responseDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }, 2000);
}

function handleChatKeypress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

/* ============================================
   EXPORT FUNCTIONS FOR HTML
   ============================================ */

// Make functions available globally
window.trackService = trackService;
window.centerOnTechnician = centerOnTechnician;
window.toggleTraffic = toggleTraffic;
window.refreshLocation = refreshLocation;
window.callTechnician = callTechnician;
window.openChat = openChat;
window.closeChat = closeChat;
window.sendMessage = sendMessage;
window.handleChatKeypress = handleChatKeypress;
