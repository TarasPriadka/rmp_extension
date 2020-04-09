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

def get_info(names):
    '''
    This is the main communication module with the database
    Params: names - names to find

    Search text database for the teacher's name, and if it doesn't exist, invoke scraper
    '''
    dne = []
    results = {}
    for name in names:
        results[name] = []
        path = f"tools/out/rmp_{'_'.join(name.lower().split())}.json"
        if not os.path.exists(path):
            dne.append(name)
        else:
            with open(path,'r') as f:
                results[name].append(json.load(f))

    if(len(dne) > 0):
        temp_res = scrape_info(dne)
        for i,result in enumerate(temp_res):
            
            results[dne[i]].append(result)
            path = f"tools/out/rmp_{'_'.join(dne[i].lower().split())}.json"
            write_json(result,path)

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

    return result
