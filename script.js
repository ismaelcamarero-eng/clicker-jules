const COOKIE_NAME = 'cookie_clicks';

function getCookie(name) {
  const matches = document.cookie.match(new RegExp('(?:^|; )' + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + '=([^;]*)'));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

function setCookie(name, value, days = 365) {
  const date = new Date();
  date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
  const expires = "; expires=" + date.toUTCString();
  document.cookie = `${name}=${encodeURIComponent(value || 0)}${expires}; path=/; SameSite=Lax`;
}

function loadInitialCount() {
  const saved = getCookie(COOKIE_NAME);
  if (saved !== undefined) {
    const parsed = parseInt(saved, 10);
    if (!isNaN(parsed) && parsed >= 0) {
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

// Initialize display with loaded count
counterEl.textContent = count;

cookieBtn.addEventListener('click', (event) => {
  updateCounter(count + 1);
  createClickEffect(event.clientX, event.clientY);
});

resetBtn.addEventListener('click', () => {
  updateCounter(0);
});
