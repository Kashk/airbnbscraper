import requests
import json
import sys

class airbnbScraper:

    def __init__(self, init_rooms):
        self.rooms = []
        self.results = {}
        # required data with key and value for prettyprint
        self.requiredData = {
            'name':'Property Name',
            'localized_room_type':'Property Type',
            'bedrooms':'# of Bedrooms',
            'beds':'# of Beds',
            'bathroom_label':'# of Bathrooms'
            }

        # New line variable for handling prettyprint
        self.newLine = '\n\r'

        if init_rooms is not None:
            for room in init_rooms:
                self.rooms.append(room)
        else:
            # given room list, hard coded for now
            self.rooms = [
            'https://www.airbnb.co.uk/rooms/14531512?s=51',
            'https://www.airbnb.co.uk/rooms/19278160?s=51',
            'https://www.airbnb.co.uk/rooms/19292873?s=51'
            ]


    def getPrettyAttributeName(self, attribute):
        return self.requiredData[attribute]

    def getRoomJson(self, request):
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

    def getListingJson(self, roomJson):
        # return the data we're interested in from the overall JSON
        return roomJson['bootstrapData']['reduxData']['marketplacePdp']['listingInfo']['listing']

    def getAmenityJson(self, listingJson):
        # return the amenity data
        return listingJson['listing_amenities']

    def getListingId(self,listingJson):
        return listingJson['id']

    def getListingData(self, listingJson):
        # results
        listingData = {}
        # loop through each attribute in the listing
        for attribute in listingJson:

            # if it's something we're interested in, add it to the results
            if attribute in self.requiredData:
                # grabs the human friendly name for the attribute E.G. "Property Name" for "localized_room_type"
                listingData[self.getPrettyAttributeName(attribute)] = listingJson[attribute]
        return listingData

    def printListingData(self, filename, listingJson):
        filename.write( self.getListingData(listingJson) )

    def getAmenityData(self, amenityJson):
        # results
        amenityData = []
        # Iterator for unnamed elements in json
        i = 0

        # loop through each amenity
        for amenity in amenityJson:

            # all amenities are listed, but only those which 'is_present' are the ones we're interested in
            if amenity['is_present']:

                # amenity names are pretty enough, no need to tidy
                amenityData.append(amenityJson[i]['name'])
            i += 1
        return amenityData

    def printAmenityData(self, filename, amenityJson):
        filename.write( self.getAmenityData(amenityJson) )

    def getListingTitle(self, listingId):
        return self.newLine + '==== ROOM: ' + str ( listingId ) + ' ====' + self.newLine

    def printListingTitle(self, filename):
        filename.write(self.getListingTitle())

    def getAmenityTitle(self):
        return self.newLine + '==== AMENITIES ====' + self.newLine

    def printAmenityTitle(self, filename):
        filename.write(self.getAmenityTitle())

    def scrapeUrl(self, url):
        roomData = {}
        # make the request, get the overall JSON
        urlData = self.getRoomJson(requests.get(url))

        # get the listing JSON
        listingData = self.getListingJson(urlData)

        # get the amenity JSON
        amenityData = self.getAmenityJson(listingData)

        # add listing data to the room object
        roomData['Listing'] = self.getListingData(listingData)

        # add amenity data to room object
        roomData['Amenities'] = self.getAmenityData(amenityData)

        # add room object to the overall results
        self.results[self.getListingId(listingData)] = roomData

        return self.results

    def printResults(self):
        # for each room
        for entry in self.results:
            
            #print the data
            print( self.getListingTitle( entry ) )
            for key, value in self.results[entry]['Listing'].items():
                print (key + ': ' + str( value ) + self.newLine)

            print( self.getAmenityTitle() )

            for amenity in self.results[entry]['Amenities']:
                print ( str(amenity) )

if __name__ == "__main__":
    # pass parameters (ignoring function call)
    scraper = airbnbScraper(sys.argv[1:])

    # loop through each room we're interested in
    for room in scraper.rooms:
        scraper.scrapeUrl(room)

    scraper.printResults()
