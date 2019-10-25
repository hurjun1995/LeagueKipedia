from sub_commands.sub_command_base import SubCommandBase


class ChampionsStatSubCommand(SubCommandBase):
    most_played_champs_info = {}
    recent_games_info = {}

    def add_argument(self, subparser):
        subparser.add_argument('-u', '--username', nargs='+',
                               help='include to search one specific user')

    def retrieve(self):
        url = f'https://na.op.gg/summoner/userName={self.user_name}'
        self.fetch_and_set_soup(url)

    def _parse_most_played_champions(self):
        most_champion_table = self.soup \
            .find_all('div', class_='MostChampionContent')[1] \
            .find_all('div', class_='ChampionBox Ranked')

        for champ in most_champion_table:
            champ_name = champ.find('div', class_='Face')['title']
            average_cs = champ.find('div', class_='ChampionMinionKill').text.strip().split(' ', 1)[1]
            kda_ratio = champ.find('span', class_='KDA').text.split(':')[0]
            win_rate = champ.find('div', class_='WinRatio').text.strip()
            total_played = champ.find('div', class_='Title').text.split()[0]

            self.most_played_champs_info[champ_name] = {
                'average_cs': average_cs,
                'kda_ratio': kda_ratio,
                'win_rate': win_rate,
                'total_played': total_played
            }

    def _parse_recent_games(self):
        ten_recent_games_table = self.soup.find('div', class_='GameItemList').find_all('div', class_='GameItemWrap')
        for i, game in enumerate(ten_recent_games_table):
            game_result = game.find('div', class_='GameResult').text.strip()
            champ_played = game.find('div', class_='ChampionName').find('a').text
            kda_ratio = game.find('span', class_='KDARatio').text.split(':')[0]
            kill = game.find('span', class_='Kill').text
            death = game.find('span', class_='Death').text
            assist = game.find('span', class_='Assist').text

            self.recent_games_info[i] = {
                'game_result': game_result,
                'champ_played': champ_played,
                'kda_ratio': kda_ratio,
                'kda': f'{kill}/{death}/{assist}'
            }

    def parse(self):
        self._parse_most_played_champions()
        self._parse_recent_games()

    def _print_most_played_champions(self):
        print(f'7 champions most played by: {self.user_name}')
        print("{:>13} {:>10} {:>12} {:>6} {:>17}".format("name", "win rate", "tot played", "KDA",
                                                         "Avg cs(cs/min)"))
        for key in self.most_played_champs_info:
            info_dict = self.most_played_champs_info[key]
            print("{:>13} {:>10} {:>12} {:>6} {:>17}".format(key,
                                                             info_dict['win_rate'],
                                                             info_dict['total_played'],
                                                             info_dict['kda_ratio'],
                                                             info_dict['average_cs']))

    def _print_recent_games(self):
        print(f'10 recent games played by: {self.user_name}')
        print("{:>12} {:>13} {:>10} {:>10}".format("game result", "champ played", "K/D/A", "KDA ratio"))

        for key in self.recent_games_info:
            info_dict = self.recent_games_info[key]
            print("{:>12} {:>13} {:>10} {:>10}".format(info_dict['game_result'], info_dict['champ_played'], info_dict['kda'], info_dict['kda_ratio']))

    def print(self):
        self._print_most_played_champions()
        self._print_recent_games()
