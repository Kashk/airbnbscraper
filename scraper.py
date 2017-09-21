import requests
import json
from lxml import html

# New line variable for handling prettyprint
newLine = '\n\r'

rooms = ['https://www.airbnb.co.uk/rooms/14531512?s=51', 'https://www.airbnb.co.uk/rooms/19278160?s=51', 'https://www.airbnb.co.uk/rooms/19292873?s=51']
requiredData = {
    'name':'Property Name',
    'bathroom_label':'# of Bathrooms',
    'bedrooms':'# of Bedrooms',
    'beds':'# of Beds',
    'localized_room_type':'Property Type'
    }

def getPrettyAttributeName(attribute):
    return requiredData[attribute]

def getRoomJson(request):
    # grab text from http request
    rText = request.text

    trimmed = rText[rText.find('<script type="application/json" data-hypernova-key="p3show_marketplacebundlejs"'):]

    start = trimmed.find("<!--")

    end = trimmed.find("-->")

    data = trimmed[start:end]

    return json.loads(data[4:len(data)])

def getListingJson(roomJson):
    return roomJson['bootstrapData']['reduxData']['marketplacePdp']['listingInfo']['listing']

def getAmenityJson(listingJson):
    return listingJson['listing_amenities']

#print (requests.get('https://www.airbnb.co.uk/rooms/20143243').text)
#r = requests.get('https://www.airbnb.co.uk/rooms/20143243').text

"""
h = open('headers.txt','w', encoding="utf-8")
for header in loaded:
    h.write( header + newLine )
"""

def printListingData(filename, listingJson):
    for attribute in listingJson:
        if attribute in requiredData:
            filename.write( getPrettyAttributeName(attribute) + ': ' + str( listingJson[attribute] ) + newLine)

def printAmenityData(filename, amenityJson):
    # Iterator for unnamed elements in json
    i = 0
    for amenity in amenityJson:
        if amenity['is_present']:
            filename.write(amenityJson[i]['name'] + newLine)
        i += 1

def printListingTitle(filename):
    filename.write(newLine + '==== ROOM ====' + newLine)

def printAmenityTitle(filename):
    filename.write(newLine + '==== AMENITIES ====' + newLine)
#listingDataAmenities = listingData['listing_amenities']



#f = open('airbnb.txt','w', encoding="utf-8")
#f.write( data )

if __name__ == "__main__":
    resultsFile = open('results.txt','w', encoding="utf-8")
    for room in rooms:
        roomData = getRoomJson(requests.get(room))
        listingData = getListingJson(roomData)
        amenityData = getAmenityJson(listingData)

        printListingTitle(resultsFile)
        printListingData(resultsFile,listingData)
        printAmenityTitle(resultsFile)
        printAmenityData(resultsFile,amenityData)
