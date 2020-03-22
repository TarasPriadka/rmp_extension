import json
import scrapy
import rmp_scraper.spiders.rmp_parser as parser


class RMPSpider(scrapy.Spider):
    name = "rmp"
    count = 0
    def start_requests(self):
        # urls = [
        #     'https://www.ratemyprofessors.com/ShowRatings.jsp?tid=117890',
        #     'https://www.ratemyprofessors.com/ShowRatings.jsp?tid=1836438',
        #     'https://www.ratemyprofessors.com/ShowRatings.jsp?tid=1149395'
        # ]
        names = ["Manish Goel", "Dalia Garbacea", "Lana Sheridan"]
        for name in names:
            url = parser.url_parser.create_url(name)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = response.xpath("//body/div//@href").getall()
        links = [url if 'ratemyprofessor' in url else '' for url in links]
        links = list(filter(lambda i: i != '' and 'ShowRatings' in i, links))
        for link in links:
            url = parser.url_parser.reconstruct_url(link)
            yield scrapy.Request(url, callback=self.parse_teachers)


    def parse_teachers(self, response):
        # Header
        teacher_info = {}
        print("RESPONSE: ", response)
        teacher_info['header'] = parser.review_parser.parse_header(response)
        teacher_info['reviews'] = parser.review_parser.parse_review(response)

        filename = f'rmp{self.count}.json'
        self.count += 1
        with open(filename, 'w') as f:
            f.write(json.dumps(teacher_info, indent=4))
        self.log('Saved file %s' % filename)
