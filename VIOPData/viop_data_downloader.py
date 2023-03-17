# -*- coding: utf-8 -*-
import datetime
import time

from Utils.FileDownloader import FileDownloader


class VIOPDataDownloader(FileDownloader):
    def __init__(self, url, log_msg, date_format, file_date):
        super().__init__(url, log_msg, date_format, file_date)

    def check_file(self):
        return True

    def download_file(self):
        self._driver.find_element_by_xpath_selector('//*[@id="viopGunlukBulten"]/td[3]/button').click()
        time.sleep(3)  # must wait, ow download cannot be completed


if __name__ == '__main__':
    downloader = VIOPDataDownloader(
        url='https://www.borsaistanbul.com/tr/sayfa/482/bulten-ve-piyasa-verileri',
        log_msg='Vadeli islem ve opsiyon piyasası gunluk bulteni', date_format="%Y-%m-%d",
        file_date=datetime.date.today() + datetime.timedelta(days=-1))

    downloader.main("config.cfg")

