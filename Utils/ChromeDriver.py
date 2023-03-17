from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# from pyvirtualdisplay import Display
import atexit


class ChromeDriver:
    def __init__(self, driver_path, prefs=None, display=True):
        self._driver_path = driver_path
        self._chrome_options = webdriver.ChromeOptions()
        self._chrome_options.add_argument('--no-sandbox')
        self._display = None
        if prefs:
            self._chrome_options.add_experimental_option('prefs', prefs)
        # if display:
        #     self._display = Display(visible=False, size=(1000, 800))
        #     self._display.start()
        self._driver = webdriver.Chrome(executable_path=self._driver_path, chrome_options=self._chrome_options)
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

    def find_element_by_xpath_selector(self, x_path, timeout=10):
        return WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((By.XPATH, x_path)))

    def find_element_by_css_selector(self, css_selector, timeout=10):
        return WebDriverWait(self._driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

    def click_button_by_id(self, element_id, timeout=10):
        print('Clicking the button ...')
        button = WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((By.ID, element_id)))
        button.click()

    def fill_text_field_by_name(self, element_name, text, timeout=10):
        print('Filling the field...')
        text_field = WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((By.NAME, element_name)))
        text_field.send_keys(Keys.CONTROL + "a")
        text_field.send_keys(Keys.DELETE)
        text_field.send_keys(text)
        text_field.click()






