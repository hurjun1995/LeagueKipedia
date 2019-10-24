from sub_commands.sub_command_base import SubCommandBase


class ChampionsStatSubCommand(SubCommandBase):
    most_played_champs_info = {}

    def add_argument(self, subparser):
        subparser.add_argument('-u', '--username',
                               help='include to search one specific user')

    def retrieve(self):
        url = f'https://na.op.gg/summoner/userName={self.user_name}'
        self.fetch_and_set_soup(url)

    def parse(self):
        most_champion_table = self.soup \
            .find_all('div', class_='MostChampionContent')[1] \
            .find_all('div', class_='ChampionBox Ranked')

        for champ in most_champion_table:
            champ_name = champ.find('div', class_='Face')['title']
            average_cs = champ.find('div', class_='ChampionMinionKill').text.strip().split(' ', 1)[1]
            kda = champ.find('span', class_='KDA').text.split(':')[0]
            win_rate = champ.find('div', class_='WinRatio').text.strip()
            total_played = champ.find('div', class_='Title').text.split()[0]

            self.most_played_champs_info[champ_name] = {
                'average_cs': average_cs,
                'kda': kda,
                'win_rate': win_rate,
                'total_played': total_played
            }

    def print(self):
        print(f'Most 7 Champions played by user: {self.user_name}')
        print("{:>13} {:>10} {:>12} {:>6} {:>17}".format("name", "win rate", "tot played", "KDA",
                                                          "Avg cs(cs/min)"))
        for key in self.most_played_champs_info:
            info_dict = self.most_played_champs_info[key]
            print("{:>13} {:>10} {:>12} {:>6} {:>17}".format(key, info_dict['win_rate'],
                                                                     info_dict['total_played'],
                                                                     info_dict['kda'],
                                                                     info_dict['average_cs']))
