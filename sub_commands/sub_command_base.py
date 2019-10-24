from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests


class SubCommandBase(ABC):
    soup = None
    champ_name = None
    champ_lane = None
    user_name = None

    def set_champ_info(self, champ_name, champ_lane):
        self.champ_name = champ_name
        self.champ_lane = champ_lane

    def set_user_name(self, user_name):
        self.user_name = user_name

    def fetch_and_set_soup(self, url):
        res = requests.get(url)
        self.soup = BeautifulSoup(res.content, features="html.parser")

    @abstractmethod
    def add_argument(self, subparser):
        ...

    @abstractmethod
    def retrieve(self):
        ...

    @abstractmethod
    def parse(self):
        ...

    @abstractmethod
    def print(self):
        ...
