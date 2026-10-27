<script>
  import { onMount } from 'svelte';

  export let selectedModel = '';
  
  let messages = [];
  let inputMessage = '';
  let loading = false;
  let chatContainer;

  async function sendMessage() {
    if (!inputMessage.trim() || !selectedModel) return;
    
    const userMessage = { role: 'user', content: inputMessage, timestamp: new Date() };
    messages = [...messages, userMessage];
    
    const prompt = inputMessage;
    inputMessage = '';
    loading = true;
    
    try {
      const res = await fetch('/ollama/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: selectedModel,
          prompt: prompt,
          stream: false
        })
      });
      
      const result = await res.json();
      const assistantMessage = { 
        role: 'assistant', 
        content: result.response, 
        timestamp: new Date(),
        model: selectedModel
      };
      messages = [...messages, assistantMessage];
    } catch (e) {
      const errorMessage = { 
        role: 'error', 
        content: `Error: ${e.message}`, 
        timestamp: new Date() 
      };
      messages = [...messages, errorMessage];
    }
    
    loading = false;
    scrollToBottom();
  }

  function scrollToBottom() {
    setTimeout(() => {
      if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
      }
    }, 100);
  }

  function clearChat() {
    messages = [];
  }

  function formatTime(timestamp) {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  onMount(() => {
    scrollToBottom();
  });
</script>

<div class="quick-chat-panel">
  <div class="chat-header">
    <h3>🚀 Quick Chat</h3>
    <div class="chat-controls">
      <span class="model-info">Model: {selectedModel || 'None'}</span>
      <button class="clear-btn" on:click={clearChat} disabled={messages.length === 0}>
        🗑️ Clear
      </button>
    </div>
  </div>

  <div class="chat-messages" bind:this={chatContainer}>
    {#each messages as message}
      <div class="message {message.role}">
        <div class="message-header">
          <span class="role-badge {message.role}">
            {#if message.role === 'user'}👤 You
            {:else if message.role === 'assistant'}🤖 {message.model || 'AI'}
            {:else}⚠️ Error{/if}
          </span>
          <span class="timestamp">{formatTime(message.timestamp)}</span>
        </div>
        <div class="message-content">
          {message.content}
        </div>
      </div>
    {/each}
    
    {#if loading}
      <div class="message assistant loading">
        <div class="message-header">
          <span class="role-badge assistant">🤖 {selectedModel}</span>
          <span class="timestamp">Thinking...</span>
        </div>
        <div class="message-content">
          <div class="typing-indicator">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>
    {/if}
  </div>

  <div class="chat-input">
    <input 
      type="text" 
      bind:value={inputMessage} 
      placeholder={selectedModel ? "Type your message..." : "Select a model first"}
      disabled={!selectedModel || loading}
      class="message-input"
      on:keydown={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage()}
    />
    <button 
      class="send-btn ultron-button" 
      on:click={sendMessage}
      disabled={!inputMessage.trim() || !selectedModel || loading}
    >
      {loading ? '⏳' : '📤'} Send
    </button>
  </div>
</div>

<style>
  .quick-chat-panel {
    background: rgba(5, 5, 5, 0.9);
    border: 2px solid #ff0000;
    border-radius: 10px;
    padding: 1.5rem;
    height: 600px;
    display: flex;
    flex-direction: column;
  }

  .chat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #ff0000;
  }

  .chat-header h3 {
    color: #ff3333;
    margin: 0;
  }

  .chat-controls {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .model-info {
    color: #fff;
    font-size: 0.9rem;
    background: rgba(255, 0, 0, 0.1);
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    border: 1px solid #ff0000;
  }

  .clear-btn {
    background: rgba(255, 0, 0, 0.2);
    border: 1px solid #ff0000;
    color: #ff3333;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.8rem;
    transition: all 0.3s;
  }

  .clear-btn:hover:not(:disabled) {
    background: rgba(255, 0, 0, 0.3);
    box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
  }

  .clear-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 1rem 0;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .message {
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid;
    animation: fadeIn 0.3s ease-out;
  }

  .message.user {
    background: rgba(0, 100, 255, 0.1);
    border-color: #0066ff;
    margin-left: 2rem;
  }

  .message.assistant {
    background: rgba(0, 255, 0, 0.1);
    border-color: #00ff00;
    margin-right: 2rem;
  }

  .message.error {
    background: rgba(255, 0, 0, 0.1);
    border-color: #ff0000;
  }

  .message.loading {
    opacity: 0.8;
  }

  .message-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }

  .role-badge {
    font-weight: bold;
    font-size: 0.9rem;
  }

  .role-badge.user {
    color: #0066ff;
  }

  .role-badge.assistant {
    color: #00ff00;
  }

  .role-badge.error {
    color: #ff0000;
  }

  .timestamp {
    font-size: 0.8rem;
    color: #999;
  }

  .message-content {
    color: #fff;
    line-height: 1.5;
    white-space: pre-wrap;
  }

  .typing-indicator {
    display: flex;
    gap: 4px;
    align-items: center;
  }

  .typing-indicator span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #00ff00;
    animation: typing 1.4s infinite ease-in-out;
  }

  .typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
  .typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

  @keyframes typing {
    0%, 80%, 100% { transform: scale(0); opacity: 0.5; }
    40% { transform: scale(1); opacity: 1; }
  }

  .chat-input {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #ff0000;
  }

  .message-input {
    flex: 1;
    padding: 0.75rem;
    background: rgba(10, 10, 10, 0.9);
    border: 1px solid #ff0000;
    border-radius: 5px;
    color: #fff;
    font-size: 1rem;
    resize: none;
  }

  .message-input:focus {
    outline: none;
    box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
  }

  .message-input:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .send-btn {
    padding: 0.75rem 1.5rem;
    white-space: nowrap;
  }

  .send-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }

  /* Scrollbar styling */
  .chat-messages::-webkit-scrollbar {
    width: 8px;
  }

  .chat-messages::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 4px;
  }

  .chat-messages::-webkit-scrollbar-thumb {
    background: rgba(255, 0, 0, 0.5);
    border-radius: 4px;
  }

  .chat-messages::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 0, 0, 0.7);
  }
</style>