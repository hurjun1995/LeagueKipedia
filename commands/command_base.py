from abc import ABC, abstractmethod


class CommandBase(ABC):

    @abstractmethod
    def add_command_to_subparser(self, subparsers):
        ...

    @abstractmethod
    def run_command(self):
        ...
