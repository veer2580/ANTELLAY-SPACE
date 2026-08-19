/**
 * ORBITAL MAP VISUALIZER ENGINE (LEAFLET.JS)
 * Dark-themed high-tech geospatial map rendering satellite positions & ground track.
 */

const MapEngine = {
    map: null,
    satMarker: null,
    trajectoryLine: null,
    trajectoryCoords: [],

    init(containerId) {
        if (this.map) return;

        // Initialize Leaflet Map centered on global view
        this.map = L.map(containerId, {
            center: [20, 0],
            zoom: 2.2,
            minZoom: 1.8,
            maxZoom: 10,
            zoomControl: false
        });

        // Add CartoDB Dark Matter tile layer
        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; <a href="https://carto.com/">CARTO</a> &copy; OpenStreetMap',
            subdomains: 'abcd',
            maxZoom: 19
        }).addTo(this.map);

        // Add custom zoom controls at top right
        L.control.zoom({ position: 'topright' }).addTo(this.map);

        // Custom Glowing Neon Satellite Icon
        const satIcon = L.divIcon({
            className: 'custom-sat-icon',
            html: `
                <div class="sat-marker-ping"></div>
                <div class="sat-marker-core">
                    <i class="fa-solid fa-satellite"></i>
                </div>
            `,
            iconSize: [36, 36],
            iconAnchor: [18, 18]
        });

        // Initialize Marker
        this.satMarker = L.marker([51.64, 128.45], { icon: satIcon }).addTo(this.map);
        
        // Initialize Ground Track Polyline
        this.trajectoryLine = L.polyline([], {
            color: '#00F0FF',
            weight: 2,
            opacity: 0.7,
            dashArray: '6, 8'
        }).addTo(this.map);

        // CSS Injection for Marker Animation
        const style = document.createElement('style');
        style.innerHTML = `
            .custom-sat-icon {
                position: relative;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .sat-marker-core {
                width: 28px;
                height: 28px;
                background: #04070D;
                border: 2px solid #00F0FF;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #00F0FF;
                font-size: 0.85rem;
                box-shadow: 0 0 15px rgba(0, 240, 255, 0.6);
                z-index: 2;
            }
            .sat-marker-ping {
                position: absolute;
                width: 44px;
                height: 44px;
                border-radius: 50%;
                background: rgba(0, 240, 255, 0.25);
                border: 1px solid #00F0FF;
                animation: pingPulse 2s infinite ease-out;
                z-index: 1;
            }
            @keyframes pingPulse {
                0% { transform: scale(0.5); opacity: 1; }
                100% { transform: scale(1.6); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    },

    /**
     * Update satellite marker position and extend trajectory line
     */
    updatePosition(lat, lng, name) {
        if (!this.map || !this.satMarker) return;

        const newLatLng = [lat, lng];
        this.satMarker.setLatLng(newLatLng);

        // Append coordinate to trajectory history
        this.trajectoryCoords.push(newLatLng);
        if (this.trajectoryCoords.length > 50) {
            this.trajectoryCoords.shift();
        }

        this.trajectoryLine.setLatLngs(this.trajectoryCoords);
    },

    /**
     * Clear trajectory line when switching satellites
     */
    clearTrajectory() {
        this.trajectoryCoords = [];
        if (this.trajectoryLine) {
            this.trajectoryLine.setLatLngs([]);
        }
    },

    /**
     * Center map on current satellite marker
     */
    recenter() {
        if (this.map && this.satMarker) {
            this.map.panTo(this.satMarker.getLatLng());
        }
    }
};
