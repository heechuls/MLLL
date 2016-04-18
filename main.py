from flask import Flask, request
import stardict

app = Flask(__name__)
@app.route('/')
def index():
    return 'This is the homepage'

@app.route('/tuna')
def tuna():
    return '<h2> Tuna is good <h2>'

@app.route('/profile/<path:word>')
def show_post(word) :
    return  stardict.dict_reader.get_dict_by_word(word)

if __name__ == "__main__":
    app.run(debug=True)