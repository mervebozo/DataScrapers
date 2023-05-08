from retrying import retry
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from Utils.ChromeDriver import ChromeDriver


def retryIfSpecificDriverException(exception):
    return isinstance(exception, TimeoutException) or isinstance(exception, NoSuchElementException) or isinstance(
        exception, StaleElementReferenceException) or isinstance(exception, ConnectionResetError)


class DataNAException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class Scraper:
    def __init__(self, config):
        self._url = config['URL']['url']
        self._appName = config['LOGGING']['appName']
        self._config = config
        self._driverPath = None
        self._prefs = None

    # open url and manipulate
    # check requested info is available in url
    def request(self):
        raise NotImplementedError("Implement request Method")

    @retry(retry_on_exception=retryIfSpecificDriverException, stop_max_attempt_number=3, wait_random_min=4000,
           wait_random_max=6000)
    def run_chrome_driver_once(self, requestTimeout=None):
        self._driver = ChromeDriver(driver_path=self._driverPath, prefs=self._prefs)
        self._driver.get(self._url, requestTimeout)
        response = self.request()
        if response:
            print('%s is executed.' % self._appName)
            return True
        else:
            msg = '%s cannot be executed. Data is not available.' % self._appName
            print(msg)
            return False




