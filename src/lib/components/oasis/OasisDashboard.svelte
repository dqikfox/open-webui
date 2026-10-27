<script>
  import { onMount } from 'svelte';
  import AutoGenPanel from './AutoGenPanel.svelte';
  import WorkflowPanel from './WorkflowPanel.svelte';
  import CUDAMonitor from './CUDAMonitor.svelte';
  import QuickChatPanel from './QuickChatPanel.svelte';
  import SystemMonitor from './SystemMonitor.svelte';
  import LoadingSpinner from './LoadingSpinner.svelte';

  let activeTab = 'dashboard';
  let stats = {};
  let loading = false;
  let commandInput = '';
  let commandOutput = '';
  let models = [];
  let selectedModel = '';
  let notifications = [];

  async function loadStats() {
    loading = true;
    try {
      const res = await fetch('/api/oasis/status');
      stats = await res.json();
      await loadModels();
    } catch (e) {
      console.error('Stats error:', e);
      addNotification('Failed to load stats', 'error');
    }
    loading = false;
  }

  async function loadModels() {
    try {
      const res = await fetch('/ollama/api/tags');
      const data = await res.json();
      models = data.models || [];
      if (models.length > 0 && !selectedModel) {
        selectedModel = models[0].name;
      }
    } catch (e) {
      console.error('Models error:', e);
    }
  }

  async function executeCommand() {
    if (!commandInput.trim()) return;
    
    try {
      const res = await fetch('/api/oasis/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command: commandInput })
      });
      const result = await res.json();
      commandOutput = JSON.stringify(result, null, 2);
      addNotification('Command executed successfully', 'success');
    } catch (e) {
      commandOutput = `Error: ${e.message}`;
      addNotification('Command failed', 'error');
    }
    commandInput = '';
  }

  function addNotification(message, type = 'info') {
    const id = Date.now();
    notifications = [...notifications, { id, message, type }];
    setTimeout(() => {
      notifications = notifications.filter(n => n.id !== id);
    }, 5000);
  }



  onMount(() => {
    loadStats();
    // Auto-refresh every 30 seconds
    const interval = setInterval(loadStats, 30000);
    return () => clearInterval(interval);
  });
</script>

