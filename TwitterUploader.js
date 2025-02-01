const puppeteer = require('puppeteer');

async function runTwitterBot(username, password, tweet) {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  const page = await browser.newPage();

  try {
    console.log('Navigating to Twitter login...');
    await page.goto('https://twitter.com/login', { waitUntil: 'networkidle2' });

    // Enter username
    console.log('Typing username...');
    await page.waitForSelector('input[name="text"]', { timeout: 30000 });
    await page.type('input[name="text"]', username);

    // Click "Next"
    console.log('Clicking Next button...');
    await page.waitForSelector('button[role="button"][type="button"]', { timeout: 30000 });
    await page.evaluate(() => {
      const nextButton = [...document.querySelectorAll('button[role="button"][type="button"]')]
        .find((btn) => btn.innerText.trim() === 'Next');
      if (nextButton) nextButton.click();
      else throw new Error('Next button not found');
    });

    // Wait for password field
    console.log('Waiting for password field...');
    await page.waitForSelector('input[name="password"]', { timeout: 30000 });
    await page.type('input[name="password"]', password);

    // Click "Log in" button
    console.log('Clicking Log in button...');
    await page.waitForSelector('button[data-testid="LoginForm_Login_Button"]', { timeout: 30000 });
    await page.click('button[data-testid="LoginForm_Login_Button"]');

    // Wait for login navigation
    console.log('Waiting for login navigation...');
    await page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 60000 });

    console.log('Navigating to tweet composer...');
    await page.goto('https://x.com/compose/post', { waitUntil: 'networkidle2' });

    console.log('Ensuring tweet composer is ready...');
    await new Promise((resolve) => setTimeout(resolve, 2000)); // Small delay for dynamic rendering

    // Check for tweet box
    const tweetBoxExists = await page.$('div[role="textbox"][aria-label="Post text"]');
    if (!tweetBoxExists) {
      throw new Error('Tweet box not found!');
    }

    console.log('Tweet box found, typing...');
    await page.type('div[role="textbox"][aria-label="Post text"]', tweet);

    // Click "Post" button
    console.log('Clicking Post button...');
    await page.waitForSelector('button[data-testid="tweetButton"]', { timeout: 30000 });
    await new Promise((resolve) => setTimeout(resolve, 1000)); // Ensure button is clickable
    await page.click('button[data-testid="tweetButton"]');

    console.log('Verifying if tweet was posted...');
    await new Promise((resolve) => setTimeout(resolve, 5000)); // Wait for Twitter to process the tweet

    // Verify tweet was posted
    const tweetPosted = await page.$('div[data-testid="toast"]');
    if (tweetPosted) {
      console.log('Tweet posted successfully (verified).');
    } else {
      throw new Error('Tweet post not confirmed.');
    }
  } catch (error) {
    console.error('Error in Puppeteer bot:', error.message);
    // Take a screenshot for debugging
    await page.screenshot({ path: 'error_screenshot.png', fullPage: true });
    console.log('Screenshot saved as error_screenshot.png');
    throw error;
  } finally {
    await browser.close();
  }
}

module.exports = runTwitterBot;
