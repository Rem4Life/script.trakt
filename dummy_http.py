# TMDB_PARAMS = {'api_key': 'f090bb54758cabf231fb605d3e3e0468'}
# BASE_URL = 'https://api.themoviedb.org/3/{}'
# SEARCH_URL = BASE_URL.format('search/movie')
# FIND_URL = BASE_URL.format('find/{}')
# MOVIE_URL = BASE_URL.format('movie/{}')
# COLLECTION_URL = BASE_URL.format('collection/{}')
# CONFIG_URL = BASE_URL.format('configuration')

# headers = {"Accept": "application/json", "Authorization": self.token}

import resources.lib.simpleRequests as requests

headers = {
    "User-Agent": "Kodi Movie scraper by Team Kodi",
    "Accept": "application/json",
}

url = "https://api.themoviedb.org/3/tv/95479/season/2?api_key=f090bb54758cabf231fb605d3e3e0468&language=en-US"

response = requests.get(url, headers=headers)

if response.status_code == 404:
    print("404")
    print(response.json())