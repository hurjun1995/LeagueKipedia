from sub_commands.sub_command_base import SubCommandBase


class ItemSubCommand(SubCommandBase):
    item_info_list_sorted = None

    def add_argument(self, subparser):
        subparser.add_argument('-i', '--item', action='store_true',
                               help='include to see item trees in the output')

    def retrieve(self):
        self.fetch_and_set_soup(f'https://na.op.gg/champion/{self.champ_name}/statistics/{self.champ_lane}/item?')

    def parse(self):
        self.item_info_list_sorted = self.soup.find("div", class_="championLayout-item") \
            .find('div', class_='l-champion-statistics-content__side') \
            .find('tbody') \
            .find_all('tr')

    def print(self):
        print("Recommended Items:")
        print("{:>12} {:>25} {:>12} {:>12}".format("index", "item name", "win rate", "pick rate"))
        for i, item_info in enumerate(self.item_info_list_sorted):
            if i < 10:
                name = item_info.find('span').text
                win_rate = item_info.find('td', class_='champion-stats__table__cell--winrate').text
                pick_rate = item_info \
                    .find('td', class_='champion-stats__table__cell--pickrate') \
                    .find(text=True).strip()
                print("{:>12} {:>25} {:>12} {:>12}".format(i, name, win_rate, pick_rate))
            else:
                break
