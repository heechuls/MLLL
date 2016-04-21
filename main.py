from flask import Flask, request
from stardict import DictFileReader
from dbmanager import DBManager

app = Flask(__name__)
@app.route('/')
def index():
    return 'This is the homepage'

@app.route('/tuna')
def tuna():
    return '<h2> Tuna is good <h2>'

@app.route('/dict', methods=['GET', 'POST'])
def dict():
    word = request.args.get('word')
    ###word_desc = stardict.dict_reader.get_dict_by_word(word)
    dbm = DBManager()
    word_desc = dbm.get_dict_by_word(word)
    i = len(word_desc)
    if word_desc != False:
        return word_desc[i-1]['g']

if __name__ == "__main__":
    app.run(debug=True)