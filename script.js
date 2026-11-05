const COOKIE_NAME = 'cookie_clicks';

const ACHIEVEMENTS = [
  {
    id: 'trophy-10',
    threshold: 10,
    name: 'Bronze Trophy',
    icon: '🥉'
  },
  {
    id: 'trophy-100',
    threshold: 100,
    name: 'Silver Trophy',
    icon: '🥈'
  },
  {
    id: 'trophy-1000',
    threshold: 1000,
    name: 'Gold Trophy',
    icon: '🥇'
  }
];

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
const toastEl = document.getElementById('achievement-toast');
const toastTitleEl = document.getElementById('achievement-toast-title');

let toastTimeout = null;

function showAchievementToast(achievement) {
  if (!toastEl || !toastTitleEl) return;
  toastTitleEl.textContent = `${achievement.name} (${achievement.threshold} clicks)`;
  toastEl.classList.add('show');

  if (toastTimeout) {
    clearTimeout(toastTimeout);
  }

  toastTimeout = setTimeout(() => {
    toastEl.classList.remove('show');
  }, 3000);
}

function checkAchievements(prevCount, newCount) {
  ACHIEVEMENTS.forEach((achievement) => {
    const card = document.getElementById(achievement.id);
    if (!card) return;

    const statusEl = card.querySelector('.trophy-status');
    const isUnlocked = newCount >= achievement.threshold;

    if (isUnlocked) {
      card.classList.remove('locked');
      card.classList.add('unlocked');
      if (statusEl) statusEl.textContent = 'Unlocked';

      // Check if newly unlocked during this click transition
      if (prevCount < achievement.threshold && newCount >= achievement.threshold) {
        showAchievementToast(achievement);
      }
    } else {
      card.classList.remove('unlocked');
      card.classList.add('locked');
      if (statusEl) statusEl.textContent = 'Locked';
    }
  });
}

function updateCounter(newVal) {
  const prevCount = count;
  count = newVal;
  counterEl.textContent = count;
  setCookie(COOKIE_NAME, count);
  checkAchievements(prevCount, count);
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

// Initialize display and achievements with loaded count
counterEl.textContent = count;
checkAchievements(0, count);

cookieBtn.addEventListener('click', (event) => {
  updateCounter(count + 1);
  createClickEffect(event.clientX, event.clientY);
});

resetBtn.addEventListener('click', () => {
  updateCounter(0);
});