<div class="oasis-dashboard">
  <div class="dashboard-header">
    <h1 class="ultron-text-glow">🌟 OASIS Control Center</h1>
    <div class="status-indicator {stats.agent ? 'online' : 'offline'}">
      {stats.agent ? '🟢 Online' : '🔴 Offline'}
    </div>
  </div>

  <div class="dashboard-tabs">
    <button class="tab-btn" class:active={activeTab === 'dashboard'} on:click={() => activeTab = 'dashboard'}>
      📊 Dashboard
    </button>
    <button class="tab-btn" class:active={activeTab === 'autogen'} on:click={() => activeTab = 'autogen'}>
      🤖 AutoGen
    </button>
    <button class="tab-btn" class:active={activeTab === 'workflows'} on:click={() => activeTab = 'workflows'}>
      ⚙️ Workflows
    </button>
    <button class="tab-btn" class:active={activeTab === 'cuda'} on:click={() => activeTab = 'cuda'}>
      🎮 CUDA
    </button>
    <button class="tab-btn" class:active={activeTab === 'chat'} on:click={() => activeTab = 'chat'}>
      💬 Chat
    </button>
    <button class="tab-btn" class:active={activeTab === 'terminal'} on:click={() => activeTab = 'terminal'}>
      💻 Terminal
    </button>
    <button class="tab-btn" class:active={activeTab === 'system'} on:click={() => activeTab = 'system'}>
      📊 System
    </button>
  </div>

  <div class="dashboard-content">
    {#if activeTab === 'dashboard'}
      <div class="stats-grid">
        <div class="stat-card ultron-card">
          <h3>Agent Status</h3>
          {#if loading}
            <LoadingSpinner />
          {:else}
            <p class="stat-value">{stats.agent?.status || 'Unknown'}</p>
          {/if}
        </div>
        <div class="stat-card ultron-card">
          <h3>Memory Usage</h3>
          <p class="stat-value">{stats.memory?.messages || 0} messages</p>
        </div>
        <div class="stat-card ultron-card">
          <h3>Tools Loaded</h3>
          <p class="stat-value">20+ tools</p>
        </div>
        <div class="stat-card ultron-card">
          <h3>Functions</h3>
          <p class="stat-value">20 functions</p>
        </div>
      </div>

      <div class="quick-actions">
        <h3>Quick Actions</h3>
        <div class="action-grid">
          <button class="action-btn ultron-button" on:click={() => activeTab = 'autogen'}>
            🧠 Generate Suggestions
          </button>
          <button class="action-btn ultron-button" on:click={() => activeTab = 'workflows'}>
            🔄 Run Workflow
          </button>
          <button class="action-btn ultron-button" on:click={loadStats}>
            🔄 Refresh Stats
          </button>
          <button class="action-btn ultron-button" on:click={() => activeTab = 'cuda'}>
            📊 Check GPU
          </button>
          <button class="action-btn ultron-button" on:click={() => activeTab = 'chat'}>
            💬 Quick Chat
          </button>
          <button class="action-btn ultron-button" on:click={() => activeTab = 'terminal'}>
            💻 Terminal
          </button>
          <button class="action-btn ultron-button" on:click={() => activeTab = 'system'}>
            📊 System Monitor
          </button>
        </div>
      </div>

      <!-- Model Selector -->
      <div class="model-selector">
        <h3>Active Model</h3>
        <select bind:value={selectedModel} class="model-select">
          {#each models as model}
            <option value={model.name}>{model.name} ({(model.size / 1e9).toFixed(1)}GB)</option>
          {/each}
        </select>
      </div>
    {:else if activeTab === 'autogen'}
      <AutoGenPanel />
    {:else if activeTab === 'workflows'}
      <WorkflowPanel />
    {:else if activeTab === 'cuda'}
      <CUDAMonitor />
    {:else if activeTab === 'chat'}
      <QuickChatPanel {selectedModel} />
    {:else if activeTab === 'system'}
      <SystemMonitor />
    {:else if activeTab === 'terminal'}
      <div class="terminal-panel">
        <h3>OASIS Command Terminal</h3>
        <div class="command-input">
          <input 
            type="text" 
            bind:value={commandInput} 
            placeholder="Enter OASIS command (e.g., 'test', 'analyze file.py', 'tool list')" 
            class="terminal-input"
            on:keydown={(e) => e.key === 'Enter' && executeCommand()}
          />
          <button class="execute-btn ultron-button" on:click={executeCommand}>
            ⚡ Execute
          </button>
        </div>
        {#if commandOutput}
          <div class="command-output">
            <pre>{commandOutput}</pre>
          </div>
        {/if}
      </div>
    {/if}
  </div>
</div>

<!-- Notifications -->
{#if notifications.length > 0}
  <div class="notifications">
    {#each notifications as notification}
      <div class="notification {notification.type}">
        {notification.message}
      </div>
    {/each}
  </div>
{/if}

<style>
  .oasis-dashboard {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
    background: rgba(10, 10, 10, 0.95);
    border: 2px solid #ff0000;
    border-radius: 10px;
    box-shadow: 0 0 30px rgba(255, 0, 0, 0.3);
  }

  .dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid #ff0000;
  }

  .dashboard-header h1 {
    margin: 0;
    font-size: 2.5rem;
  }

  .status-indicator {
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: bold;
    border: 2px solid;
  }

  .status-indicator.online {
    background: rgba(0, 255, 0, 0.1);
    border-color: #00ff00;
    color: #00ff00;
  }

  .status-indicator.offline {
    background: rgba(255, 0, 0, 0.1);
    border-color: #ff0000;
    color: #ff0000;
  }

  .dashboard-tabs {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    border-bottom: 1px solid #ff0000;
  }

  .tab-btn {
    padding: 1rem 2rem;
    background: rgba(5, 5, 5, 0.8);
    border: 1px solid #ff0000;
    color: #ff3333;
    cursor: pointer;
    transition: all 0.3s;
    border-bottom: none;
    border-radius: 10px 10px 0 0;
  }

  .tab-btn:hover {
    background: rgba(255, 0, 0, 0.1);
    box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
  }

  .tab-btn.active {
    background: rgba(255, 0, 0, 0.2);
    color: #ff0000;
    box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
  }

  .dashboard-content {
    min-height: 600px;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
  }

  .stat-card {
    padding: 1.5rem;
    text-align: center;
    background: rgba(5, 5, 5, 0.8);
    border: 2px solid #ff0000;
    border-radius: 10px;
    transition: all 0.3s;
  }

  .stat-card:hover {
    box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
    transform: translateY(-5px);
  }

  .stat-card h3 {
    color: #ff3333;
    margin-bottom: 1rem;
    font-size: 1.1rem;
  }

  .stat-value {
    font-size: 2rem;
    font-weight: bold;
    color: #fff;
    margin: 0;
  }

  .quick-actions {
    margin-top: 2rem;
  }

  .quick-actions h3 {
    color: #ff3333;
    margin-bottom: 1rem;
  }

  .action-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
  }

  .action-btn {
    padding: 1rem;
    font-size: 1rem;
    border-radius: 8px;
    transition: all 0.3s;
  }

  .action-btn:hover {
    transform: scale(1.05);
  }

  .model-selector {
    margin-top: 2rem;
    padding: 1.5rem;
    background: rgba(5, 5, 5, 0.8);
    border: 2px solid #ff0000;
    border-radius: 10px;
  }

  .model-selector h3 {
    color: #ff3333;
    margin-bottom: 1rem;
  }

  .model-select {
    width: 100%;
    padding: 0.75rem;
    background: rgba(10, 10, 10, 0.9);
    border: 1px solid #ff0000;
    border-radius: 5px;
    color: #fff;
    font-size: 1rem;
  }

  .model-select:focus {
    outline: none;
    box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
  }

  .terminal-panel {
    background: rgba(5, 5, 5, 0.9);
    border: 2px solid #ff0000;
    border-radius: 10px;
    padding: 1.5rem;
  }

  .terminal-panel h3 {
    color: #ff3333;
    margin-bottom: 1rem;
  }

  .command-input {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .terminal-input {
    flex: 1;
    padding: 0.75rem;
    background: rgba(10, 10, 10, 0.9);
    border: 1px solid #ff0000;
    border-radius: 5px;
    color: #00ff00;
    font-family: 'Courier New', monospace;
    font-size: 1rem;
  }

  .terminal-input:focus {
    outline: none;
    box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
  }

  .execute-btn {
    padding: 0.75rem 1.5rem;
    white-space: nowrap;
  }

  .command-output {
    background: rgba(0, 0, 0, 0.8);
    border: 1px solid #ff0000;
    border-radius: 5px;
    padding: 1rem;
    max-height: 400px;
    overflow-y: auto;
  }

  .command-output pre {
    color: #00ff00;
    font-family: 'Courier New', monospace;
    font-size: 0.9rem;
    margin: 0;
    white-space: pre-wrap;
  }

  .notifications {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1000;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .notification {
    padding: 1rem 1.5rem;
    border-radius: 5px;
    color: #fff;
    font-weight: bold;
    animation: slideIn 0.3s ease-out;
    min-width: 250px;
  }

  .notification.success {
    background: rgba(0, 255, 0, 0.2);
    border: 1px solid #00ff00;
  }

  .notification.error {
    background: rgba(255, 0, 0, 0.2);
    border: 1px solid #ff0000;
  }

  .notification.warning {
    background: rgba(255, 255, 0, 0.2);
    border: 1px solid #ffff00;
  }

  .notification.info {
    background: rgba(0, 0, 255, 0.2);
    border: 1px solid #0000ff;
  }

  @keyframes slideIn {
    from {
      transform: translateX(100%);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }
</style>