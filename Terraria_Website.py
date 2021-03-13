'''
All actions that may need to be taken envolving the Terraria website
- Pulling latest Server/game version
- Downloading the latest Server/Game Version
'''

import re
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


def request_headers(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    req = Request(url, headers={'User-Agent': user_agent})
    return req


# Get the page into a variable
def get_website(url):
    # user agent is needed, request fails without it
    with urlopen(request_headers(url)) as u:
        site = u.read().decode()
    return site


def find_a_href():
    url = 'http://terraria.org'
    site_info = get_website(url)
    soup = BeautifulSoup(site_info, 'html.parser')
    get_footer = soup.find(class_="page-footer")
    a_tags_in_footer = get_footer.find_all('a')
    a_tags_list = str(a_tags_in_footer).split(',')

    for a_tag in a_tags_list:
        if re.findall(r'terraria-server-\d{4}', a_tag):
            a_href = a_tag
            break

    return a_href


def get_version():
    """
    returns website version as string--
    Return Example: 'terraria-server-1411'
    """
    a_href = find_a_href()
    version_info = re.findall(r'terraria-server-\d{4}', a_href)

    return version_info[0]


def download_latest_version():
    a_href = find_a_href()
    root = 'http://terraria.org'
    start_of_link = a_href.find('"') + 1
    end_of_link = a_href.find('zip') + 3
    download_link = a_href[start_of_link:end_of_link]

    full_url = root + download_link
    version = get_version()

    with urlopen(request_headers(full_url)) as u:
        data = u.read()

    with open(version+'.zip', 'wb') as zip_file:
        zip_file.write(data)
