from typing import List
import scrapy
import json
# custom logging which saves all the loggin into a txt file
from rmp.utils.logging.rmp_logger import logging
import os
from pprint import pprint

from .rmp_parser import url_parser as url_parser
from .rmp_parser import review_parser as review_parser

from rmp.utils.sqlite.database import SqlConnector
from rmp.models.models import Teacher, TeacherMeta, Review, ReviewMeta

logging.root.setLevel(logging.DEBUG)


class RMPSpider(scrapy.Spider):
    name = "rmp"

    def __init__(self, *args, **kwargs):
        super(RMPSpider, self).__init__(*args, **kwargs)
        input_path = os.path.join(
            os.environ['DATAROOT'], 'scraping', kwargs['input_file'])

        with open(input_path) as fp:
            spider_input = json.load(fp)

        self.college_sid = spider_input['college_sid']
        self.names = spider_input['names']
        logging.info(f'Running scraping job on school SID {self.college_sid}. Got names: {self.names}')

        db_path = os.path.join(os.environ['DATAROOT'], 'db', kwargs['db_file'])
        
        self.sql = SqlConnector(db_path, spider_input['table_name'])
        logging.info(f'Initialized RMP spider with db at {db_path}, and table name {spider_input["table_name"]}')
        

    def start_requests(self):
        for name in self.names:
            url = url_parser.create_rmp_url(name, self.college_sid)
            logging.debug(f"Parsing url: {url}")
            yield scrapy.Request(url=url, callback=self.parseRMP)

    def parseRMP(self, response: scrapy.Request):
        urls = response.xpath("//a[contains(@class,'TeacherCard')]//@href").getall()
        urls = ["https://www.ratemyprofessors.com" + url for url in urls]
        logging.debug(f'Response from {response.url}, urls: [{urls}]')
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_teachers)

    def parse_teachers(self, response):
        # Header
        teacher_info = {}
        teacher_info['header'] = review_parser.parse_header(response)
        teacher_info['reviews'] = review_parser.parse_review(response)
        teacher = self._parse_dict(teacher_info)
        self.sql.insert(teacher)
        logging.debug(f'Successfully parsed teacher: {teacher.last} {teacher.first}')
        yield teacher

    def _parse_dict(self, teacher_dict):
        """Parse teacher dict outputted by the scrapper."""
        first: str = teacher_dict['header']['first']
        last: str = teacher_dict['header']['last']
        avggrade: float = teacher_dict['header']['grade']
        college: str = teacher_dict['header']['college']
        department: str = teacher_dict['header']['department']
        total_ratings: int = teacher_dict['header']['total_ratings']
        would_take_again: float = teacher_dict['header']['would_take_again']
        difficulty: float = teacher_dict['header']['difficulty']

        meta: TeacherMeta = TeacherMeta(teacher_dict['header']['tags'])
        meta.most_helpful_line = {'date': teacher_dict['header']['mhl']['date'],
                                  'comment': teacher_dict['header']['mhl']['comment'],
                                  'upvotes': teacher_dict['header']['mhl']['upvotes'],
                                  'downvotes': teacher_dict['header']['mhl']['downvotes'],
                                  } if len(teacher_dict['header']['mhl'])!=0 else {}

        reviews: List[Review] = []
        for c in teacher_dict['reviews']:
            quality: float = c['score']['quality']
            difficulty: float = c['score']['difficulty']
            extra_info: List[str] = [f'{k}:{v}' for k, v in c['info'].items()]
            # "Accessible outside class" "EXTRA CREDIT"
            labels: List[str] = c['labels']
            upvotes: int = c['footer']['upvotes']
            downvotes: int = c['footer']['downvotes']
            review_date: str = c['header']['time']

            class_name: str = c['header']['class']
            # "great", "awful", etc.
            class_experience: str = c['header']['experience']
            comment: str = c['comment']
            meta: ReviewMeta = ReviewMeta(
                quality, difficulty, extra_info, labels, upvotes, downvotes, review_date)
            c = Review(class_name, class_experience, comment, meta)
            reviews.append(c)

        return Teacher(first, last, avggrade, college, department, total_ratings, would_take_again, difficulty, meta, reviews)