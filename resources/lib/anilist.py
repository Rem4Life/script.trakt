import requests
from resources.lib import kodiUtilities

from resources.lib.loggingService import get_logger

stream_logger = get_logger("customLogger")

ANILIST_URL = "https://graphql.anilist.co"
ANILIST_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjJjMTA5MmMwNmQwMDM4ZGEzNjAyY2UxYTgyZDAzOTM3NTdlMGQyODcwN2NkOWVmMTdmMmUwNGZjMDhiZWVlZTM5YTI5NTBjOTA3Y2M3NTQxIn0.eyJhdWQiOiIxNjg0MyIsImp0aSI6IjJjMTA5MmMwNmQwMDM4ZGEzNjAyY2UxYTgyZDAzOTM3NTdlMGQyODcwN2NkOWVmMTdmMmUwNGZjMDhiZWVlZTM5YTI5NTBjOTA3Y2M3NTQxIiwiaWF0IjoxNzA3NTkyNjA2LCJuYmYiOjE3MDc1OTI2MDYsImV4cCI6MTczOTIxNTAwNiwic3ViIjoiMjk1MTEiLCJzY29wZXMiOltdfQ.ZzM0te32JT5YxNZsHhiMrZmdkTxUKR995rxv_D3XbK3vupHBP2U4hLfEmGIoYtFReOyMpp9iW9x00utO6czDhi24d-4PgyBs2TQQ7aKxzwKtOe0r8w5RpIztQiVO3Harjkzk3UDL_Zo26EFARanZMmOwwgMa3Rc3AeKV0XsW99AmVS4Ai3Gau2_TKtAiyzqS34gVto5gAa5U8l9mJ7_Zuy-lbLzzVyc9CMp-hY8pUd4p0easFo14DPA7WYiM0FMy6qsKHuPXFo81LRGLTkxO70b4SlFVh42iBLXfUSURGP-9e8ZXEinDDIKheDaXs5AHvx6l2I4GGbvH2Im47QmctVBum_Y2JToaNcDj5smMqp_DScuDNZ0A0pheOd9PiKr9nLRkOUTgIcbV3w-cAwdBxF4Fjf92RKOLlwDP3kXSh0xMElNWvUknArOqXV5vGGQiaBnrAkJrqWjrjN8QRFLQrmkvvURpVZ_3s09YUeK6tT6Q3CYnS4Y3iRZzjfsJShAFb93cGebQOQ8b5qlrTH_DwvqsBjF58GAHYJh8TPUJVyItHqGpEAMjWC1rm1Vg99chcikkt7gpVuopYlrEfMx_QhDoVIztfEKO1vcKMkcgyVLQiMbelc1Kt6Ahh5gMtMy0PJMzsV_-dp6Qv5maZucyUR6dGvMradDpD871XzBPIo8"
TVDB_URL = "https://api4.thetvdb.com/v4/series/259640/episodes/default/eng"
TVDB_TOKEN = "your_tvdb_token_here"

QUERY_MEDIA_DETAILS = """
   query ($id: Int) {
        Media(id: $id, type: ANIME) {
            id
            episodes
            title {
                english
            }
            relations {
                edges {
                    node {
                        id
                        episodes
                    }
                    relationType
                }
            }
        }
    }
"""

QUERY_SEARCH_ANIME = """
    query ($name: String) {
        Media(search: $name, type: ANIME) {
            id
            episodes
            title {
                english
            }
            relations {
                edges {
                    node {
                        id
                        episodes
                    }
                    relationType
                }
            }
        }
    }
"""

QUERY_USER_ANIME_LIST = """
    query ($id: Int) {
        MediaListCollection(userId:$id,type:ANIME){
            lists{
                name
                entries{
                    media{
                        id
                        title{
                            english
                            romaji
                        }
                    }
                    score
                    progress
                }
            }

        }
    }
"""

MUTATION_USER_UPDATE_ANIME_LIST = """
    mutation ($mediaId: Int, $progress: Int, $score: Float) {
    SaveMediaListEntry(mediaId:$mediaId,score:$score,progress:$progress){
            score
        }
    }
"""


def fetch_media_details(sequel_id, seasons=[], season_number=1):
    response = requests.post(
        ANILIST_URL,
        json={
            "query": QUERY_MEDIA_DETAILS,
            "variables": {"id": sequel_id},
        },
    )
    media = response.json()["data"]["Media"]
    title = media["title"]["english"]
    episodes = media["episodes"]

    if "movie" not in title.lower():
        seasons.append(
            {
                "season": season_number,
                "episodes": episodes,
                "title": title,
                "id": media["id"],
            }
        )
        season_number += 1

    sequels = [
        edge
        for edge in media["relations"]["edges"]
        if edge["relationType"] == "SEQUEL" and edge["node"]["episodes"]
    ]
    if sequels:
        sequel_with_most_episodes = max(sequels, key=lambda x: x["node"]["episodes"])
        return fetch_media_details(
            sequel_with_most_episodes["node"]["id"], seasons, season_number
        )
    return seasons


