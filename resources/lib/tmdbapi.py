import resources.lib.simpleRequests as requests

# Determines if a series uses absolute numbering or not.
def is_numbering_absolute(tmdb_id):
    headers = {
        "User-Agent": "Kodi Movie scraper by Team Kodi",
        "Accept": "application/json",
    }

    # Sorry kodi, for ripping the API key from your code. I'll make sure to get my own. :)
    url = f'https://api.themoviedb.org/3/tv/{tmdb_id}/season/2?api_key=f090bb54758cabf231fb605d3e3e0468&language=en-US'

    response = requests.get(url, headers=headers)

    if response.status_code == 404:
        return True

    return False