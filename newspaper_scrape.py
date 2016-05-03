import newspaper
import dbmanager

import requests
import re
import urlparse

def rate_words(text):
    word_cnt = 0;
    for word in text.split():
        word = word.replace("'","")
        dbmanager.dbm.rating_word_with_commit(word)
        word_cnt = word_cnt + 1

    return word_cnt

##cnn = newspaper.build('http://edition.cnn.com/2016/05/01/politics/donald-trump-indiana-obama-white-house-dinner/index.html')
###url = u'http://edition.cnn.com/2016/05/01/politics/donald-trump-indiana-obama-white-house-dinner/index.htm'
###cnn_article = newspaper.Article(url)
"""for category in cnn.category_urls():
    print(categor)"""

def scrap_words(url):
    article = newspaper.Article(url)
    word_cnt = 0

    if dbmanager.dbm.is_url_scraped(article.url) == 0:
        try:
            article.download()
            article.parse()
            word_cnt = rate_words(article.text)
            dbmanager.dbm.insert_scraped_url(article.url, word_cnt)
        except newspaper.ArticleException as e:
            print(e)

    return word_cnt

# Basic e-mail regexp:
# letter/number/dot/comma @ letter/number/dot/comma . letter/number
email_re = re.compile(r'([\w\.,]+@[\w\.,]+\.\w+)')

# HTML <a> regexp
# Matches href="" attribute
link_re = re.compile(r'href="(.*?)"')

def crawl(url, maxlevel):
    # Limit the recursion, we're not downloading the whole Internet
    if(maxlevel == 0):
        return

    # Get the webpage
    try:
        req = requests.get(url)
    except requests.exceptions.InvalidSchema as e:
        print(e)
        return

    result = []

    # Check if successful
    if(req.status_code != 200):
        return []

    # Find and follow all the links
    links = link_re.findall(req.text)
    for link in links:
        # Get an absolute URL for a link
        link = urlparse.urljoin(url, link)
        if link.endswith('.html') and link != url:
            print ("Scraped : %s"%link)
            scrap_words(link)
            crawl(link, maxlevel - 1)

    # Find all emails on current page
    ##result += email_re.findall(req.text)
    ##return result

crawl('http://www.cnn.com/index.html', 100)