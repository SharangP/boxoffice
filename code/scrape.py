# Script to scrape movie metadata for movies in test set
import csv
from db.db import Database
from themoviedb.tmdb import TMDBApi

sagat = ['../datas/sagat_good_titles.csv', '../datas/sagat_bad_titles.csv']

D = Database('boxoffice.db')
TMDB = TMDBApi()

# load sagat csvs
for file in sagat:
    with open(file, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for movie in reader:
            mid = TMDB.MovieSearch(movie)[0]['id']
            print mid, movie


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

