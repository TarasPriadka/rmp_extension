import json
import scrapy
import os.path
from multiprocessing import Process, Queue

from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher
from scrapy.utils.log import configure_logging

from twisted.internet import reactor

from .spiders.rmp_spider import RMPSpider, write_json

def same_name(first, last, full):
    return first.lower() in full.lower() and last.lower() in full.lower()


def get_info(names):
    '''
    This is the main communication module with the database
    Params: names - names to find

    Search text database for the teacher's name, and if it doesn't exist, invoke scraper
    '''
    dne = []
    results = {}
    files_path = '/mnt/c/Users/taras/OneDrive/Documents/Code/rate-profs/web/tools/out'
    files = os.listdir(files_path)

    names_exist = []
    for f in files:
        names_exist.append({'name' : ' '.join(f[:-5].split('_')[1:]), 'path': f})

    for name in names:
        results[name] = []
        path = 'dne'

        for e_name in names_exist:
            match = True
            for piece in name.split():
                if piece.lower() in e_name['name']:
                    continue
                else:
                    match = False
                    break
            if match:
                path = files_path + '/' + e_name['path']

        if path == 'dne':
            dne.append(name)
        else:
            with open(path,'r') as f:
                results[name].append(json.load(f))

    if(len(dne) > 0):
        temp_res = scrape_info(dne)
        for name in dne:
            for i in range(len(temp_res)):
                if same_name(temp_res[i]['header']['first'], temp_res[i]['header']['last'], name):
                    results[name].append(temp_res[i])
                    break
        for res in temp_res:
            first = res['header']['first']
            last = res['header']['last']
            path = f"tools/out/rmp_{'_'.join([last.lower(), first.lower()])}.json"
            write_json(temp_res[i], path)
    

    return results


def scrape_info(names):
    '''
        Invoke spider with the following names
    '''

    return run_spider(RMPSpider(names))


def run_spider(spider):

    def start_spider(error_queue, response_queue):
        '''
        Anonymous method to create an invoke spider with a new reactor
        Params: error_queue - queue to append error to
                response_queue - queue to append the results of the response
        '''

        try:
            results = []

            def crawler_results(signal, sender, item, response, spider):
                results.append(item)
            dispatcher.connect(crawler_results, signal=signals.item_passed)

            runner = CrawlerRunner()
            deferred = runner.crawl(spider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            response_queue.put(results)
            error_queue.put(None)
        except Exception as e:
            error_queue.put(e)

    error_queue = Queue()
    response_queue = Queue()
    process = Process(target=start_spider, args=(error_queue, response_queue))
    process.start()
    result = response_queue.get()
    errors = error_queue.get()
    process.join()

    if errors is not None:
        raise errors
    
    # print(result)

    return result
