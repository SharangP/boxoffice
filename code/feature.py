from db.db import Database

D = Database('boxoffice.db')
# features:
# basic:
# movies.genre, movies.release_date (MAKE INTO A NUMBER), movies.production_id
# cast:
# IGNORE movies with < 4 non-director cast members,
# cast.mean_rating, cast.std_rating, cast.order_num (or sort)
# score (target value):
# IGNORE movies with no score
