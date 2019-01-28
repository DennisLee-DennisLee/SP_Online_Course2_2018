import threading
import time
import requests

# Powered by News API

NEWS_API_KEY = "61c76c103ff8421ca7b0d3903f3b730d"
BASE_URL = 'https://newsapi.org/v1/'
WORD = 'trump'

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
    print("Here are the sources:")
    print(sources)
    return sources

def get_articles(source):
    """
    https://newsapi.org/v1/articles?source=associated-press&sortBy=top&apiKey=1f
    """
    url = BASE_URL + "articles"
    params = {
        "source": source,
        "apiKey": NEWS_API_KEY,
        "sortBy": "top"
    }
    print("Requesting the following:", source)
    resp = requests.get(url, params=params)
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
    """Count the number of occurrences of the word in the titles."""
    word = word.lower()
    count = 0
    for title in titles:
        if word in title.lower():
            count += 1
    return count

def tester():
    """Test the scraper and time it."""
    start = time.time()
    sources = get_sources()

    art_count = 0
    word_count = 0
    for source in sources:
        titles = get_articles(source)
        art_count += len(titles)
        word_count += count_word(WORD, titles)

    print(WORD, "found {} times in {} articles".format(word_count, art_count))
    print("Process took {:.0f} seconds".format(time.time() - start))

if __name__ == "__main__":
    tester()