def search_anilist_for_anime(title):
    response = requests.post(
        ANILIST_URL,
        json={
            "query": QUERY_SEARCH_ANIME,
            "variables": {"name": title},
        },
    )
    anime_id = response.json()["data"]["Media"]["id"]
    return fetch_media_details(anime_id,[])


def get_season_for_episode_number(seasons, absolute_episode_number):
    cumulative_episodes = 0
    for season in seasons:
        previous_cumulative = cumulative_episodes
        cumulative_episodes += season["episodes"]
        if cumulative_episodes >= absolute_episode_number:
            seasonal_episode_number = absolute_episode_number - previous_cumulative
            return (season, seasonal_episode_number)
    return (None, None)


def get_user_rating_for_anime(anime_id):
    response = requests.post(
        ANILIST_URL,
        json={
            "query": QUERY_USER_ANIME_LIST,
            "variables": {"id": 29511},
        },
        headers={"Authorization": f"Bearer {ANILIST_TOKEN}"},
    )
    stream_logger.debug(response.json())
    if response.status_code == 200:
        lists = response.json()["data"]["MediaListCollection"]["lists"]
        for list_ in lists:
            match = next(
                (item for item in list_["entries"] if item["media"]["id"] == anime_id),
                None,
            )
            if match:
                return match
    return None


def set_anilist_rating(anime_id, rating, episode, current_rating_details):
    actual_rating = 0
    if current_rating_details:
        actual_rating = (
            (current_rating_details["score"] * current_rating_details["progress"])
            + (rating * 10)
        ) / (current_rating_details["progress"] + 1)
    else:
        actual_rating = rating * 10

    progress = episode
    if current_rating_details and current_rating_details.get("progress", 0) >= episode:
        return

    requests.post(
        ANILIST_URL,
        json={
            "query": MUTATION_USER_UPDATE_ANIME_LIST,
            "variables": {
                "mediaId": anime_id,
                "score": actual_rating,
                "progress": progress,
            },
        },
        headers={"Authorization": f"Bearer {ANILIST_TOKEN}"},
    )
    kodiUtilities.notification("AniList - Rating Updated", f"Set to {actual_rating}", 3000)


def get_anilist_auth_token():
    payload = {
        "grant_type": "authorization_code",
        "client_id": "16843",
        "client_secret": "yzAkwl67VmZUWaOI6yG7MPmcjKObvRDT9mAPObxs",
        "redirect_uri": "https://anilist.co/api/v2/oauth/pin",
        "code": "def50200a0fbea40dc943529df4fe11ade2af06db919892e211ad8b0d8870aac75cb8895f68724196dfb5933f2fbca821012d11b95fa103013f7823ae3d5d1944e344c7c7858d338d9b8993c48f6d0b90bffb7a7f2253ee65089e475bccdcc79909899fa5f710b84f510f01a7b29130d865ed2e2db7a2460f66fbad9873d7ec747410ab915d2a93f88f3c84cfd02619a256d49b26fcbbd64066a560ad97d7ef1ab73bdafb0cd3bc99b7c8266a8db2fd7d778c76d6bfcabf843aa38714d7818ea38f679ad98ce3ec212403e19c84e0991d9df0c7d4cb283f75a687744101dc3758025a4f044678213d1fe4614aa450523db2f9b2ae2343cc403329c115b7ace20e966ac1df1e312431a19bd938ac979bac138f329e78405060c9e799914a8fae842fde26ce61040fa5b3e635d44f4e3fb5e0ca15262c6207d429fb18835d5a010130f299ceba565ab68a1e8998b082ffed35b84436c3f30032eb8d9ea9f117570bfb880fb417a76dcbd9c21658ed10de2",
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    response = requests.post(
        "https://anilist.co/api/v2/oauth/token", json=payload, headers=headers
    )
    stream_logger.debug(response.json())


def mainAnilist(anime_name, episode_number, rating):
    seasons = search_anilist_for_anime(anime_name)
    stream_logger.debug("Anime Name : " + anime_name)
    stream_logger.debug("Episode Number : " + str(episode_number))
    # stream_logger.debug("Seasons: " + str(seasons))
    season, episode = get_season_for_episode_number(seasons, episode_number)
    stream_logger.debug("Season and Episode : " + str(season) + " " + str(episode))
    current_rating_details = get_user_rating_for_anime(season["id"])
    # stream_logger.debug(current_rating_details)
    set_anilist_rating(season["id"], rating, episode, current_rating_details)
    # se
    # Implement setAniListRating similarly if needed


# if __name__ == "__main__":
#     mainAnilist("Attack on Titan", 87, 10)
#     # Uncomment to use getAniListAuthToken if needed
