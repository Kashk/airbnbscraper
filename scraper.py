import requests
import json

# New line variable for handling prettyprint
newLine = '\n\r'

# room list, hard coded for now
rooms = [
    'https://www.airbnb.co.uk/rooms/14531512?s=51',
    'https://www.airbnb.co.uk/rooms/19278160?s=51',
    'https://www.airbnb.co.uk/rooms/19292873?s=51'
    ]

# required data with key and value for prettyprint
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
    startTag = "<!--"
    endTag = "-->"

    # grab text from http request
    rText = request.text

    # trim down the html page
    trimmed = rText[rText.find('<script type="application/json" data-hypernova-key="p3show_marketplacebundlejs"'):]

    # extract the data we need by the HTML comment tags (remembering to include the length of the start tag itself)
    data = trimmed[ trimmed.find(startTag) + len(startTag) : trimmed.find(endTag) ]

    # load it as json and return it
    return json.loads(data)

def getListingJson(roomJson):
    # return the data we're interested in from the overall JSON
    return roomJson['bootstrapData']['reduxData']['marketplacePdp']['listingInfo']['listing']

def getAmenityJson(listingJson):
    # return the amenity data
    return listingJson['listing_amenities']

def printListingData(filename, listingJson):
    # loop through each attribute in the listing
    for attribute in listingJson:

        # if it's something we're interested in, add it to the results
        if attribute in requiredData:

            # grabs the human friendly name for the attribute E.G. "Property Name" for "localized_room_type"
            filename.write( getPrettyAttributeName(attribute) + ': ' + str( listingJson[attribute] ) + newLine)

def printAmenityData(filename, amenityJson):
    # Iterator for unnamed elements in json
    i = 0

    # loop through each amenity
    for amenity in amenityJson:

        # all amenities are listed, but only those which 'is_present' are the ones we're interested in
        if amenity['is_present']:

            # amenity names are pretty enough, no need to tidy
            filename.write(amenityJson[i]['name'] + newLine)
        i += 1

def printListingTitle(filename):
    filename.write(newLine + '==== ROOM ====' + newLine)

def printAmenityTitle(filename):
    filename.write(newLine + '==== AMENITIES ====' + newLine)

if __name__ == "__main__":
    # opens / creates results file
    resultsFile = open('results.txt','w', encoding="utf-8")

    # loop through each room we're interested in
    for room in rooms:
        # make the request, get the overall JSON
        roomData = getRoomJson(requests.get(room))

        # get the listing JSON
        listingData = getListingJson(roomData)

        # get the amenity JSON
        amenityData = getAmenityJson(listingData)

        printListingTitle(resultsFile)

        # loop around and print each attribute we need
        printListingData(resultsFile,listingData)

        printAmenityTitle(resultsFile)

        # loop around and print all present amenities
        printAmenityData(resultsFile,amenityData)
