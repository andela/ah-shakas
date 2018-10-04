import re
from math import ceil

def get_time_to_read_article(article, wpm=250):
    '''
    wpm is words per minute, article is an instance of ArticleModels classs
    '''
    body = article.body
    word_count = len(re.sub('[^A-Za-z0-9]+', ' ', body).split())
    return f"{ceil(word_count/wpm)} mins"