const puppeteer = require('puppeteer');
const path = require('path');

async function capture() {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const files = ['login.html', 'dashboard.html', 'integrations.html', 'stats.html'];
  
  for (const file of files) {
    const page = await browser.newPage();
    await page.setViewport({ width: 1400, height: 900 });
    
    const htmlPath = path.join(__dirname, file);
    await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });
    
    const pngPath = path.join(__dirname, 'captures', file.replace('.html', '.png'));
    await page.screenshot({ path: pngPath, fullPage: true });
    
    console.log(`Captured: ${file} -> ${pngPath}`);
    await page.close();
  }
  
  await browser.close();
}

capture().catch(console.error);