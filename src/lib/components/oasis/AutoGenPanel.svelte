<script>
  import { onMount } from 'svelte';

  let suggestions = [];
  let analysis = null;
  let loading = false;
  let context = 'OASIS OASIS System';
  let selectedFile = '';
  let fileContent = '';
  let featureRequest = '';
  let implementation = null;
  let scanDirs = [
    '/home/ultro/projects/openui/oasis/backend/open_webui/qasy',
    '/home/ultro/projects/openui/oasis/src/lib/components/qasy'
  ];
  let improvements = [];
  let schedulerStatus = null;

  async function getSuggestions() {
    loading = true;
    try {
      const res = await fetch('/api/oasis/autogen/suggest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ context })
      });
      const data = await res.json();
      suggestions = data.suggestions || [];
    } catch (e) {
      console.error('Suggestion error:', e);
    }
    loading = false;
  }

  async function analyzeCode() {
    if (!selectedFile || !fileContent) return;
    loading = true;
    try {
      const res = await fetch('/api/oasis/autogen/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_path: selectedFile, content: fileContent })
      });
      analysis = await res.json();
    } catch (e) {
      console.error('Analysis error:', e);
    }
    loading = false;
  }

  async function implementFeature() {
    if (!featureRequest) return;
    loading = true;
    try {
      const res = await fetch('/api/oasis/autogen/implement', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ feature_request: featureRequest, file_context: {} })
      });
      implementation = await res.json();
    } catch (e) {
      console.error('Implementation error:', e);
    }
    loading = false;
  }

  async function runContinuous() {
    loading = true;
    try {
      const res = await fetch('/api/oasis/autogen/continuous', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scan_dirs: scanDirs })
      });
      const data = await res.json();
      improvements = data.improvements || [];
    } catch (e) {
      console.error('Continuous scan error:', e);
    }
    loading = false;
  }

  async function startScheduler() {
    loading = true;
    try {
      const res = await fetch('/api/oasis/autogen/scheduler/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scan_dirs: scanDirs })
      });
      schedulerStatus = await res.json();
    } catch (e) {
      console.error('Scheduler start error:', e);
    }
    loading = false;
  }

  async function stopScheduler() {
    loading = true;
    try {
      const res = await fetch('/api/oasis/autogen/scheduler/stop', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      schedulerStatus = await res.json();
    } catch (e) {
      console.error('Scheduler stop error:', e);
    }
    loading = false;
  }

  async function getSchedulerStatus() {
    try {
      const res = await fetch('/api/oasis/autogen/scheduler/status');
      schedulerStatus = await res.json();
    } catch (e) {
      console.error('Scheduler status error:', e);
    }
  }

  onMount(() => {
    getSuggestions();
    getSchedulerStatus();
  });
</script>

<div class="autogen-panel ultron-card">
  <h2 class="ultron-text-glow">AutoGen Studio</h2>
  
  <div class="tabs">
    <button on:click={() => getSuggestions()}>💡 Suggestions</button>
    <button on:click={() => analyzeCode()}>🔍 Analyze</button>
    <button on:click={() => implementFeature()}>🚀 Implement</button>
    <button on:click={() => runContinuous()}>🔄 Continuous</button>
  </div>

  {#if loading}
    <div class="loading ultron-pulse">Processing...</div>
  {/if}

  <div class="section">
    <h3>Enhancement Suggestions</h3>
    <input bind:value={context} placeholder="Context" class="ultron-input" />
    <button on:click={getSuggestions} class="ultron-button">Get Suggestions</button>
    
    {#if suggestions.length > 0}
      <div class="suggestions">
        {#each suggestions as s}
          <div class="suggestion-card ultron-card-hover">
            <h4>{s.title}</h4>
            <p>{s.description}</p>
            <span class="priority priority-{s.priority?.toLowerCase()}">{s.priority}</span>
            <p class="impl">{s.implementation}</p>
          </div>
        {/each}
      </div>
    {/if}
  </div>

  <div class="section">
    <h3>Code Analysis</h3>
    <input bind:value={selectedFile} placeholder="File path" class="ultron-input" />
    <textarea bind:value={fileContent} placeholder="Code content" class="ultron-input" rows="5"></textarea>
    <button on:click={analyzeCode} class="ultron-button">Analyze</button>
    
    {#if analysis}
      <div class="analysis ultron-card-hover">
        <pre>{JSON.stringify(analysis, null, 2)}</pre>
      </div>
    {/if}
  </div>

  <div class="section">
    <h3>Auto-Implement Feature</h3>
    <textarea bind:value={featureRequest} placeholder="Feature request" class="ultron-input" rows="3"></textarea>
    <button on:click={implementFeature} class="ultron-button">Implement</button>
    
    {#if implementation}
      <div class="implementation ultron-card-hover">
        {#if implementation.design}
          <div class="phase">
            <h4>🏗️ Architecture</h4>
            <pre>{implementation.design}</pre>
          </div>
        {/if}
        {#if implementation.implementation}
          <div class="phase">
            <h4>💻 Implementation</h4>
            <pre>{implementation.implementation}</pre>
          </div>
        {/if}
        {#if implementation.review}
          <div class="phase">
            <h4>✅ Review</h4>
            <pre>{implementation.review}</pre>
          </div>
        {/if}
      </div>
    {/if}
  </div>

  <div class="section">
    <h3>Continuous Improvement</h3>
    <div class="controls">
      <button on:click={runContinuous} class="ultron-button">Run Scan</button>
      <button on:click={startScheduler} class="ultron-button">Start Auto-Scan</button>
      <button on:click={stopScheduler} class="ultron-button">Stop Auto-Scan</button>
      <button on:click={getSchedulerStatus} class="ultron-button">Status</button>
    </div>
    {#if schedulerStatus}
      <div class="scheduler-status ultron-card-hover">
        <p>Running: {schedulerStatus.running ? '✅' : '❌'}</p>
        <p>Interval: {schedulerStatus.interval_minutes} minutes</p>
        <p>Last Run: {schedulerStatus.last_run || 'Never'}</p>
        <p>Total Runs: {schedulerStatus.total_runs}</p>
      </div>
    {/if}
    
    {#if improvements.length > 0}
      <div class="improvements">
        <div class="summary ultron-card-hover">
          <h4>Summary</h4>
          <p>{improvements[0]?.summary || 'Analysis complete'}</p>
        </div>
        <p>Found {improvements.length} improvements</p>
        {#each improvements as imp}
          <div class="improvement-card ultron-card-hover">
            <h4>{imp.file}</h4>
            <p>{imp.analysis?.substring(0, 200)}...</p>
            {#if imp.reviews}
              <div class="reviews">
                {#each imp.reviews as review}
                  <div class="review-item">
                    <strong>{review.agent}:</strong> {review.message?.substring(0, 100)}...
                  </div>
                {/each}
              </div>
            {/if}
          </div>
        {/each}
      </div>
    {/if}
  </div>
</div>

<style>
  .autogen-panel {
    padding: 1.5rem;
    max-width: 1200px;
    margin: 0 auto;
  }

  .tabs {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
  }

  .tabs button {
    padding: 0.5rem 1rem;
    background: rgba(255, 0, 0, 0.1);
    border: 1px solid #ff0000;
    color: #ff3333;
    cursor: pointer;
    transition: all 0.3s;
  }

  .tabs button:hover {
    background: rgba(255, 0, 0, 0.2);
    box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
  }

  .section {
    margin-bottom: 2rem;
    padding: 1rem;
    background: rgba(10, 10, 10, 0.5);
    border: 1px solid #ff0000;
  }

  .section h3 {
    color: #ff3333;
    margin-bottom: 1rem;
  }

  .suggestions, .improvements {
    display: grid;
    gap: 1rem;
    margin-top: 1rem;
  }

  .suggestion-card, .improvement-card {
    padding: 1rem;
    background: rgba(5, 5, 5, 0.8);
    border: 1px solid #ff0000;
  }

  .suggestion-card h4, .improvement-card h4 {
    color: #ff3333;
    margin-bottom: 0.5rem;
  }

  .priority {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
    margin: 0.5rem 0;
  }

  .priority-high {
    background: rgba(255, 0, 0, 0.3);
    color: #ff0000;
  }

  .priority-medium {
    background: rgba(255, 165, 0, 0.3);
    color: #ffa500;
  }

  .priority-low {
    background: rgba(0, 255, 0, 0.3);
    color: #00ff00;
  }

  .impl {
    font-size: 0.9rem;
    color: #999;
    margin-top: 0.5rem;
  }

  .analysis, .implementation {
    margin-top: 1rem;
    padding: 1rem;
    background: rgba(5, 5, 5, 0.9);
    border: 1px solid #ff0000;
    overflow-x: auto;
  }

  pre {
    color: #ff3333;
    font-size: 0.9rem;
  }

  .loading {
    text-align: center;
    padding: 2rem;
    color: #ff3333;
    font-size: 1.2rem;
  }

  .controls {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1rem;
    flex-wrap: wrap;
  }

  .scheduler-status {
    padding: 1rem;
    margin-top: 1rem;
    background: rgba(5, 5, 5, 0.8);
    border: 1px solid #ff0000;
  }

  .scheduler-status p {
    margin: 0.5rem 0;
    color: #ff3333;
  }

  .phase {
    margin: 1rem 0;
    padding: 1rem;
    background: rgba(10, 10, 10, 0.5);
    border-left: 3px solid #ff0000;
  }

  .phase h4 {
    color: #ff3333;
    margin-bottom: 0.5rem;
  }

  .reviews {
    margin-top: 1rem;
    padding: 0.5rem;
    background: rgba(0, 0, 0, 0.3);
  }

  .review-item {
    margin: 0.5rem 0;
    font-size: 0.9rem;
    color: #999;
  }

  .review-item strong {
    color: #ff3333;
  }

  .summary {
    margin-bottom: 1rem;
    padding: 1rem;
    background: rgba(255, 0, 0, 0.1);
    border: 2px solid #ff0000;
  }

  .summary h4 {
    color: #ff0000;
    margin-bottom: 0.5rem;
  }
</style>
