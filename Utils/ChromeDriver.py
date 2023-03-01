from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# from pyvirtualdisplay import Display
import atexit


class ChromeDriver:
    def __init__(self, driverPath, prefs=None, display=True):
        self._driverPath = driverPath
        self._chromeOptions = webdriver.ChromeOptions()
        self._chromeOptions.add_argument('--no-sandbox')
        self._display = None
        if prefs:
            self._chromeOptions.add_experimental_option('prefs', prefs)
        # if display:
        #     self._display = Display(visible=False, size=(1000, 800))
        #     self._display.start()
        self._driver = webdriver.Chrome(executable_path=self._driverPath, chrome_options=self._chromeOptions)
        global __call__
        __call__ = self
        atexit.register(self.quit)

    def get_driver(self):
        return self._driver

    def get(self, url, sec=None):
        print('Getting the url: %s...' % url)
        if sec:
            self._driver.set_page_load_timeout(sec)
            self._driver.get(url)
        else:
            self._driver.get(url)

    def close(self):
        print('Closing the driver...')
        self._driver.close()
        self.stop_display()

    def quit(self):
        print('Shutting down the driver...')
        self._driver.quit()
        self.stop_display()

    def stop_display(self):
        print('Stopping display...')
        if self._display:
            self._display.stop()

    def find_element_by_xPath_selector(self, xPath, timeout=10):
        return WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((By.XPATH, xPath)))








