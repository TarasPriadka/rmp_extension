import scrapy
import json
# custom logging which saves all the loggin into a txt file
from rmp.utils.logging.rmp_logger import logging
import os
from pprint import pprint

from .rmp_parser import url_parser as url_parser
from .rmp_parser import review_parser as review_parser

from rmp.utils.sqlite.database import SqlConnector
from rmp.models.models import Teacher

logging.root.setLevel(logging.DEBUG)


class RMPSpider(scrapy.Spider):
    name = "rmp"

    def __init__(self, *args, **kwargs):
        super(RMPSpider, self).__init__(*args, **kwargs)
        input_path = os.path.join(
            os.environ['DATAROOT'], 'scraping', kwargs['input_file'])

        with open(input_path) as fp:
            spider_input = json.load(fp)

        self.college = spider_input['college']
        self.names = spider_input['names']
        logging.info(f'Running scraping job on school {self.college}. Got names: {self.names}')

        db_path = os.path.join(os.environ['DATAROOT'], 'db', kwargs['db_file'])
        
        self.sql = SqlConnector(db_path, spider_input['table_name'])
        logging.info(f'Initialized RMP spider with db at {db_path}, and table name {spider_input["table_name"]}')
        

    def start_requests(self):
        for name in self.names:
            url = url_parser.create_rmp_url(name, 'De Anza')
            logging.debug(f"Parsing url: {url}")
            yield scrapy.Request(url=url, callback=self.parseRMP)

    def parseRMP(self, response: scrapy.Request):
        urls = response.xpath(
            "//body//ul[contains(@class,'listing')]//@href").getall()
        urls = ["https://www.ratemyprofessors.com" + url for url in urls]
        logging.debug(f'Response from {response.url}, urls: [{urls}]')
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_teachers)

    def parse_teachers(self, response):
        # Header
        teacher_info = {}
        teacher_info['header'] = review_parser.parse_header(response)
        teacher_info['reviews'] = review_parser.parse_review(response)
        teacher = Teacher.parse_dict(teacher_info)
        self.sql.insert(teacher)
        logging.debug(
            f'Successfully parsed teacher: {teacher.last} {teacher.first}')
        yield teacher
