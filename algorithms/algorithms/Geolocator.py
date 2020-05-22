import math
import re

import googlemaps

speed = {
    "default":1.5,
    "masina":0,
    "bicicleta":7,
    "tren":30,
    "tramvai":20,
    "autobuz":0,
    "pas":1.5
} # metri /secunda


def get_coordinates(directions,city):
    api_key = open("algorithms/data/google_api_key.txt", "r").read()
    # get API key from https://console.cloud.google.com/apis/credentials

    global gmaps
    gmaps = googlemaps.Client(key=api_key)

    decoder_function = [
        rule_TRANSPORT_TIMP_DIRECTIE_DIRECTIE,
        rule_TIMP_DIRECTIE_DIRECTIE,
        rule_TRANSPORT_TIMP_DIRECTIE,
        rule_TIMP_DIRECTIE,
        rule_TRANSPORT_DIRECTIE_DIRECTIE_TIMP,
        rule_DIRECTIE_DIRECTIE_TIMP,
        rule_TRANSPORT_DIRECTIE_TIMP,
        rule_DIRECTIE_TIMP,
        rule_LOCATIE
    ]
    coordonates_list = list()

    bearing = 0
    coords = [0,0]
    for d in directions:
        response = decoder_function[d[0]](d[1],coords,bearing,city)
        if response:
            coords,name,bearing=response
            coordonates_list += [coords+[name]]

    return coordonates_list


def rule_TRANSPORT_TIMP_DIRECTIE_DIRECTIE(arg,coords,bearing,oras):
    bearing = calculate_new_bearing(bearing, arg[2]+arg[3])
    meters = to_seconds(arg[1]) * speed[arg[0]]
    return move_by_bearing_and_distance(bearing, meters, coords), "ocol", bearing

def rule_TIMP_DIRECTIE_DIRECTIE(arg,coords,bearing,oras):
    bearing = calculate_new_bearing(bearing, arg[1]+arg[2])
    meters = to_seconds(arg[0]) * speed["default"]
    return move_by_bearing_and_distance(bearing, meters, coords), "ocol", bearing

def rule_TRANSPORT_TIMP_DIRECTIE(arg,coords,bearing,oras):
    bearing = calculate_new_bearing(bearing, arg[2])
    meters = to_seconds(arg[1]) * speed[arg[0]]
    return move_by_bearing_and_distance(bearing, meters, coords), "ocol", bearing

def rule_TIMP_DIRECTIE(arg,coords,bearing,oras):
    bearing = calculate_new_bearing(bearing, arg[1])
    meters = to_seconds(arg[0]) * speed["default"]
    return move_by_bearing_and_distance(bearing, meters, coords), "ocol", bearing

def rule_TRANSPORT_DIRECTIE_DIRECTIE_TIMP(arg,coords,bearing,oras):
    bearing = calculate_new_bearing(bearing, arg[1]+arg[2])
    meters = to_seconds(arg[3]) * speed[arg[0]]
    return move_by_bearing_and_distance(bearing, meters, coords), "ocol", bearing

def rule_DIRECTIE_DIRECTIE_TIMP(arg,coords,bearing,oras):
    bearing = calculate_new_bearing(bearing, arg[0]+arg[1])
    meters = to_seconds(arg[2]) * speed["default"]
    return move_by_bearing_and_distance(bearing, meters, coords), "ocol", bearing

def rule_TRANSPORT_DIRECTIE_TIMP(arg,coords,bearing,oras):
    bearing = calculate_new_bearing(bearing, arg[1])
    meters = to_seconds(arg[2]) * speed[arg[0]]
    return move_by_bearing_and_distance(bearing, meters, coords), "ocol", bearing

def rule_DIRECTIE_TIMP(arg,coords,bearing,oras):
    bearing = calculate_new_bearing(bearing,arg[0])
    meters = to_seconds(arg[1]) * speed["default"]
    return move_by_bearing_and_distance(bearing,meters,coords),"ocol",bearing

def rule_LOCATIE(arg,coords,bearing,oras):
    loc_data = gmaps.geocode(oras+" "+arg[0])
    if len(loc_data)>0:
        lat = loc_data[0]["geometry"]["location"]["lat"]
        lng = loc_data[0]["geometry"]["location"]["lng"]
        return [lat,lng],arg[0],bearing_between_two_points(coords,[lat,lng])
    else:
        pass

def move_by_bearing_and_distance(bearing, distanceMeters, origin):
    distRadians = distanceMeters / (6372797.6)

    rbearing = bearing * math.pi / 180.0

    lat1 = origin[0] * math.pi / 180
    lon1 = origin[1] * math.pi / 180

    lat2 = math.asin(math.sin(lat1) * math.cos(distRadians) + math.cos(lat1) * math.sin(distRadians) * math.cos(rbearing))
    lon2 = lon1 + math.atan2(math.sin(rbearing) * math.sin(distRadians) * math.cos(lat1), math.cos(distRadians) - math.sin(lat1) * math.sin(lat2))

    return [lat2 * 180 / math.pi, lon2 * 180 / math.pi]

def bearing_between_two_points(pointA,pointB):

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                                           * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

def to_meters(distance):
    dst_metri = 1
    dst = int(re.findall(r'\d+',distance)[0])
    if dst:
        dst_metri = dst
    if re.search("(\smetri)|(\dm)",distance):
        dst_metri *= 1
    if re.search(r"(\skilometri)|(\dkm)",distance):
        dst_metri *= 1000
    return dst_metri

def to_seconds(time):
    seconds = 1
    tm = int(re.findall(r'\d+',time)[0])
    if tm:
        seconds = tm
    if re.search("(\ssecunde)|(\ds)",time):
        seconds *= 1
    if re.search(r"(\sminute)|(\dm)",time):
        seconds *= 60
    return seconds


def calculate_new_bearing(initial_bearing,direction):
    if direction in ["nord","N"]:
        return 0
    if direction in ["est","E"]:
        return 90
    if direction in ["sud","S"]:
        return 180
    if direction in ["vest","V"]:
        return 270
    if direction in ["nord-est","NE"]:
        return 45
    if direction in ["sud-est","SE"]:
        return 135
    if direction in ["sud-vest","SV"]:
        return 225
    if direction in ["nord-vest","NV"]:
        return 315
    if direction in ["inainte"]:
        return initial_bearing
    if direction in ["stanga"]:
        return initial_bearing-90
    if direction in ["dreapta"]:
        return initial_bearing+90
    return initial_bearing
