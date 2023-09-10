import simpleRequests as requests

class tvdbAPI():
    login_url = "https://api4.thetvdb.com/v4/login"
    login_api_key = "edae60dc-1b44-4bac-8db7-65c0aaf5258b"
    login_pin = "51bdbd35-bcd5-40d9-9bc3-788e24454baf"
    token = None

    def __init__(self):
        self.token = self.get_token()

    def get_token(self):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        token_info = {}

        token_info["apikey"] = self.login_api_key
        token_info["pin"] = self.login_pin

        response = requests.post(self.login_url, headers=headers, json=token_info)

        if not response.ok:
            response.raise_for_status()

        token = response.json()['data']['token']
        return token

    def get_series_extended(self, id, meta, short):
        url = f'https://api4.thetvdb.com/v4/series/{id}/extended?meta={meta}&short={short}'

        headers = {
            'Accept': 'application/json',
            'Authorization': self.token
        }

        response = requests.get(url, headers=headers)

        if not response.ok:
            response.raise_for_status()

        return response.json()

    def convert_to_absolute_numbering(self, episodes, season, epi):
        filtered_episodes = [episode for episode in episodes if episode.get('seasonNumber') != 0]
        specific_episode = [episode for episode in episodes if episode.get('number') == epi and episode.get('seasonNumber') == season]
        
        index = filtered_episodes.index(specific_episode[0])

        return index + 1