import json
import scrapy
from rmp_scraper.spiders.rmp_parser.review_parser import parse_review


class RMPSpider(scrapy.Spider):
    name = "rmp"
    count = 0
    def start_requests(self):
        urls = [
            'https://www.ratemyprofessors.com/ShowRatings.jsp?tid=117890',
            'https://www.ratemyprofessors.com/ShowRatings.jsp?tid=1836438',
            'https://www.ratemyprofessors.com/ShowRatings.jsp?tid=1149395'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_header(self, response):
        header = {}
        name_line = response.xpath("//div[contains(@class,'Wrapper')]/div[1]/div[1]/div[2]//text()").getall()
        header['last'] = name_line[0]
        header['first'] = name_line[2]
        header['department'] = name_line[4]
        header['college'] = name_line[8]

        avggrade_line = response.xpath("//div[contains(@class,'Wrapper')]/div[1]/div[1]/div[1]//text()").getall()
        header['grade'] = float(avggrade_line[0])
        header['total_ratings'] = int(avggrade_line[5])

        stats_line = response.xpath("//div[contains(@class,'Wrapper')]/div[1]/div[1]/div[3]//text()").getall()
        header['would_take_again'] = stats_line[0]
        header['difficulty'] = float(stats_line[2])

        tags_line = response.xpath("//div[contains(@class,'Wrapper')]/div[1]/div[1]/div[5]//text()").getall()
        header['tags'] = tags_line[3:]

        most_helpful_line = response.xpath("//div[contains(@class,'Wrapper')]/div[1]/div[2]/div[1]//text()").getall()
        header['date'] = most_helpful_line[2]
        header['comment'] = most_helpful_line[3]
        header['upvotes'] = int(most_helpful_line[5])
        header['downvotes'] = int(most_helpful_line[7])
        return header


    '''
        head:       -- 4 vals(class, emojii, grade, date) := repeating
        info:       -- 3 vals (for credit), (attendance), (would take again), (grade), (textbook) := repeating
        Score:      -- 4 vals (quality, num, difficulty, num) := repeating
        Comment:    -- comments := repeating
        labels:     -- val(' '), (upvote), val, (downvote), val, (tags(many, maybe)) := repeating
    '''

    def parse_reviews(self, response):
        review = response.xpath("//div[contains(@class,'Wrapper')]/div[4]").getall()
        reviews = parse_review(review[0])
        return reviews


    def parse(self, response):
        # Header
        teacher_info = {}
        teacher_info['header'] = self.parse_header(response)
        teacher_info['reviews'] = self.parse_reviews(response)

        filename = f'rmp{self.count}.json'
        self.count += 1
        with open(filename, 'w') as f:
            f.write(json.dumps(teacher_info, indent=4))
        self.log('Saved file %s' % filename)
