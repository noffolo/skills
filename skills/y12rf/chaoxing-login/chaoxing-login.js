const puppeteer = require('puppeteer-extra');
const stealthPlugin = require('puppeteer-extra-plugin-stealth');

puppeteer.use(stealthPlugin());

// 填入你的超星账号
const PHONE = 'your phone number';
const PASSWORD = 'password';

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--no-first-run',
      '--no-zygote',
      '--single-process',
      '--ignore-certificate-errors',
      '--ignore-certificate-errors-spki-list'
    ],
    protocolTimeout: 120000
  });
  
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
  
  try {
    await page.goto('https://passport2.chaoxing.com/login?fid=&newversion=true&refer=https%3A%2F%2Fi.chaoxing.com', { waitUntil: 'networkidle2', timeout: 30000 });
    
    await page.evaluate(({ phone, pwd }) => {
      const phoneInput = document.getElementById('phone');
      const pwdInput = document.getElementById('pwd');
      const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
      nativeInputValueSetter.call(phoneInput, phone);
      phoneInput.dispatchEvent(new Event('input', { bubbles: true }));
      nativeInputValueSetter.call(pwdInput, pwd);
      pwdInput.dispatchEvent(new Event('input', { bubbles: true }));
    }, { phone: PHONE, pwd: PASSWORD });
    
    await page.evaluate(() => {
      document.querySelector('.btn-big-blue')?.click();
    });
    
    await page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 30000 });
    
    // Click 课程 tab
    await page.evaluate(() => {
      const allElements = document.querySelectorAll('*');
      for (const el of allElements) {
        if (el.childNodes.length === 1 && el.textContent?.trim() === '课程') {
          el.click();
          break;
        }
      }
    });
    
    await new Promise(r => setTimeout(r, 5000));
    
    const frames = page.frames();
    const courseFrame = frames.find(f => f.url().includes('mooc1-2.chaoxing.com'));
    
    if (courseFrame) {
      const result = await courseFrame.evaluate(() => {
        const allElements = document.querySelectorAll('*');
        const results = [];
        for (const el of allElements) {
          if (el.textContent?.trim() === '国际贸易樊瑛-2026春季' || el.textContent?.trim().startsWith('国际贸易 ')) {
            let clickable = el;
            while (clickable && !clickable.href && clickable.tagName !== 'A') {
              clickable = clickable.parentElement;
            }
            results.push({
              text: el.textContent?.trim().substring(0, 50),
              tag: el.tagName,
              parentTag: clickable?.tagName,
              parentHref: clickable?.href,
              parentOnclick: clickable?.onclick
            });
          }
        }
        return results;
      });
      console.log('国际贸易 elements:', JSON.stringify(result, null, 2));
      
      if (result.length > 0 && result[0].parentHref) {
        console.log('Clicking:', result[0].parentHref);
        await courseFrame.goto(result[0].parentHref);
        await new Promise(r => setTimeout(r, 5000));
      }
    }
    
    await page.screenshot({ path: '/home/xiaochang/.openclaw/workspace/chaoxing-guomao.png', timeout: 60000 });
    console.log('Screenshot saved');
    console.log('Current URL:', page.url());
  } catch (e) {
    console.error('Error:', e.message);
  }
  
  await browser.close();
})();
