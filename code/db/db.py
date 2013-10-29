import sqlite3 as lite

class Database:
  def __init__(self, db_file):
    self.conn = lite.connect(db_file)
    self.cur = self.conn.cursor()
    with self.conn:
      try:
        self.cur.execute('CREATE TABLE IF NOT EXISTS movies (movie_id INTEGER PRIMARY KEY, movie_title VARCHAR(64), release_date VARCHAR(32), production_id INTEGER, production_name VARCHAR(64));')
        self.cur.execute('CREATE TABLE IF NOT EXISTS people (person_id INTEGER PRIMARY KEY, person_name VARCHAR(32), movie_ids VARCHAR(32), mean_rating REAL, std_rating REAL);')
        self.cur.execute('CREATE TABLE IF NOT EXISTS genres (movie_id INTEGER, genre_id INTEGER, genre_name VARCHAR(64), PRIMARY KEY(movie_id, genre_id), FOREIGN KEY(movie_id) REFERENCES movies(movie_id));')
        self.cur.execute('CREATE TABLE IF NOT EXISTS cast (movie_id INTEGER , person_id INTEGER, order_num INTEGER, PRIMARY KEY(movie_id, person_id), FOREIGN KEY(movie_id) REFERENCES movies(movie_id),FOREIGN KEY(person_id) REFERENCES people(person_id));')
        # self.categories = ["advertising", "agriculture", "art", "automotive", "aviation", "banking", "business", "celebrity", "computer", "disasters", "drugs", "economics", "education", "energy", "entertainment", "fashion", "finance", "food", "games", "health", "hobbies", "humor", "intellectual property", "labor", "legal", "lgbt", "marriage", "military", "mobile devices", "news", "philosophy", "politics", "real estate", "reference", "science", "sexuality", "shopping", "social media", "sports", "technology", "travel", "weapons", "weather", "none"]

        self.cur.execute('SELECT * FROM categories;')
        if len(self.cur.fetchall()) == 0:
          for category in self.categories:
            with self.conn:
                self.cur.execute('INSERT INTO categories(name) VALUES(?)', [category])
      except Exception, err:
        print ('SQL BROKE: %s\n' % str(err))

  def add_category(self, link_hash, c_id):
    with self.conn:
      try:
        self.cur.execute('INSERT INTO link_categories VALUES(?,?)', [link_hash, c_id])
      except Exception, err:
        print ('SQL BROKE: %s\n' % str(err))

  def add_click(self, link_hash, num_clicks, time):
    with self.conn:
      try:
        self.cur.execute('INSERT INTO clicks VALUES(?,?,?)', [link_hash, num_clicks, time])
      except Exception, err:
        print ('SQL BROKE: %s\n' % str(err))

  def category_id(self, category):
    try:
      return self.categories.index(category.lower())
    except Exception, err:
      return self.categories.index("none")

  def categories(self):
    return self.categories
