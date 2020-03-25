import scrapy
from scrapy.crawler import CrawlerProcess
from rmp_scraper.spiders.rmp_spider import RMPSpider

def scrape_info(names):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(RMPSpider(names))
    process.start()  # the script will block here until the crawling is finished

scrape_info(['Manish Goel', 'Delia Garbacea'])