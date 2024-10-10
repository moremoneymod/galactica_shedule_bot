import urllib.request
import requests
from bs4 import BeautifulSoup
import lxml

# url = 'https://galaxycollege.ru/students/schedule/'
# r = requests.get(url)
#
# soup = BeautifulSoup(r.text, 'html.parser')
# link = soup.find(name="a", attrs={"class": "mr-1 sf-link sf-link-theme sf-link-dashed"})
#
# file_link = "https://galaxycollege.ru" + link["href"]
#
# file = requests.get(file_link)
#
# with open("shedule.xls", 'wb') as f:
#     f.write(file.content)

import os


class Downloader:
    SCHEDULE_URL = "https://galaxycollege.ru/students/schedule/"

    def __init__(self, base_file_dir="documents"):
        current_path = os.path.dirname(os.path.abspath(__file__))
        self._base_file_dir = os.path.join(current_path, base_file_dir)

    def _get_links(self):
        r = requests.get(self.SCHEDULE_URL)
        soup = BeautifulSoup(r.text, 'html.parser')
        link1 = soup.findAll(name="a", attrs={"class": "mr-1 sf-link sf-link-theme sf-link-dashed"})[0]
        link2 = soup.findAll(name="a", attrs={"class": "mr-1 sf-link sf-link-theme sf-link-dashed"})[1]

        self.file_link1 = "https://galaxycollege.ru" + link1["href"]
        self.file_link2 = "https://galaxycollege.ru" + link2["href"]

    def _get_files(self):
        file1 = requests.get(self.file_link1)
        with open("files/schedule.xls", 'wb') as f:
            f.write(file1.content)
        file2 = requests.get(self.file_link2)
        with open("files/schedule_zaoch.xls", 'wb') as f:
            f.write(file2.content)

    def get_schedule(self):
        self._get_links()
        self._get_files()


downloader = Downloader()
downloader.get_schedule()
