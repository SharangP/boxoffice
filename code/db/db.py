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
                    'CREATE TABLE IF NOT EXISTS rotten (movie_id INTEGER PRIMARY KEY, movie_title VARCHAR(64), score REAL, rotten_id INTEGER, release_date VARCHAR(32));')
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

    def AddRotten(self, movie_id, movie_title, score, rotten_id):
        with self.conn:
            try:
                self.cur.execute('INSERT INTO rotten VALUES(?,?,?,?,?)', [movie_id, movie_title, score, rotten_id, release_date])
                return True
            except Exception, err:
                print ('Sqlite error in AddRotten: %s' % str(err))
                return False

    def GetAllPersonIdsNames(self):
        with self.conn:
            try:
                self.cur.execute('SELECT person_id, person_name FROM people;')
                data = self.cur.fetchall()
                return data
            except Exception, err:
                print ('SQL BROKE: %s\n' % str(err))
