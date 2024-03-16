import requests

ACCESS_TOKEN = "m6IcbLC0YjipcksL7SOgNoYESK49qYVZK3FttXbblaaaoYLSRV0fqbePTeUVg"
base_url = "https://api.genius.com"
headers = {"Authorization": "Bearer " + ACCESS_TOKEN}

def get_artist_id(artist_name):
    search_url = base_url + "/search?q=" + artist_name
    response = requests.get(search_url, headers=headers)
    data = response.json()
    print(data)
    artist_id = None
    for hit in data["response"]["hits"]:
        if hit["result"]["primary_artist"]["name"].lower() == artist_name.lower():
            artist_id = hit["result"]["primary_artist"]["id"]
            break
    
    if artist_id is None:
        raise NameError("L'artiste spécifié n'a pas été trouvé.")
    
    return artist_id

def search_artist_songs(artist_name):
    artist_id = get_artist_id(artist_name)
    artist_url = base_url + "/artists/" + str(artist_id) + "/songs"
    response = requests.get(artist_url, headers=headers)
    data = response.json()

    if "songs" in data["response"]:
        print("Chansons de", artist_name, ":")
        for song in data["response"]["songs"]:
            print("-", song["title"])
    else:
        print("Aucune chanson n'a été trouvée pour cet artiste :(")


if __name__ == "__main__":
    search_artist_songs("Radiohead")