import { test, expect } from '@playwright/test';

test.describe('OASIS Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    // Mock authentication
    await page.route('**/api/v1/auths/signin', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ token: 'mock-token', user: { id: 'test', email: 'test@example.com' } })
      });
    });
    
    // Mock OASIS status
    await page.route('**/api/oasis/status', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          agent: { status: 'active', active: true },
          memory: { messages: 5 }
        })
      });
    });
    
    // Mock Ollama models
    await page.route('**/ollama/api/tags', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          models: [
            { name: 'llama3:latest', size: 4700000000 },
            { name: 'deepseek-coder:latest', size: 776000000 }
          ]
        })
      });
    });
  });

  test('should load dashboard with stats', async ({ page }) => {
    await page.goto('/oasis');
    
    // Check if dashboard loads
    await expect(page.locator('h1')).toContainText('OASIS Control Center');
    
    // Check status indicator
    await expect(page.locator('.status-indicator')).toBeVisible();
    
    // Check stats cards
    await expect(page.locator('.stat-card')).toHaveCount(4);
  });

  test('should switch between tabs', async ({ page }) => {
    await page.goto('/oasis');
    
    // Click AutoGen tab
    await page.click('button:has-text("AutoGen")');
    await expect(page.locator('.dashboard-content')).toContainText('AutoGen');
    
    // Click Chat tab
    await page.click('button:has-text("Chat")');
    await expect(page.locator('.quick-chat-panel')).toBeVisible();
    
    // Click System tab
    await page.click('button:has-text("System")');
    await expect(page.locator('.system-monitor')).toBeVisible();
  });

  test('should execute commands in terminal', async ({ page }) => {
    await page.route('**/api/oasis/execute', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ status: 'success', message: 'Command executed' })
      });
    });
    
    await page.goto('/oasis');
    
    // Switch to terminal tab
    await page.click('button:has-text("Terminal")');
    
    // Type command
    await page.fill('.terminal-input', 'test command');
    await page.click('.execute-btn');
    
    // Check output
    await expect(page.locator('.command-output')).toBeVisible();
  });

  test('should send chat messages', async ({ page }) => {
    await page.route('**/ollama/api/generate', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ response: 'Hello! How can I help you?' })
      });
    });
    
    await page.goto('/oasis');
    
    // Switch to chat tab
    await page.click('button:has-text("Chat")');
    
    // Send message
    await page.fill('.message-input', 'Hello AI');
    await page.click('.send-btn');
    
    // Check message appears
    await expect(page.locator('.message.user')).toContainText('Hello AI');
    await expect(page.locator('.message.assistant')).toContainText('Hello! How can I help you?');
  });
});