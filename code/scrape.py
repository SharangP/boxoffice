# Script to scrape movie metadata for movies in test set
import csv
from db.db import Database
from themoviedb.tmdb import TMDBApi

sagat = ['../datas/sagat_good_titles.csv', '../datas/sagat_bad_titles.csv']

D = Database('boxoffice.db')
TMDB = TMDBApi()

# load sagat csvs
for sagatList in sagat:
    with open(sagatList, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for movie in reader:
            try:
                # fix up movie names
                movieName = movie[0]
                paren = str.rfind(movie[0], " (")
                if paren > 0:
                    movieName = movieName[0:paren]

                print "Processing movie: " + movieName
                mid = TMDB.MovieSearch(movieName)[0]['id']
                info = TMDB.MovieById(mid)
                cast = TMDB.MovieCastById(mid)

                if len(cast['cast']) == 0:
                    continue

                prod_companies = info['production_companies']
                if len(prod_companies) == 0:
                    prod_companies = [{'id': None, 'name': None}]

                if not D.AddMovie(info['id'],
                                  info['title'],
                                  info['release_date'],
                                  prod_companies[0]['id'],
                                  prod_companies[0]['name']):
                    continue

                for genre in info['genres']:
                    D.AddGenre(info['id'], genre['id'], genre['name'])

                for person in cast['crew']:
                    if person['job'] == "Director":
                        D.AddPerson(person['id'], person['name'])
                        D.AddCast(mid, person['id'], 0)
                for person in cast['cast'][0:4]:
                    D.AddPerson(person['id'], person['name'])
                    D.AddCast(mid, person['id'], person['order'])

            except Exception, e:
                print "Error with movie: " + movieName
                print e.message


# connect to db
# for movie in movies:
#   id = TMDBApi.MovieSearch(movie)[0]["id"]
#   info = TMDBApi.MovieById(id)
#   cast = TMDBApi.MovieCastById(id)
#   db.AddMovie <- info
#   db.AddGenre <- info
#   for person in cast: (not everyone)
#       db.AddPerson(person.["id"],person["name"])
#       db.AddCastMember(id,person["id"])
