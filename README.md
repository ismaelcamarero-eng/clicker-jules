# Cookie Clicker

A lightweight, responsive web application featuring a centered interactive chocolate chip cookie and a click counter.

## Features

- **Centered Cookie**: A realistic chocolate chip cookie rendered purely with modern CSS in the middle of the screen.
- **Click Counter**: Live count that increments every time the cookie is clicked.
- **Interactive Feedback**:
  - Tactile press animation when clicked or tapped.
  - Floating `+1` indicator spawned at the click position.
- **Accessible & Responsive**: Accessible button labeling, ARIA live region for screen readers, and fully responsive across mobile and desktop devices.
- **Reset Option**: Convenient button to reset the count back to 0.
- **Zero Dependencies**: Pure HTML, CSS, and vanilla JavaScript.

## How to Run

1. Open `index.html` directly in any modern web browser:
   - Double click `index.html` in your file explorer, or
   - Right-click `index.html` and choose **Open With** -> your preferred browser.

2. Alternatively, serve it locally with Python:
   ```bash
   python3 -m http.server 8000
   ```
   Then visit `http://localhost:8000` in your browser.
