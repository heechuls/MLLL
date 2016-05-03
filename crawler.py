import requests
import re
import urlparse

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
            print (link)
            crawl(link, maxlevel - 1)

    # Find all emails on current page
    ##result += email_re.findall(req.text)
    ##return result

emails = crawl('http://www.cnn.com/index.html', 100)
