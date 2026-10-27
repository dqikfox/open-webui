<script>
  export let size = 60;
  export let color = '#ff0000';
</script>

<div class="ultron-loader" style="--size: {size}px; --color: {color}">
  <div class="loader-ring"></div>
  <div class="loader-ring"></div>
  <div class="loader-ring"></div>
  <div class="loader-core"></div>
</div>

<style>
  .ultron-loader {
    position: relative;
    width: var(--size);
    height: var(--size);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .loader-ring {
    position: absolute;
    width: 100%;
    height: 100%;
    border: 3px solid transparent;
    border-top-color: var(--color);
    border-radius: 50%;
    animation: spin 1.5s cubic-bezier(0.5, 0, 0.5, 1) infinite;
  }

  .loader-ring:nth-child(1) {
    animation-delay: 0s;
    border-width: 3px;
  }

  .loader-ring:nth-child(2) {
    animation-delay: -0.5s;
    border-width: 2px;
    width: 80%;
    height: 80%;
  }

  .loader-ring:nth-child(3) {
    animation-delay: -1s;
    border-width: 2px;
    width: 60%;
    height: 60%;
  }

  .loader-core {
    width: 30%;
    height: 30%;
    background: radial-gradient(circle, var(--color), transparent);
    border-radius: 50%;
    animation: pulse 1.5s ease-in-out infinite;
    box-shadow: 0 0 20px var(--color), 0 0 40px var(--color);
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.6; transform: scale(1.2); }
  }
</style>
