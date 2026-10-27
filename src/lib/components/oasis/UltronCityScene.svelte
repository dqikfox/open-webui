<script>
  import { onMount } from 'svelte';
  
  let canvas;
  let ctx;
  let buildings = [];
  let particles = [];
  let loading = false;
  let cityImage = null;

  class Building {
    constructor(x, y, width, height, color) {
      this.x = x;
      this.y = y;
      this.width = width;
      this.height = height;
      this.color = color;
      this.windows = [];
      this.generateWindows();
    }

    generateWindows() {
      for (let i = 0; i < this.height; i += 20) {
        for (let j = 0; j < this.width; j += 15) {
          if (Math.random() > 0.3) {
            this.windows.push({ x: this.x + j + 5, y: this.y + i + 5 });
          }
        }
      }
    }

    draw(ctx) {
      ctx.fillStyle = this.color;
      ctx.fillRect(this.x, this.y, this.width, this.height);
      
      ctx.fillStyle = Math.random() > 0.5 ? '#ff0000' : '#ff3333';
      this.windows.forEach(w => {
        ctx.fillRect(w.x, w.y, 8, 8);
      });
    }
  }

  class Particle {
    constructor(x, y) {
      this.x = x;
      this.y = y;
      this.vx = (Math.random() - 0.5) * 2;
      this.vy = Math.random() * -2;
      this.life = 100;
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;
      this.life--;
    }

    draw(ctx) {
      ctx.fillStyle = `rgba(255, 0, 0, ${this.life / 100})`;
      ctx.fillRect(this.x, this.y, 2, 2);
    }
  }

  function generateCity() {
    buildings = [];
    const width = canvas.width;
    const height = canvas.height;
    
    for (let i = 0; i < 15; i++) {
      const bWidth = 40 + Math.random() * 60;
      const bHeight = 100 + Math.random() * 200;
      const x = i * (width / 15);
      const y = height - bHeight;
      const color = `rgba(${10 + Math.random() * 20}, ${10 + Math.random() * 20}, ${10 + Math.random() * 20}, 0.9)`;
      
      buildings.push(new Building(x, y, bWidth, bHeight, color));
    }
  }

  function animate() {
    if (!ctx) return;
    
    ctx.fillStyle = 'rgba(10, 10, 10, 0.1)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    if (cityImage) {
      ctx.globalAlpha = 0.3;
      ctx.drawImage(cityImage, 0, 0, canvas.width, canvas.height);
      ctx.globalAlpha = 1;
    }
    
    buildings.forEach(b => b.draw(ctx));
    
    if (Math.random() > 0.95) {
      const building = buildings[Math.floor(Math.random() * buildings.length)];
      for (let i = 0; i < 5; i++) {
        particles.push(new Particle(
          building.x + Math.random() * building.width,
          building.y
        ));
      }
    }
    
    particles = particles.filter(p => p.life > 0);
    particles.forEach(p => {
      p.update();
      p.draw(ctx);
    });
    
    requestAnimationFrame(animate);
  }

  async function generateCityWithMiniMax() {
    loading = true;
    try {
      const res = await fetch('/api/oasis/minimax/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: 'futuristic cyberpunk city at night, neon lights, red glowing circuits in sky, dark atmosphere, ultra detailed, 8K',
          width: 1024,
          height: 768
        })
      });
      
      const data = await res.json();
      if (data.image_url) {
        const img = new Image();
        img.onload = () => { cityImage = img; };
        img.src = data.image_url;
      }
    } catch (error) {
      console.error('MiniMax generation failed:', error);
    }
    loading = false;
  }

  onMount(() => {
    ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    generateCity();
    animate();
    
    window.addEventListener('resize', () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      generateCity();
    });
  });
</script>

<div class="city-scene">
  <canvas bind:this={canvas}></canvas>
  
  <div class="controls">
    <button on:click={generateCity} class="ultron-button">
      Regenerate City
    </button>
    <button on:click={generateCityWithMiniMax} disabled={loading} class="ultron-button">
      {loading ? 'Generating...' : 'Generate with AI'}
    </button>
  </div>
  
  <div class="info">
    <h2>ULTRON CITY</h2>
    <p>Buildings: {buildings.length}</p>
    <p>Particles: {particles.length}</p>
  </div>
</div>

<style>
  .city-scene {
    position: relative;
    width: 100vw;
    height: 100vh;
    background: #0a0a0a;
    overflow: hidden;
  }

  canvas {
    display: block;
    width: 100%;
    height: 100%;
  }

  .controls {
    position: absolute;
    top: 20px;
    right: 20px;
    display: flex;
    gap: 10px;
  }

  .info {
    position: absolute;
    top: 20px;
    left: 20px;
    font-family: 'Orbitron', sans-serif;
    color: #ff6666;
    text-shadow: 0 0 10px rgba(255, 0, 0, 0.8);
  }

  .info h2 {
    margin: 0;
    font-size: 2rem;
    letter-spacing: 3px;
  }

  .info p {
    margin: 5px 0;
    font-size: 0.9rem;
  }

  button {
    background: linear-gradient(135deg, #1a0a0a, #2a1515);
    border: 1px solid #ff0000;
    color: #ff6666;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-family: 'Orbitron', sans-serif;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: all 0.3s;
  }

  button:hover:not(:disabled) {
    box-shadow: 0 0 20px rgba(255, 0, 0, 0.8);
    transform: translateY(-2px);
  }

  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style>
