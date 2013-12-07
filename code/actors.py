import sys, time
from db.db import Database
from themoviedb.tmdb import TMDBApi
from rottentomatoes.rtapi import RTApi

D = Database('boxoffice.db')
TMDB = TMDBApi()
RT = RTApi()
RTapicalls = 0

people = D.GetAllPersonIdsNames()
psize=len(people)
people_num=0
for person in [x for x in people]: #person[0] = id, person[1] = name

    #check how many api calls have been done so far today
    if RTapicalls > 28900:
        print "Reached RTApi limit for today: " + str(RTapicalls)
        print time.asctime()
        print "Exiting on person: " + person[1]

    people_num+=1

    # skip people who have already been processed
    # if people_num <7100:
    #     continue
    if len(D.GetRottenCastByPersonId(person[0])) > 0:
        continue

    print "=========================================="
    try:
        print "Processing person: " + person[1] +str(person[0]) + " number "+str(people_num)+" out of "+str(psize)
    except Exception, err:
        print "Cant read person name/ unicode to ascii error, id:"
        continue
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
            if len(D.GetRottenMovieByMovieId(movie['id'])) > 0:
                print "skipping movie: " + movie['title'] + " and adding cast member "+person[1]
                D.AddRottenCast(person[0], movie['id'])
                continue
            try:
                print "Processing movie: " + movie['title'] + " , RTapicalls at " +str(RTapicalls)
            except Exception, err:
                print "Error printing movie with id: " + str(movie['id'])
                continue
            # print "Now exiting because rottencast should now be accurate"
            # sys.exit()
            rottenMovie = RT.MovieSearch(movie['title'], 1)
            RTapicalls += 1

            if len(rottenMovie) > 0:
                D.AddRottenMovie(movie['id'],
                                 movie['title'],
                                 rottenMovie[0]['ratings']['audience_score'],
                                 rottenMovie[0]['id'],
                                 rottenMovie[0]['title'],
                                 movie['release_date'])
                D.AddRottenCast(person[0], movie['id'])
            else:
            	print "Movie not found in Rotten Tomatoes"
    else:
        print person[1] + " doesnt have credits"
