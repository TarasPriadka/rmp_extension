
from lxml import html


def parse_header(response):
        header = {}
        name_line = response.xpath(
            "//div[contains(@class,'Wrapper')]/div[1]/div[1]/div[2]//text()").getall()
        header['last'] = name_line[0]
        header['first'] = name_line[2]
        header['department'] = name_line[4]
        header['college'] = name_line[8]

        avggrade_line = response.xpath(
            "//div[contains(@class,'Wrapper')]/div[1]/div[1]/div[1]//text()").getall()
        header['grade'] = float(avggrade_line[0])
        header['total_ratings'] = int(avggrade_line[5])

        stats_line = response.xpath(
            "//div[contains(@class,'Wrapper')]/div[1]/div[1]/div[3]//text()").getall()
        header['would_take_again'] = stats_line[0]
        header['difficulty'] = float(stats_line[2])

        tags_line = response.xpath(
            "//div[contains(@class,'Wrapper')]/div[1]/div[1]/div[5]//text()").getall()
        header['tags'] = tags_line[3:]

        most_helpful_line = response.xpath(
            "//div[contains(@class,'Wrapper')]/div[1]/div[2]/div[1]//text()").getall()
        header['date'] = most_helpful_line[2]
        header['comment'] = most_helpful_line[3]
        header['upvotes'] = int(most_helpful_line[5])
        header['downvotes'] = int(most_helpful_line[7])
        return header

def parse_review_header(review):
    out = {}
    review = review.xpath("./div/div")[2]
    review = review.xpath("./div")[0]
    review = review.xpath(".//text()")
    out['class'] = review[0]
    out['experience'] = review[2]
    out['time'] = review[3]
    return out

def parse_score(review):
    review = review.xpath("./div/div")[1]
    review = review.xpath("./div//text()")
    return {'quality': float(review[1]), 'difficulty': float(review[3])}


def parse_info(review):
    out = {}
    review = review.xpath("./div/div")[2]
    review = review.xpath("./div")[1]
    review = review.xpath(".//text()")
    for i in range(0,len(review),3):
        out[review[i]] = review[i+2]
    # print(etree.tostring(review, encoding='unicode', pretty_print=True))
    return out

def parse_comment(review):
    review = review.xpath("./div/div")[2]
    review = review.xpath("./div")[2]
    review = review.xpath(".//text()")
    return review[0]

def parse_labels(review):
    out = []
    review = review.xpath("./div/div")[2]
    review = review.xpath("./div")
    classes = [ 'Tags' in s.get('class') for s in review]
    if True in classes:
        r = review[classes.index(True)]
        r = r.xpath(".//text()")
        return r
    return []

def parse_footer(review):
    review = review.xpath("./div/div")[2]
    review = review.xpath("./div")
    classes = ['Footer' in s.get('class') for s in review]
    if True in classes:
        r = review[classes.index(True)]
        r = r.xpath(".//text()")
        return {
            'upvotes': r[1],
            'downvotes': r[3]  }
    return {}

def parse_review(response):
    review = response.xpath(
        "//div[contains(@class,'Wrapper')]/div[4]").getall()
    tree = html.fromstring(review[0])
    comments = tree.xpath("//ul")
    comments = comments[1]
    reviews = []
    for comment in comments:
        try:
            review = {}
            review['header'] = parse_review_header(comment)
            review['score'] = parse_score(comment)
            review['info'] = parse_info(comment)
            review['comment'] = parse_comment(comment)
            review['labels'] = parse_labels(comment)
            review['footer'] = parse_footer(comment)
            reviews.append(review)
        except(IndexError):
            continue
    return reviews
