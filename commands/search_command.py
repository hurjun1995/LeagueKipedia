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
        self.champions_stat_sub_command.set_user_name(args.username)
        self.champions_stat_sub_command.retrieve()
        self.champions_stat_sub_command.parse()
        self.champions_stat_sub_command.print()
