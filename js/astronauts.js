/**
 * ASTRONAUTS IN ORBIT ROSTER ENGINE
 * Render visual cards for humans currently in space aboard ISS & Tiangong
 */

const AstronautsEngine = {
    astronauts: [
        { name: 'Sunita Williams', role: 'Pilot / Flight Engineer', agency: 'NASA', craft: 'ISS (Expedition 71)', days: 168, icon: 'fa-user-astronaut' },
        { name: 'Butch Wilmore', role: 'Commander', agency: 'NASA', craft: 'ISS (Expedition 71)', days: 168, icon: 'fa-user-astronaut' },
        { name: 'Oleg Kononenko', role: 'Commander', agency: 'Roscosmos', craft: 'ISS (Expedition 71)', days: 345, icon: 'fa-user-astronaut' },
        { name: 'Nikolai Chub', role: 'Flight Engineer', agency: 'Roscosmos', craft: 'ISS (Expedition 71)', days: 345, icon: 'fa-user-astronaut' },
        { name: 'Tracy Caldwell Dyson', role: 'Flight Engineer', agency: 'NASA', craft: 'ISS (Expedition 71)', days: 148, icon: 'fa-user-astronaut' },
        { name: 'Ye Guangfu', role: 'Commander', agency: 'CMSA', craft: 'Tiangong (Shenzhou-18)', days: 112, icon: 'fa-user-astronaut' },
        { name: 'Li Cong', role: 'Operator', agency: 'CMSA', craft: 'Tiangong (Shenzhou-18)', days: 112, icon: 'fa-user-astronaut' }
    ],

    renderAstronauts(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <div class="card-header flex-between">
                <h3><i class="fa-solid fa-user-astronaut cyan"></i> HUMANS IN SPACE (7 ASTRONAUTS ORBITING EARTH)</h3>
                <span class="badge badge-success">ISS & TIANGONG ACTIVE</span>
            </div>
            <div class="card-body">
                <div class="crew-grid">
                    ${this.astronauts.map(a => `
                        <div class="crew-card">
                            <div class="c-avatar">
                                <i class="fa-solid ${a.icon}"></i>
                            </div>
                            <div class="c-info">
                                <span class="c-name">${a.name}</span>
                                <span class="c-role">${a.role}</span>
                                <span class="c-craft"><i class="fa-solid fa-satellite"></i> ${a.craft}</span>
                            </div>
                            <div class="c-badge-box">
                                <span class="badge badge-info">${a.agency}</span>
                                <span class="c-days">${a.days} days in space</span>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
};
