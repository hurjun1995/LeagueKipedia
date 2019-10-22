#! ~/.virtualenv/leaguekipedia python

import argparse, json, requests
from bs4 import BeautifulSoup
from enum import Enum


class Lane(Enum):
    top = 'top'
    jg = 'jungle'
    mid = 'mid'
    bot = 'bot'
    sup = 'support'

    def __str__(self):
        return self.name


class LeagueKipedia:
    champion_info_dict = None
    champ_name = None
    champ_lane = None

    def __init__(self):
        self.champion_info_dict = self.get_official_champion_info()

    @staticmethod
    def get_official_champion_info():
        data = requests.get("http://ddragon.leagueoflegends.com/cdn/9.20.1/data/en_US/champion.json").text
        json_data = json.loads(data)
        champion_info_dict = json_data["data"]
        return champion_info_dict

    def is_valid_champion(self):
        """check if given champion name exists in riot's official champion list"""
        champ_name = self.champ_name.lower()
        s = list(champ_name)
        s[0] = s[0].upper()
        champ_name = "".join(s)
        return champ_name in self.champion_info_dict

    def print_skill(self):
        # fetch and parse information
        res = requests.get("https://na.op.gg/champion/{champ}/statistics/{lane}/skill?"
                           .format(champ=self.champ_name, lane=self.champ_lane))
        soup = BeautifulSoup(res.content, features="html.parser")
        skill_order_info_list = soup.find("div", class_="tabItem Content championLayout-skill") \
            .find('div', class_='champion-box-content') \
            .find_all('li', class_='champion-stats__filter__item')
        skill_order_info_list = skill_order_info_list[0:2]

        # print
        print("Skill Orders:")
        print("{:>12} {:>20} {:>12} {:>12}".format("index", "skill order", "win rate", "pick rate"))
        for i, skill_order_info in enumerate(skill_order_info_list):
            skill_order = ' -> '.join(
                [s.find('span').text for s in skill_order_info.find_all('li', class_='champion-stats__list__item')])
            # somehow class names are reversed for pick_rate and win_rate on op.gg
            win_rate = skill_order_info\
                .find('div', class_='champion-stats__filter_item_value--pickrate')\
                .find('b').text
            pick_rate = skill_order_info\
                .find('div', class_='champion-stats__filter_item_value--winrate')\
                .find('b').text
            print("{:>12} {:>20} {:>12} {:>12}".format(i, skill_order, win_rate, pick_rate))

    def print_counter(self):
        # fetch and parse information
        res = requests.get("https://na.op.gg/champion/{champ}/statistics/{lane}/matchup?"
                           .format(champ=self.champ_name, lane=self.champ_lane))
        soup = BeautifulSoup(res.content, features="html.parser")
        counter_champion_list = soup.find_all("div", class_="champion-matchup-champion-list__item")
        counter_champion_list \
            .sort(key=lambda c: float(c.find('span', class_="champion-matchup-list__winrate").text.strip().strip('%')))

        # print
        print("Counter Champions:")
        print("{:>12} {:>13} {:>14} {:>15}".format("index", "name", "win rate", "total played"))
        for i, champ in enumerate(counter_champion_list):
            name = champ.find('div', class_='champion-matchup-list__champion').find('span').text
            win_rate = champ.find('span', class_='champion-matchup-list__winrate').text.strip()
            total_played = champ.find('div', class_='champion-matchup-list__totalplayed').find('span').text
            print("{:>12} {:>13} {:>14} {:>15}".format(i, name, win_rate, total_played))

    def print_item(self):
        # fetch and parse information
        res = requests.get("https://na.op.gg/champion/{champ}/statistics/{lane}/item?"
                           .format(champ=self.champ_name, lane=self.champ_lane))
        soup = BeautifulSoup(res.content, features="html.parser")
        item_info_list_sorted = soup.find("div", class_="championLayout-item")\
            .find('div', class_='l-champion-statistics-content__side')\
            .find('tbody')\
            .find_all('tr')

        # print
        print("Recommended Items:")
        print("{:>12} {:>20} {:>12} {:>12}".format("index", "item name", "win rate", "pick rate"))
        for i, item_info in enumerate(item_info_list_sorted):
            if i < 10:
                name = item_info.find('span').text
                win_rate = item_info.find('td', class_='champion-stats__table__cell--winrate').text
                pick_rate = item_info\
                    .find('td', class_='champion-stats__table__cell--pickrate')\
                    .find(text=True).strip()
                print("{:>12} {:>20} {:>12} {:>12}".format(i, name, win_rate, pick_rate))
            else:
                break

    def handle_champion_command(self, args):
        self.champ_name = args.champion_name
        self.champ_lane = args.lane.value

        if not self.is_valid_champion():
            print("'{champ}' is not existing champion name".format(champ=self.champ_name))
            return

        print("information on: {champ} at {lane}".format(champ=self.champ_name, lane=self.champ_lane))
        if not args.skill and not args.counter and not args.item:
            self.print_skill()
            self.print_item()
            self.print_counter()
        else:
            if args.skill:
                self.print_skill()
            if args.item:
                self.print_item()
            if args.counter:
                self.print_counter()

    def main(self):
        command_parser = argparse.ArgumentParser()
        subparsers = command_parser.add_subparsers()

        champion_subparser = subparsers.add_parser("champion")
        champion_subparser.add_argument('champion_name', type=str, help="Name of the champion")
        champion_subparser.add_argument('lane', type=Lane, choices=list(Lane), help='Lane to which champion goes')
        champion_subparser.add_argument('-s', '--skill', action='store_true',
                                        help='include to see skill master order in the output')
        champion_subparser.add_argument('-c', '--counter', action='store_true',
                                        help='include to see counter champions in the output')
        champion_subparser.add_argument('-i', '--item', action='store_true',
                                        help='include to see item trees in the output')
        champion_subparser.set_defaults(func=self.handle_champion_command)

        args = command_parser.parse_args()
        args.func(args)


if __name__ == "__main__":
    LeagueKipedia().main()
