
from lxml import html

def parse_header(review):
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

def parse_review(review):
    tree = html.fromstring(review)
    comments = tree.xpath("//ul")
    comments = comments[1]
    reviews = []
    for comment in comments:
        try:
            review = {}
            review['header'] = parse_header(comment)
            review['score'] = parse_score(comment)
            review['info'] = parse_info(comment)
            review['comment'] = parse_comment(comment)
            review['labels'] = parse_labels(comment)
            review['footer'] = parse_footer(comment)
            reviews.append(review)
        except(IndexError):
            continue
    return reviews
