/**
 * SPACE DEBRIS & COLLISION RISK MONITOR ENGINE (KESSLER SYNDROME RADAR)
 * Monitors conjunction events and close approaches for tracked space junk.
 */

const SpaceDebrisEngine = {
    debrisObjects: [
        { id: '33758', name: 'COSMOS 2251 DEBRIS', rcs: 'MEDIUM', alt: 785, missDistanceKm: 1.42, prob: '1.2e-4', threatLevel: 'HIGH' },
        { id: '31112', name: 'FENGYUN 1C DEBRIS', rcs: 'SMALL', alt: 842, missDistanceKm: 4.18, prob: '4.8e-6', threatLevel: 'MEDIUM' },
        { id: '40115', name: 'SPENT ROCKET BODY (SL-16)', rcs: 'LARGE', alt: 620, missDistanceKm: 8.90, prob: '1.1e-7', threatLevel: 'LOW' },
        { id: '48992', name: 'CZ-3B UPPER STAGE', rcs: 'LARGE', alt: 512, missDistanceKm: 2.30, prob: '8.4e-5', threatLevel: 'HIGH' }
    ],

    /**
     * Render Debris Radar Widget into HTML container
     */
    renderDebrisRadar(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <div class="debris-radar-header">
                <span class="d-title"><i class="fa-solid fa-triangle-exclamation"></i> DEBRIS CONJUNCTION WARNINGS</span>
                <span class="badge badge-warning">KESSLER RADAR ACTIVE</span>
            </div>
            <div class="debris-list">
                ${this.debrisObjects.map(d => `
                    <div class="debris-item ${d.threatLevel.toLowerCase()}">
                        <div class="d-info">
                            <span class="d-id">${d.id} • ${d.name}</span>
                            <span class="d-meta">Miss Distance: <strong>${d.missDistanceKm} km</strong> | Alt: ${d.alt} km</span>
                        </div>
                        <div class="d-badge">
                            <span class="tag threat-${d.threatLevel.toLowerCase()}">${d.threatLevel} RISK</span>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }
};
