import pyperclip
import re

from commands.command_base import CommandBase
from sub_commands.champions_stat_sub_command import ChampionsStatSubCommand


class SearchCommand(CommandBase):
    champions_stat_sub_command = None
    
    def __init__(self):
        self.champions_stat_sub_command = ChampionsStatSubCommand()

    def add_command_to_subparser(self, subparsers):
        search_subparser = subparsers.add_parser("search")
        self.champions_stat_sub_command.add_argument(search_subparser)
        search_subparser.set_defaults(func=self.run_command)

    def run_command(self, args):
        if args.username is not None:
            self.run_champions_stat_sub_command(' '.join(args.username))
        else:
            clipboard_text = pyperclip.paste()
            if clipboard_text is None:
                return
            else:
                user_name_set = set()
                for line in clipboard_text.split('\n'):
                    match = re.search(r'(.+)\sjoined the lobby', line)
                    if match is not None:
                        user_name_set.add(match.group(1))

                for user_name in user_name_set:
                    self.run_champions_stat_sub_command(user_name)

    def run_champions_stat_sub_command(self, user_name):
        self.champions_stat_sub_command.set_user_name(user_name)
        self.champions_stat_sub_command.retrieve()
        self.champions_stat_sub_command.parse()
        self.champions_stat_sub_command.print()
