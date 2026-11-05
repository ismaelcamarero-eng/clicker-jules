const COOKIE_NAME = 'cookie_clicks';
const COOKIE_HASH = 'cookie_clicks_hash';

// Simple client-side hash / checksum to deter casual tampering with cookie values
function simpleHash(val) {
  let hash = 0;
  const str = String(val) + '_salt_cookie_clicker_secure_';
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = (hash << 5) - hash + char;
    hash |= 0;
  }
  return String(hash);
}

function getCookie(name) {
  const matches = document.cookie.match(new RegExp('(?:^|; )' + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + '=([^;]*)'));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

function setCookie(name, value, days = 365) {
  const date = new Date();
  date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
  const expires = "; expires=" + date.toUTCString();
  document.cookie = `${name}=${encodeURIComponent(value)}${expires}; path=/; SameSite=Lax`;
}

function loadInitialCount() {
  const saved = getCookie(COOKIE_NAME);
  const hash = getCookie(COOKIE_HASH);

  if (saved !== undefined) {
    const parsed = parseInt(saved, 10);
    // Validate value and checksum
    if (!isNaN(parsed) && parsed >= 0 && hash === simpleHash(parsed)) {
      return parsed;
    }
  }
  return 0;
}

let count = loadInitialCount();
const counterEl = document.getElementById('counter');
const cookieBtn = document.getElementById('cookie');
const cookieWrapper = document.getElementById('cookie-wrapper');
const resetBtn = document.getElementById('reset');

function updateCounter(newVal) {
  count = newVal;
  counterEl.textContent = count;
  setCookie(COOKIE_NAME, count);
  setCookie(COOKIE_HASH, simpleHash(count));
}

function createClickEffect(x, y) {
  const text = document.createElement('span');
  text.className = 'floating-text';
  text.textContent = '+1';

  if (x !== undefined && y !== undefined) {
    const rect = cookieWrapper.getBoundingClientRect();
    text.style.left = `${x - rect.left}px`;
    text.style.top = `${y - rect.top}px`;
  } else {
    text.style.left = '50%';
    text.style.top = '40%';
  }

  cookieWrapper.appendChild(text);

  text.addEventListener('animationend', () => {
    text.remove();
  });
}

// Initialize display with loaded count and ensure hash cookie is valid
updateCounter(count);

cookieBtn.addEventListener('click', (event) => {
  updateCounter(count + 1);
  createClickEffect(event.clientX, event.clientY);
});

resetBtn.addEventListener('click', () => {
  updateCounter(0);
});

// Client-side deterrence against casual inspection / developer tools opening
// 1. Disable context menu (right click)
document.addEventListener('contextmenu', (event) => {
  event.preventDefault();
});

// 2. Disable F12 and common DevTools shortcuts (Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+Shift+C, Ctrl+U)
document.addEventListener('keydown', (event) => {
  // F12
  if (event.key === 'F12' || event.keyCode === 123) {
    event.preventDefault();
    return false;
  }

  // Ctrl+Shift+I / Cmd+Option+I (Inspect), Ctrl+Shift+J / Cmd+Option+J (Console), Ctrl+Shift+C (Element picker)
  if ((event.ctrlKey || event.metaKey) && event.shiftKey && (['I', 'i', 'J', 'j', 'C', 'c'].includes(event.key) || [73, 74, 67].includes(event.keyCode))) {
    event.preventDefault();
    return false;
  }

  // Ctrl+U / Cmd+Option+U (View Source)
  if ((event.ctrlKey || event.metaKey) && (event.key === 'u' || event.key === 'U' || event.keyCode === 85)) {
    event.preventDefault();
    return false;
  }
});
