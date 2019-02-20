import os
import sys
from selenium.webdriver import Chrome
from selenium.webdriver.chrome import webdriver as chrome_webdriver

class DriverBuilder():
    def get_driver(self, headless=False):
        driver = self._get_chrome_driver(headless)
        driver.set_window_size(1400, 700)
        return driver

    def _get_chrome_driver(self, headless):
        chrome_options = chrome_webdriver.Options()

        if headless:
            chrome_options.add_argument("--headless")

        dir_path = os.path.dirname(os.path.realpath(__file__))
        driver_path = os.path.join(dir_path, "drivers/chromedriver")
        if sys.platform.startswith("win"):
            driver_path += ".exe"

        driver = Chrome(executable_path=driver_path, options=chrome_options)
        return driver
