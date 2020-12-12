'''
    Data containers for teachers and their reviews
'''
from dataclasses import dataclass
from typing import List

@dataclass
class ReviewMeta:
    quality:float
    difficulty:float
    extra_info:List[str] # "For Credit: Yes", "Would Take Again: No", etc.
    labels:List[str] # "Accessible outside class" "EXTRA CREDIT"
    upvotes:int
    downvotes:int
    review_date:str
    

@dataclass
class Review:
    class_name:str
    class_experience:str #"great", "awful", etc.
    comment:str
    meta:ReviewMeta
    

@dataclass
class TeacherMeta:
    department:str
    college:str
    total_ratings:int
    would_take_again:float
    difficulty:float
    tags:List[str]
    most_helpful_line={ 'date':'',
                        'comment':'',
                        'upvotes':0,
                        'downvotes':0,
                        }

@dataclass
class Teacher:
    first:str
    last:str
    avggrade:float
    meta:TeacherMeta
    reviews:List[Review] #student reviews