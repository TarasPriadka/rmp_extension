import json
import scrapy
import os.path

from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher
from scrapy.utils.log import configure_logging

from twisted.internet import reactor

from .spiders.rmp_spider import RMPSpider, write_json

def get_info(names):
    dne = []
    results = []
    for name in names:
        path = f"tools/out/rmp_{'_'.join(name.lower().split())}.json"
        if not os.path.exists(path):
            dne.append(name)
        else:
            with open(path,'r') as f:
                results.append(json.load(f))

    if(len(dne) > 0):
        temp_res = scrape_info(dne)
        for i,result in enumerate(temp_res):
            path = f"tools/out/rmp_{'_'.join(dne[i].lower().split())}.json"
            write_json(result,path)
        results = results + temp_res

    return results

def scrape_info(names):
    '''
        Scrape rmp for the names in the list
    '''

    runner = CrawlerRunner()

    results = []

    def crawler_results(signal, sender, item, response, spider):
        results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_passed)

    d = runner.crawl(RMPSpider(names))
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished

    return results