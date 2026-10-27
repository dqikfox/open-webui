<script>
  import { onMount } from 'svelte';

  let systemStats = {
    cpu: { usage: 0, cores: 0, temperature: 0 },
    memory: { used: 0, total: 0, available: 0 },
    disk: { used: 0, total: 0, free: 0 },
    gpu: { usage: 0, memory: 0, temperature: 0 },
    network: { sent: 0, received: 0 }
  };
  
  let processes = [];
  let loading = true;
  let autoRefresh = true;
  let refreshInterval;
  let isLoading = false;

  async function loadSystemStats() {
    if (isLoading) return;
    isLoading = true;
    
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000);
      
      const res = await fetch('/api/oasis/system/stats', {
        signal: controller.signal
      });
      clearTimeout(timeoutId);
      
      if (res.ok) {
        systemStats = await res.json();
      }
    } catch (e) {
      if (e.name !== 'AbortError') {
        console.error('Failed to load system stats:', e);
      }
    } finally {
      isLoading = false;
    }
  }

  async function loadProcesses() {
    try {
      const res = await fetch('/api/oasis/system/processes');
      if (res.ok) {
        processes = await res.json();
      }
    } catch (e) {
      console.error('Failed to load processes:', e);
    }
  }

  async function refreshData() {
    loading = true;
    await Promise.all([loadSystemStats(), loadProcesses()]);
    loading = false;
  }

  function formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  function getUsageColor(percentage) {
    if (percentage < 50) return '#00ff00';
    if (percentage < 80) return '#ffff00';
    return '#ff0000';
  }

  onMount(() => {
    refreshData();
    
    if (autoRefresh) {
      refreshInterval = setInterval(refreshData, 15000); // Reduced frequency
    }
    
    return () => {
      if (refreshInterval) clearInterval(refreshInterval);
    };
  });

  $: if (autoRefresh && !refreshInterval) {
    refreshInterval = setInterval(refreshData, 5000);
  } else if (!autoRefresh && refreshInterval) {
    clearInterval(refreshInterval);
    refreshInterval = null;
  }
</script>

