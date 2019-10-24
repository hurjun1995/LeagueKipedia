import requests
import os

class Watcher:
    RIOT_BASE_URL = 'https://na1.api.riotgames.com/{path}'
    RIOT_SUMMONOR_BY_NAME_URL = RIOT_BASE_URL.format(path='/lol/summoner/v4/summoners/by-name/{summoner_name}')
    user_input = None

    def __init__(self, user_input):
        self.user_input = user_input

    def run_watcher(self):
        summonor_name = 'ch22se'
        riot_api_key = os.environ['RIOT_API_KEY']
        riot_api_key = "RGAPI-1de4ce16-f276-4665-b90b-361aece8b3a7"  # TODO: delete this later!
        url = self.RIOT_SUMMONOR_BY_NAME_URL.format(summoner_name=summonor_name)
        headers = {"X-Riot-Token": riot_api_key}
        res = requests.get(url, headers=headers)