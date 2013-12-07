from db.db import Database
import numpy
D = Database('boxoffice.db')
genres = D.GetAllGenreIdsNames()
gsize = len(genres)
g_num = 0

for genre in [x for x in genres]:
    g_num += 1
    # print "Updating stats for " + genre[1]
    print "genre " + str(g_num) + " out of " + str(gsize)
    scoreArray = D.GetRottenScoresByGenreId(genre[0])
    if not scoreArray:
        mean = -1
        std = -1
    else:
        mean = numpy.mean(scoreArray)
        std = numpy.std(scoreArray)
    D.UpdateGenreScore(genre[0], mean, std)
