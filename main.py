#! ~/.virtualenv/leaguekipedia python

import argparse
from commands.champion_command import ChampionCommand
from commands.search_command import SearchCommand


def main():
    command_parser = argparse.ArgumentParser()
    subparsers = command_parser.add_subparsers()

    champion_command = ChampionCommand()
    search_command = SearchCommand()
    for c in [champion_command, search_command]:
        c.add_command_to_subparser(subparsers)

    args = command_parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

