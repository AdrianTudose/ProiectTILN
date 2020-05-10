from pprint import pprint

import googlemaps


def get_coordinates(directions):
    api_key = open("algorithms/data/google_api_key.txt", "r").read()
    # get API key from https://console.cloud.google.com/apis/credentials

    global gmaps
    gmaps = googlemaps.Client(key=api_key)

    decoder_function = [rule_LOCATION,rule_2]
    coordonates_list = list()

    for d in directions:
        loc = decoder_function[d[1]](d[0])
        if loc:
            coordonates_list += [loc]

    return coordonates_list


def rule_LOCATION(place):
    loc_data = gmaps.geocode(place)
    return [loc_data[0]["geometry"]["location"]["lat"],loc_data[0]["geometry"]["location"]["lng"],place[0]]

def rule_2(place):
    pass