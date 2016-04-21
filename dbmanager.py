import MySQLdb

class DBManager(object):
    host = "40.74.112.135"
    db_id = "dict_feeder"
    db_pw = "slrtm97"
    db_name = "mlll"
    db = MySQLdb.connect(host, db_id, db_pw, db_name)


    def __del__(self):
        self.db.close()

    def get_dict_by_word(self, word):
        query = "select word_desc from word where word_str = '%s'" %word
        cursor = self.db.cursor()
        cursor.excute(query)
        word_desc = cursor.fetchone()
        return word_desc

