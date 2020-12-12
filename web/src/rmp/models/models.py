'''
    Data containers for teachers and their reviews
'''
import json

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
    tags:List[str]
    most_helpful_line={ 'date':'',
                        'comment':'',
                        'upvotes':0,
                        'downvotes':0,
                        }

@dataclass
class Teacher:
    FIELDS = [
        ('first','str'),
        ('last','str'),
        ('avggrade','real'), 
        ('college','str'), 
        ('department','str'),
        ('total_ratings','int'),
        ('would_take_again','int'),
        ('difficulty','real'),
        ('meta','json'),
        ('reviews','json'),
    ]

    first:str
    last:str
    avggrade:float
    college:str
    department:str
    total_ratings:int
    would_take_again:float
    difficulty:float
    meta:TeacherMeta
    reviews:List[Review] #student reviews

    def json_serialize(self):
        teacher_dict = self.__dict__
        teacher_dict['meta'] = json.dumps(teacher_dict['meta'].__dict__)
  
        #need to make everything json-serializable
        def to_dict(review):
            review.meta = review.meta.__dict__
            return review
  
        teacher_dict['reviews'] = json.dumps([review.__dict__ for review in map(to_dict,teacher_dict['reviews'])])
        teacher_tuple = tuple([teacher_dict[key] for key in teacher_dict])
        return teacher_tuple