import json
import urllib2

class RTApi:

    __baseUrl__ = "http://api.rottentomatoes.com/api/public/v1.0{endpoint}.json?apikey={api-key}"

    def __init__(self,apiKey):
        self.__ApiKey__ = apiKey

    def MovieInfo(self,id):
        print 'go get the movie info'
