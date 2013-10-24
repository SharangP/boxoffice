import json
import urllib2

class RTApi:

    __baseUrl__ = "http://mymovieapi.com/s"

    # def __init__(self,apiKey):
    #     self.__ApiKey__ = apiKey

    def GetByID(self,id):
        __URL__= __baseUrl__+
