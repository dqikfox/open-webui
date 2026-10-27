<script>
  import { onMount } from 'svelte';

  let messages = [];
  let input = '';
  let loading = false;
  let selectedModel = 'llama3';

  async function sendMessage() {
    if (!input.trim() || loading) return;
    
    const userMessage = { role: 'user', content: input };
    messages = [...messages, userMessage];
    
    const currentInput = input;
    input = '';
    loading = true;

    try {
      const res = await fetch('/api/oasis/ollama/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: selectedModel,
          messages: [...messages],
          use_functions: true
        })
      });

      const data = await res.json();
      
      if (data.response) {
        messages = [...messages, { role: 'assistant', content: data.response }];
      }
    } catch (e) {
      console.error('Chat error:', e);
      messages = [...messages, { role: 'assistant', content: 'Error: Could not connect to OASIS' }];
    }
    
    loading = false;
  }

  function handleKeyPress(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }
</script>

<div class="oasis-chat oasis-container">
  <div class="chat-header">
    <h2 class="oasis-text-glow">💬 OASIS Chat</h2>
    <select bind:value={selectedModel} class="model-selector oasis-input">
      <option value="llama3">Llama 3</option>
      <option value="qwen2.5">Qwen 2.5</option>
      <option value="mistral">Mistral</option>
    </select>
  </div>

  <div class="chat-messages">
    {#each messages as message}
      <div class="message message-{message.role}">
        <div class="message-content">
          {message.content}
        </div>
      </div>
    {/each}
    
    {#if loading}
      <div class="message message-assistant">
        <div class="message-content oasis-pulse">
          🤖 OASIS is thinking...
        </div>
      </div>
    {/if}
  </div>

  <div class="chat-input-container">
    <textarea
      bind:value={input}
      on:keypress={handleKeyPress}
      placeholder="Ask OASIS anything..."
      class="chat-input oasis-input"
      rows="3"
      disabled={loading}
    ></textarea>
    <button 
      on:click={sendMessage} 
      class="send-button oasis-button"
      disabled={loading || !input.trim()}
    >
      {loading ? '⏳' : '🚀'} Send
    </button>
  </div>
</div>

<style>
  .oasis-chat {
    max-width: 800px;
    margin: 2rem auto;
    height: 600px;
    display: flex;
    flex-direction: column;
  }

  .chat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border-bottom: 2px solid var(--oasis-primary);
  }

  .chat-header h2 {
    margin: 0;
    font-size: 1.5rem;
  }

  .model-selector {
    min-width: 150px;
  }

  .chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .message {
    max-width: 80%;
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid var(--oasis-primary);
  }

  .message-user {
    align-self: flex-end;
    background: linear-gradient(135deg, rgba(255, 0, 0, 0.2) 0%, rgba(255, 0, 0, 0.1) 100%);
    border-color: var(--oasis-secondary);
  }

  .message-assistant {
    align-self: flex-start;
    background: linear-gradient(135deg, rgba(10, 10, 10, 0.9) 0%, rgba(26, 10, 10, 0.9) 100%);
    border-color: var(--oasis-primary);
  }

  .message-content {
    color: #fff;
    line-height: 1.6;
    white-space: pre-wrap;
  }

  .chat-input-container {
    display: flex;
    gap: 1rem;
    padding: 1rem;
    border-top: 2px solid var(--oasis-primary);
  }

  .chat-input {
    flex: 1;
    resize: vertical;
    min-height: 60px;
  }

  .send-button {
    align-self: flex-end;
    white-space: nowrap;
  }

  .send-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  /* Custom scrollbar */
  .chat-messages::-webkit-scrollbar {
    width: 8px;
  }

  .chat-messages::-webkit-scrollbar-track {
    background: rgba(10, 10, 10, 0.5);
  }

  .chat-messages::-webkit-scrollbar-thumb {
    background: var(--oasis-primary);
    border-radius: 4px;
  }

  .chat-messages::-webkit-scrollbar-thumb:hover {
    background: var(--oasis-secondary);
  }
</style>