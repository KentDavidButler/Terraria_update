'''
All actions that may need to be taken envolving the Terraria website
- Pulling latest Server/game version
- Downloading the latest Server/Game Version
'''

import re
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import time
from selenium import webdriver


class TerrariaWebsite:
    def __init__(self):
        self.url = 'https://terraria.fandom.com/wiki/Server'
        self._siteVersion = ''
        self.site_version()

    def site_version(self):
        if (self._siteVersion == '') or (self._siteVersion is None):
            self.set_version()

        return self._siteVersion

    def set_version(self):
        """
        returns website version as string--
        Return Example: 'terraria-server-1411'
        """
        version_info = re.findall(r'terraria-server-\d{4}', self._find_a_href())

        self._siteVersion = version_info[0]

    def _request_headers(self):
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
        req = Request(self.url, headers={'User-Agent': user_agent})
        return req

    def _get_website(self):
        driver = webdriver.Chrome()
        driver.get(self.url)
        html = driver.page_source
        driver.quit()

        return html

    def _find_a_href(self):
        a_href = None
        site_info = self._get_website()
        soup = BeautifulSoup(site_info, 'html.parser')
        find_by_class = soup.find(class_="external text")
        a_tags = find_by_class.find_all('a')
        a_tags_list = str(a_tags).split(',')

        count = 0
        for a_tag in a_tags_list:
            count = count + 1
            print(f"{count}: {a_tag}")
            if re.findall(r'terraria-server-\d{4}', a_tag):
                a_href = a_tag
                break

        return a_href

    @staticmethod
    def driver_test():
        """ Selenium example"""
        driver = webdriver.Chrome('/path/to/chromedriver')  # Optional argument, if not specified will search path.
        driver.get('http://www.google.com/');
        time.sleep(5)  # Let the user actually see something!
        search_box = driver.find_element('q')
        search_box.send_keys('ChromeDriver')
        search_box.submit()
        time.sleep(5)  # Let the user actually see something!
        driver.quit()

    def download_latest_version(self):
        a_href = self._find_a_href()
        start_of_link = a_href.find('"') + 1
        end_of_link = a_href.find('zip') + 3
        download_link = a_href[start_of_link:end_of_link]

        full_url = self.url + download_link
        version = self.site_version()

        with urlopen(self._request_headers(full_url)) as u:
            data = u.read()

        with open(version+'.zip', 'wb') as zip_file:
            zip_file.write(data)
