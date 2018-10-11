import re
from math import ceil

def get_time_to_read_article(article, words_per_minute=250):
    '''
    This function returns the time it takes to read an article
    '''
    body = article.body
    word_count = len(re.sub('[^A-Za-z0-9]+', ' ', body).split())
    return f"{ceil(word_count/wpm)} mins"
