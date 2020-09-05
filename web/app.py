import logging

from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from tools.rmp_scraper.rmp_spider_run import get_info

log = logging.getLogger(__name__)
log.setLevel('DEBUG')

app = Flask(__name__)
CORS(app, resources={r"/scrape": {"origins": "*"}})
app.logger


@app.route('/')
def index():
    abort(404)


@app.route('/scrape', methods=['GET','POST'])
def scrape():
    log.info(f"Received a POST request on 'scrape': {request}")
    if request.method == 'POST':
        if 'names' in request.form and request.form['names']: # if field names exists in request form and if it is not NULL
            names = request.form['names']
            names = names.split(',')
            # print(app.logger)
            log.info(f"Got names to scrape: {names}")
            # data = get_info(names);
            data = {}
            out_request = jsonify({'status': 'ok', 'data': data})
            log.debug(f"Returning request: {out_request}")
            return out_request
        else:
            log.warning("Didn't get any names. Falling back on 404")
            return abort(404)
    else:
        log.warning("Receiving a GET request. Falling back on 404")
        abort(404)

if __name__ == '__main__':
    #Setup the logger
    log.info('here')
    app.run(debug=True)