import sqlite3 as lite

class Database:
  def __init__(self, db_file):
    self.conn = lite.connect(db_file)
    self.cur = self.conn.cursor()
    with self.conn:
      try:
        self.cur.execute('CREATE TABLE IF NOT EXISTS clicks (hash VARCHAR(10), num INTEGER, time INTEGER, PRIMARY KEY(hash, time));')
        self.cur.execute('CREATE TABLE IF NOT EXISTS categories (c_id INTEGER PRIMARY KEY, name VARCHAR(100));')
        self.cur.execute('CREATE TABLE IF NOT EXISTS link_categories (hash VARCHAR(10), c_id INTEGER NOT NULL, PRIMARY KEY(hash, c_id), FOREIGN KEY(c_id) REFERENCES categories(c_id));')
        self.categories = ["advertising", "agriculture", "art", "automotive", "aviation", "banking", "business", "celebrity", "computer", "disasters", "drugs", "economics", "education", "energy", "entertainment", "fashion", "finance", "food", "games", "health", "hobbies", "humor", "intellectual property", "labor", "legal", "lgbt", "marriage", "military", "mobile devices", "news", "philosophy", "politics", "real estate", "reference", "science", "sexuality", "shopping", "social media", "sports", "technology", "travel", "weapons", "weather", "none"]

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
