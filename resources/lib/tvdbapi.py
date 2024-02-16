import resources.lib.simpleRequests as requests
from resources.lib.loggingService import get_logger
from pprint import pformat

stream_logger = get_logger("customLogger")


class tvdbAPI:
    login_url = "https://api4.thetvdb.com/v4/login"
    login_api_key = "edae60dc-1b44-4bac-8db7-65c0aaf5258b"
    login_pin = "51bdbd35-bcd5-40d9-9bc3-788e24454baf"
    token = None

    def __init__(self):
        self.token = self.get_token()  # Disabled for now, to prevent rate limiting.
        # self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZ2UiOiIiLCJhcGlrZXkiOiJlZGFlNjBkYy0xYjQ0LTRiYWMtOGRiNy02NWMwYWFmNTI1OGIiLCJjb21tdW5pdHlfc3VwcG9ydGVkIjpmYWxzZSwiZXhwIjoxNjk3MDA2NTY4LCJnZW5kZXIiOiIiLCJoaXRzX3Blcl9kYXkiOjEwMDAwMDAwMCwiaGl0c19wZXJfbW9udGgiOjEwMDAwMDAwMCwiaWQiOiIxIiwiaXNfbW9kIjp0cnVlLCJpc19zeXN0ZW1fa2V5IjpmYWxzZSwiaXNfdHJ1c3RlZCI6ZmFsc2UsInBpbiI6IjUxYmRiZDM1LWJjZDUtNDBkOS05YmMzLTc4OGUyNDQ1NGJhZiIsInJvbGVzIjpbIk1vZCJdLCJ0ZW5hbnQiOiJ0dmRiIiwidXVpZCI6IiJ9.IdjcBIFpvh8Tk_vw3AUZQXM73ZmcuWQbcRkMcTl_TpS_L2n_9LfihdALWd8Ppr-XNylU5SMkZW7kDjjZvGTc4yHTALHV5Q415ioOhCyUYzGuJzKl9gamu1AY7rhJqEAmsczqIVnO-T4IHBLfXIU7UJDFQ8UjzZuWlkc0vJ_pBMgUTUxeHy6whlE6NXBMzVRfzT7p8d3gbdOzsdO3kYu0acf3WJ-d98eBX_VJzr8xfAmBlIWs_S6XdFQk33Bn25zgVmpphFB4erDW_HuGc145mTAyZ5KZBKUL5sVcnOMs3BZ6MtB_j98h7REt5Q9v2lzIcW2EMcx7AhRT1ZBJOoGvrqWAETrw4JPsl086qSYnd_P_TvjpvIlQ4M29Upf3oi0xmeCv42wvB9KTWl9tW6oTLrdY1kzLS3XboWcCnIk-RRXG6LGT_sTYIHlMTTmxlGoB12VuDIGM5imm_Q4L3hcHEmKE5VIui369pqCr3IIUKBzi4y6XK-je6EBhpHbd0OiQBcF3uZjtOpfOPk50WQNmrC3OOfYg4d8XSpp_UmY9rmUafqwXN75LvRjVuV28izLKVtgE1pIX7OMeUWPVoWrIImfTwjAtrUJ8FmUciRP8FOfrw20Zinak_-qpnjBzJ7mkooAtIl-wDlPGAS6lkQELJqxgKiQmt7qYQ_uXUEdlmk8"
        stream_logger.debug("tvdbAPI init.")
        stream_logger.debug(self.token)

    def get_token(self):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        token_info = {}

        token_info["apikey"] = self.login_api_key
        token_info["pin"] = self.login_pin

        response = requests.post(self.login_url, headers=headers, json=token_info)

        if not response.ok:
            response.raise_for_status()

        token = response.json()["data"]["token"]
        return token

    def get_series_extended(self, id, meta, short):
        url = f"https://api4.thetvdb.com/v4/series/{id}/extended?meta={meta}&short={short}"

        headers = {"Accept": "application/json", "Authorization": self.token}

        response = requests.get(url, headers=headers)

        if not response.ok:
            response.raise_for_status()

        return response.json()

    def convert_to_absolute_numbering(self, episodes, season, epi):
        filtered_episodes = [
            episode for episode in episodes if episode.get("seasonNumber") != 0
        ]

        specific_episode = [
            episode
            for episode in episodes
            if episode.get("number") == epi and episode.get("seasonNumber") == season
        ]

        index = filtered_episodes.index(specific_episode[0])

        return index + 1

    def convert_to_relative_numbering(self, episodes, season, epi):
        # TODO Implement this
        pass
