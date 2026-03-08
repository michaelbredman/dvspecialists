import puppeteer from '/Users/michaelredman/node_modules/puppeteer/lib/cjs/puppeteer/puppeteer.js';
import fs from 'fs';
import path from 'path';

const url = process.argv[2] || 'http://localhost:3000';
const label = process.argv[3] || '';

const dir = './temporary screenshots';
if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

// Find next available screenshot number
const existing = fs.readdirSync(dir).filter(f => f.startsWith('screenshot-') && f.endsWith('.png'));
let n = 1;
while (existing.includes(label ? `screenshot-${n}-${label}.png` : `screenshot-${n}.png`)) n++;
const filename = label ? `screenshot-${n}-${label}.png` : `screenshot-${n}.png`;
const outPath = path.join(dir, filename);

const browser = await puppeteer.launch({
  executablePath: '/Users/michaelredman/.cache/puppeteer/chrome/mac_arm-145.0.7632.77/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing',
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox'],
});

const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 2 });
await page.goto(url, { waitUntil: 'networkidle2' });
//await page.screenshot({ path: outPath, fullPage: true });
await page.screenshot({ path: outPath, clip: { x: 0, y: 0, width: 1440, height: 900 } });

await browser.close();

console.log(`Screenshot saved: ${outPath}`);