<div class="system-monitor">
  <div class="monitor-header">
    <h3>🖥️ System Monitor</h3>
    <div class="monitor-controls">
      <label class="auto-refresh">
        <input type="checkbox" bind:checked={autoRefresh} />
        Auto Refresh (5s)
      </label>
      <button class="refresh-btn ultron-button" on:click={refreshData} disabled={loading}>
        {loading ? '⏳' : '🔄'} Refresh
      </button>
    </div>
  </div>

  <div class="stats-grid">
    <!-- CPU Stats -->
    <div class="stat-panel">
      <h4>🔥 CPU</h4>
      <div class="stat-item">
        <span>Usage:</span>
        <div class="progress-bar">
          <div 
            class="progress-fill" 
            style="width: {systemStats.cpu.usage}%; background-color: {getUsageColor(systemStats.cpu.usage)}"
          ></div>
          <span class="progress-text">{systemStats.cpu.usage.toFixed(1)}%</span>
        </div>
      </div>
      <div class="stat-item">
        <span>Cores:</span>
        <span class="stat-value">{systemStats.cpu.cores}</span>
      </div>
      <div class="stat-item">
        <span>Temp:</span>
        <span class="stat-value">{systemStats.cpu.temperature}°C</span>
      </div>
    </div>

    <!-- Memory Stats -->
    <div class="stat-panel">
      <h4>🧠 Memory</h4>
      <div class="stat-item">
        <span>Usage:</span>
        <div class="progress-bar">
          <div 
            class="progress-fill" 
            style="width: {(systemStats.memory.used / systemStats.memory.total * 100)}%; background-color: {getUsageColor(systemStats.memory.used / systemStats.memory.total * 100)}"
          ></div>
          <span class="progress-text">{((systemStats.memory.used / systemStats.memory.total) * 100).toFixed(1)}%</span>
        </div>
      </div>
      <div class="stat-item">
        <span>Used:</span>
        <span class="stat-value">{formatBytes(systemStats.memory.used)}</span>
      </div>
      <div class="stat-item">
        <span>Total:</span>
        <span class="stat-value">{formatBytes(systemStats.memory.total)}</span>
      </div>
    </div>

    <!-- Disk Stats -->
    <div class="stat-panel">
      <h4>💾 Disk</h4>
      <div class="stat-item">
        <span>Usage:</span>
        <div class="progress-bar">
          <div 
            class="progress-fill" 
            style="width: {(systemStats.disk.used / systemStats.disk.total * 100)}%; background-color: {getUsageColor(systemStats.disk.used / systemStats.disk.total * 100)}"
          ></div>
          <span class="progress-text">{((systemStats.disk.used / systemStats.disk.total) * 100).toFixed(1)}%</span>
        </div>
      </div>
      <div class="stat-item">
        <span>Used:</span>
        <span class="stat-value">{formatBytes(systemStats.disk.used)}</span>
      </div>
      <div class="stat-item">
        <span>Free:</span>
        <span class="stat-value">{formatBytes(systemStats.disk.free)}</span>
      </div>
    </div>

    <!-- GPU Stats -->
    <div class="stat-panel">
      <h4>🎮 GPU</h4>
      <div class="stat-item">
        <span>Usage:</span>
        <div class="progress-bar">
          <div 
            class="progress-fill" 
            style="width: {systemStats.gpu.usage}%; background-color: {getUsageColor(systemStats.gpu.usage)}"
          ></div>
          <span class="progress-text">{systemStats.gpu.usage.toFixed(1)}%</span>
        </div>
      </div>
      <div class="stat-item">
        <span>Memory:</span>
        <span class="stat-value">{formatBytes(systemStats.gpu.memory)}</span>
      </div>
      <div class="stat-item">
        <span>Temp:</span>
        <span class="stat-value">{systemStats.gpu.temperature}°C</span>
      </div>
    </div>
  </div>

  <!-- Top Processes -->
  <div class="processes-panel">
    <h4>🔄 Top Processes</h4>
    <div class="processes-table">
      <div class="table-header">
        <span>Process</span>
        <span>CPU %</span>
        <span>Memory</span>
        <span>PID</span>
      </div>
      {#each processes.slice(0, 10) as process}
        <div class="table-row">
          <span class="process-name">{process.name}</span>
          <span class="process-cpu" style="color: {getUsageColor(process.cpu)}">{process.cpu.toFixed(1)}%</span>
          <span class="process-memory">{formatBytes(process.memory)}</span>
          <span class="process-pid">{process.pid}</span>
        </div>
      {/each}
    </div>
  </div>
</div>

<style>
  .system-monitor {
    background: rgba(5, 5, 5, 0.9);
    border: 2px solid #ff0000;
    border-radius: 10px;
    padding: 1.5rem;
  }

  .monitor-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #ff0000;
  }

  .monitor-header h3 {
    color: #ff3333;
    margin: 0;
  }

  .monitor-controls {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .auto-refresh {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #fff;
    font-size: 0.9rem;
    cursor: pointer;
  }

  .auto-refresh input[type="checkbox"] {
    accent-color: #ff0000;
  }

  .refresh-btn {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .stat-panel {
    background: rgba(10, 10, 10, 0.8);
    border: 1px solid #ff0000;
    border-radius: 8px;
    padding: 1rem;
  }

  .stat-panel h4 {
    color: #ff3333;
    margin: 0 0 1rem 0;
    font-size: 1.1rem;
  }

  .stat-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
    color: #fff;
  }

  .stat-item:last-child {
    margin-bottom: 0;
  }

  .stat-value {
    font-weight: bold;
    color: #00ff00;
  }

  .progress-bar {
    position: relative;
    width: 100px;
    height: 20px;
    background: rgba(0, 0, 0, 0.5);
    border: 1px solid #ff0000;
    border-radius: 10px;
    overflow: hidden;
  }

  .progress-fill {
    height: 100%;
    transition: width 0.3s ease;
    border-radius: 10px;
  }

  .progress-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 0.8rem;
    font-weight: bold;
    color: #fff;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
  }

  .processes-panel {
    background: rgba(10, 10, 10, 0.8);
    border: 1px solid #ff0000;
    border-radius: 8px;
    padding: 1rem;
  }

  .processes-panel h4 {
    color: #ff3333;
    margin: 0 0 1rem 0;
  }

  .processes-table {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .table-header {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr;
    gap: 1rem;
    padding: 0.5rem;
    background: rgba(255, 0, 0, 0.1);
    border-radius: 4px;
    font-weight: bold;
    color: #ff3333;
    font-size: 0.9rem;
  }

  .table-row {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr;
    gap: 1rem;
    padding: 0.5rem;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 4px;
    color: #fff;
    font-size: 0.9rem;
    transition: background 0.2s;
  }

  .table-row:hover {
    background: rgba(255, 0, 0, 0.1);
  }

  .process-name {
    font-weight: bold;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .process-cpu {
    font-weight: bold;
  }

  .process-memory {
    color: #00ff00;
  }

  .process-pid {
    color: #999;
    font-family: monospace;
  }
</style>