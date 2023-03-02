# -*- coding: utf-8 -*-
__description__ = "Agricultural commodities data scraper"
__notes__ = "Read website https://apps.fas.usda.gov/export-sales/wkHistData.htm and save data in links " \
            "All Wheat, Corn, Soybeans, Soybean Cake and Meal and All Upland Cotton."

import configparser
import requests
from bs4 import BeautifulSoup
import pandas as pd

requests.packages.urllib3.disable_warnings()


def scraper(url_base, url):
    link_names = ['All Wheat', 'Corn', 'Soybeans', 'Soybean Cake and Meal', 'All Upland Cotton']
    data = []

    for link_name in link_names:
        html = requests.get(url, verify=False).content
        soup = BeautifulSoup(html, 'html.parser')
        commodity_name = link_name.replace(' ', '')

        for link in soup.findAll('a', href=True, text=link_name):
            html = requests.get(url_base + link.get("href"), verify=False).content
            soup = BeautifulSoup(html, 'html.parser')
            line_count = 0
            for link_tr in soup.select('tr'):
                line_count += 1
                row = [commodity_name]
                if line_count > 4:
                    for link_td in link_tr.select('td'):
                        text = link_td.text
                        row.append(text)
                    if len(row) == 8:
                        data.append(row)

    df = pd.DataFrame(data)
    return df


def main():
    config = configparser.ConfigParser()
    config.read('config.cfg')
    url_base = config['PATH']['urlBase']
    url = config['PATH']['url']
    result = scraper(url_base, url)
    print(result)


if __name__ == '__main__':
    main()

