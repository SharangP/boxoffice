import sys, time
from db.db import Database
from themoviedb.tmdb import TMDBApi
from rottentomatoes.rtapi import RTApi

D = Database('boxoffice.db')
TMDB = TMDBApi()
RT = RTApi()
RTapicalls = 0

people = D.GetAllPersonIdsNames()
for person in [x for x in people]: #person[0] = id, person[1] = name

    #check how many api calls have been done so far today
    if RTapicalls > 29900:
        print "Reached RTApi limit for today: " + RTapicalls
        print time.asctime()
        print "Exiting on person: " + person[1]

    #skip people who have already been processed
    if len(D.GetRottenCastByPersonId(person[0])) > 0:
        continue

    print "=========================================="
    print "Processing person: " + person[1]
    print "=========================================="
    
    credits = TMDB.PersonCreditsById(person[0])
    movies = []
    if len(credits) > 0:
        #credits['cast'].sort(key=lambda x: x['release_date'])
        #credits['crew'].sort(key=lambda x: x['release_date'])
        if len(credits['cast']) > len(credits['crew']):
            movies = credits['cast']
        else:
            movies = credits['crew']
        for movie in movies:
            if len(D.GetRottenMovieByMovieId(movie[0])) > 0:
                continue
            print "Processing movie: " + movie['title']
            rottenMovie = RT.MovieSearch(movie['title'], 1)
            RTapicalls += 1

            if len(rottenMovie) > 0:
                D.AddRottenMovie(movie['id'], movie['title'], rottenMovie[0]['ratings']['audience_score'], rottenMovie[0]['id'], movie['release_date'])
                D.AddRottenCast(person[0], movie['id'])
    else:
        print person[1] + " doesnt have credits"
