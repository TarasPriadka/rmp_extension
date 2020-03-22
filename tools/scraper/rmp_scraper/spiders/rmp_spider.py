import json
import scrapy
import rmp_scraper.spiders.rmp_parser as parser


class RMPSpider(scrapy.Spider):
    name = "rmp"
    count = 0
    def start_requests(self):
        names = ["Manish Goel", "Dalia Garbacea", "Lana Sheridan"]
        for name in names:
            url = parser.url_parser.create_rmp_url(name,'De Anza')
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
