<script>
  import { onMount } from 'svelte';
  import QasyChat from './QasyChat.svelte';
  import QasyToolPanel from './QasyToolPanel.svelte';
  import UltronCityScene from './UltronCityScene.svelte';
  
  let activeTab = 'chat';
  let status = {};
  let features = [];

  async function loadStatus() {
    try {
      const [qasyRes, nemoRes, nvidia3dRes, autogptRes] = await Promise.all([
        fetch('/api/oasis/status'),
        fetch('/api/oasis/nemo/status'),
        fetch('/api/oasis/nvidia3d/status'),
        fetch('/api/oasis/autogpt/status')
      ]);
      
      status = {
        qasy: await qasyRes.json(),
        nemo: await nemoRes.json(),
        nvidia3d: await nvidia3dRes.json(),
        autogpt: await autogptRes.json()
      };
      
      features = [
        { name: 'OASIS Agent', enabled: status.qasy.agent.active, icon: '🤖' },
        { name: 'NeMo Toolkit', enabled: status.nemo.enabled, icon: '🧠' },
        { name: 'NVIDIA 3D Gen', enabled: status.nvidia3d.enabled, icon: '🏗️' },
        { name: 'AutoGPT Code', enabled: status.autogpt.enabled, icon: '💻' },
        { name: 'MiniMax AI', enabled: true, icon: '🎨' },
        { name: 'Ultron Theme', enabled: true, icon: '🌃' }
      ];
    } catch (error) {
      console.error('Failed to load status:', error);
    }
  }

  onMount(loadStatus);
</script>

<div class="qasy-dashboard">
  <header class="dashboard-header">
    <h1>OASIS CONTROL CENTER</h1>
    <div class="status-grid">
      {#each features as feature}
        <div class="status-card" class:enabled={feature.enabled}>
          <span class="icon">{feature.icon}</span>
          <span class="name">{feature.name}</span>
          <span class="badge">{feature.enabled ? 'ACTIVE' : 'OFFLINE'}</span>
        </div>
      {/each}
    </div>
  </header>

  <nav class="tabs">
    <button class:active={activeTab === 'chat'} on:click={() => activeTab = 'chat'}>
      💬 Chat
    </button>
    <button class:active={activeTab === 'tools'} on:click={() => activeTab = 'tools'}>
      🔧 Tools
    </button>
    <button class:active={activeTab === 'city'} on:click={() => activeTab = 'city'}>
      🌃 City Scene
    </button>
    <button class:active={activeTab === 'code'} on:click={() => activeTab = 'code'}>
      💻 Code Gen
    </button>
  </nav>

  <main class="dashboard-content">
    {#if activeTab === 'chat'}
      <QasyChat />
    {:else if activeTab === 'tools'}
      <QasyToolPanel />
    {:else if activeTab === 'city'}
      <UltronCityScene />
    {:else if activeTab === 'code'}
      <div class="code-panel">
        <h2>AutoGPT Code Generation</h2>
        <textarea placeholder="Describe the code you want to generate..." rows="5"></textarea>
        <button class="ultron-button">Generate Code</button>
      </div>
    {/if}
  </main>
</div>

<style>
  .qasy-dashboard {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background: #0a0a0a;
    color: #ff6666;
    font-family: 'Rajdhani', sans-serif;
  }

  .dashboard-header {
    padding: 1rem 2rem;
    background: linear-gradient(135deg, #1a0a0a, #2a1515);
    border-bottom: 2px solid #ff0000;
    box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);
  }

  h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: 2rem;
    margin: 0 0 1rem 0;
    text-transform: uppercase;
    letter-spacing: 3px;
    text-shadow: 0 0 20px rgba(255, 0, 0, 0.8);
  }

  .status-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
  }

  .status-card {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem;
    background: rgba(255, 0, 0, 0.05);
    border: 1px solid rgba(255, 0, 0, 0.3);
    border-radius: 4px;
    font-size: 0.9rem;
  }

  .status-card.enabled {
    border-color: #ff0000;
    box-shadow: 0 0 10px rgba(255, 0, 0, 0.3);
  }

  .icon {
    font-size: 1.5rem;
  }

  .name {
    flex: 1;
    font-weight: 500;
  }

  .badge {
    font-size: 0.7rem;
    padding: 2px 6px;
    background: rgba(255, 0, 0, 0.2);
    border-radius: 3px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .status-card.enabled .badge {
    background: #ff0000;
    color: #fff;
  }

  .tabs {
    display: flex;
    gap: 0.5rem;
    padding: 1rem 2rem;
    background: #0a0a0a;
    border-bottom: 1px solid rgba(255, 0, 0, 0.3);
  }

  .tabs button {
    background: transparent;
    border: 1px solid rgba(255, 0, 0, 0.3);
    color: #ff6666;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-family: 'Orbitron', sans-serif;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: all 0.3s;
  }

  .tabs button:hover {
    border-color: #ff0000;
    box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
  }

  .tabs button.active {
    background: linear-gradient(135deg, #1a0a0a, #2a1515);
    border-color: #ff0000;
    box-shadow: 0 0 20px rgba(255, 0, 0, 0.6);
  }

  .dashboard-content {
    flex: 1;
    overflow: auto;
    padding: 2rem;
  }

  .code-panel {
    max-width: 800px;
    margin: 0 auto;
  }

  .code-panel h2 {
    font-family: 'Orbitron', sans-serif;
    color: #ff6666;
    margin-bottom: 1rem;
  }

  .code-panel textarea {
    width: 100%;
    background: #1a1a1a;
    border: 1px solid rgba(255, 0, 0, 0.3);
    color: #ff6666;
    padding: 1rem;
    border-radius: 4px;
    font-family: 'Exo 2', monospace;
    margin-bottom: 1rem;
  }

  .code-panel textarea:focus {
    outline: none;
    border-color: #ff0000;
    box-shadow: 0 0 15px rgba(255, 0, 0, 0.5);
  }
</style>
