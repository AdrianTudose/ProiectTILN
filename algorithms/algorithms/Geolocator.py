import googlemaps

viteza = {
    "default":0,
    "masina":0,
    "bicicleta":0,
    "tren":0,
    "tramvai":0,
    "autobuz":0,
    "avion":0,
    "pas":0
} # metri /secunda


def get_coordinates(directions,oras):
    api_key = open("algorithms/data/google_api_key.txt", "r").read()
    # get API key from https://console.cloud.google.com/apis/credentials

    global gmaps
    gmaps = googlemaps.Client(key=api_key)

    decoder_function = [
        rule_TRANSPORT_TIMP_DIRECTIE_DIRECTIE,
        rule_TIM_DIRECTIE_DIRECTIE,
        rule_TRANSPORT_TIMP_DIRECTIE,
        rule_TIMP_DIRECTIE,
        rule_TRANSPORT_DIRECTIE_DIRECTIE_TIMP,
        rule_DIRECTIE_DIRECTIE_TIMP,
        rule_TRANSPORT_DIRECTIE_TIMP,
        rule_DIRECTIE_TIMP,
        rule_LOCATIE
    ]
    coordonates_list = list()

    coords = [0,0]
    for d in directions:
        response = decoder_function[d[0]](d[1],coords,oras)
        if response:
            coords,name=response
            coordonates_list += [coords+[name]]

    return coordonates_list


def rule_TRANSPORT_TIMP_DIRECTIE_DIRECTIE(arg,coord,oras):
    pass

def rule_TIM_DIRECTIE_DIRECTIE(arg,coord,oras):
    pass

def rule_TRANSPORT_TIMP_DIRECTIE(arg,coord,oras):
    pass

def rule_TIMP_DIRECTIE(arg,coord,oras):
    pass

def rule_TRANSPORT_DIRECTIE_DIRECTIE_TIMP(arg,coord,oras):
    pass

def rule_DIRECTIE_DIRECTIE_TIMP(arg,coord,oras):
    pass

def rule_TRANSPORT_DIRECTIE_TIMP(arg,coord,oras):
    pass

def rule_DIRECTIE_TIMP(arg,coord,oras):
    pass

def rule_LOCATIE(arg,coord,oras):
    loc_data = gmaps.geocode(oras+" "+arg[0])
    lat = loc_data[0]["geometry"]["location"]["lat"]
    lng = loc_data[0]["geometry"]["location"]["lng"]
    return [lat,lng],arg[0]