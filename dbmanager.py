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
        self.cursor.excute(query)
        word_desc = self.cursor.fetchone()
        return word_desc

