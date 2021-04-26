'''
    Data containers for teachers and their reviews
'''
import json

from dataclasses import dataclass
from typing import List


@dataclass
class ReviewMeta:
    quality: float
    difficulty: float
    extra_info: List[str]  # "For Credit: Yes", "Would Take Again: No", etc.
    labels: List[str]  # "Accessible outside class" "EXTRA CREDIT"
    upvotes: int
    downvotes: int
    review_date: str


@dataclass
class Review:
    class_name: str
    class_experience: str  # "great", "awful", etc.
    comment: str
    meta: ReviewMeta


@dataclass
class TeacherMeta:
    tags: List[str]
    most_helpful_line = {'date': '',
                         'comment': '',
                         'upvotes': 0,
                         'downvotes': 0,
                         }


@dataclass
class Teacher:
    FIELDS = [
        ('first', 'str'),
        ('last', 'str'),
        ('avggrade', 'real'),
        ('college', 'str'),
        ('department', 'str'),
        ('total_ratings', 'int'),
        ('would_take_again', 'int'),
        ('difficulty', 'real'),
        ('meta', 'json'),
        ('reviews', 'json'),
    ]

    first: str
    last: str
    avggrade: float
    college: str
    department: str
    total_ratings: int
    would_take_again: float
    difficulty: float
    meta: TeacherMeta
    reviews: List[Review]  # student reviews

    def json_serialize(self):
        teacher_dict = self.__dict__
        teacher_dict['meta'] = json.dumps(teacher_dict['meta'].__dict__)

        # need to make everything json-serializable
        def to_dict(review):
            review.meta = review.meta.__dict__
            return review

        teacher_dict['reviews'] = json.dumps(
            [review.__dict__ for review in map(to_dict, teacher_dict['reviews'])])
        teacher_tuple = tuple([teacher_dict[key] for key in teacher_dict])
        return teacher_tuple

    @staticmethod
    def parse_dict(teacher_dict):
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
