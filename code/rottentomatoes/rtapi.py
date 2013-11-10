import os
import json
import urllib2

class RTApi:

    __baseUrl__ = "http://api.rottentomatoes.com/api/public/v1.0/{endpoint}.json?apikey={apiKey}{params}"

    def __init__(self):
        cd = os.path.dirname(os.path.abspath(__file__))
        fp = os.path.join(cd, 'api.keys')
        with open(fp) as f:
            self.__ApiKey__ = json.load(f)["key"]
        if not self.__ApiKey__:
            raise("RT Api Key Error")

    def MovieSearch(self,query,limit):
        results = []
        try:
            url = self.__baseUrl__.format(
                endpoint = "movies",
                apiKey = self.__ApiKey__,
                params = "&q=" + urllib2.quote(query) + "&page_limit=" + str(limit))
            req = urllib2.Request(url)
            jsonResponse = urllib2.urlopen(req)
            jsonResponse = json.load(jsonResponse)
            if 'movies' in jsonResponse:
                results = jsonResponse["movies"]
            return results
        except urllib2.URLError, e:
            print e.message
            return results
