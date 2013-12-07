from db.db import Database
import numpy

D = Database('boxoffice.db')

# features:
# basic:
# movies.genre, movies.release_date (MAKE INTO A NUMBER), movies.production_id
# cast:
# IGNORE movies with < 4 non-director cast members,
# cast.mean_rating, cast.std_rating, cast.order_num (or sort)
# score (target value):
# IGNORE movies with no score

movies = D.GetAllMovies()
msize = len(movies)
m_num = 0

for movie in [x for x in movies]:
    m_num += 1
    print "Getting features for movie: " + str(movie[0])
    print "Movie " + str(m_num) + " out of " + str(msize)
    
    movie_id = movie[0]
    score = D.GetRottenScoreByMovieId(movie_id)
    if not score:
        print "Skipping movie b/c score is null id: " + str(movie[0]) + " name: " + movie[1]
        continue
    score = score[0][0]
    if score == 0:
        print "Skipping movie b/c score==0 id: " + str(movie[0]) + " name: " + movie[1]
        continue

    # genre
    # release_date = movie[2] #TODO: convert this into a number
    # production_id = movie[3] #TODO: normalize?

    people = D.GetCastStatsByMovieId(movie_id)
    directors = [x for x in people if x[0] == 100]
    crew = [x for x in people if x[0] != 100]

    if not directors or len(crew) < 4:
        print "Skipping movie b/c lack of cast id: " + str(movie[0]) + " name: " + movie[1]
        continue

    # find the director with the maximum mean rating
    d = max((v[1], i) for i, v in enumerate(directors))[1]
    director_mean = directors[d][1]
    director_std = directors[d][2]
    cast1_mean = crew[0][1]
    cast1_std = crew[0][2]
    cast2_mean = crew[1][1]
    cast2_std = crew[1][2]
    cast3_mean = crew[2][1]
    cast3_std = crew[2][2]
    cast4_mean = crew[3][1]
    cast4_std = crew[3][2]

    # D.AddFeatureForMovie(movie_id, score, genre, release_date, production_id, director_mean, director_std, cast1_mean, cast1_std, cast2_mean, cast2_std, cast3_mean, cast3_std, cast4_mean, cast4_std)
    D.AddFeatureForMovie(movie_id, score, None, None, None, director_mean, director_std, cast1_mean, cast1_std, cast2_mean, cast2_std, cast3_mean, cast3_std, cast4_mean, cast4_std)
