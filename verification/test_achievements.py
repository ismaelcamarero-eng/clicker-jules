import os
import unittest
from playwright.sync_api import sync_playwright

class TestCookieClickerAchievements(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)
        html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'index.html'))
        cls.file_url = f"file://{html_path}"

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        # Create a new browser context with clear cookies and storage for each test
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def tearDown(self):
        self.context.close()

    def _class_list(self, locator):
        return (locator.get_attribute("class") or "").split()

    def test_initial_state(self):
        """Initial state should have counter 0 and all 3 trophies locked."""
        self.page.goto(self.file_url)
        counter = self.page.locator('#counter')
        self.assertEqual(counter.inner_text(), "0")

        # Trophies exist
        t10 = self.page.locator('#trophy-10')
        t100 = self.page.locator('#trophy-100')
        t1000 = self.page.locator('#trophy-1000')

        self.assertTrue(t10.is_visible())
        self.assertTrue(t100.is_visible())
        self.assertTrue(t1000.is_visible())

        # Check all are locked
        self.assertIn("locked", self._class_list(t10))
        self.assertNotIn("unlocked", self._class_list(t10))
        self.assertEqual(t10.locator('.trophy-status').inner_text(), "LOCKED")

        self.assertIn("locked", self._class_list(t100))
        self.assertNotIn("unlocked", self._class_list(t100))
        self.assertEqual(t100.locator('.trophy-status').inner_text(), "LOCKED")

        self.assertIn("locked", self._class_list(t1000))
        self.assertNotIn("unlocked", self._class_list(t1000))
        self.assertEqual(t1000.locator('.trophy-status').inner_text(), "LOCKED")

    def test_unlock_10_clicks_trophy(self):
        """Clicking 10 times unlocks the Bronze trophy and displays notification."""
        self.page.goto(self.file_url)
        cookie = self.page.locator('#cookie')

        # Click 9 times -> still locked
        for _ in range(9):
            cookie.click()

        self.assertEqual(self.page.locator('#counter').inner_text(), "9")
        t10 = self.page.locator('#trophy-10')
        self.assertIn("locked", self._class_list(t10))

        # Click 10th time
        cookie.click()
        self.assertEqual(self.page.locator('#counter').inner_text(), "10")
        self.assertIn("unlocked", self._class_list(t10))
        self.assertNotIn("locked", self._class_list(t10))
        self.assertEqual(t10.locator('.trophy-status').inner_text(), "UNLOCKED")

        # Toast notification is shown with trophy info
        toast = self.page.locator('#achievement-toast')
        self.assertIn("show", self._class_list(toast))
        self.assertIn("Bronze Trophy (10 clicks)", self.page.locator('#achievement-toast-title').inner_text())

        # Other trophies remain locked
        t100 = self.page.locator('#trophy-100')
        t1000 = self.page.locator('#trophy-1000')
        self.assertIn("locked", self._class_list(t100))
        self.assertIn("locked", self._class_list(t1000))

    def test_unlock_100_clicks_trophy(self):
        """Simulate reaching 100 clicks unlocks Silver and Bronze trophies."""
        self.page.goto(self.file_url)
        # Advance to 99 clicks via script call
        self.page.evaluate("updateCounter(99)")
        t100 = self.page.locator('#trophy-100')
        self.assertIn("locked", self._class_list(t100))

        # Click cookie for 100th click
        self.page.locator('#cookie').click()
        self.assertEqual(self.page.locator('#counter').inner_text(), "100")
        self.assertIn("unlocked", self._class_list(t100))
        self.assertEqual(t100.locator('.trophy-status').inner_text(), "UNLOCKED")

        # Bronze is also unlocked
        t10 = self.page.locator('#trophy-10')
        self.assertIn("unlocked", self._class_list(t10))

        # Gold is still locked
        t1000 = self.page.locator('#trophy-1000')
        self.assertIn("locked", self._class_list(t1000))

        # Toast shows Silver Trophy
        self.assertIn("Silver Trophy (100 clicks)", self.page.locator('#achievement-toast-title').inner_text())

    def test_unlock_1000_clicks_trophy(self):
        """Simulate reaching 1000 clicks unlocks Gold trophy."""
        self.page.goto(self.file_url)
        # Advance to 999 clicks
        self.page.evaluate("updateCounter(999)")
        t1000 = self.page.locator('#trophy-1000')
        self.assertIn("locked", self._class_list(t1000))

        # Click cookie for 1000th click
        self.page.locator('#cookie').click()
        self.assertEqual(self.page.locator('#counter').inner_text(), "1000")
        self.assertIn("unlocked", self._class_list(t1000))
        self.assertEqual(t1000.locator('.trophy-status').inner_text(), "UNLOCKED")

        # Toast shows Gold Trophy
        self.assertIn("Gold Trophy (1000 clicks)", self.page.locator('#achievement-toast-title').inner_text())

        # All 3 trophies are unlocked
        self.assertIn("unlocked", self._class_list(self.page.locator('#trophy-10')))
        self.assertIn("unlocked", self._class_list(self.page.locator('#trophy-100')))
        self.assertIn("unlocked", self._class_list(self.page.locator('#trophy-1000')))

    def test_reset_counter_resets_trophies(self):
        """Clicking Reset Counter resets the count to 0 and re-locks trophies."""
        self.page.goto(self.file_url)
        # Advance to 1000 clicks (all unlocked)
        self.page.evaluate("updateCounter(1000)")
        self.assertIn("unlocked", self._class_list(self.page.locator('#trophy-10')))
        self.assertIn("unlocked", self._class_list(self.page.locator('#trophy-100')))
        self.assertIn("unlocked", self._class_list(self.page.locator('#trophy-1000')))

        # Click Reset button
        self.page.locator('#reset').click()
        self.assertEqual(self.page.locator('#counter').inner_text(), "0")

        # All trophies should now be locked
        self.assertIn("locked", self._class_list(self.page.locator('#trophy-10')))
        self.assertIn("locked", self._class_list(self.page.locator('#trophy-100')))
        self.assertIn("locked", self._class_list(self.page.locator('#trophy-1000')))

    def test_floating_text_on_cookie_click(self):
        """Clicking the cookie creates a floating +1 element."""
        self.page.goto(self.file_url)
        self.page.locator('#cookie').click()
        floating_elements = self.page.locator('.floating-text')
        self.assertGreaterEqual(floating_elements.count(), 1)
        self.assertEqual(floating_elements.first.inner_text(), "+1")

if __name__ == '__main__':
    unittest.main()
