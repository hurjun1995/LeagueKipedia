from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests

from my_util import *


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

    def get_champ_name_no_space(self):
        return no_space_and_lower(self.champ_name)

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
