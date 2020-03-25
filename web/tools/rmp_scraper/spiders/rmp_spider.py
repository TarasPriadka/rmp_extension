import json
import scrapy
import rmp_scraper.spiders.rmp_parser.url_parser as url_parser
import rmp_scraper.spiders.rmp_parser.review_parser as review_parser


class RMPSpider(scrapy.Spider):
    name = "rmp"
    names = []
    count = 0

    def __init__(self,*args, **kwargs):
        super(RMPSpider, self).__init__(*args, **kwargs)
        for a in args:
            self.names.append(a)


    def start_requests(self):
        for name in self.names[0]:
            url = url_parser.create_rmp_url(name,'De Anza')
            yield scrapy.Request(url=url, callback=self.parseRMP)


    def parseRMP(self, response):
            urls = response.xpath(
                "//body//ul[contains(@class,'listing')]//@href").getall()

            urls = ["https://www.ratemyprofessors.com/" + url for url in urls]
            for url in urls:
                yield scrapy.Request(url, callback=self.parse_teachers)


    def parseGoogle(self, response):
        links = response.xpath("//body/div//@href").getall()
        links = [url if 'ratemyprofessor' in url else '' for url in links]
        links = list(filter(lambda i: i != '' and 'ShowRatings' in i, links))
        for link in links:
            url = url_parser.reconstruct_url(link)
            yield scrapy.Request(url, callback=self.parse_teachers)


    def parse_teachers(self, response):
        # Header
        teacher_info = {}
        print("RESPONSE: ", response)
        teacher_info['header'] = review_parser.parse_header(response)
        teacher_info['reviews'] = review_parser.parse_review(response)

        filename = f"out/rmp_{teacher_info['header']['last'].lower()}_{teacher_info['header']['first'].lower()}.json"
        self.count += 1
        with open(filename, 'w') as f:
            f.write(json.dumps(teacher_info, indent=4))
        self.log('Saved file %s' % filename)
