<script>
  export let size = 'medium';
  export let color = '#ff0000';
</script>

<div class="spinner {size}" style="--color: {color}">
  <div class="bounce1"></div>
  <div class="bounce2"></div>
  <div class="bounce3"></div>
</div>

<style>
  .spinner {
    display: inline-flex;
    gap: 4px;
    align-items: center;
  }

  .spinner.small {
    transform: scale(0.5);
  }

  .spinner.medium {
    transform: scale(0.8);
  }

  .spinner.large {
    transform: scale(1.2);
  }

  .bounce1, .bounce2, .bounce3 {
    width: 8px;
    height: 8px;
    background-color: var(--color);
    border-radius: 100%;
    animation: sk-bouncedelay 1.4s infinite ease-in-out both;
  }

  .bounce1 {
    animation-delay: -0.32s;
  }

  .bounce2 {
    animation-delay: -0.16s;
  }

  @keyframes sk-bouncedelay {
    0%, 80%, 100% {
      transform: scale(0);
    } 40% {
      transform: scale(1.0);
    }
  }
</style>