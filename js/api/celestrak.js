/**
 * CELESTRAK API INTEGRATION ENGINE
 * Integrated with Antellay SpaceOS Satellite Mission Constellations
 * Source: CelesTrak GP Data & Antellay Space Mission Constellations
 */

const CelestrakAPI = {
    // Satellite Mission Constellations from Antellay SpaceOS
    catalog: [
        { id: '25544', name: 'ISS (ZARYA)', category: 'Space Station', inc: 51.64, alt: 418, vel: 7.66, period: 92.9 },
        { id: '88001', name: 'Emergency Response Satellite (ERS-1)', category: 'Disaster Relief', inc: 97.80, alt: 520, vel: 7.61, period: 94.8 },
        { id: '88002', name: 'VHF Marine & Aviation Ground Station (VHF-MAR-1)', category: 'Maritime & Flight AIS', inc: 53.20, alt: 550, vel: 7.58, period: 95.5 },
        { id: '88003', name: 'Astronomical Signal Satellite (ASTRO-SIG-1)', category: 'Deep Space Signal', inc: 65.40, alt: 680, vel: 7.51, period: 98.2 },
        { id: '20580', name: 'HST - Hubble Space Telescope', category: 'Observatory', inc: 28.47, alt: 535, vel: 7.59, period: 95.3 },
        { id: '44713', name: 'STARLINK-1007', category: 'Communication', inc: 53.05, alt: 550, vel: 7.58, period: 95.6 },
        { id: '33591', name: 'NOAA 19', category: 'Weather', inc: 98.70, alt: 852, vel: 7.42, period: 102.1 },
        { id: '48274', name: 'TIANGONG Space Station', category: 'Space Station', inc: 41.47, alt: 390, vel: 7.68, period: 92.2 }
    ],

    cache: {},

    /**
     * Fetch Live GP JSON for a specific Satellite NORAD ID
     */
    async fetchSatelliteData(noradId) {
        try {
            const url = `https://celestrak.org/NORAD/elements/gp.php?CATNR=${noradId}&FORMAT=json`;
            const response = await fetch(url);
            if (!response.ok) throw new Error(`CelesTrak HTTP error! status: ${response.status}`);
            
            const data = await response.json();
            if (data && data.length > 0) {
                const sat = data[0];
                this.cache[noradId] = sat;
                return this.parseGPData(sat);
            }
        } catch (error) {
            console.warn(`[CelesTrak] API direct fetch failed (using fallback propagation):`, error);
        }

        return this.getFallbackSatelliteData(noradId);
    },

    /**
     * Parse raw GP JSON from CelesTrak
     */
    parseGPData(gp) {
        const meanMotion = parseFloat(gp.MEAN_MOTION) || 15.5;
        const periodMinutes = (1440 / meanMotion).toFixed(1);
        const inclination = parseFloat(gp.INCLINATION).toFixed(4);
        const eccentricity = parseFloat(gp.ECCENTRICITY).toFixed(6);

        const mu = 398600.4418;
        const nRad = (meanMotion * 2 * Math.PI) / 86400;
        const semiMajorAxis = Math.cbrt(mu / (nRad * nRad));
        const altitude = (semiMajorAxis - 6371).toFixed(2);
        const velocity = Math.sqrt(mu / semiMajorAxis).toFixed(2);

        const now = new Date();
        const seconds = now.getUTCSeconds() + now.getUTCMinutes() * 60 + now.getUTCHours() * 3600;
        const phase = (seconds % (periodMinutes * 60)) / (periodMinutes * 60);

        const lat = (Math.sin(phase * 2 * Math.PI) * inclination).toFixed(2);
        const lon = (((phase * 360 * 3) % 360) - 180).toFixed(2);

        return {
            noradId: gp.NORAD_CAT_ID,
            name: gp.OBJECT_NAME,
            epoch: gp.EPOCH,
            inclination: `${inclination}°`,
            eccentricity: eccentricity,
            period: `${periodMinutes} mins`,
            altitude: `${altitude} km`,
            velocity: `${velocity} km/s`,
            lat: parseFloat(lat),
            lng: parseFloat(lon)
        };
    },

    /**
     * Fallback calculation engine for orbital position when CelesTrak is offline
     */
    getFallbackSatelliteData(noradId) {
        const found = this.catalog.find(s => s.id === noradId) || this.catalog[0];
        const now = Date.now() / 1000;
        
        const orbitSecs = found.period * 60;
        const phase = (now % orbitSecs) / orbitSecs;

        const lat = Math.sin(phase * 2 * Math.PI) * (found.inc > 90 ? 180 - found.inc : found.inc);
        let lng = (phase * 360 * 2.5) % 360;
        if (lng > 180) lng -= 360;

        return {
            noradId: found.id,
            name: found.name,
            epoch: new Date().toISOString().split('T')[0] + ' UTC',
            inclination: `${found.inc.toFixed(4)}°`,
            eccentricity: '0.000624',
            period: `${found.period} mins`,
            altitude: `${found.alt.toFixed(2)} km`,
            velocity: `${found.vel.toFixed(2)} km/s`,
            lat: parseFloat(lat.toFixed(2)),
            lng: parseFloat(lng.toFixed(2))
        };
    }
};
