import json
import logging
import os.path
from multiprocessing import Process, Queue

import scrapy
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher
from scrapy.utils.log import configure_logging

from twisted.internet import reactor

from .spiders.rmp_spider import RMPSpider, write_json
# from src.logger.logging_utils import get_logger

class ScraperWrapper:
    def __init__(self, app):
        self.log = app.logger

    def same_name(self, first, last, full):
        return first.lower() in full.lower() and last.lower() in full.lower()

    def scrape(self, names):
        '''
        This is the main communication module with the database
        Params: names - names to find

        Search text database for the teacher's name, and if it doesn't exist, invoke scraper
        '''
        log = self.log
        dne = []
        results = {}
        files_path = '/mnt/c/Users/taras/OneDrive/Documents/Code/rate-profs/temp/'
        files = os.listdir(files_path)

        log.debug(f'Printing files to {files_path}')
        names_exist = []
        for f in files:
            names_exist.append({'name' : ' '.join(f[:-5].split('_')[1:]), 'path': f})

        for name in names:
            results[name] = []
            path = None

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

            if not path:
                dne.append(name)
            else:

                with open(path,'r') as f:
                    results[name].append(json.load(f))
        
        existing_names = set(dne).intersection(set(names))
        if len(existing_names) > 0:
            log.debug(f"Found {existing_names} in the back...")

        if(len(dne) > 0):
            log.debug(f"Did not find [{dne}] in the back. Starting scraping...")
            scrape_results = self.scrape_info(dne)
            for name in dne:
                for result in scrape_results:
                    if self.same_name(result['header']['first'], result['header']['last'], name):
                        results[name].append(result)
                        break
            for result in scrape_results:
                first = result['header']['first']
                last = result['header']['last']
                path = f"tools/out/rmp_{'_'.join([last.lower(), first.lower()])}.json"
                write_json(result, path)
        
        return results


    def scrape_info(self, names):
        '''
            Invoke spider with the following names
        '''

        return self.run_spider(RMPSpider(names,logger = self.log))


    def run_spider(self, spider):

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
