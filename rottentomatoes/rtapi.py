import json
import urllib2

class RTApi:

    __baseUrl__ = "http://api.rottentomatoes.com/api/public/v1.0{endpoint}.json?apikey={apiKey}{params}"

    def __init__(self,apiKey):
        self.__ApiKey__ = apiKey

    def MovieSearch(self,query,limit):
        results = []
        url = self.__baseUrl__.format(
                endpoint = "movies",
                apiKey = self.__ApiKey__,
                params = "&q=" + query + "&page_limit=" + str(limit))
        url = url.replace(' ','%20')
        try:
            req = urllib2.Request(url)
            jsonResponse = urllib2.urlopen(req)
            results = json.load(jsonResponse)["movies"]
            return results
        except urllib2.URLError, e:
            print e.message
            return results
