<script>
  import { onMount } from 'svelte';
  import AtlasBackground from '$lib/components/layout/AtlasBackground.svelte';

  let stats = { users: 0, models: 0, chats: 0 };
  let loading = true;

  onMount(async () => {
    try {
      // Simulate loading stats
      await new Promise(resolve => setTimeout(resolve, 1000));
      stats = { users: 1247, models: 15, chats: 8934 };
    } catch (e) {
      console.error('Stats error:', e);
    }
    loading = false;
  });
</script>

<svelte:head>
  <title>ATLAS - Advanced Technologies & Logistics AI System</title>
</svelte:head>

<AtlasBackground />

<div class="hero-section">
  <div class="hero-content">
    <div class="logo-container">
      <img src="/static/assets/atlas/hero.jpg" alt="ATLAS" class="hero-logo" style="border-radius: 50%; border: 4px solid #00ffff; box-shadow: 0 0 30px rgba(0, 255, 255, 0.6);" />
    </div>
    <h1 class="hero-title atlas-text-glow">ATLAS</h1>
    <p class="hero-subtitle">Omniscient AI System Interface</p>
    <p class="hero-description">
      The nexus of your digital universe. Connect, control, and explore with advanced AI workflows, memory repositories, and universal device integration. Energy, frequencies, and boundless possibilities.
    </p>

    <div class="hero-stats">
      {#if loading}
        <div class="stat-loading">Initiating quantum link...</div>
      {:else}
        <div class="stat-item">
          <span class="stat-number">{stats.users.toLocaleString()}</span>
          <span class="stat-label">Connected Nodes</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">{stats.models}</span>
          <span class="stat-label">Neural Models</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">{stats.chats.toLocaleString()}</span>
          <span class="stat-label">Data Synapses</span>
        </div>
      {/if}
    </div>

    <div class="hero-actions">
      <button class="cta-button primary atlas-button">
        ⚡ Initialize ATLAS
      </button>
      <button class="cta-button secondary atlas-button">
        🌌 Explore Nexus
      </button>
    </div>
  </div>
</div>

<div class="features-section">
  <div class="container">
    <h2 class="section-title atlas-text-glow">Core Functions</h2>

    <div class="features-grid">
      <div class="feature-card atlas-card">
        <div class="feature-icon" style="background: url('/static/assets/atlas/bg1.jpg') center/cover; border-radius: 50%; height: 80px; width: 80px; margin: 0 auto 1rem auto; border: 2px solid #00ffff; box-shadow: 0 0 15px #00ffff;"></div>
        <h3>Omni-Device Control</h3>
        <p>Seamlessly control all attached devices via SSH, ADB, WiFi, KDE Connect, and WebRTC protocols.</p>
      </div>

      <div class="feature-card atlas-card">
        <div class="feature-icon" style="background: url('/static/assets/atlas/bg2.jpg') center/cover; border-radius: 50%; height: 80px; width: 80px; margin: 0 auto 1rem auto; border: 2px solid #ff00ff; box-shadow: 0 0 15px #ff00ff;"></div>
        <h3>Neural Repository</h3>
        <p>A unified memory hub storing your tools, MCPs, skills, and deep contextual connections.</p>
      </div>

      <div class="feature-card atlas-card">
        <div class="feature-icon" style="background: url('/static/assets/atlas/bg3.jpg') center/cover; border-radius: 50%; height: 80px; width: 80px; margin: 0 auto 1rem auto; border: 2px solid #ffff00; box-shadow: 0 0 15px #ffff00;"></div>
        <h3>Universal Physics</h3>
        <p>Harness the power of energy, light, and frequencies inspired by Tesla and Einstein.</p>
      </div>
    </div>
  </div>
</div>

<style>
  .hero-section {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    background: transparent;
    overflow: hidden;
  }

  .hero-content {
    text-align: center;
    max-width: 800px;
    padding: 2rem;
    z-index: 10;
    background: rgba(5, 10, 25, 0.6);
    border: 1px solid rgba(0, 255, 255, 0.2);
    border-radius: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 40px rgba(0, 255, 255, 0.1);
  }

  .logo-container {
    margin-bottom: 2rem;
  }

  .hero-logo {
    width: 150px;
    height: 150px;
    animation: float 4s ease-in-out infinite;
    object-fit: cover;
  }

  @keyframes float {
    0%, 100% { transform: translateY(0px) scale(1); }
    50% { transform: translateY(-15px) scale(1.05); }
  }

  .hero-title {
    font-size: 5rem;
    font-weight: 900;
    margin: 1rem 0;
    background: linear-gradient(135deg, #00ffff, #0099ff, #ff00ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 4px;
    text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
  }

  .hero-subtitle {
    font-size: 1.5rem;
    color: #00ffff;
    margin-bottom: 1rem;
    font-weight: 400;
    letter-spacing: 2px;
    text-transform: uppercase;
  }

  .hero-description {
    font-size: 1.1rem;
    color: #e0f7fa;
    line-height: 1.8;
    margin-bottom: 3rem;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
  }

  .hero-stats {
    display: flex;
    justify-content: center;
    gap: 3rem;
    margin: 3rem 0;
    flex-wrap: wrap;
  }

  .stat-item {
    text-align: center;
    background: rgba(0, 255, 255, 0.05);
    padding: 1.5rem;
    border-radius: 15px;
    border: 1px solid rgba(0, 255, 255, 0.2);
    transition: all 0.3s ease;
  }

  .stat-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 255, 255, 0.2);
    border-color: rgba(0, 255, 255, 0.5);
  }

  .stat-number {
    display: block;
    font-size: 2.5rem;
    font-weight: bold;
    color: #00ffff;
    text-shadow: 0 0 15px rgba(0, 255, 255, 0.8);
    font-family: 'Orbitron', monospace;
  }

  .stat-label {
    display: block;
    font-size: 0.9rem;
    color: #a0d8ef;
    margin-top: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .stat-loading {
    color: #00ffff;
    font-size: 1.2rem;
    animation: pulse 2s infinite;
  }

  .hero-actions {
    display: flex;
    gap: 1.5rem;
    justify-content: center;
    flex-wrap: wrap;
  }

  .cta-button {
    padding: 1rem 2.5rem;
    font-size: 1.2rem;
    font-weight: bold;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s;
    border: 2px solid;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .cta-button.primary {
    background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(0, 153, 255, 0.4));
    border-color: #00ffff;
    color: #ffffff;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.4);
  }

  .cta-button.secondary {
    background: rgba(10, 20, 40, 0.5);
    border-color: #ff00ff;
    color: #ff00ff;
    box-shadow: 0 0 20px rgba(255, 0, 255, 0.2);
  }

  .cta-button:hover {
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 15px 30px rgba(0, 255, 255, 0.6);
  }

  .cta-button.secondary:hover {
    box-shadow: 0 15px 30px rgba(255, 0, 255, 0.5);
    background: rgba(255, 0, 255, 0.1);
  }

  .features-section {
    padding: 6rem 0;
    background: rgba(5, 10, 25, 0.85);
    border-top: 1px solid rgba(0, 255, 255, 0.3);
    position: relative;
    z-index: 10;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
  }

  .section-title {
    text-align: center;
    font-size: 3.5rem;
    margin-bottom: 4rem;
    color: #ffffff;
    text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
    letter-spacing: 3px;
  }

  .features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 3rem;
  }

  .feature-card {
    padding: 2.5rem;
    background: rgba(10, 15, 30, 0.7);
    border: 1px solid rgba(0, 255, 255, 0.3);
    border-radius: 20px;
    text-align: center;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    backdrop-filter: blur(5px);
  }

  .feature-card:hover {
    transform: translateY(-15px) scale(1.02);
    box-shadow: 0 20px 40px rgba(0, 255, 255, 0.2), inset 0 0 20px rgba(0, 255, 255, 0.1);
    border-color: #00ffff;
  }

  .feature-card h3 {
    color: #ffffff;
    font-size: 1.8rem;
    margin-bottom: 1rem;
    text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
  }

  .feature-card p {
    color: #b0d0e0;
    line-height: 1.7;
    font-size: 1.1rem;
  }

  @media (max-width: 768px) {
    .hero-title {
      font-size: 3rem;
    }

    .hero-stats {
      gap: 1.5rem;
    }

    .features-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
