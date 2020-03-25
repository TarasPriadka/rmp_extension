from flask import Flask, request, abort, jsonify
from tools.rmp_scraper import rmp_spider_run


app = Flask(__name__)

@app.route('/')
def index():
    abort(404)


@app.route('/scrape', methods=['GET','POST'])
def scrape():
    if request.method == 'POST':
        if('names' in request.form):
            if(request.form['names']):
                names = request.form['names'].split(',')
                print(names)
                data = rmp_spider_run.get_info(names);
                return jsonify(data)
        else:
            return abort(404)
    else:
        abort(404)
