from db.db import Database
from themoviedb.tmdb import TMDBApi
from rottentomatoes.rtapi import RTApi

D = Database('boxoffice.db')
TMDB = TMDBApi()
RT = RTApi()

people = D.GetAllPersonIdsNames()
for person in [x for x in people]: #person[0] = id, person[1] = name
    print "Processing person: " + person[1]
    credits = TMDB.PersonCreditsById(person[0])
    movies = []
    if len(credits) > 0:
        #credits['cast'].sort(key=lambda x: x['release_date'])
        #credits['crew'].sort(key=lambda x: x['release_date'])
        if(len(credits['cast']) > len(credits['crew'])):
            movies = credits['cast']
        else:
            movies = credits['crew']
        for movie in movies:
            print "Processing movie: " + movie['title']
            rottenMovie = RT.MovieSearch(movie['title'], 1)
            if(len(rottenMovie) > 0):
                D.AddRotten(movie['id'], movie['title'], rottenMovie[0]['ratings']['audience_score'], rottenMovie[0]['id'], movie['release_date'])
                #D.AddRottenCast()
    else:
        print person[1] + " doesnt have credits"