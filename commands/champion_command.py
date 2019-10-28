import json
import requests
from enum import Enum

from commands.command_base import CommandBase
from sub_commands.counter_sub_command import CounterSubCommand
from sub_commands.item_sub_command import ItemSubCommand
from sub_commands.skill_sub_command import SkillSubCommand
from my_util import *


class Lane(Enum):
    top = 'top'
    jg = 'jungle'
    mid = 'mid'
    bot = 'bot'
    sup = 'support'

    def __str__(self):
        return self.name


class ChampionCommand(CommandBase):
    champion_names_set = None
    champ_name = None
    champ_lane = None

    skill_sub_command = None
    counter_sub_command = None
    item_sub_command = None

    def __init__(self):
        self.champion_names_set = self.get_official_champion_names_set()
        self.skill_sub_command = SkillSubCommand()
        self.counter_sub_command = CounterSubCommand()
        self.item_sub_command = ItemSubCommand()

    def get_all_sub_commands(self):
        return [self.skill_sub_command, self.counter_sub_command, self.item_sub_command]

    def add_command_to_subparser(self, subparsers):
        champion_subparser = subparsers.add_parser("champion")
        champion_subparser.add_argument('champion_name', type=str, nargs='+', help="Name of the champion")
        champion_subparser.add_argument('lane', type=Lane, choices=list(Lane), help='Lane to which champion goes')

        for sc in self.get_all_sub_commands():
            sc.add_argument(champion_subparser)

        champion_subparser.set_defaults(func=self.run_command)

    @staticmethod
    def get_official_champion_names_set():
        data = requests.get("http://ddragon.leagueoflegends.com/cdn/9.20.1/data/en_US/champion.json").text
        json_data = json.loads(data)
        champion_names_set = {key.lower() for key in json_data["data"].keys()}
        return champion_names_set

    def is_valid_champion(self):
        """check if given champion name exists in riot's official champion list"""
        champ_name = self.champ_name.lower()
        champ_name = no_space_and_lower(self.champ_name)
        return champ_name in self.champion_names_set

    def run_command(self, args):
        self.champ_name = ' '.join(args.champion_name)
        self.champ_lane = args.lane.value
        for sc in self.get_all_sub_commands():
            sc.set_champ_info(self.champ_name, self.champ_lane)

        if not self.is_valid_champion():
            print("'{champ}' is not an existing champion name".format(champ=self.champ_name))
            return

        sub_commands_to_run = []
        if not args.skill and not args.counter and not args.item:
            sub_commands_to_run = self.get_all_sub_commands()
        else:
            if args.skill:
                sub_commands_to_run.append(self.skill_sub_command)
            if args.item:
                sub_commands_to_run.append(self.item_sub_command)
            if args.counter:
                sub_commands_to_run.append(self.counter_sub_command)

        print("information on: {champ} at {lane}".format(champ=self.champ_name, lane=self.champ_lane))
        for sc in sub_commands_to_run:
            sc.retrieve()
            sc.parse()
            sc.print()
