import logging
import requests

from utils.tools import sanitize_str

logging.getLogger().setLevel(logging.INFO)


class TFT():
    platform_routing_url = 'https://na1.api.riotgames.com'
    region_routing_url = 'https://americas.api.riotgames.com'

    def __init__(self, token: str = None) -> None:
        self.headers = {}
        self.summoners = {}

        if token is None:
            # initialize later
            return
        self.initialize(token)

    def initialize(self, token) -> None:
        logging.info("Starting session for TFT API")
        if token is None:
            raise Exception("API token must be defined.")

        self.headers = {
            'Content-Type': 'application/json',
            'X-Riot-Token': token
        }

    def get(self, path, routing="platform", **params):
        if routing == "platform":
            url = f"{self.platform_routing_url}{path}"
        else:
            url = f"{self.region_routing_url}{path}"

        logging.info(f"Getting request for {url}")
        results = requests.get(url, headers=self.headers)

        if results.ok:
            return results.json()
        else:
            raise Exception(results.text)

    def _get_challenger(self) -> list:
        logging.info("Getting challenger rank")

        path = "/tft/league/v1/challenger"

        return self.get(path)

    def _get_grandmaster(self) -> list:
        logging.info("Getting grandmaster rank")

        path = "/tft/league/v1/grandmaster"

        return self.get(path)

    def _get_master(self) -> list:
        logging.info("Getting master rank")

        path = "/tft/league/v1/master"

        return self.get(path)

    def get_ranked_cutoff(self) -> list:
        """
        returns LP cutoff for challenger and grandmaster
        get all challenger, grandmaster, master LPs
        get 250th rank and 750th rank for challenger and grandmaster, respectively
        """

        _challenger_list = self._get_challenger()
        _grandmaster_list = self._get_grandmaster()
        _master_list = self._get_master()
        _lp_list = [d['leaguePoints'] for d in _challenger_list['entries']]
        _lp_list += [d['leaguePoints'] for d in _grandmaster_list['entries']]
        _lp_list += [d['leaguePoints'] for d in _master_list['entries']]
        _lp_list.sort(reverse=True)

        return {
            'challenger': _lp_list[249],
            'grandmaster': _lp_list[749]
        }

    def set_summoners(self, summoner_info) -> None:
        self.summoners[sanitize_str(summoner_info['name'])] = summoner_info

    def get_summoner_metadata(self, summoner_name) -> list:
        """
        returns metadata on the summoner (i.e., id, account id, puuid, and etc.)
        """
        path = f"/tft/summoner/v1/summoners/by-name/{summoner_name}"

        results = self.get(path)
        self.set_summoners(results)

        return results

    def get_summoner_data(self, summoner_id) -> list:
        path = f"/tft/league/v1/entries/by-summoner/{summoner_id}"
        return self.get(path)

    def get_match_list_by_summoner(self, puuid) -> list:
        path = f"/tft/match/v1/matches/by-puuid/{puuid}/ids"
        return self.get(path, routing="region")

    def get_match(self, match_id) -> list:
        path = f"/tft/match/v1/matches/{match_id}"
        return self.get(path, routing="region")


TFT_API = TFT()
