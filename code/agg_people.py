from db.db import Database
import numpy
D = Database('boxoffice.db')
people = D.GetAllPersonIdsNames()
psize = len(people)
people_num = 0

for person in [x for x in people]:
    people_num += 1
    print "Updating stats for " + person[1]
    print "Person " + str(people_num) + " out of " + str(psize)
    scoreArray = D.GetRottenScoresByPersonId(person[0])
    if not scoreArray:
        mean = -1
        std = -1
    else:
        mean = numpy.mean(scoreArray)
        std = numpy.std(scoreArray)
    D.UpdatePersonScore(person[0], mean, std)
