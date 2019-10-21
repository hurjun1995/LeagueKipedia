#! ~/Env/holololo python

import argparse, json, requests
from bs4 import BeautifulSoup


class Leagkipedia:
    soup = None
    champion_info_dict = None

    def __init__(self):
        self.champion_info_dict = self.get_official_champion_info()

    @staticmethod
    def get_official_champion_info():
        data = requests.get("http://ddragon.leagueoflegends.com/cdn/9.20.1/data/en_US/champion.json").text
        json_data = json.loads(data)
        champion_info_dict = json_data["data"]
        return champion_info_dict

    def is_valid_champion(self, champ_name):
        """check if given champion name exists in riot's official champion list"""
        champ_name = champ_name.lower()
        s = list(champ_name)
        s[0] = s[0].upper()
        champ_name = "".join(s)
        return champ_name in self.champion_info_dict

    def print_skill(self):
        spell_and_skill = self.soup.find_all('table')[2]
        skills = spell_and_skill.find_all('tbody')[1]
        skill_master_order = [skill.text for i, skill in enumerate(skills.find_all('span')) if i < 3]
        print("skill master order: ", ' -> '.join(skill_master_order))

    @staticmethod
    def print_counter():
        print("print counter: stub")

    @staticmethod
    def print_item():
        print("print item: stub")

    def handle_champion_command(self, args):
        champ_name = args.champion_name
        if not self.is_valid_champion(champ_name):
            print("'{champ}' is not existing champion name".format(champ=champ_name))
            return

        res = requests.get("https://na.op.gg/champion/{champ}/statistics/".format(champ=champ_name))
        self.soup = BeautifulSoup(res.content, features="html.parser").find('body')

        if not args.skill and not args.counter and not args.item:
            self.print_skill()
            self.print_item()
            self.print_counter()
        else:
            if args.skill:
                self.print_skill()
            if args.counter:
                self.print_counter()
            if args.item:
                self.print_counter()

    def main(self):
        command_parser = argparse.ArgumentParser("Leagkipedia: League of Legend cheat sheet")
        subparsers = command_parser.add_subparsers()

        champion_subparser = subparsers.add_parser("champion")
        champion_subparser.add_argument('champion_name', type=str, help="Name of the champion")
        champion_subparser.add_argument('-s', '--skill', action='store_true')
        champion_subparser.add_argument('-c', '--counter', action='store_true')
        champion_subparser.add_argument('-i', '--item', action='store_true')
        champion_subparser.set_defaults(func=self.handle_champion_command)

        args = command_parser.parse_args()
        args.func(args)

if __name__ == "__main__":
    Leagkipedia().main()
