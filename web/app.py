from flask import Flask
from markupsafe import escape
from flask import request
from flask import abort

app = Flask(__name__)


@app.route('/')
def index():
    abort(404)


@app.route('/scrape', methods=['GET','POST'])
def scrape():
    if request.method == 'POST':
        if('name' in request.form):
            if(request.form['name']):
                return request.form['name']
        else:
            return abort(404)
    else:
        abort(404)
