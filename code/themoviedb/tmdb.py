import os
import json
import urllib2


class TMDBApi:
    __baseUrl__ = "http://api.themoviedb.org/3/{endpoint}?api_key={apiKey}{params}"

    def __init__(self):
        cd = os.path.dirname(os.path.abspath(__file__))
        fp = os.path.join(cd, 'api.keys')
        with open(fp) as f:
            self.__ApiKey__ = json.load(f)["key"]
        if not self.__ApiKey__:
            raise ("TMDB Api Key Error")

    def MovieSearch(self, query):
        results = []
        headers = {"Accept": "application/json"}
        try:
            url = self.__baseUrl__.format(
                endpoint="search/movie",
                apiKey=self.__ApiKey__,
                params="&query=" + urllib2.quote(query))
            req = urllib2.Request(url, headers=headers)
            jsonResponse = urllib2.urlopen(req)
            jsonResponse = json.load(jsonResponse)
            if 'results' in jsonResponse:
                results = jsonResponse["results"]
            return results
        except urllib2.URLError, e:
            print "Error finding movie: " + query
            return results

    def MovieById(self, id):
        results = []
        headers = {"Accept": "application/json"}
        url = self.__baseUrl__.format(
            endpoint="movie/" + str(id),
            apiKey=self.__ApiKey__,
            params="")
        try:
            req = urllib2.Request(url, headers=headers)
            jsonResponse = urllib2.urlopen(req)
            results = json.load(jsonResponse)
            return results
        except urllib2.URLError, e:
            print "Error finding movie id: " + str(id)
            return results

    def MovieCastById(self, id):
        results = []
        headers = {"Accept": "application/json"}
        url = self.__baseUrl__.format(
            endpoint="movie/" + str(id) + "/casts",
            apiKey=self.__ApiKey__,
            params="")
        try:
            req = urllib2.Request(url, headers=headers)
            jsonResponse = urllib2.urlopen(req)
            results = json.load(jsonResponse)
            return results
        except urllib2.URLError, e:
            print "Error finding movie cast by id: " + str(id)
            return results

    def PersonSearch(self, query):
        results = []
        headers = {"Accept": "application/json"}
        try:
            url = self.__baseUrl__.format(
                endpoint="search/people",
                apiKey=self.__ApiKey__,
                params="&query=" + urllib2.quote(query))
            req = urllib2.Request(url, headers=headers)
            jsonResponse = urllib2.urlopen(req)
            jsonResponse = json.load(jsonResponse)
            if 'results' in jsonResponse:
                results = jsonResponse["results"]
            return results
        except urllib2.URLError, e:
            print "Error finding person: " + query
            return results

    def PersonCreditsById(self, id):
        results = []
        headers = {"Accept": "application/json"}
        url = self.__baseUrl__.format(
            endpoint="person/" + str(id) + "/credits",
            apiKey=self.__ApiKey__,
            params="")
        try:
            req = urllib2.Request(url, headers=headers)
            jsonResponse = urllib2.urlopen(req)
            results = json.load(jsonResponse)
            return results
        except urllib2.URLError, e:
            print "Error finding credits by person id: " + str(id)
            return results
