import requests

ACCESS_TOKEN = "CSFGkLhCgxLBJvGxF3sp7wUydQZTLQHoxVQkWB8_QObcQpsrmCcGU_lnLJE15fYC"
base_url = "https://api.genius.com"
headers = {"Authorization": "Bearer " + ACCESS_TOKEN}

def get_artist_id(artist_name):
    search_url = base_url + "/search?q=" + artist_name
    response = requests.get(search_url, headers=headers)
    data = response.json()

    artist_id = None
    for hit in data["response"]["hits"]:
        if hit["result"]["primary_artist"]["name"].lower() == artist_name.lower():
            artist_id = hit["result"]["primary_artist"]["id"]
            break
    
    if artist_id is None:
        raise NameError("L'artiste spécifié n'a pas été trouvé.")
    
    return artist_id

def search_artist_songs(artist_name, number_of_songs=10):
    artist_id = get_artist_id(artist_name)
    number_of_pages = number_of_songs// 50 + 1 # Genius API only allows 50 songs per page
    result = []
    song_titles = []
    total = 0

    print("Requesting", number_of_songs, "songs from", artist_name, f"(id {artist_id})...")
    for page in range(1, number_of_pages + 1):
        params = {"per_page": 50, "page": page, "sort": "popularity"}
        artist_url = base_url + "/artists/" + str(artist_id) + "/songs"
        response = requests.get(artist_url, headers=headers, params=params)
        data = response.json()
        if "songs" in data["response"]:
            songs = data["response"]["songs"]
            total += len(songs)
            result.append(songs)
            print(f"Got {len(songs)} songs (total {total})")

    # Construct titles list
    if result:
        for page in result:
            for song in page:
                song_titles.append(song["title"])
    else:
        print("Aucune chanson n'a été trouvée pour cet artiste :(")

    song_titles = list(set(song_titles[:number_of_songs])) # Remove duplicates from titles list
    print("Returned", len(song_titles), "unique titles")
    return song_titles


if __name__ == "__main__":
    titles = search_artist_songs("Radiohead", 150)
    