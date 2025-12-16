<script>
  import { onMount } from 'svelte';
  
  let command = '';
  let messages = [];
  let loading = false;

  async function executeCommand() {
    if (!command.trim()) return;
    
    loading = true;
    messages = [...messages, { role: 'user', content: command }];
    
    try {
      const res = await fetch('/api/oasis/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command })
      });
      
      const data = await res.json();
      messages = [...messages, { role: 'qasy', content: JSON.stringify(data, null, 2) }];
    } catch (error) {
      messages = [...messages, { role: 'error', content: error.message }];
    }
    
    command = '';
    loading = false;
  }

  onMount(async () => {
    const res = await fetch('/api/oasis/memory');
    const data = await res.json();
    messages = data.messages || [];
  });
</script>

<div class="qasy-chat ultron-glow">
  <div class="messages">
    {#each messages as msg}
      <div class="message {msg.role}">
        <strong>{msg.role}:</strong>
        <pre>{msg.content}</pre>
      </div>
    {/each}
  </div>
  
  <form on:submit|preventDefault={executeCommand}>
    <input
      bind:value={command}
      placeholder="Enter OASIS command..."
      disabled={loading}
      class="ultron-input"
    />
    <button type="submit" disabled={loading} class="ultron-button">
      {loading ? 'Processing...' : 'Execute'}
    </button>
  </form>
</div>

<style>
  .qasy-chat {
    display: flex;
    flex-direction: column;
    height: 100%;
    background: #0a0a0a;
    border: 1px solid rgba(255, 0, 0, 0.3);
    border-radius: 8px;
    padding: 1rem;
  }

  .messages {
    flex: 1;
    overflow-y: auto;
    margin-bottom: 1rem;
  }

  .message {
    margin: 0.5rem 0;
    padding: 0.5rem;
    border-left: 3px solid #ff0000;
    background: rgba(255, 0, 0, 0.05);
  }

  .message.user { border-left-color: #ff6666; }
  .message.qasy { border-left-color: #ff0000; }
  .message.error { border-left-color: #ff3333; background: rgba(255, 0, 0, 0.1); }

  pre {
    margin: 0.5rem 0 0 0;
    font-family: 'Exo 2', monospace;
    font-size: 0.9rem;
    color: #ff6666;
  }

  form {
    display: flex;
    gap: 0.5rem;
  }

  input {
    flex: 1;
    background: #1a1a1a;
    border: 1px solid rgba(255, 0, 0, 0.3);
    color: #ff6666;
    padding: 0.5rem;
    border-radius: 4px;
  }

  input:focus {
    outline: none;
    border-color: #ff0000;
    box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
  }

  button {
    background: linear-gradient(135deg, #1a0a0a, #2a1515);
    border: 1px solid #ff0000;
    color: #ff6666;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-family: 'Orbitron', sans-serif;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  button:hover:not(:disabled) {
    box-shadow: 0 0 20px rgba(255, 0, 0, 0.6);
    transform: translateY(-2px);
  }

  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style>
