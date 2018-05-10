from flask import Flask, Response, abort, render_template
import json


app = Flask (__name__)

books = [{
    'id': 33,
    'title': 'The Raven',
    'author_id': 1,
}]


@app.route('/')
def hello_world() : 
    return render_template('home.html')


@app.route('/book')
def book_list() : 
    response = Response(
        json.dumps(books), status = 200)
    return response



if __name__ == '__main__' : 
    app.run(debug=True)