#! ~/Env/holololo python

import cmd
import requests
from bs4 import BeautifulSoup


class HololoShell(cmd.Cmd):
    intro = 'Welcome to the league of legend shell. Type help or ? to list commands.\n'
    prompt = '> '

    def do_skill(self, arg):
        print_skill(arg)


def print_skill(champ_name):
    r = requests.get("https://na.op.gg/champion/{champ}/statistics/mid".format(champ=champ_name))
    soup = BeautifulSoup(r.text, features="html.parser").find('body')
    spell_and_skill = soup.find_all('table')[2]
    skills = spell_and_skill.find_all('tbody')[1]
    skill_master_order = [skill.text for i, skill in enumerate(skills.find_all('span')) if i < 3]
    print("skill master order: ", ' -> '.join(skill_master_order))


def main():
    HololoShell().cmdloop()


if __name__ == "__main__":
    main()
