from lxml import html

from rmp.utils.general import isfloat

def parse_header(response):
    header = {}
    name_line = response.xpath(
        "//div[contains(@class,'Wrapper')]/div[1]/div[1]/div[2]//text()").getall()
    header['last'] = name_line[0]
    header['first'] = name_line[2]
    header['department'] = name_line[5]
    header['college'] = name_line[-1]

    avggrade_line = response.xpath(
        "//div[contains(@class,'Wrapper')]/div[1]/div[1]/div[1]//text()").getall()
    header['grade'] = float(avggrade_line[0]) if isfloat(avggrade_line[0]) else float('nan')
    header['total_ratings'] = int(avggrade_line[5]) if 'No ratings yet.' not in avggrade_line else 0 

    stats_line = response.xpath(
        "//div[contains(@class,'Wrapper')]/div[1]/div[1]/div[3]//text()").getall()

    if 'Would take again' in stats_line:
        i = stats_line.index('Would take again') - 1 #used to find index of wta or difficulty in case one is missing
        header['would_take_again'] = stats_line[i] 
    else:
        header['would_take_again'] = float('nan') 

    if 'Level of Difficulty' in stats_line:
        i = stats_line.index('Level of Difficulty') - 1 #used to find index of wta or difficulty in case one is missing
        header['difficulty'] = stats_line[i] 
    else:
        header['difficulty'] = float('nan') 

    tags_line = response.xpath(
        "//div[contains(@class,'Wrapper')]/div[1]/div[1]/div[5]//text()").getall()
    header['tags'] = tags_line[3:] if len(tags_line)>4 else []

    most_helpful_line = response.xpath(
        "//div[contains(@class,'Wrapper')]/div[1]/div[2]/div[1]//text()").getall()

    header['mhl'] = {}
    if 'Be the first to rate Professor ' not in most_helpful_line and 'Bummer, Professor ' not in most_helpful_line:
        header['mhl']['class'] = most_helpful_line[3]
        header['mhl']['date'] = most_helpful_line[4]
        header['mhl']['comment'] = most_helpful_line[5]
        header['mhl']['upvotes'] = int(most_helpful_line[7])
        header['mhl']['downvotes'] = int(most_helpful_line[9])
    return header

def parse_review_header(review):
    out = {}
    review = review.xpath("./div/div/div[3]/div[1]//text()")
    out['class'] = review[1]
    out['experience'] = review[3]
    out['time'] = review[4]
    return out

def parse_score(review):
    review = review.xpath("./div/div/div[2]/div//text()")
    return {'quality': float(review[1]), 'difficulty': float(review[3])}

def parse_info(review):
    out = {}
    review = review.xpath("./div/div/div[3]/div[2]//text()")
    for i in range(0,len(review),3): 
        out[review[i]] = review[i+2]
    return out

def parse_comment(review):
    return review.xpath("./div/div/div[3]/div[3]//text()")[0]

def parse_labels(review):
    return review.xpath("./div//div[contains(@class,'Tags')]//text()")

def parse_footer(review):
    review = review.xpath("./div//div[contains(@class,'Footer')]//text()")
    return {
            'upvotes': review[1],
            'downvotes': review[3]  }

def parse_review(response):
    review = response.xpath("//ul[contains(@id,'ratingsList')]").getall()
    
    if len(review)==0:
        return []

    tree = html.fromstring(review[0])
    comments = tree.xpath("//li")
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
