# 🛰️ Antally Space Operations & Satellite Dashboard

> **Mission Control & Orbital Intelligence Platform**  
> Integrated with live real-time API feeds from **CelesTrak**, **NOAA SWPC**, and **NASA DONKI**.

---

## 🌟 Features Overview

### 1. 🛰️ Live Earth Orbital Visualizer (CelesTrak API Integration)
- **Real-Time Satellite Tracking**: Visualizes live positions, altitude, velocity, and trajectory of tracked space objects including:
  - **ISS (ZARYA)** - International Space Station
  - **HST** - Hubble Space Telescope
  - **STARLINK-1007** - Broadband Satellite Constellation
  - **NOAA 19** - Weather Observation Satellite
  - **TIANGONG** - Chinese Space Station
- **Live Orbit Parameters**: Computes NORAD ID, Inclination (°), Eccentricity, Orbit Period (mins), and Epoch timestamps.
- **Dynamic 2D Orbital Map**: Interactive dark-themed map (Leaflet.js) rendering custom satellite icons, pulse markers, and ground track polylines.

### 2. ☀️ NOAA Space Weather Monitoring (NOAA SWPC API Integration)
- **Planetary K-Index Gauge**: Displays real-time geomagnetic disturbance levels ($Kp\text{ }0 - 9$ scale).
- **Solar Wind Plasma**: Real-time line chart (Chart.js) visualizing solar wind velocity ($\text{km/s}$) and plasma density.
- **Space Weather Alerts & Warnings**: Live stream of NOAA alerts regarding solar storms and geomagnetic impulses.

### 3. ☀️ Space Weather Intelligence (NASA DONKI API Integration)
- **Solar Flares (FLR)**: Live detections with flare class classifications (C-class, M-class, X-class) and active region numbers.
- **Coronal Mass Ejections (CME)**: Real-time coronal mass ejection velocities and direction notes.
- **Geomagnetic Storms (GST)**: Storm logs and severity indexes.

### 4. 🛰️ Orbit Intelligence & Ground Stations
- **Global Ground Station Network**: Pass countdowns and elevation angles for:
  - **ISTRAC Bengaluru** (ISRO, India)
  - **Svalbard Satellite Station** (Norway)
  - **Vandenberg Space Force Base** (USA)
  - **McMurdo Station** (Antarctica)
- **Satellite Catalog Table**: Interactive selection table allowing one-click satellite tracking.

### 5. 📡 Telemetry & Data Sources
- Live health indicators for external APIs (`CelesTrak`, `NOAA SWPC`, `NASA DONKI`).
- Subsystem telemetry metrics (Battery capacity, Core temperature, Signal strength, Solar panel wattage).

---

## 🔌 API Integration Matrix

| API / Source | Data Provided | Authentication | Status in MVP |
| :--- | :--- | :--- | :--- |
| **CelesTrak** | Satellite orbital GP data, TLE parameters | Free / Public | ✅ **Integrated (Active)** |
| **NOAA SWPC** | Live space weather, Kp-index, solar wind | Free / Public | ✅ **Integrated (Active)** |
| **NASA DONKI** | Solar flares, CME, geomagnetic storms | Free (`DEMO_KEY`) | ✅ **Integrated (Active)** |
| **Space-Track** | Official orbital catalog | Free Account Req. | 🔄 Phase 2 Ready |
| **USGS EarthExplorer** | Landsat / Remote sensing data | Account / API Req. | 🔄 Phase 2 Ready |

---

## 🚀 How to Run the Project

### Method 1: Direct Browser Launch (Easiest)
1. Open the project folder `antally space`.
2. Double click **`index.html`** to open it in Chrome, Edge, Firefox, or Safari.

### Method 2: Local HTTP Server (Recommended)
Using Python or Node.js:
```bash
# Using Python:
python -m http.server 8000

# Or using Node npx:
npx serve .
```
Then open `http://localhost:8000` in your web browser.

---

## 📦 How to Submit / Deliver to Your Sir

1. **Send as a ZIP File**:
   - Right click the `antally space` folder $\rightarrow$ **Compress to ZIP file**.
   - Email or share the ZIP file via Google Drive / Pen Drive.

2. **Share via GitHub Link**:
   - Push this folder to a GitHub repository and send the repository URL to Sir.

3. **Deploy Live for Free (Vercel / Netlify)**:
   - Drag and drop the `antally space` folder on [Netlify Drop](https://app.netlify.com/drop) or Vercel.
   - Send the live generated web link to Sir so he can open it directly on mobile or laptop!
