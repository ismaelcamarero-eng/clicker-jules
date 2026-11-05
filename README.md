# Cookie Clicker

A lightweight, responsive web application featuring a centered interactive chocolate chip cookie, a click counter, and cookie-based persistence with client-side protections.

## Features

- **Centered Cookie**: A realistic chocolate chip cookie rendered purely with modern CSS in the middle of the screen.
- **Click Counter**: Live count that increments every time the cookie is clicked.
- **Persistence with Cookies**: The click counter is stored in a browser cookie (`cookie_clicks`), preserving your score across page reloads and sessions.
- **Separation of Concerns**: HTML markup and layout in `index.html`, and application logic organized cleanly in `script.js`.
- **Client-Side Deterrents**:
  - Right-click context menu disabled to prevent casual inspection.
  - Keyboard shortcuts for opening developer tools (F12, Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+Shift+C, Ctrl+U) intercepted and prevented.
  - Checksum cookie (`cookie_clicks_hash`) validation to detect and handle manual cookie value tampering.
  - *Note:* Client-side protections are deterrence mechanisms; robust security for critical data should always be enforced on an authoritative server.
- **Interactive Feedback**:
  - Tactile press animation when clicked or tapped.
  - Floating `+1` indicator spawned at the click position.
- **Accessible & Responsive**: Accessible button labeling, ARIA live region for screen readers, and fully responsive across mobile and desktop devices.
- **Reset Option**: Convenient button to reset the count back to 0.
- **Zero Dependencies**: Pure HTML, CSS, and vanilla JavaScript.

## Project Structure

- `index.html` — The markup and styling for the page, cookie, and counter layout.
- `script.js` — The client-side logic handling click events, animations, cookie persistence, and client-side protection handlers.
- `README.md` — Project documentation.

## How to Run

1. Open `index.html` directly in any modern web browser:
   - Double click `index.html` in your file explorer, or
   - Right-click `index.html` and choose **Open With** -> your preferred browser.

2. Alternatively, serve it locally with Python (recommended for browser cookie handling):
   ```bash
   python3 -m http.server 8000
   ```
   Then visit `http://localhost:8000` in your browser.
