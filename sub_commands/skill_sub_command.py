from sub_commands.sub_command_base import SubCommandBase


class SkillSubCommand(SubCommandBase):
    skill_order_info_list = None

    def add_argument(self, subparser):
        subparser.add_argument('-s', '--skill', action='store_true',
                               help='include to see skill master order in the output')

    def retrieve(self):
        self.fetch_and_set_soup(f"https://na.op.gg/champion/{self.get_champ_name_no_space()}/statistics/{self.champ_lane}/skill?")

    def parse(self):
        self.skill_order_info_list = self.soup.find("div", class_="tabItem Content championLayout-skill") \
            .find('div', class_='champion-box-content') \
            .find_all('li', class_='champion-stats__filter__item')
        self.skill_order_info_list = [info for info in self.skill_order_info_list if info['data-index'] != 'All']

    def print(self):
        print("Skill Orders:")
        print("{:>7} {:>15} {:>12} {:>12}".format("index", "skill order", "win rate", "pick rate"))
        for i, skill_order_info in enumerate(self.skill_order_info_list):
            skill_order = ' -> '.join(
                [s.find('span').text for s in skill_order_info.find_all('li', class_='champion-stats__list__item')])
            # somehow class names are reversed for pick_rate and win_rate on op.gg
            win_rate = skill_order_info \
                .find('div', class_='champion-stats__filter_item_value--pickrate') \
                .find('b').text
            pick_rate = skill_order_info \
                .find('div', class_='champion-stats__filter_item_value--winrate') \
                .find('b').text
            print("{:>7} {:>15} {:>12} {:>12}".format(i+1, skill_order, win_rate, pick_rate))
