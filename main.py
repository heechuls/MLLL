from flask import Flask, request, render_template
from stardict import DictFileReader
import dbmanager
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

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
    return find_word(word)

@app.route('/find/<word>')
def find(word):
    return find_word(word)

@app.route('/dictionary/')
@app.route('/dictionary/<word>')
def dictionary(word):
    word_desc = find_word(word)
    return render_template('dictionary.html', word_str=word, word_desc=word_desc)

@app.route('/foo', methods=['GET', 'POST'])
def foo(x=None, y=None):
    # do something to send email
    pass

def find_word(word):
    word_desc = dbmanager.dbm.get_dict_by_word(word)
    if word_desc is not False:
        refined = word_desc_refine(word_desc[0], word)
        return refined
    else:
        return 'No word found'

def word_desc_refine(word_desc, word_str):
    word_desc = word_desc.replace('<span foreground="blue" weight="bold">', '')
    word_desc = word_desc.replace(word_str, '')
    word_desc = word_desc.replace('</span> ', '')
    return word_desc


if __name__ == "__main__":
    ###app.run(host='127.0.0.1', debug=True)
    app.run(host='0.0.0.0', debug=True)