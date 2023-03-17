import configparser

import requests.packages.urllib3
from .ChromeDriver import ChromeDriver

requests.packages.urllib3.disable_warnings()


class RecordNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class FileDownloader:
    def __init__(self, url, log_msg, date_format, file_date):
        self._url = url
        self._log_msg = log_msg
        self._date_format = date_format
        self._file_date = file_date
        self._driver = None
        self._driver_path = None

    def check_file(self):
        raise NotImplementedError("Implement checkFile Method")

    def download_file(self):
        raise NotImplementedError("Implement downloadFile Method")

    def main(self, cfg, request_time_out = None):
        print('Initialize...')
        config = configparser.ConfigParser()
        config.read(cfg)
        self._driver_path = config['DRIVER']['chromeDriver']

        try:
            print('Getting url %s ...' % self._url)
            self._driver = ChromeDriver(driver_path=self._driver_path)
            self._driver.get(self._url, request_time_out)
            response = self.check_file()
            if response:
                self.download_file()

        except:
            import traceback
            msg = '%s for %s cannot be downloaded. \n' % (self._log_msg, self._file_date.strftime(self._date_format))
            msg += '%s' % traceback.format_exc()
            print(msg)
            if isinstance(self._driver, ChromeDriver):
                self._driver.quit()
