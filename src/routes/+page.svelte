<script>
  import { onMount } from 'svelte';
  import UltronBackground from '$lib/components/oasis/UltronBackground.svelte';

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
  <title>OASIS - Omniscient AI System Interface & Services</title>
</svelte:head>

<UltronBackground />

<div class="hero-section">
  <div class="hero-content">
    <div class="logo-container">
      <img src="/static/assets/ultron/ultron_logo.svg" alt="OASIS" class="hero-logo" />
    </div>
    <h1 class="hero-title ultron-text-glow">OASIS</h1>
    <p class="hero-subtitle">Omniscient AI System Interface & Services</p>
    <p class="hero-description">
      The most powerful, extensible AI platform designed to operate entirely offline.
      Multi-agent collaboration, advanced workflows, and enterprise-ready features.
    </p>
    
    <div class="hero-stats">
      {#if loading}
        <div class="stat-loading">Loading stats...</div>
      {:else}
        <div class="stat-item">
          <span class="stat-number">{stats.users.toLocaleString()}</span>
          <span class="stat-label">Active Users</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">{stats.models}</span>
          <span class="stat-label">AI Models</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">{stats.chats.toLocaleString()}</span>
          <span class="stat-label">Conversations</span>
        </div>
      {/if}
    </div>

    <div class="hero-actions">
      <button class="cta-button primary ultron-button">
        🚀 Launch OASIS
      </button>
      <button class="cta-button secondary ultron-button">
        📚 Documentation
      </button>
    </div>
  </div>
</div>

<div class="features-section">
  <div class="container">
    <h2 class="section-title ultron-text-glow">Core Features</h2>
    
    <div class="features-grid">
      <div class="feature-card ultron-card">
        <div class="feature-icon">🤖</div>
        <h3>Multi-Agent System</h3>
        <p>Architect, Developer, Reviewer, and Optimizer agents working together</p>
      </div>
      
      <div class="feature-card ultron-card">
        <div class="feature-icon">⚙️</div>
        <h3>Automated Workflows</h3>
        <p>Code review, feature development, bug fixes, and optimization workflows</p>
      </div>
      
      <div class="feature-card ultron-card">
        <div class="feature-icon">🧠</div>
        <h3>Knowledge Base</h3>
        <p>Persistent learning with facts, patterns, solutions, and insights</p>
      </div>
      
      <div class="feature-card ultron-card">
        <div class="feature-icon">🎮</div>
        <h3>CUDA Acceleration</h3>
        <p>GPU-optimized inference with CUDA 13.0 and multi-GPU support</p>
      </div>
      
      <div class="feature-card ultron-card">
        <div class="feature-icon">🔌</div>
        <h3>Plugin System</h3>
        <p>Extensible architecture with custom plugins and marketplace</p>
      </div>
      
      <div class="feature-card ultron-card">
        <div class="feature-icon">📊</div>
        <h3>Analytics Engine</h3>
        <p>Real-time usage tracking, cost monitoring, and performance metrics</p>
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
    background: linear-gradient(135deg, rgba(10, 10, 10, 0.9) 0%, rgba(26, 10, 10, 0.9) 100%);
    overflow: hidden;
  }

  .hero-content {
    text-align: center;
    max-width: 800px;
    padding: 2rem;
    z-index: 10;
  }

  .logo-container {
    margin-bottom: 2rem;
  }

  .hero-logo {
    width: 120px;
    height: 120px;
    filter: drop-shadow(0 0 30px rgba(255, 0, 0, 0.8));
    animation: logo-pulse 3s ease-in-out infinite;
  }

  @keyframes logo-pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
  }

  .hero-title {
    font-size: 4rem;
    font-weight: bold;
    margin: 1rem 0;
    background: linear-gradient(135deg, #ff0000, #ff6666);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .hero-subtitle {
    font-size: 1.5rem;
    color: #ff3333;
    margin-bottom: 1rem;
    font-weight: 300;
  }

  .hero-description {
    font-size: 1.1rem;
    color: #ccc;
    line-height: 1.6;
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
  }

  .stat-number {
    display: block;
    font-size: 2.5rem;
    font-weight: bold;
    color: #ff0000;
    text-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
  }

  .stat-label {
    display: block;
    font-size: 0.9rem;
    color: #999;
    margin-top: 0.5rem;
  }

  .stat-loading {
    color: #ff3333;
    font-size: 1.2rem;
    animation: pulse 2s infinite;
  }

  .hero-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
  }

  .cta-button {
    padding: 1rem 2rem;
    font-size: 1.1rem;
    font-weight: bold;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s;
    border: 2px solid;
  }

  .cta-button.primary {
    background: linear-gradient(135deg, #ff0000, #cc0000);
    border-color: #ff3333;
    color: white;
  }

  .cta-button.secondary {
    background: transparent;
    border-color: #ff0000;
    color: #ff3333;
  }

  .cta-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(255, 0, 0, 0.3);
  }

  .features-section {
    padding: 6rem 0;
    background: rgba(5, 5, 5, 0.95);
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
  }

  .section-title {
    text-align: center;
    font-size: 3rem;
    margin-bottom: 4rem;
    color: #ff3333;
  }

  .features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
  }

  .feature-card {
    padding: 2rem;
    background: rgba(10, 10, 10, 0.8);
    border: 2px solid #ff0000;
    border-radius: 15px;
    text-align: center;
    transition: all 0.3s;
  }

  .feature-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(255, 0, 0, 0.3);
  }

  .feature-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
  }

  .feature-card h3 {
    color: #ff3333;
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }

  .feature-card p {
    color: #ccc;
    line-height: 1.6;
  }

  @media (max-width: 768px) {
    .hero-title {
      font-size: 2.5rem;
    }
    
    .hero-stats {
      gap: 1.5rem;
    }
    
    .features-grid {
      grid-template-columns: 1fr;
    }
  }
</style>