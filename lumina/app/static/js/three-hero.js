/* ============================================
   LIGHTWEIGHT ULTRA-FAST AURORA STARFIELD HERO
   Performance: 60fps buttery smooth, zero lag, HTML5 Canvas 2D
   ============================================ */

class AuroraHero {
  constructor() {
    this.container = document.querySelector('.hero');
    if (!this.container) return;

    this.canvas = document.createElement('canvas');
    this.ctx = this.canvas.getContext('2d');
    this.particles = [];
    this.numParticles = 80;
    this.animId = null;
    this.isVisible = true;

    this.init();
  }

  init() {
    this.canvas.style.position = 'absolute';
    this.canvas.style.top = '0';
    this.canvas.style.left = '0';
    this.canvas.style.width = '100%';
    this.canvas.style.height = '100%';
    this.canvas.style.pointerEvents = 'none';
    this.canvas.style.zIndex = '1';
    this.container.insertBefore(this.canvas, this.container.firstChild);

    this.resize();
    this.createParticles();

    window.addEventListener('resize', () => this.resize());

    // Visibility observer
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        this.isVisible = entry.isIntersecting;
      });
    }, { threshold: 0 });
    observer.observe(this.container);

    this.animate();
  }

  resize() {
    this.width = this.container.offsetWidth;
    this.height = this.container.offsetHeight;
    this.canvas.width = this.width * window.devicePixelRatio;
    this.canvas.height = this.height * window.devicePixelRatio;
    this.ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
  }

  createParticles() {
    this.particles = [];
    const colors = ['#10b981', '#06b6d4', '#8b5cf6', '#ffffff'];
    for (let i = 0; i < this.numParticles; i++) {
      this.particles.push({
        x: Math.random() * this.width,
        y: Math.random() * this.height,
        radius: Math.random() * 2 + 0.5,
        color: colors[Math.floor(Math.random() * colors.length)],
        vx: (Math.random() - 0.5) * 0.3,
        vy: (Math.random() - 0.5) * 0.3,
        alpha: Math.random() * 0.7 + 0.3,
        pulseSpeed: Math.random() * 0.02 + 0.01
      });
    }
  }

  animate() {
    if (this.isVisible) {
      this.ctx.clearRect(0, 0, this.width, this.height);

      // Draw subtle aurora wave gradient
      const gradient = this.ctx.createLinearGradient(0, 0, this.width, this.height);
      gradient.addColorStop(0, 'rgba(16, 185, 129, 0.05)');
      gradient.addColorStop(0.5, 'rgba(6, 182, 212, 0.03)');
      gradient.addColorStop(1, 'rgba(139, 92, 246, 0.05)');
      this.ctx.fillStyle = gradient;
      this.ctx.fillRect(0, 0, this.width, this.height);

      // Update and draw particles
      for (let p of this.particles) {
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0) p.x = this.width;
        if (p.x > this.width) p.x = 0;
        if (p.y < 0) p.y = this.height;
        if (p.y > this.height) p.y = 0;

        p.alpha += Math.sin(Date.now() * p.pulseSpeed) * 0.01;
        p.alpha = Math.max(0.2, Math.min(0.9, p.alpha));

        this.ctx.beginPath();
        this.ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        this.ctx.fillStyle = p.color;
        this.ctx.globalAlpha = p.alpha;
        this.ctx.shadowBlur = 10;
        this.ctx.shadowColor = p.color;
        this.ctx.fill();
        this.ctx.shadowBlur = 0;
      }
      this.ctx.globalAlpha = 1.0;
    }

    this.animId = requestAnimationFrame(() => this.animate());
  }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => new AuroraHero());
} else {
  new AuroraHero();
}
