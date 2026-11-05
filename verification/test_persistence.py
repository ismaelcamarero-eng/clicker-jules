import http.server
import socketserver
import threading
import os
import unittest
from playwright.sync_api import sync_playwright

PORT = 8124

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

class TestCookieClickerWithHttp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start local HTTP server to properly test standard HTTP cookie handling
        cls.repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        class CustomHandler(QuietHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=cls.repo_dir, **kwargs)

        socketserver.TCPServer.allow_reuse_address = True
        cls.httpd = socketserver.TCPServer(("", PORT), CustomHandler)
        cls.server_thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.server_thread.start()

        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)
        cls.url = f"http://localhost:{PORT}/index.html"

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def setUp(self):
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def tearDown(self):
        self.context.close()

    def test_cookie_persistence_and_trophy_restoration(self):
        """Clicks persist in browser cookie across reloads and restore unlocked trophies."""
        self.page.goto(self.url)
        # Advance to 10 clicks by clicking cookie 10 times
        for _ in range(10):
            self.page.locator('#cookie').click()

        self.assertEqual(self.page.locator('#counter').inner_text(), "10")
        self.assertIn("unlocked", self.page.locator('#trophy-10').get_attribute("class"))

        # Reload the page
        self.page.reload()
        self.assertEqual(self.page.locator('#counter').inner_text(), "10")
        self.assertIn("unlocked", self.page.locator('#trophy-10').get_attribute("class"))
        self.assertIn("locked", self.page.locator('#trophy-100').get_attribute("class"))
        self.assertIn("locked", self.page.locator('#trophy-1000').get_attribute("class"))

    def test_persistence_at_100_and_1000(self):
        """Reloading when counter is at 100 or 1000 properly preserves all unlocked trophies."""
        self.page.goto(self.url)
        self.page.evaluate("updateCounter(100)")
        self.page.reload()

        self.assertEqual(self.page.locator('#counter').inner_text(), "100")
        self.assertIn("unlocked", self.page.locator('#trophy-10').get_attribute("class"))
        self.assertIn("unlocked", self.page.locator('#trophy-100').get_attribute("class"))
        self.assertIn("locked", self.page.locator('#trophy-1000').get_attribute("class"))

        self.page.evaluate("updateCounter(1000)")
        self.page.reload()

        self.assertEqual(self.page.locator('#counter').inner_text(), "1000")
        self.assertIn("unlocked", self.page.locator('#trophy-10').get_attribute("class"))
        self.assertIn("unlocked", self.page.locator('#trophy-100').get_attribute("class"))
        self.assertIn("unlocked", self.page.locator('#trophy-1000').get_attribute("class"))

        # Resetting updates cookie to 0 and persists across reload
        self.page.locator('#reset').click()
        self.page.reload()
        self.assertEqual(self.page.locator('#counter').inner_text(), "0")
        self.assertIn("locked", self.page.locator('#trophy-10').get_attribute("class"))
        self.assertIn("locked", self.page.locator('#trophy-100').get_attribute("class"))
        self.assertIn("locked", self.page.locator('#trophy-1000').get_attribute("class"))

if __name__ == '__main__':
    unittest.main()
