import requests
import json

class airbnbScraper:

    def __init__(self, *init_rooms):
        self.rooms = []
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

        if len(init_rooms)>0:
            for room in init_rooms:
                rooms.append(room)
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

    def getListingData(self, listingJson):
        # results
        listingData = ''
        # loop through each attribute in the listing
        for attribute in listingJson:

            # if it's something we're interested in, add it to the results
            if attribute in self.requiredData:
                # grabs the human friendly name for the attribute E.G. "Property Name" for "localized_room_type"
                listingData += self.getPrettyAttributeName(attribute) + ': ' + str( listingJson[attribute] ) + self.newLine
        return listingData

    def printListingData(self, filename, listingJson):
        filename.write( self.getListingData(listingJson) )

    def getAmenityData(self, amenityJson):
        # results
        amenityData =''
        # Iterator for unnamed elements in json
        i = 0

        # loop through each amenity
        for amenity in amenityJson:

            # all amenities are listed, but only those which 'is_present' are the ones we're interested in
            if amenity['is_present']:

                # amenity names are pretty enough, no need to tidy
                amenityData += amenityJson[i]['name'] + self.newLine
            i += 1
        return amenityData

    def printAmenityData(self, filename, amenityJson):
        filename.write( self.getAmenityData(amenityJson) )

    def getListingTitle(self):
        return self.newLine + '==== ROOM ====' + self.newLine

    def printListingTitle(self, filename):
        filename.write(self.getListingTitle())

    def getAmenityTitle(self):
        return self.newLine + '==== AMENITIES ====' + self.newLine

    def printAmenityTitle(self, filename):
        filename.write(self.getAmenityTitle())

    def scrapeUrl(self, url):
        # make the request, get the overall JSON
        roomData = self.getRoomJson(requests.get(url))

        # get the listing JSON
        listingData = self.getListingJson(roomData)

        # get the amenity JSON
        amenityData = self.getAmenityJson(listingData)

        print( self.getListingTitle() )

        # loop around and print each attribute we need
        print( self.getListingData(listingData) )

        print( self.getAmenityTitle() )

        # loop around and print all present amenities
        print( self.getAmenityData(amenityData) )

if __name__ == "__main__":
    scraper = airbnbScraper()
    # opens / creates results file
    #resultsFile = open('results.txt','w', encoding="utf-8")

    # loop through each room we're interested in
    for room in scraper.rooms:

        scraper.scrapeUrl(room)
