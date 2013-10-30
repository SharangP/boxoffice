from db.db import Database
from themoviedb.tmdb import TMDBApi
from rottentomatoes.rtapi import RTApi

D = Database('boxoffice.db')
TMDB = TMDBApi()
RT = RTApi()

actors = D.GetAllPersonIdsNames()
for actor in [x for x in actors[0:100]]: #actor[0] = id, actor[1] = name
    credits = TMDB.PersonCreditsById(actor[0])
    if len(credits) > 0:
        credits['cast'].sort(key=lambda x: x['release_date'])
        credits['crew'].sort(key=lambda x: x['release_date'])
        print len(credits['cast']), len(credits['crew'])
    else:
        print actor[1] + " doesnt have credits"