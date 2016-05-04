import MySQLdb

class DBManager(object):
    host = "40.74.112.135"
    db_id = "dict_feeder"
    db_pw = "slrtm97"
    db_name = "mlll"
    db = MySQLdb.connect(host, db_id, db_pw, db_name)
    cursor = db.cursor()

    def __del__(self):
        self.db.close()

    def get_dict_by_word(self, word):
        query = "select word_desc from word where word_str = '%s'" %word
        cursor = self.db.cursor()
        cursor.execute(query)
        word_desc = cursor.fetchone()
        return word_desc

    def get_wordid_by_word(self, word):
        query = "select word_id from word where word_str = '%s'" %word
        ##print(query)
        cursor = self.db.cursor()
        try:
           cursor.execute(query)
        except UnicodeEncodeError, ProgrammingError:
            print(query)

        return cursor.fetchone()

    def find_word(self, word):
        word_desc = dbm.get_dict_by_word(word)
        if word_desc is not False:
            refined = self.word_desc_refine(word_desc[0], word)
            return refined
        else:
            return 'No word found'

    def word_desc_refine(self, word_desc, word_str):
        word_desc = word_desc.replace('<span foreground="blue" weight="bold">', '')
        word_desc = word_desc.replace(word_str, '')
        word_desc = word_desc.replace('</span> ', '')
        return word_desc

    def is_url_scraped(self, url):
        query = "select count(*) from scrap where scrap_url = '%s'" % url
        cursor = self.db.cursor()
        cursor.execute(query)
        ret_val = cursor.fetchone()
        return ret_val[0]

    def insert_scraped_url(self, url, word_count):
        try:
            query = "INSERT INTO scrap (scrap_url, no_of_scrap_words) VALUES( '%s', %d)" % (url, word_count)
            cursor = self.db.cursor()
            cursor.execute(query)
            self.db.commit()
        except MySQLdb.OperationalError:
            self.db.commit()
        finally:
            self.db.commit()

    def rating_word_with_commit(self, word):
        try:
            self.rating_word(word)
            self.db.commit()
        except MySQLdb.OperationalError:
            self.db.commit()
        finally:
            self.db.commit()

    def rating_word(self, word):
        word_id = self.get_wordid_by_word(word)
        if word_id:
            query = "INSERT INTO rating (word_id, rating_value) VALUES( %d, 1) ON DUPLICATE KEY UPDATE rating_value = rating_value + 1"%word_id[0]
            ###print query
            cursor = self.db.cursor()
            cursor.execute(query)
            print('Word rated (%s)') % word

    def get_random_words(self, start_val, end_val, limit):
        query = "SELECT word.word_str, word.word_desc, rating.rating_value FROM word inner join rating where rating.word_id = word.word_id and rating.rating_value > %d and rating.rating_value < %d ORDER BY RAND() LIMIT %d"%(start_val, end_val, limit)
        cursor = self.db.cursor()
        cursor.execute(query)
        print cursor
        return cursor

dbm = DBManager()

if __name__ == '__main__' :
    dbm.rating_word('love')