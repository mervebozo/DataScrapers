# -*- coding: utf-8 -*-

import configparser
import datetime
import os
import time

from Utils.scraper import Scraper


class FileDownloaderNASA(Scraper):
    def __init__(self, config, url, log_message, date_format, file_date):
        super().__init__(config)
        self._url = url
        self._log_msg = log_message
        self._date_format = date_format
        self._file_date = file_date
        self._driverPath = config['DRIVER']['chromeDriver']
        self._download_dir_path = config['PATH']['dataRootPath']
        self._prefs = {'download.default_directory': self._download_dir_path,
                       'profile.default_content_settings.popups': 0}

    def request(self):
        try:
            self._driver.find_element_by_xpath_selector('//*[@id="button-download"]').click()
        except:
            print(self._log_msg + " could not be downloaded.")
            return True

        time.sleep(60)
        file_list = [name for name in os.listdir(self._download_dir_path) if name.endswith('.jpg')]
        if len(file_list) > 0:
            return True
        return False


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("config.cfg")

    today = datetime.datetime.now()
    dt = today.strftime("%Y-%m-%d")

    base_url = config['URL']['url']
    SEE = config['PATH']['rootFolderSEE']
    SPAIN = config['PATH']['rootFolderESP']
    ALPS = config['PATH']['rootFolderALPS']
    TURKEY = config['PATH']['rootFolderTR']

    year = str(today.year)
    regions = ['SEE', 'SPAIN', 'ALPS', 'TURKEY']

    for region in regions:
        print("Getting %s files for %s " % (region, dt))
        coords = config[region]['coords']
        url = base_url.format(dt, coords)
        scraper = FileDownloaderNASA(
            config=config,
            url=url,
            log_message='NASA ' + region + ' File',
            date_format="%Y-%m-%d",
            file_date=datetime.date.today())

        scraper.run_chrome_driver_once(60)


