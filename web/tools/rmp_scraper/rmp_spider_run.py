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

    print(results)

    return results


def scrape_info(names):
    '''
        Scrape rmp for the names in the list
    '''

    return run_spider(RMPSpider(names))


def run_spider(spider):
    out = []
    def f(q):
        try:
            results = []
            def crawler_results(signal, sender, item, response, spider):
                results.append(item)
            dispatcher.connect(crawler_results, signal=signals.item_passed)
            
            runner = CrawlerRunner()
            deferred = runner.crawl(spider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            out.append(results)
            # print(results)
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result
    
    # print(out)c
    return out
