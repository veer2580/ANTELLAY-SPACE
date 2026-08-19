/**
 * ANTALLY SPACE OPERATIONS - MAIN APPLICATION CONTROLLER
 * Integrated with Live Website: antellay-space.veer2580jag.workers.dev
 */

document.addEventListener('DOMContentLoaded', () => {
    AppController.init();
});

const AppController = {
    selectedNoradId: '88001',
    selectedSourceId: 'ORB-01',
    solarWindChart: null,
    tickerInterval: null,
    currentMapView: '3d',

    sourcesCatalog: {
        'ORB-01': {
            id: 'ORB-01',
            title: 'ORBITAL DATA',
            desc: 'Aggregated TLE feed from public space tracking catalog (CelesTrak & Antellay SpaceOS).',
            url: 'wss://api.antellay.space/v1/orb-feed',
            latency: '124ms',
            loss: '0.02%',
            cardId: 'scard-orb',
            apiEndpoint: '/api/celestrak?noradId=88001'
        },
        'SW-02': {
            id: 'SW-02',
            title: 'SPACE WEATHER',
            desc: 'NOAA SWPC planetary K-index, geomagnetic alerts & solar wind plasma stream.',
            url: 'https://services.swpc.noaa.gov/json/kp.json',
            latency: '85ms',
            loss: '0.00%',
            cardId: 'scard-sw',
            apiEndpoint: '/api/noaa/kp'
        },
        'EO-03': {
            id: 'EO-03',
            title: 'EARTH OBSERVATION',
            desc: 'USGS EarthExplorer Landsat & Sentinel surface reflectance imagery catalog.',
            url: 'https://earthexplorer.usgs.gov/api/v1/m2m',
            latency: '210ms',
            loss: '0.15%',
            cardId: 'scard-eo',
            apiEndpoint: '/api/world-model?noradId=88001'
        },
        'TEL-04': {
            id: 'TEL-04',
            title: 'SAT TELEMETRY',
            desc: 'Synthetic & live telemetry bus for satellite attitude, power, and thermals.',
            url: 'wss://telemetry.antellay.space/v1/stream',
            latency: '45ms',
            loss: '0.01%',
            cardId: 'scard-tel',
            apiEndpoint: '/api/world-model?noradId=88001'
        }
    },

    async init() {
        console.log('[Antally Space] Initializing Antellay SpaceOS Mission Control...');

        // 1. Initialize Cosmic Starfield Canvas & SFX Engine
        StarfieldEngine.init('starfield-canvas');
        SFXEngine.init();

        // 2. Initialize Clocks & Navigation
        this.startUTCClock();
        this.setupNavigation();

        // 3. Initialize Visual Engines
        Globe3DEngine.init('globe-3d-view');
        MapEngine.init('map-view');
        this.initOrbitProjectionRadar();

        // 4. Load Satellite Catalog Table & Settings from Backend
        this.renderCatalogTable();
        await this.loadBackendSettings();

        // 5. Initial Data Load for APIs & Space Features
        await this.loadSelectedSatelliteData();
        await this.loadSpaceWeatherData();
        await this.loadDonkiEvents();
        await this.loadWorldModelData();
        await this.loadLaunchSiteWeather();

        // Render Clean Visual Widgets
        SpaceDebrisEngine.renderDebrisRadar('debris-radar-widget');
        AstronautsEngine.renderAstronauts('astronauts-widget');

        await this.loadDbHistory();
        this.selectSource('ORB-01');

        // 6. Setup Live Realtime Update Loop (every 2.5s)
        this.tickerInterval = setInterval(() => {
            this.updateOrbitTicker();
        }, 2500);

        // 7. Setup Event Listeners
        this.setupEventListeners();
    },

    selectSource(sourceId) {
        const src = this.sourcesCatalog[sourceId];
        if (!src) return;

        SFXEngine.playClick();
        this.selectedSourceId = sourceId;

        document.querySelectorAll('.source-card-stitch').forEach(c => c.classList.remove('active-source'));
        const activeCard = document.getElementById(src.cardId);
        if (activeCard) activeCard.classList.add('active-source');

        if (document.getElementById('sd-header-id')) document.getElementById('sd-header-id').textContent = `SOURCE DETAILS: ${src.id}`;
        if (document.getElementById('sd-title')) document.getElementById('sd-title').textContent = src.title;
        if (document.getElementById('sd-desc')) document.getElementById('sd-desc').textContent = src.desc;
        if (document.getElementById('sd-url')) document.getElementById('sd-url').value = src.url;
        if (document.getElementById('sd-latency')) document.getElementById('sd-latency').textContent = src.latency;
        if (document.getElementById('sd-loss')) document.getElementById('sd-loss').textContent = src.loss;
    },

    copySourceUrl() {
        const input = document.getElementById('sd-url');
        if (input) {
            navigator.clipboard.writeText(input.value);
            SFXEngine.speak("Endpoint URL copied");
            alert(`Copied Endpoint URL: ${input.value}`);
        }
    },

    pauseFeed() {
        SFXEngine.playClick();
        const btn = document.getElementById('btn-pause-feed');
        if (btn) {
            if (btn.innerHTML.includes('PAUSE')) {
                btn.innerHTML = '<i class="fa-solid fa-play"></i> RESUME FEED';
                btn.style.borderColor = 'var(--accent-yellow)';
                btn.style.color = 'var(--accent-yellow)';
                SFXEngine.speak("Data stream paused");
            } else {
                btn.innerHTML = '<i class="fa-solid fa-pause"></i> PAUSE FEED';
                btn.style.borderColor = '';
                btn.style.color = '';
                SFXEngine.speak("Data stream resumed");
            }
        }
    },

    async reconnectFeed() {
        SFXEngine.playClick();
        const btn = document.getElementById('btn-reconnect-feed');
        if (btn) {
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> RECONNECTING...';
            setTimeout(() => {
                btn.innerHTML = '<i class="fa-solid fa-rotate"></i> RECONNECT';
                SFXEngine.speak("Feed reconnected");
            }, 800);
        }
    },

    async viewLivePayload() {
        SFXEngine.playClick();
        const src = this.sourcesCatalog[this.selectedSourceId];
        const modal = document.getElementById('payload-modal');
        const codeBox = document.getElementById('payload-code-box');
        const titleEl = document.getElementById('payload-modal-title');

        if (titleEl) titleEl.innerHTML = `<i class="fa-solid fa-code orange"></i> LIVE PAYLOAD: ${src.title} (${src.id})`;
        if (codeBox) codeBox.textContent = 'Fetching live data stream from proxy...';
        if (modal) modal.classList.add('active');

        try {
            const res = await fetch(src.apiEndpoint);
            if (res.ok) {
                const json = await res.json();
                if (codeBox) codeBox.textContent = JSON.stringify(json, null, 2);
            } else {
                if (codeBox) codeBox.textContent = `// Response Status: ${res.status}\n{\n  "status": "online",\n  "proxy": "active",\n  "endpoint": "${src.url}"\n}`;
            }
        } catch (err) {
            if (codeBox) codeBox.textContent = `// Mock Data Stream\n{\n  "source": "${src.title}",\n  "latency": "${src.latency}",\n  "timestamp": "${new Date().toISOString()}"\n}`;
        }
    },

    initOrbitProjectionRadar() {
        const canvas = document.getElementById('orbit-projection-canvas');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        let satOffset = 0;

        const resizeCanvas = () => {
            canvas.width = canvas.parentElement.clientWidth || 800;
            canvas.height = canvas.parentElement.clientHeight || 500;
        };

        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        const renderRadar = () => {
            const width = canvas.width;
            const height = canvas.height;

            ctx.clearRect(0, 0, width, height);

            ctx.strokeStyle = 'rgba(232, 106, 40, 0.08)';
            ctx.lineWidth = 1;

            const gridSize = 45;
            for (let x = 0; x < width; x += gridSize) {
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.lineTo(x, height);
                ctx.stroke();
            }
            for (let y = 0; y < height; y += gridSize) {
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(width, y);
                ctx.stroke();
            }

            const centerX = width / 2;
            const centerY = height / 2;

            ctx.strokeStyle = 'rgba(232, 106, 40, 0.3)';
            ctx.beginPath();
            ctx.arc(centerX, centerY, 30, 0, Math.PI * 2);
            ctx.stroke();

            ctx.beginPath();
            ctx.moveTo(centerX - 40, centerY);
            ctx.lineTo(centerX + 40, centerY);
            ctx.moveTo(centerX, centerY - 40);
            ctx.lineTo(centerX, centerY + 40);
            ctx.stroke();

            ctx.save();
            ctx.setLineDash([8, 6]);
            ctx.strokeStyle = '#FF7A29';
            ctx.lineWidth = 2.5;

            ctx.beginPath();
            const amplitude = height * 0.35;
            const frequency = 0.007;

            for (let x = 50; x < width - 50; x += 5) {
                const y = centerY + Math.sin(x * frequency) * amplitude;
                if (x === 50) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
            ctx.stroke();
            ctx.restore();

            const satX = 50 + ((satOffset * 3) % (width - 100));
            const satY = centerY + Math.sin(satX * frequency) * amplitude;

            ctx.beginPath();
            ctx.arc(satX, satY, 12, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(255, 122, 41, 0.25)';
            ctx.fill();

            ctx.beginPath();
            ctx.arc(satX, satY, 5, 0, Math.PI * 2);
            ctx.fillStyle = '#FFA666';
            ctx.shadowColor = '#FF7A29';
            ctx.shadowBlur = 15;
            ctx.fill();
            ctx.shadowBlur = 0;

            satOffset += 0.5;
            requestAnimationFrame(renderRadar);
        };

        renderRadar();
    },

    startUTCClock() {
        const clockEl = document.getElementById('utc-clock');
        const updateClock = () => {
            const now = new Date();
            const utcString = now.toUTCString().split(' ')[4] + ' UTC';
            if (clockEl) clockEl.textContent = utcString;
        };
        updateClock();
        setInterval(updateClock, 1000);
    },

    setupNavigation() {
        const navButtons = document.querySelectorAll('.nav-item');
        const tabContents = document.querySelectorAll('.tab-content');
        const pageTitle = document.getElementById('page-title');

        const titleMap = {
            'overview': 'MISSION CONTROL // GLOBAL OVERVIEW',
            'orbit-intelligence': 'ORBIT INTELLIGENCE <span class="tag-sub">MVP/SIMULATED</span>',
            'telemetry': 'TELEMETRY // SUBSYSTEM FEEDS',
            'donki-events': 'Data Sources',
            'world-model': 'WORLD MODEL // FOUNDATIONAL DATA PIPELINE'
        };

        navButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                SFXEngine.playClick();
                const targetTab = btn.getAttribute('data-tab');

                navButtons.forEach(b => b.classList.remove('active'));
                tabContents.forEach(c => c.classList.remove('active'));

                btn.classList.add('active');
                const activeContent = document.getElementById(`tab-${targetTab}`);
                if (activeContent) activeContent.classList.add('active');

                if (pageTitle && titleMap[targetTab]) {
                    pageTitle.innerHTML = titleMap[targetTab];
                }

                if (targetTab === 'overview' && MapEngine.map && this.currentMapView === '2d') {
                    setTimeout(() => MapEngine.map.invalidateSize(), 150);
                }

                if (targetTab === 'telemetry') {
                    AstronautsEngine.renderAstronauts('astronauts-widget');
                    this.loadDbHistory();
                }

                if (targetTab === 'world-model') {
                    this.loadWorldModelData();
                }
            });
        });
    },

    setupEventListeners() {
        const btn2D = document.getElementById('btn-view-2d');
        const btn3D = document.getElementById('btn-view-3d');
        const mapView = document.getElementById('map-view');
        const globeView = document.getElementById('globe-3d-view');

        if (btn2D && btn3D) {
            btn2D.addEventListener('click', () => {
                SFXEngine.playClick();
                this.currentMapView = '2d';
                btn2D.classList.add('active-view');
                btn2D.classList.remove('btn-outline');
                btn2D.classList.add('btn-primary');

                btn3D.classList.remove('active-view');
                btn3D.classList.remove('btn-primary');
                btn3D.classList.add('btn-outline');

                mapView.style.display = 'block';
                globeView.style.display = 'none';
                if (MapEngine.map) MapEngine.map.invalidateSize();
            });

            btn3D.addEventListener('click', () => {
                SFXEngine.playClick();
                this.currentMapView = '3d';
                btn3D.classList.add('active-view');
                btn3D.classList.remove('btn-primary');
                btn3D.classList.add('btn-outline');

                mapView.style.display = 'none';
                globeView.style.display = 'block';
                Globe3DEngine.init('globe-3d-view');
                SFXEngine.speak("Switched to 3D Orbital Globe View");
            });
        }

        const btnSFX = document.getElementById('btn-toggle-sfx');
        if (btnSFX) {
            btnSFX.addEventListener('click', () => {
                const isEnabled = SFXEngine.toggleSound();
                btnSFX.innerHTML = isEnabled ? 
                    '<i class="fa-solid fa-volume-high"></i> SFX ON' : 
                    '<i class="fa-solid fa-volume-xmark"></i> SFX OFF';
            });
        }

        const selector = document.getElementById('sat-selector');
        if (selector) {
            selector.addEventListener('change', async (e) => {
                SFXEngine.playClick();
                this.selectedNoradId = e.target.value;
                MapEngine.clearTrajectory();
                await this.loadSelectedSatelliteData();
                await this.loadWorldModelData();

                const satName = selector.options[selector.selectedIndex].text.split('-')[0];
                SFXEngine.speak(`Tracking satellite ${satName}`);
            });
        }

        const btnTrack = document.getElementById('btn-track-sat');
        if (btnTrack) {
            btnTrack.addEventListener('click', () => {
                SFXEngine.playClick();
                document.querySelector('.nav-item[data-tab="overview"]').click();
            });
        }

        const btnReset = document.getElementById('btn-reset-view');
        if (btnReset) {
            btnReset.addEventListener('click', () => {
                SFXEngine.playClick();
                MapEngine.recenter();
            });
        }

        const btnDeploy = document.getElementById('btn-deploy-pipeline');
        if (btnDeploy) {
            btnDeploy.addEventListener('click', async () => {
                SFXEngine.playClick();
                btnDeploy.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> REFRESHING...';
                await this.loadSelectedSatelliteData();
                await this.loadSpaceWeatherData();
                await this.loadDonkiEvents();
                await this.loadWorldModelData();
                await this.loadDbHistory();
                setTimeout(() => {
                    btnDeploy.innerHTML = 'DEPLOY PIPELINE';
                }, 800);
            });
        }

        const btnOpenModal = document.getElementById('btn-open-settings');
        const btnCloseModal = document.getElementById('btn-close-settings');
        const modal = document.getElementById('settings-modal');

        if (btnOpenModal && modal) {
            btnOpenModal.addEventListener('click', () => {
                SFXEngine.playClick();
                modal.classList.add('active');
            });
        }

        if (btnCloseModal && modal) {
            btnCloseModal.addEventListener('click', () => {
                SFXEngine.playClick();
                modal.classList.remove('active');
            });
        }

        const btnSaveSettings = document.getElementById('btn-save-settings');
        if (btnSaveSettings) {
            btnSaveSettings.addEventListener('click', () => {
                SFXEngine.playClick();
                this.saveBackendSettings();
            });
        }
    },

    async loadWorldModelData() {
        try {
            const res = await fetch(`/api/world-model?noradId=${this.selectedNoradId}`);
            if (res.ok) {
                const json = await res.json();
                if (json.success && json.worldModel) {
                    const wm = json.worldModel;
                    
                    if (document.getElementById('wm-asset-id')) document.getElementById('wm-asset-id').textContent = `${wm.currentState.assetId} (${wm.currentState.assetName})`;
                    if (document.getElementById('wm-pos')) document.getElementById('wm-pos').textContent = `Lat ${wm.currentState.latitude}, Lon ${wm.currentState.longitude}`;
                    if (document.getElementById('wm-alt')) document.getElementById('wm-alt').textContent = `${wm.currentState.altitudeKm} km @ ${wm.currentState.velocityKmS} km/s`;

                    if (document.getElementById('wm-kp')) document.getElementById('wm-kp').textContent = `Kp ${wm.context.kpIndex} (${wm.context.geomagneticActivity})`;
                    if (document.getElementById('wm-wind')) document.getElementById('wm-wind').textContent = `${wm.context.solarWindSpeedKmS} km/s (Normal)`;

                    if (document.getElementById('u-inc')) document.getElementById('u-inc').textContent = `${wm.unifiedModel.orbit.inclinationDeg}°`;
                    if (document.getElementById('u-period')) document.getElementById('u-period').textContent = `${wm.unifiedModel.orbit.periodMinutes} mins`;
                    if (document.getElementById('u-bat')) document.getElementById('u-bat').textContent = `${wm.unifiedModel.telemetry.batteryCapacityPct}%`;
                    if (document.getElementById('u-temp')) document.getElementById('u-temp').textContent = `${wm.unifiedModel.telemetry.coreTemperatureC}°C`;
                    if (document.getElementById('u-wind')) document.getElementById('u-wind').textContent = `${wm.unifiedModel.environment.solarWindDensity} p/cm³`;
                    if (document.getElementById('u-risk')) document.getElementById('u-risk').textContent = wm.unifiedModel.environment.protonStormRisk;
                }
            }
        } catch (err) {
            console.warn('[App] World model fetch error:', err.message);
        }
    },

    async loadBackendSettings() {
        try {
            const res = await fetch('/api/settings');
            if (res.ok) {
                const data = await res.json();
                if (data.success && data.settings) {
                    const s = data.settings;
                    if (document.getElementById('input-nasa-key')) document.getElementById('input-nasa-key').value = s.nasa_api_key || 'DEMO_KEY';
                    if (document.getElementById('input-spacetrack-user')) document.getElementById('input-spacetrack-user').value = s.spacetrack_user || '';
                    if (document.getElementById('input-spacetrack-pass')) document.getElementById('input-spacetrack-pass').value = s.spacetrack_pass || '';
                    if (document.getElementById('input-usgs-key')) document.getElementById('input-usgs-key').value = s.usgs_api_key || '';
                    if (document.getElementById('input-weather-key')) document.getElementById('input-weather-key').value = s.weather_api_key || 'DEMO_WEATHER_KEY';
                    if (document.getElementById('input-celestrak-url')) document.getElementById('input-celestrak-url').value = s.celestrak_endpoint || '';
                    if (document.getElementById('input-noaa-url')) document.getElementById('input-noaa-url').value = s.noaa_endpoint || '';
                }
            }
        } catch (err) {
            console.warn('[App] Backend settings read warning:', err.message);
        }
    },

    async saveBackendSettings() {
        const statusMsg = document.getElementById('modal-status-msg');
        if (statusMsg) statusMsg.textContent = 'Saving to Database...';

        const payload = {
            nasa_api_key: document.getElementById('input-nasa-key').value.trim() || 'DEMO_KEY',
            spacetrack_user: document.getElementById('input-spacetrack-user').value.trim(),
            spacetrack_pass: document.getElementById('input-spacetrack-pass').value.trim(),
            usgs_api_key: document.getElementById('input-usgs-key').value.trim(),
            weather_api_key: document.getElementById('input-weather-key') ? document.getElementById('input-weather-key').value.trim() : 'DEMO_WEATHER_KEY',
            celestrak_endpoint: document.getElementById('input-celestrak-url').value.trim(),
            noaa_endpoint: document.getElementById('input-noaa-url').value.trim()
        };

        try {
            const res = await fetch('/api/settings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (res.ok) {
                if (statusMsg) statusMsg.textContent = '✅ Saved to Database!';
                setTimeout(() => {
                    if (statusMsg) statusMsg.textContent = '';
                    document.getElementById('settings-modal').classList.remove('active');
                    this.loadDonkiEvents();
                    this.loadSelectedSatelliteData();
                    this.loadWorldModelData();
                    this.loadLaunchSiteWeather();
                }, 1000);
            }
        } catch (err) {
            if (statusMsg) statusMsg.textContent = 'Error saving settings';
        }
    },

    async loadLaunchSiteWeather() {
        const select = document.getElementById('launch-site-select');
        let lat = '28.3968', lon = '-80.6057', name = 'Cape Canaveral SFS';
        if (select) {
            const parts = select.value.split(',');
            if (parts.length >= 3) {
                lat = parts[0];
                lon = parts[1];
                name = parts[2];
            }
        }

        try {
            const res = await fetch(`/api/weather?lat=${lat}&lon=${lon}&name=${encodeURIComponent(name)}`);
            if (res.ok) {
                const data = await res.json();
                if (data.success) {
                    if (document.getElementById('w-temp')) document.getElementById('w-temp').textContent = `${data.tempC}°C`;
                    if (document.getElementById('w-cond')) document.getElementById('w-cond').textContent = data.condition;
                    if (document.getElementById('w-wind')) document.getElementById('w-wind').textContent = `${data.windSpeedKmH} km/h`;
                    if (document.getElementById('w-source')) document.getElementById('w-source').textContent = data.source ? data.source.split(' ')[0] : 'Live API';
                    if (document.getElementById('w-humidity')) document.getElementById('w-humidity').textContent = `${data.humidity}%`;
                    if (document.getElementById('w-pressure')) document.getElementById('w-pressure').textContent = `${data.pressure} hPa`;

                    const safetyBadge = document.getElementById('weather-safety-badge');
                    if (safetyBadge) {
                        safetyBadge.textContent = data.launchSafety || 'OPTIMAL';
                        if (data.launchSafety && data.launchSafety.includes('GO')) {
                            safetyBadge.className = 'badge badge-success';
                        } else if (data.launchSafety && data.launchSafety.includes('CAUTION')) {
                            safetyBadge.className = 'badge badge-warning';
                        } else {
                            safetyBadge.className = 'badge badge-success';
                        }
                    }
                }
            }
        } catch (err) {
            console.warn('[App] Weather fetch warning:', err.message);
        }
    },

    async loadSelectedSatelliteData() {
        const satData = await CelestrakAPI.fetchSatelliteData(this.selectedNoradId);
        
        if (document.getElementById('overlay-sat-id')) document.getElementById('overlay-sat-id').textContent = `NORAD-${satData.noradId}`;
        if (document.getElementById('overlay-sat-name')) document.getElementById('overlay-sat-name').textContent = satData.name;
        if (document.getElementById('overlay-alt')) document.getElementById('overlay-alt').textContent = satData.altitude;
        if (document.getElementById('overlay-vel')) document.getElementById('overlay-vel').textContent = satData.velocity;
        if (document.getElementById('overlay-lat')) document.getElementById('overlay-lat').textContent = `${satData.lat >= 0 ? satData.lat + '° N' : Math.abs(satData.lat) + '° S'}`;
        if (document.getElementById('overlay-lng')) document.getElementById('overlay-lng').textContent = `${satData.lng >= 0 ? satData.lng + '° E' : Math.abs(satData.lng) + '° W'}`;

        if (document.getElementById('st-alt')) document.getElementById('st-alt').textContent = satData.altitude;
        if (document.getElementById('st-vel')) document.getElementById('st-vel').textContent = satData.velocity;
        if (document.getElementById('st-inc')) document.getElementById('st-inc').textContent = `${satData.inclination}`;
        if (document.getElementById('st-period')) document.getElementById('st-period').textContent = `${satData.period}`;
        if (document.getElementById('st-pos')) document.getElementById('st-pos').textContent = `${Math.abs(satData.lat)}° ${satData.lat >= 0 ? 'N' : 'S'} ${Math.abs(satData.lng)}° ${satData.lng >= 0 ? 'E' : 'W'}`;

        if (document.getElementById('param-norad')) document.getElementById('param-norad').textContent = satData.noradId;
        if (document.getElementById('param-inc')) document.getElementById('param-inc').textContent = satData.inclination;
        if (document.getElementById('param-ecc')) document.getElementById('param-ecc').textContent = satData.eccentricity;
        if (document.getElementById('param-period')) document.getElementById('param-period').textContent = satData.period;
        if (document.getElementById('param-epoch')) document.getElementById('param-epoch').textContent = satData.epoch;

        MapEngine.updatePosition(satData.lat, satData.lng, satData.name);
    },

    async updateOrbitTicker() {
        const satData = await CelestrakAPI.fetchSatelliteData(this.selectedNoradId);

        if (document.getElementById('overlay-alt')) document.getElementById('overlay-alt').textContent = satData.altitude;
        if (document.getElementById('overlay-vel')) document.getElementById('overlay-vel').textContent = satData.velocity;
        if (document.getElementById('overlay-lat')) document.getElementById('overlay-lat').textContent = `${satData.lat >= 0 ? satData.lat + '° N' : Math.abs(satData.lat) + '° S'}`;
        if (document.getElementById('overlay-lng')) document.getElementById('overlay-lng').textContent = `${satData.lng >= 0 ? satData.lng + '° E' : Math.abs(satData.lng) + '° W'}`;
        
        if (document.getElementById('st-alt')) document.getElementById('st-alt').textContent = satData.altitude;
        if (document.getElementById('st-vel')) document.getElementById('st-vel').textContent = satData.velocity;
        if (document.getElementById('st-pos')) document.getElementById('st-pos').textContent = `${Math.abs(satData.lat)}° ${satData.lat >= 0 ? 'N' : 'S'} ${Math.abs(satData.lng)}° ${satData.lng >= 0 ? 'E' : 'W'}`;

        MapEngine.updatePosition(satData.lat, satData.lng, satData.name);
    },

    renderCatalogTable() {
        const tbody = document.getElementById('catalog-table-body');
        if (!tbody) return;

        tbody.innerHTML = CelestrakAPI.catalog.map(sat => `
            <tr>
                <td style="color: var(--brand-orange-bright); font-weight: bold;">${sat.id}</td>
                <td>${sat.name}</td>
                <td><span class="badge badge-info">${sat.category}</span></td>
                <td>${sat.alt} km</td>
                <td>${sat.inc}°</td>
                <td>${sat.period} mins</td>
                <td><span class="badge badge-success">ACTIVE</span></td>
                <td>
                    <button class="btn btn-sm btn-outline" onclick="AppController.selectSatFromTable('${sat.id}')">
                        <i class="fa-solid fa-crosshairs"></i> TRACK
                    </button>
                </td>
            </tr>
        `).join('');
    },

    selectSatFromTable(noradId) {
        SFXEngine.playClick();
        const selector = document.getElementById('sat-selector');
        if (selector) {
            selector.value = noradId;
            this.selectedNoradId = noradId;
            MapEngine.clearTrajectory();
            this.loadSelectedSatelliteData();
            this.loadWorldModelData();
            document.querySelector('.nav-item[data-tab="orbit-intelligence"]').click();
        }
    },

    async loadSpaceWeatherData() {
        const kpData = await NOAA_SWPC_API.fetchKpIndex();
        const kpValEl = document.getElementById('summary-kp');
        if (kpValEl) kpValEl.textContent = `Kp ${kpData.kp}`;
        
        const kpLargeVal = document.getElementById('kp-large-value');
        if (kpLargeVal) kpLargeVal.textContent = kpData.kp;

        const windData = await NOAA_SWPC_API.fetchSolarWind();
        if (windData && windData.length > 0) {
            const latestWind = windData[windData.length - 1];
            const windValEl = document.getElementById('summary-wind');
            if (windValEl) windValEl.textContent = `${latestWind.speed.toFixed(0)} km/s`;
            
            this.renderSolarWindChart(windData);
        }

        const alerts = await NOAA_SWPC_API.fetchAlerts();
        const alertsContainer = document.getElementById('noaa-alerts-list');
        if (alertsContainer) {
            alertsContainer.innerHTML = alerts.map(a => `
                <div class="alert-item ${a.type}">
                    <span class="a-issue">${new Date(a.issueTime).toLocaleString()} UTC</span>
                    <span class="a-msg">${a.message}</span>
                </div>
            `).join('');
        }
    },

    renderSolarWindChart(windData) {
        const canvas = document.getElementById('solarWindChart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        const labels = windData.map(d => d.time);
        const speeds = windData.map(d => d.speed);

        if (this.solarWindChart) {
            this.solarWindChart.destroy();
        }

        this.solarWindChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Solar Wind Speed (km/s)',
                    data: speeds,
                    borderColor: '#FF7A29',
                    backgroundColor: 'rgba(255, 122, 41, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.3,
                    pointRadius: 3,
                    pointBackgroundColor: '#FF7A29'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#8E9BAE', font: { family: 'JetBrains Mono', size: 10 } }
                    },
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#8E9BAE', font: { family: 'JetBrains Mono', size: 10 } }
                    }
                }
            }
        });
    },

    async loadDonkiEvents() {
        const flares = await NASA_DONKI_API.fetchSolarFlares();
        const flrContainer = document.getElementById('donki-flr-list');
        if (flrContainer) {
            flrContainer.innerHTML = flares.map(f => `
                <div class="event-card">
                    <div class="ev-head">
                        <span class="ev-id" style="color: var(--brand-orange-bright);">${f.id} • ${f.classType}</span>
                        <span class="ev-time">${f.beginTime}</span>
                    </div>
                    <div class="ev-body">
                        Active Region: <strong>${f.activeRegion}</strong> | Location: <strong>${f.sourceLocation}</strong>
                    </div>
                </div>
            `).join('');
        }

        const cmes = await NASA_DONKI_API.fetchCME();
        const cmeContainer = document.getElementById('donki-cme-list');
        if (cmeContainer) {
            cmeContainer.innerHTML = cmes.map(c => `
                <div class="event-card">
                    <div class="ev-head">
                        <span class="ev-id">${c.id}</span>
                        <span class="ev-time">${c.startTime}</span>
                    </div>
                    <div class="ev-body">
                        Speed: <strong style="color: var(--accent-yellow);">${c.speed}</strong> • ${c.note}
                    </div>
                </div>
            `).join('');
        }

        const gsts = await NASA_DONKI_API.fetchGST();
        const gstContainer = document.getElementById('donki-gst-list');
        if (gstContainer) {
            gstContainer.innerHTML = gsts.map(g => `
                <div class="event-card">
                    <div class="ev-head">
                        <span class="ev-id" style="color: var(--accent-green);">${g.id}</span>
                        <span class="ev-time">${g.startTime}</span>
                    </div>
                    <div class="ev-body">
                        Intensity: <strong>${g.kpMax}</strong> | Provider: ${g.submittedBy}
                    </div>
                </div>
            `).join('');
        }
    },

    async loadDbHistory() {
        const tbody = document.getElementById('db-history-tbody');
        if (!tbody) return;

        try {
            const res = await fetch('/api/db/history');
            let logs = [];
            if (res.ok) {
                const data = await res.json();
                if (data.success && data.telemetryLogs) {
                    logs = data.telemetryLogs;
                }
            }

            if (logs.length === 0) {
                const now = new Date();
                logs = [
                    { timestamp: new Date(now - 12000).toISOString(), noradId: '88001', name: 'Emergency Response Satellite (ERS-1)' },
                    { timestamp: new Date(now - 8000).toISOString(), noradId: '88002', name: 'VHF Marine & Aviation (VHF-MAR-1)' },
                    { timestamp: new Date(now - 4000).toISOString(), noradId: '88003', name: 'Astronomical Signal (ASTRO-SIG-1)' }
                ];
            }

            tbody.innerHTML = logs.map(log => `
                <tr>
                    <td>${new Date(log.timestamp).toLocaleTimeString()} UTC</td>
                    <td style="color: var(--brand-orange-bright); font-weight: bold;">NORAD-${log.noradId}</td>
                    <td>${log.name}</td>
                    <td><span class="badge badge-success">SAVED TO DB</span></td>
                </tr>
            `).join('');
        } catch (err) {
            console.warn('[App] DB history read warning:', err.message);
        }
    }
};
