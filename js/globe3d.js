/**
 * HIGH-TECH SCI-FI HOLOGRAPHIC ORBIT GLOBE ENGINE (THREE.JS)
 * Official Antellay Space Brand Theme: Solar Copper Orange (#FF7A29) & Deep Space Dark (#030712)
 */

const Globe3DEngine = {
    scene: null,
    camera: null,
    renderer: null,
    globeGroup: null,
    satellitesGroup: null,
    isInitialized: false,
    animId: null,

    init(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        if (this.animId) cancelAnimationFrame(this.animId);
        container.innerHTML = '';

        const width = container.clientWidth || 800;
        const height = container.clientHeight || 500;

        // 1. Scene Setup
        this.scene = new THREE.Scene();

        // 2. Camera Setup
        this.camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
        this.camera.position.set(0, 15, 35);
        this.camera.lookAt(0, 0, 0);

        // 3. Renderer Setup
        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        this.renderer.setSize(width, height);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(this.renderer.domElement);

        // 4. Lights
        const ambientLight = new THREE.AmbientLight(0xE86A28, 1.5);
        this.scene.add(ambientLight);

        const pointLight = new THREE.PointLight(0xFF7A29, 2.5, 100);
        pointLight.position.set(20, 20, 20);
        this.scene.add(pointLight);

        // 5. Create Holographic Sci-Fi Globe Group
        this.globeGroup = new THREE.Group();
        this.scene.add(this.globeGroup);
        this.createHolographicSciFiGlobe();

        // 6. Create Orbiting Satellites
        this.satellitesGroup = new THREE.Group();
        this.scene.add(this.satellitesGroup);
        this.populate3DSatellites();

        // 7. Window Resize
        window.addEventListener('resize', () => {
            if (!container) return;
            const w = container.clientWidth;
            const h = container.clientHeight;
            if (w > 0 && h > 0 && this.camera && this.renderer) {
                this.camera.aspect = w / h;
                this.camera.updateProjectionMatrix();
                this.renderer.setSize(w, h);
            }
        });

        this.setupDragControls(container);
        this.animate();
        this.isInitialized = true;
    },

    /**
     * Create Sleek Holographic Mesh Globe (Official Antellay Copper Orange Theme)
     */
    createHolographicSciFiGlobe() {
        // Inner Core Dark Glass Sphere
        const coreGeo = new THREE.SphereGeometry(9.8, 48, 48);
        const coreMat = new THREE.MeshPhongMaterial({
            color: 0x050a14,
            emissive: 0x280e04,
            transparent: true,
            opacity: 0.9,
            shininess: 80
        });
        const coreMesh = new THREE.Mesh(coreGeo, coreMat);
        this.globeGroup.add(coreMesh);

        // Holographic Latitude/Longitude Wireframe Grid Ring Mesh (Amber Copper)
        const gridGeo = new THREE.SphereGeometry(10.0, 36, 36);
        const gridMat = new THREE.MeshBasicMaterial({
            color: 0xFF7A29,
            wireframe: true,
            transparent: true,
            opacity: 0.4
        });
        const gridMesh = new THREE.Mesh(gridGeo, gridMat);
        this.globeGroup.add(gridMesh);

        // Outer Glow Shell
        const glowGeo = new THREE.SphereGeometry(10.4, 32, 32);
        const glowMat = new THREE.MeshBasicMaterial({
            color: 0xE86A28,
            transparent: true,
            opacity: 0.15,
            side: THREE.BackSide
        });
        const glowMesh = new THREE.Mesh(glowGeo, glowMat);
        this.globeGroup.add(glowMesh);
    },

    /**
     * Populate 3D Orbiting Satellites
     */
    populate3DSatellites() {
        const sats = [
            { name: 'ISS (ZARYA)', radius: 13.5, inc: 0.9, speed: 0.008, color: 0xFF7A29 },
            { name: 'HST (Hubble)', radius: 15.0, inc: 0.5, speed: 0.006, color: 0x00E676 },
            { name: 'STARLINK-1007', radius: 12.8, inc: 1.2, speed: 0.01, color: 0xFFC107 },
            { name: 'TIANGONG', radius: 14.2, inc: -0.7, speed: 0.007, color: 0xFF3366 }
        ];

        sats.forEach((s) => {
            const orbitGeo = new THREE.BufferGeometry();
            const points = [];
            for (let i = 0; i <= 128; i++) {
                const theta = (i / 128) * Math.PI * 2;
                const x = Math.cos(theta) * s.radius;
                const z = Math.sin(theta) * s.radius;
                const y = Math.sin(theta * s.inc) * 3;
                points.push(new THREE.Vector3(x, y, z));
            }
            orbitGeo.setFromPoints(points);

            const orbitMat = new THREE.LineBasicMaterial({
                color: s.color,
                transparent: true,
                opacity: 0.45
            });

            const orbitLine = new THREE.Line(orbitGeo, orbitMat);
            this.scene.add(orbitLine);

            const satMesh = new THREE.Mesh(
                new THREE.SphereGeometry(0.4, 16, 16),
                new THREE.MeshBasicMaterial({ color: s.color })
            );

            satMesh.userData = { ...s, angle: Math.random() * Math.PI * 2 };
            this.satellitesGroup.add(satMesh);
        });
    },

    setupDragControls(container) {
        let isMouseDown = false;
        let prevMousePos = { x: 0, y: 0 };

        container.addEventListener('mousedown', (e) => {
            isMouseDown = true;
            prevMousePos = { x: e.clientX, y: e.clientY };
        });

        window.addEventListener('mouseup', () => { isMouseDown = false; });

        container.addEventListener('mousemove', (e) => {
            if (!isMouseDown || !this.globeGroup) return;
            const deltaX = e.clientX - prevMousePos.x;
            const deltaY = e.clientY - prevMousePos.y;

            this.globeGroup.rotation.y += deltaX * 0.005;
            this.globeGroup.rotation.x += deltaY * 0.005;

            prevMousePos = { x: e.clientX, y: e.clientY };
        });
    },

    animate() {
        this.animId = requestAnimationFrame(() => this.animate());

        if (this.globeGroup) {
            this.globeGroup.rotation.y += 0.002;
        }

        if (this.satellitesGroup) {
            this.satellitesGroup.children.forEach((sat) => {
                const d = sat.userData;
                d.angle += d.speed;
                sat.position.x = Math.cos(d.angle) * d.radius;
                sat.position.z = Math.sin(d.angle * d.radius / d.radius);
                sat.position.y = Math.sin(d.angle * d.inc) * 3;
            });
        }

        if (this.renderer && this.scene && this.camera) {
            this.renderer.render(this.scene, this.camera);
        }
    }
};
