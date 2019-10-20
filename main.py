#! ~/Env/holololo python

import requests
from bs4 import BeautifulSoup

def main():
    champion = 'ahri'
    r = requests.get("https://na.op.gg/champion/{champ}/statistics/mid".format(champ=champion))
    soup = BeautifulSoup(r.text, features="html.parser").find('body')
    spell_and_skill = soup.find_all('table')[2]
    skills = spell_and_skill.find_all('tbody')[1]

    skill_master_order = [skill.text for i, skill in enumerate(skills.find_all('span')) if i < 3]

    print("skill master order: ", ' -> '.join(skill_master_order))


if __name__ == "__main__":
    main()
