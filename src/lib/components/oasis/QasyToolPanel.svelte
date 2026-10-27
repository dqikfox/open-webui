<script>
  import { onMount } from 'svelte';
  
  let tools = [];
  let selectedTool = null;
  let params = {};
  let result = null;

  async function loadTools() {
    const res = await fetch('/api/oasis/tools');
    const data = await res.json();
    tools = data.tools || [];
  }

  async function executeTool() {
    if (!selectedTool) return;
    
    try {
      const res = await fetch(`/api/oasis/tool/${selectedTool}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ params })
      });
      result = await res.json();
    } catch (error) {
      result = { error: error.message };
    }
  }

  onMount(loadTools);
</script>

<div class="tool-panel ultron-glow">
  <h3>OASIS Tools</h3>
  
  <select bind:value={selectedTool} class="ultron-input">
    <option value={null}>Select a tool...</option>
    {#each tools as tool}
      <option value={tool.name}>{tool.name} - {tool.description}</option>
    {/each}
  </select>

  {#if selectedTool}
    <div class="params">
      <input
        bind:value={params.message}
        placeholder="Parameters (JSON or text)"
        class="ultron-input"
      />
      <button on:click={executeTool} class="ultron-button">Execute Tool</button>
    </div>
  {/if}

  {#if result}
    <div class="result">
      <h4>Result:</h4>
      <pre>{JSON.stringify(result, null, 2)}</pre>
    </div>
  {/if}
</div>

<style>
  .tool-panel {
    background: #0a0a0a;
    border: 1px solid rgba(255, 0, 0, 0.3);
    border-radius: 8px;
    padding: 1rem;
  }

  h3 {
    font-family: 'Orbitron', sans-serif;
    color: #ff6666;
    text-transform: uppercase;
    margin: 0 0 1rem 0;
  }

  select, input {
    width: 100%;
    background: #1a1a1a;
    border: 1px solid rgba(255, 0, 0, 0.3);
    color: #ff6666;
    padding: 0.5rem;
    border-radius: 4px;
    margin-bottom: 0.5rem;
  }

  .params {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-top: 1rem;
  }

  .result {
    margin-top: 1rem;
    padding: 1rem;
    background: rgba(255, 0, 0, 0.05);
    border-left: 3px solid #ff0000;
    border-radius: 4px;
  }

  h4 {
    font-family: 'Orbitron', sans-serif;
    color: #ff6666;
    margin: 0 0 0.5rem 0;
  }

  pre {
    font-family: 'Exo 2', monospace;
    color: #ff6666;
    font-size: 0.9rem;
  }
</style>
