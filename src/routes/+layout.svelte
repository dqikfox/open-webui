<script>
  import '../app.css';
  import { onMount } from 'svelte';

  let showAtlasDashboard = false;

  onMount(() => {
    // Add ATLAS dashboard toggle
    const toggleBtn = document.createElement('button');
    toggleBtn.innerHTML = '🌟 ATLAS';
    toggleBtn.className = 'atlas-toggle-btn';
    toggleBtn.onclick = () => showAtlasDashboard = !showAtlasDashboard;
    
    // Add to header if exists
    const header = document.querySelector('header') || document.querySelector('nav') || document.body;
    header.appendChild(toggleBtn);
  });
</script>

<main>
  <slot />
  
  {#if showAtlasDashboard}
    <div class="atlas-overlay">
      <div class="atlas-modal">
        <button class="close-btn" on:click={() => showAtlasDashboard = false}>✕</button>
        {#await import('$lib/components/atlas/AtlasDashboard.svelte')}
          <div class="loading">Loading ATLAS...</div>
        {:then { default: AtlasDashboard }}
          <AtlasDashboard />
        {/await}
      </div>
    </div>
  {/if}
</main>

<style>
  :global(.atlas-toggle-btn) {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1000;
    padding: 0.75rem 1.5rem;
    background: linear-gradient(135deg, #00ffff, #00cccc);
    border: 2px solid #33ffff;
    color: white;
    border-radius: 25px;
    cursor: pointer;
    font-weight: bold;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
    transition: all 0.3s;
  }

  :global(.atlas-toggle-btn:hover) {
    transform: scale(1.1);
    box-shadow: 0 0 30px rgba(0, 255, 255, 0.8);
  }

  .atlas-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.9);
    backdrop-filter: blur(10px);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
  }

  .atlas-modal {
    position: relative;
    max-width: 95vw;
    max-height: 95vh;
    overflow-y: auto;
    border-radius: 15px;
    box-shadow: 0 0 50px rgba(0, 255, 255, 0.5);
  }

  .close-btn {
    position: absolute;
    top: 15px;
    right: 15px;
    z-index: 10000;
    background: rgba(0, 255, 255, 0.8);
    border: none;
    color: white;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    cursor: pointer;
    font-size: 1.2rem;
    font-weight: bold;
    transition: all 0.3s;
  }

  .close-btn:hover {
    background: #00ffff;
    transform: scale(1.1);
  }

  .loading {
    padding: 4rem;
    text-align: center;
    color: #33ffff;
    font-size: 1.5rem;
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 1; }
  }
</style>