from sub_commands.sub_command_base import SubCommandBase


class CounterSubCommand(SubCommandBase):
    counter_champion_list = None

    def add_argument(self, subparser):
        subparser.add_argument('-c', '--counter', action='store_true',
                               help='include to see counter champions in the output')

    def retrieve(self):
        self.fetch_and_set_soup(f"https://na.op.gg/champion/{self.champ_name}/statistics/{self.champ_lane}/matchup?")

    def parse(self):
        self.counter_champion_list = self.soup.find_all("div", class_="champion-matchup-champion-list__item")
        self.counter_champion_list \
            .sort(key=lambda c: float(c.find('span', class_="champion-matchup-list__winrate").text.strip().strip('%')))

    def print(self):
        print("Counter Champions and win rate against them:")
        print("{:>12} {:>13} {:>14} {:>15}".format("index", "name", "win rate", "total played"))
        for i, champ in enumerate(self.counter_champion_list):
            name = champ.find('div', class_='champion-matchup-list__champion').find('span').text
            win_rate = champ.find('span', class_='champion-matchup-list__winrate').text.strip()
            total_played = champ.find('div', class_='champion-matchup-list__totalplayed').find('span').text
            print("{:>12} {:>13} {:>14} {:>15}".format(i, name, win_rate, total_played))
