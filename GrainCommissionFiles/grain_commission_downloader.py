# -*- coding: utf-8 -*-
__notes__ = "Go website http://www.grainscanada.gc.ca/statistics-statistiques/gsw-shg/gswm-mshg-eng.htm " \
            "and download files in links."

import configparser
import os
import requests
from bs4 import BeautifulSoup
import urllib

requests.packages.urllib3.disable_warnings()


class GrainCommissionDownloaderCAN:
    def __init__(self, config):
        print('Init Grain Commission Downloader..')
        self._data_root_path = config['PATH']['data_root_path']
        self._url = config['PATH']['url']
        self._years = config['PARAM']['years']

    @staticmethod
    def download(url, destination):
        print('Downloading %s ' % url)
        testfile = urllib.request.URLopener()
        testfile.retrieve(url, destination)

    def scraper(self):
        html = requests.get(self._url, verify=False).content
        soup = BeautifulSoup(html, 'html.parser')

        for link in soup.findAll('a'):
            if self._years in link['href']:
                download_url = self._url + link.get("href")
                f_name = download_url.split('/')[-1]
                f_name = f_name[:f_name.index('.')] + f_name[f_name.index('.'):]

                self.download(download_url, os.path.join(self._data_root_path, f_name))


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.cfg')
    downloader = GrainCommissionDownloaderCAN(config)
    downloader.scraper()
    print('Finish.')
