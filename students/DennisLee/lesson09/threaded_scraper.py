"""
Count the number of article titles containing a certain word, and the
number of times the word appears in the article titles.

This version of the tool uses multithreading.
"""

import threading
import time
import requests

# Powered by News API

NEWS_API_KEY = "61c76c103ff8421ca7b0d3903f3b730d"
BASE_URL = 'https://newsapi.org/v1/'
ARTICLE_BASE_URL = BASE_URL  + "articles"
WORD = 'trump'
art_count_dict, word_count_dict = {}, {}

def get_sources():
    """
    Get all the English language sources of news

    'https://newsapi.org/v1/sources?language=en'
    """
    url = BASE_URL + "sources"
    params = {"language": "en"}
    resp = requests.get(url, params=params)
    data = resp.json()
    sources = [src['id'].strip() for src in data['sources']]
    print("There are {} sources:", len(sources))
    print(sources)
    return sources

def get_articles(source):
    """
    https://newsapi.org/v1/articles?source=associated-press&sortBy=top&apiKey=1f
    """
    params = {
        "source": source,
        "apiKey": NEWS_API_KEY,
        "sortBy": "top"
    }
    print("Requesting the following:", source)
    resp = requests.get(ARTICLE_BASE_URL, params=params)
    if resp.status_code != 200:
        print("Something went wrong with {}".format(source))
        print(resp)
        print(resp.text)
        return []
    data = resp.json()
    # the URL to the article itself is in data['articles'][i]['url']
    titles = [str(art['title']) + str(art['description'])
              for art in data['articles']]
    return titles

def count_word(word, titles):
    """
    Count the number of occurrences of the word in the titles/descriptions.
    """
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count

def get_article_and_word_counts(source):
    """
    Add the article count and word count for a source to the dict of
    article counts and the dict of word counts.
    """
    titles = get_articles(source)
    art_count_dict[source] = len(titles)
    word_count_dict[source] = count_word(WORD, titles)

def tester():
    """Test the scraper and time it."""
    threads = []
    lock = threading.Lock()
    start = time.time()
    sources = get_sources()

    lock.acquire()
    for source in sources:
        thread = threading.Thread(target=get_article_and_word_counts,
                                  kwargs={"source": source})
        thread.start()
        threads.append(thread)
    lock.release()

    print(WORD,
          "found {} times in {} articles out of {} publications.".format(
              sum(word_count_dict.values()),
              sum(art_count_dict.values()),
              len(art_count_dict)
          )
         )
    print("Process took {:.0f} seconds".format(time.time() - start))

if __name__ == "__main__":
    tester()