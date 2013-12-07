import sqlite3 as lite


class Database:
    def __init__(self, db_file):
        self.conn = lite.connect(db_file)
        self.cur = self.conn.cursor()
        with self.conn:
            try:
                print "Creating Tables"
                self.cur.execute(
                    'CREATE TABLE IF NOT EXISTS movies (movie_id INTEGER PRIMARY KEY, movie_title VARCHAR(64), release_date VARCHAR(32), production_id INTEGER, production_name VARCHAR(64));')
                self.cur.execute(
                    'CREATE TABLE IF NOT EXISTS people (person_id INTEGER PRIMARY KEY, person_name VARCHAR(32), movie_ids VARCHAR(32), mean_rating REAL, std_rating REAL);')
                self.cur.execute(
                    'CREATE TABLE IF NOT EXISTS genres (movie_id INTEGER, genre_id INTEGER, genre_name VARCHAR(64), PRIMARY KEY(movie_id, genre_id), FOREIGN KEY(movie_id) REFERENCES movies(movie_id));')
                self.cur.execute(
                    'CREATE TABLE IF NOT EXISTS cast (movie_id INTEGER , person_id INTEGER, order_num INTEGER, PRIMARY KEY(movie_id, person_id), FOREIGN KEY(movie_id) REFERENCES movies(movie_id),FOREIGN KEY(person_id) REFERENCES people(person_id));')
                self.cur.execute(
                    'CREATE TABLE IF NOT EXISTS rottencast (person_id INTEGER, movie_id INTEGER, PRIMARY KEY(person_id, movie_id), FOREIGN KEY(movie_id) REFERENCES rottenmovies(movie_id),FOREIGN KEY(person_id) REFERENCES people(person_id));')
                self.cur.execute(
                    'CREATE TABLE IF NOT EXISTS rottenmovies (movie_id INTEGER PRIMARY KEY, movie_title VARCHAR(64), score REAL, rotten_id INTEGER, rotten_title VARCHAR(64), release_date VARCHAR(32));')
                self.cur.execute(
                    """CREATE TABLE IF NOT EXISTS features (
                        movie_id INTEGER PRIMARY KEY,
                        score REAL,
                        genre INTEGER,
                        release_date INTEGER,
                        production_id INTEGER,
                        director_mean REAL,
                        director_std REAL,
                        cast1_mean REAL,
                        cast1_std REAL,
                        cast2_mean REAL,
                        cast2_std REAL,
                        cast3_mean REAL,
                        cast3_std REAL,
                        cast4_mean REAL,
                        cast4_std REAL
                        );""")
            except Exception, err:
                print ('Sqlite error creating tables: %s' % str(err))

    def AddMovie(self, movie_id, title, release_date, prod_id, prod_name):
        with self.conn:
            try:
                self.cur.execute('INSERT INTO movies VALUES(?,?,?,?,?)',
                                 [movie_id, title, release_date, prod_id, prod_name])
                return True
            except Exception, err:
                print ('Sqlite error in AddMovie: %s' % str(err))
                return False

    def AddGenre(self, movie_id, genre_id, genre_name):
        with self.conn:
            try:
                self.cur.execute('INSERT INTO genres VALUES(?,?,?)', [movie_id, genre_id, genre_name])
                return True
            except Exception, err:
                print ('Sqlite error in AddGenre: %s' % str(err))
                return False

    def AddPerson(self, person_id, person_name):
        with self.conn:
            try:
                self.cur.execute('INSERT INTO people VALUES(?,?,?,?,?)', [person_id, person_name, None, None, None])
                return True
            except Exception, err:
                print ('Sqlite error in AddPerson: %s' % str(err))
                return False

    def AddCast(self, movie_id, person_id, order_num):
        with self.conn:
            try:
                self.cur.execute('INSERT INTO cast VALUES(?,?,?)', [movie_id, person_id, order_num])
                return True
            except Exception, err:
                print ('Sqlite error in AddCast: %s' % str(err))
                return False

    def AddRottenCast(self, person_id, movie_id):
        with self.conn:
            try:
                self.cur.execute('INSERT INTO rottencast VALUES(?,?)', [person_id, movie_id])
                return True
            except Exception, err:
                print ('Sqlite error in AddRottenCast: %s' % str(err))
                return False

    def AddRottenMovie(self, movie_id, movie_title, score, rotten_id, rotten_title, release_date):
        with self.conn:
            try:
                self.cur.execute('INSERT INTO rottenmovies VALUES(?,?,?,?,?,?)', [movie_id, movie_title, score, rotten_id, rotten_title, release_date])
                return True
            except Exception, err:
                print ('Sqlite error in AddRottenMovie: %s' % str(err))
                return False

    def AddFeatureForMovie(self, movie_id, score, genre, release_date, production_id, director_mean, director_std, cast1_mean, cast1_std, cast2_mean, cast2_std, cast3_mean, cast3_std, cast4_mean, cast4_std):
        with self.conn:
            try:
                self.cur.execute('INSERT INTO features VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                    [movie_id, score, genre, release_date, production_id, director_mean, director_std, cast1_mean, cast1_std, cast2_mean, cast2_std, cast3_mean, cast3_std, cast4_mean, cast4_std])
                return True
            except Exception, err:
                print ('Sqlite error in AddFeatureForMovie: %s' % str(err))
                return False

    def GetAllMovies(self):
        with self.conn:
            try:
                self.cur.execute('SELECT * FROM movies;')
                data = self.cur.fetchall()
                return data
            except Exception, err:
                print ('Sqlite error in GetAllMovies: %s\n' % str(err))

    def GetAllPersonIdsNames(self):
        with self.conn:
            try:
                self.cur.execute('SELECT person_id, person_name FROM people;')
                data = self.cur.fetchall()
                return data
            except Exception, err:
                print ('Sqlite error in GetAllPersonIdsNames: %s\n' % str(err))

    def GetRottenCastByPersonId(self, person_id):
        with self.conn:
            try:
                self.cur.execute('SELECT person_id, movie_id FROM rottencast WHERE person_id = (?);', [person_id])
                data = self.cur.fetchall()
                return data
            except Exception, err:
                print ('Sqlite error in GetRottenCastByPersonId: %s\n' % str(err))


    def GetRottenMovieByMovieId(self, movie_id):
        with self.conn:
            try:
                self.cur.execute('SELECT movie_id FROM rottenmovies WHERE movie_id = (?);', [movie_id])
                data = self.cur.fetchall()
                return data
            except Exception, err:
                print ('Sqlite error in GetRottenMovieByMovieId: %s\n' % str(err))

    def GetRottenScoreByMovieId(self, movie_id):
        with self.conn:
            try:
                self.cur.execute('SELECT score FROM rottenmovies WHERE movie_id = (?);', [movie_id])
                data = self.cur.fetchall()
                return data
            except Exception, err:
                print ('Sqlite error in GetRottenScoreByMovieId: %s\n' % str(err))

    def GetRottenScoresByPersonId(self, person_id):
        with self.conn:
            try:
                self.cur.execute('SELECT rottenmovies.score FROM rottenmovies inner join rottencast on rottenmovies.movie_id=rottencast.movie_id where rottencast.person_id = (?);', [person_id])
                data = self.cur.fetchall()
                return data
            except Exception, err:
                print ('Sqlite error in GetRottenScoresByPersonId: %s\n' % str(err))

    def GetCastStatsByMovieId(self, movie_id):
        with self.conn:
            try:
                self.cur.execute('SELECT c.order_num, p.mean_rating, p.std_rating FROM people p inner join cast c on p.person_id=c.person_id where c.movie_id = (?) order by c.order_num;', [movie_id])
                data = self.cur.fetchall()
                return data
            except Exception, err:
                print ('Sqlite error in GetCastStatsByMovieId: %s\n' % str(err))

    def GetAllFeatures(self):
        with self.conn:
            try:
                self.cur.execute('SELECT * FROM features;')
                data = self.cur.fetchall()
                return data
            except Exception, err:
                print ('Sqlite error in GetAllFeatures: %s\n' % str(err))

    def UpdatePersonScore(self, person_id, mean, std):
        with self.conn:
            try:
                self.cur.execute('update people set mean_rating=(?), std_rating=(?) where person_id=(?);', [mean, std, person_id])
                return True
            except Exception, err:
                print ('Sqlite error in UpdatePersonScore: %s' % str(err))
                return False
