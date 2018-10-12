import re
from math import ceil

def get_time_to_read_article(article, words_per_minute=250):
    '''
    This function returns the time it takes to read an article
    '''
    body = article.body
    word_count = len(re.sub('[^A-Za-z0-9]+', ' ', body).split())
    if ceil(word_count/words_per_minute) == 1:
        return f"{ceil(word_count/words_per_minute)} min"
    return f"{ceil(word_count/words_per_minute)} mins"    
