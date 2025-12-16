<script>
  import { onMount } from 'svelte';

  let workflows = [];
  let selectedWorkflow = '';
  let params = {};
  let result = null;
  let loading = false;
  let taskId = null;

  const workflowParams = {
    code_review: ['file_path', 'content'],
    feature_dev: ['feature_request'],
    bug_fix: ['bug_description', 'code'],
    optimization: ['code'],
    security_audit: ['code']
  };

  async function loadWorkflows() {
    const res = await fetch('/api/oasis/workflow/list');
    const data = await res.json();
    workflows = data.workflows || [];
  }

  async function executeWorkflow() {
    if (!selectedWorkflow) return;
    loading = true;
    try {
      const res = await fetch('/api/oasis/workflow/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          workflow_type: selectedWorkflow,
          params
        })
      });
      result = await res.json();
      taskId = result.task_id;
    } catch (e) {
      console.error('Workflow error:', e);
    }
    loading = false;
  }

  async function checkStatus() {
    if (!taskId) return;
    const res = await fetch(`/api/oasis/workflow/status/${taskId}`);
    const status = await res.json();
    console.log('Status:', status);
  }

  onMount(() => {
    loadWorkflows();
  });
</script>

<div class="workflow-panel ultron-card">
  <h2 class="ultron-text-glow">⚙️ Agent Workflows</h2>

  <div class="workflow-select">
    <select bind:value={selectedWorkflow} class="ultron-input">
      <option value="">Select Workflow</option>
      {#each workflows as wf}
        <option value={wf}>{wf.replace('_', ' ').toUpperCase()}</option>
      {/each}
    </select>
  </div>

  {#if selectedWorkflow && workflowParams[selectedWorkflow]}
    <div class="params">
      {#each workflowParams[selectedWorkflow] as param}
        <div class="param-field">
          <label>{param.replace('_', ' ')}</label>
          {#if param.includes('content') || param.includes('code')}
            <textarea bind:value={params[param]} class="ultron-input" rows="5"></textarea>
          {:else}
            <input bind:value={params[param]} class="ultron-input" />
          {/if}
        </div>
      {/each}
    </div>

    <div class="actions">
      <button on:click={executeWorkflow} class="ultron-button" disabled={loading}>
        {loading ? '⏳ Running...' : '▶️ Execute'}
      </button>
      {#if taskId}
        <button on:click={checkStatus} class="ultron-button">📊 Check Status</button>
      {/if}
    </div>
  {/if}

  {#if result}
    <div class="result ultron-card-hover">
      <h3>Result</h3>
      <pre>{JSON.stringify(result, null, 2)}</pre>
    </div>
  {/if}
</div>

<style>
  .workflow-panel {
    padding: 1.5rem;
    max-width: 1000px;
    margin: 0 auto;
  }

  .workflow-select {
    margin: 1rem 0;
  }

  .params {
    display: grid;
    gap: 1rem;
    margin: 1.5rem 0;
  }

  .param-field label {
    display: block;
    color: #ff3333;
    margin-bottom: 0.5rem;
    text-transform: capitalize;
  }

  .actions {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
  }

  .result {
    margin-top: 1.5rem;
    padding: 1rem;
    background: rgba(5, 5, 5, 0.8);
    border: 1px solid #ff0000;
    max-height: 500px;
    overflow-y: auto;
  }

  .result h3 {
    color: #ff3333;
    margin-bottom: 1rem;
  }

  pre {
    color: #fff;
    font-size: 0.9rem;
    white-space: pre-wrap;
  }
</style>
