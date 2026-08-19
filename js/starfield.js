/**
 * ANIMATED COSMIC STARFIELD & METEOR ENGINE
 * Canvas-based twinkling starfield with drifting cosmic dust and shooting stars.
 */

const StarfieldEngine = {
    canvas: null,
    ctx: null,
    stars: [],
    meteors: [],
    numStars: 220,

    init(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;

        this.ctx = this.canvas.getContext('2d');
        this.resize();
        window.addEventListener('resize', () => this.resize());

        // Create Star Particles
        this.stars = [];
        for (let i = 0; i < this.numStars; i++) {
            this.stars.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                size: Math.random() * 1.5 + 0.5,
                alpha: Math.random(),
                speed: Math.random() * 0.02 + 0.005,
                color: Math.random() > 0.8 ? '#00F0FF' : (Math.random() > 0.6 ? '#FFC107' : '#FFFFFF')
            });
        }

        // Periodically spawn shooting meteors
        setInterval(() => this.spawnMeteor(), 4000);

        // Start Animation Loop
        this.animate();
    },

    resize() {
        if (!this.canvas) return;
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    },

    spawnMeteor() {
        if (Math.random() > 0.4) return;
        this.meteors.push({
            x: Math.random() * this.canvas.width * 0.8,
            y: Math.random() * this.canvas.height * 0.4,
            length: Math.random() * 80 + 40,
            speed: Math.random() * 6 + 4,
            angle: Math.PI / 4, // 45 degrees downward
            life: 1.0,
            decay: Math.random() * 0.02 + 0.015
        });
    },

    animate() {
        if (!this.ctx || !this.canvas) return;

        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // 1. Draw Twinkling Stars
        this.stars.forEach(star => {
            star.alpha += star.speed;
            if (star.alpha > 1 || star.alpha < 0.1) {
                star.speed = -star.speed;
            }

            this.ctx.beginPath();
            this.ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
            this.ctx.fillStyle = star.color;
            this.ctx.globalAlpha = Math.abs(star.alpha);
            this.ctx.fill();
        });

        // 2. Draw Shooting Stars (Meteors)
        for (let i = this.meteors.length - 1; i >= 0; i--) {
            const m = this.meteors[i];
            const endX = m.x + Math.cos(m.angle) * m.length;
            const endY = m.y + Math.sin(m.angle) * m.length;

            const gradient = this.ctx.createLinearGradient(m.x, m.y, endX, endY);
            gradient.addColorStop(0, 'rgba(0, 240, 255, 0)');
            gradient.addColorStop(1, `rgba(0, 240, 255, ${m.life})`);

            this.ctx.beginPath();
            this.ctx.moveTo(m.x, m.y);
            this.ctx.lineTo(endX, endY);
            this.ctx.strokeStyle = gradient;
            this.ctx.lineWidth = 1.8;
            this.ctx.stroke();

            // Update meteor position
            m.x += Math.cos(m.angle) * m.speed;
            m.y += Math.sin(m.angle) * m.speed;
            m.life -= m.decay;

            if (m.life <= 0) {
                this.meteors.splice(i, 1);
            }
        }

        this.ctx.globalAlpha = 1.0;
        requestAnimationFrame(() => this.animate());
    }
};
