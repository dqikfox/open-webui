<script>
  import OasisChat from '$lib/components/oasis/OasisChat.svelte';
  import UltronBackground from '$lib/components/oasis/UltronBackground.svelte';
</script>

<svelte:head>
  <title>OASIS Chat - AI Conversation</title>
</svelte:head>

<UltronBackground />

<div class="chat-page">
  <div class="page-header">
    <h1 class="oasis-text-glow">🤖 OASIS AI Chat</h1>
    <p class="page-subtitle">
      Powered by multi-agent system with 20+ functions and tools
    </p>
  </div>

  <OasisChat />

  <div class="chat-features">
    <div class="feature-list">
      <div class="feature-item">
        <span class="feature-icon">🧠</span>
        <span>Multi-Agent Intelligence</span>
      </div>
      <div class="feature-item">
        <span class="feature-icon">🔧</span>
        <span>20+ Built-in Tools</span>
      </div>
      <div class="feature-item">
        <span class="feature-icon">⚡</span>
        <span>Function Calling</span>
      </div>
      <div class="feature-item">
        <span class="feature-icon">🎯</span>
        <span>Smart Context</span>
      </div>
    </div>
  </div>
</div>

<style>
  .chat-page {
    min-height: 100vh;
    padding: 2rem;
    background: linear-gradient(135deg, rgba(10, 10, 10, 0.95) 0%, rgba(26, 10, 10, 0.95) 100%);
  }

  .page-header {
    text-align: center;
    margin-bottom: 2rem;
  }

  .page-header h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
  }

  .page-subtitle {
    color: #ccc;
    font-size: 1.2rem;
    margin-bottom: 2rem;
  }

  .chat-features {
    max-width: 800px;
    margin: 2rem auto;
    padding: 2rem;
    background: rgba(10, 10, 10, 0.8);
    border: 2px solid var(--oasis-primary);
    border-radius: 15px;
    box-shadow: var(--oasis-glow);
  }

  .feature-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
  }

  .feature-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem;
    background: rgba(5, 5, 5, 0.8);
    border: 1px solid var(--oasis-primary);
    border-radius: 8px;
    color: #fff;
    transition: all 0.3s;
  }

  .feature-item:hover {
    background: rgba(255, 0, 0, 0.1);
    transform: translateY(-2px);
  }

  .feature-icon {
    font-size: 1.5rem;
  }
</style>