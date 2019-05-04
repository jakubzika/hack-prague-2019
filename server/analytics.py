from math import sin, cos, sqrt, atan2, radians
from geopy import distance

import json

types ={
    'Barevné sklo': 1,
    'Elektrozařízení': 2,
    'Kovy': 3,
    'Nápojové kartóny': 4,
    'Papír': 5,
    'Plast': 6,
    'Čiré sklo': 7,
    'Textil': 8,
}


def determineContainerType(type):
    if(type=='Papír'):
        return 5
    

def parseContainers(containersFileName,locationsFilename):
    locationsPublic = parseLocations(locationsFilename)
    with open(containersFileName,'r',encoding='utf-8') as f:
        data = json.loads(f.read())['features']
    locationId = 0
    location = None
    locations = {}
    index = 0
    for container in data:
        if(locationId != container['properties']['STATIONID']):
            if(location):
                location['types'] = set(location['types'])
                locations[locationId] = location
            locationId = container['properties']['STATIONID']
            location = {
                'id':locationId,
                'coordinates': (container['geometry']['coordinates'][1],container['geometry']['coordinates'][0]),
                'types': set(),
                'public': locationsPublic[locationId]['public'],
                }
            index += 1

        location['types'].add(types[container['properties']['TRASHTYPENAME']])

    return locations

def parseLocations(filename):
    data = {}
    with open(filename,'r',encoding='utf-8') as f:
        data = json.loads(f.read())['features']
    
    locations = {}
    for location in data:
        locations[location['properties']['ID']] = {
            'id': location['properties']['ID'],
            'public':  True if location['properties']['PRISTUP'] == 'volně' else False,
        }
    # locationsSorted = sorted(locations, key=lambda k: k['id'])  
    return locations
    

def getDistance(src,dest):
    # approximate radius of earth in km
    return distance.distance(src,dest).km

def getLocationsInRange(src,containerData,range,types):
    locationsInRange = []
    range = range/1000
    for location in containerData:
        distanceLength = distance.distance(src,location[1]['coordinates']).km
        if(distanceLength <= range):
            if(types.issubset(location[1]['types'])):
                locationsInRange.append(location[1])
    return locationsInRange
