<script>
  import { onMount, onDestroy } from 'svelte';

  let cudaStatus = null;
  let loading = false;
  let interval;

  async function fetchStatus() {
    try {
      const res = await fetch('/api/oasis/cuda/status');
      cudaStatus = await res.json();
    } catch (e) {
      console.error('CUDA status error:', e);
    }
  }

  async function clearCache() {
    loading = true;
    try {
      const res = await fetch('/api/oasis/cuda/clear-cache', { method: 'POST' });
      const data = await res.json();
      alert(data.message || 'Cache cleared');
      await fetchStatus();
    } catch (e) {
      console.error('Clear cache error:', e);
    }
    loading = false;
  }

  async function setDevice(deviceId) {
    loading = true;
    try {
      await fetch('/api/oasis/cuda/set-device', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ device_id: deviceId })
      });
      await fetchStatus();
    } catch (e) {
      console.error('Set device error:', e);
    }
    loading = false;
  }

  onMount(() => {
    fetchStatus();
    interval = setInterval(fetchStatus, 5000);
  });

  onDestroy(() => {
    if (interval) clearInterval(interval);
  });
</script>

<div class="cuda-monitor ultron-card">
  <h2 class="ultron-text-glow">🎮 CUDA GPU Monitor</h2>

  {#if loading}
    <div class="loading ultron-pulse">Loading...</div>
  {/if}

  {#if cudaStatus}
    {#if cudaStatus.available}
      <div class="status-grid">
        <div class="stat-card ultron-card-hover">
          <h3>CUDA Version</h3>
          <p class="value">{cudaStatus.cuda_version}</p>
        </div>
        <div class="stat-card ultron-card-hover">
          <h3>cuDNN Version</h3>
          <p class="value">{cudaStatus.cudnn_version}</p>
        </div>
        <div class="stat-card ultron-card-hover">
          <h3>GPU Count</h3>
          <p class="value">{cudaStatus.device_count}</p>
        </div>
        <div class="stat-card ultron-card-hover">
          <h3>Active Device</h3>
          <p class="value">{cudaStatus.current_device}</p>
        </div>
      </div>

      <div class="devices">
        {#each cudaStatus.devices as device, i}
          <div class="device-card ultron-card-hover" class:active={i === cudaStatus.current_device}>
            <div class="device-header">
              <h3>GPU {device.id}: {device.name}</h3>
              <button on:click={() => setDevice(device.id)} class="ultron-button-sm">
                {i === cudaStatus.current_device ? '✓ Active' : 'Activate'}
              </button>
            </div>
            <div class="device-info">
              <p>Capability: {device.capability[0]}.{device.capability[1]}</p>
              <p>Total Memory: {device.memory.toFixed(2)} GB</p>
              <p>Allocated: {device.memory_allocated_gb} GB</p>
              <p>Reserved: {device.memory_reserved_gb} GB</p>
              <div class="memory-bar">
                <div 
                  class="memory-used" 
                  style="width: {(device.memory_allocated_gb / device.memory * 100).toFixed(1)}%"
                ></div>
              </div>
            </div>
          </div>
        {/each}
      </div>

      <div class="controls">
        <button on:click={clearCache} class="ultron-button">🗑️ Clear Cache</button>
        <button on:click={fetchStatus} class="ultron-button">🔄 Refresh</button>
      </div>
    {:else}
      <div class="no-cuda">
        <p>❌ CUDA not available</p>
        {#if cudaStatus.error}
          <p class="error">{cudaStatus.error}</p>
        {/if}
      </div>
    {/if}
  {/if}
</div>

<style>
  .cuda-monitor {
    padding: 1.5rem;
    max-width: 1200px;
    margin: 0 auto;
  }

  .status-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
  }

  .stat-card {
    padding: 1rem;
    background: rgba(5, 5, 5, 0.8);
    border: 1px solid #ff0000;
    text-align: center;
  }

  .stat-card h3 {
    color: #ff3333;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
  }

  .stat-card .value {
    color: #fff;
    font-size: 1.5rem;
    font-weight: bold;
  }

  .devices {
    display: grid;
    gap: 1rem;
    margin: 1.5rem 0;
  }

  .device-card {
    padding: 1.5rem;
    background: rgba(5, 5, 5, 0.8);
    border: 1px solid #ff0000;
    transition: all 0.3s;
  }

  .device-card.active {
    border-color: #00ff00;
    box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
  }

  .device-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }

  .device-header h3 {
    color: #ff3333;
    margin: 0;
  }

  .device-info p {
    color: #999;
    margin: 0.5rem 0;
  }

  .memory-bar {
    width: 100%;
    height: 20px;
    background: rgba(0, 0, 0, 0.5);
    border: 1px solid #ff0000;
    margin-top: 1rem;
    position: relative;
    overflow: hidden;
  }

  .memory-used {
    height: 100%;
    background: linear-gradient(90deg, #ff0000, #ff3333);
    transition: width 0.3s;
  }

  .controls {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
  }

  .ultron-button-sm {
    padding: 0.25rem 0.75rem;
    background: rgba(255, 0, 0, 0.1);
    border: 1px solid #ff0000;
    color: #ff3333;
    cursor: pointer;
    transition: all 0.3s;
  }

  .ultron-button-sm:hover {
    background: rgba(255, 0, 0, 0.2);
    box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
  }

  .no-cuda {
    text-align: center;
    padding: 2rem;
    color: #ff3333;
  }

  .error {
    color: #ff0000;
    margin-top: 1rem;
  }

  .loading {
    text-align: center;
    padding: 2rem;
    color: #ff3333;
  }
</style>
