/**
 * GLOBAL ROCKET LAUNCH MANIFEST & COUNTDOWN ENGINE
 * Real-time countdown timers for upcoming orbital rocket launches.
 */

const LaunchManifestEngine = {
    launches: [
        { id: 'L-01', rocket: 'Falcon 9 Block 5', mission: 'Starlink Group 8-12', provider: 'SpaceX', pad: 'SLC-40, Cape Canaveral', targetDate: new Date(Date.now() + 48 * 3600 * 1000) },
        { id: 'L-02', rocket: 'PSLV-C59', mission: 'PROBA-3 Solar Observatory', provider: 'ISRO', pad: 'FLP, Sriharikota', targetDate: new Date(Date.now() + 120 * 3600 * 1000) },
        { id: 'L-03', rocket: 'SLS Block 1', mission: 'Artemis II Lunar Flyby', provider: 'NASA', pad: 'LC-39B, Kennedy Space Center', targetDate: new Date(Date.now() + 720 * 3600 * 1000) }
    ],

    renderLaunches(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const updateCountdowns = () => {
            const now = new Date();
            container.innerHTML = `
                <div class="launch-manifest-header">
                    <h3><i class="fa-solid fa-rocket"></i> UPCOMING ORBITAL LAUNCH MANIFEST</h3>
                </div>
                <div class="launch-list">
                    ${this.launches.map(l => {
                        const diff = l.targetDate - now;
                        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
                        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                        const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                        const secs = Math.floor((diff % (1000 * 60)) / 1000);
                        const countdownStr = `T- ${days}d ${hours.toString().padStart(2, '0')}h ${mins.toString().padStart(2, '0')}m ${secs.toString().padStart(2, '0')}s`;

                        return `
                            <div class="launch-card">
                                <div class="l-info">
                                    <span class="l-rocket">${l.rocket} • ${l.mission}</span>
                                    <span class="l-pad">${l.provider} | ${l.pad}</span>
                                </div>
                                <div class="l-timer-box">
                                    <span class="l-timer">${countdownStr}</span>
                                </div>
                            </div>
                        `;
                    }).join('')}
                </div>
            `;
        };

        updateCountdowns();
        setInterval(updateCountdowns, 1000);
    }
};
