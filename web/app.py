from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from tools.rmp_scraper import rmp_spider_run


app = Flask(__name__)
CORS(app, resources={r"/scrape": {"origins": "*"}})

@app.route('/')
def index():
    abort(404)


@app.route('/scrape', methods=['GET','POST'])
def scrape():
    if request.method == 'POST':
        if('names' in request.form):
            if(request.form['names']):
                names = request.form['names']
                names = names.split(',')
                data = rmp_spider_run.get_info(names);
                return jsonify({'status': 'ok', 'data': data})  # ,'data':data
        else:

            return abort(404)
    else:
        abort(404)
