import googlemaps


def get_coordinates(directions):
    api_key = open("data/google_api_key.txt", "r").read()
    # get API key from https://console.cloud.google.com/apis/credentials

    gmaps = googlemaps.Client(key=api_key)

    for p in directions:
        for dir in p:
            print(gmaps.geocode(dir))
